#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import twint
from urlextract import URLExtract
import newspaper
import validators
import hashlib
import base64
import gzip
import simplejson as json
import redis
import sys
import datetime
import configparser
import argparse
import requests
from urllib.parse import urlparse
import signal

def jsonclean(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

uuid = "aae656ec-d446-4a21-acf0-c88d4e09d506"
ailfeedertype = "ail_feeder_twitter"
ailurlextract = "ail_feeder_urlextract"
# config reader

config = configparser.ConfigParser()
config.read('../etc/ail-feeder-twitter.cfg')

if 'general' in config:
    uuid = config['general']['uuid']
    tweet_limit = config['general']['tweet_limit']
else:
    uuid = "aae656ec-ffff-4a21-acf0-c88d4e09d506"

if 'redis' in config:
    r = redis.Redis(host=config['redis']['host'], port=config['redis']['port'], db=config['redis']['db'])
else:
    r = redis.Redis(host='localhost', port=6379, db=0)

if 'cache' in config:
    cache_expire = config['cache']['expire']
else:
    cache_expire = 86400

def ail_publish(url=config['ail']['url'], apikey=config['ail']['apikey'], data=None):
    response = requests.post(url, headers={'Content-Type': 'application/json', 'Authorization': apikey} ,data=data, verify=False)
    return response


# arguments parsing

parser = argparse.ArgumentParser()
parser.add_argument("query", help="query to search on Twitter to feed AIL")
parser.add_argument("--verbose", help="verbose output", action="store_true")
parser.add_argument("--nocache", help="disable cache", action="store_true")
parser.add_argument("--tweetlimit", help="maximum number of tweet to fetch", type=int, default=tweet_limit)
args = parser.parse_args()

c = twint.Config()
c.Search = args.query
c.Limit = args.tweetlimit
c.Store_object = True
c.Hide_output = True
c.Filter_retweets = True

signal.alarm(10)
try:
    twint.run.Search(c)
except TimeoutException:
    print("Timeout reached for search: {}".format(c), file=sys.stderr)
    sys.exit(1)
else:
    signal.alarm(0)

tweets = twint.output.tweets_list

extractor = URLExtract()

for tweet in tweets:
    urls = extractor.find_urls(tweet.tweet)
    if r.exists("c:{}".format(tweet.id)):
        print("Tweet {} already processed".format(tweet.id), file=sys.stderr)
        if not args.nocache:
            continue
    else:
        r.set("c:{}".format(tweet.id), tweet.tweet)
        r.expire("c:{}".format(tweet.id), cache_expire)

    output_tweet = {}
    output_tweet['source'] = ailfeedertype
    output_tweet['source-uuid'] = uuid
    output_tweet['default-encoding'] = 'UTF-8'
    output_tweet['meta'] = {}
    output_tweet['meta']['twitter:tweet_id'] = tweet.id
    output_tweet['meta']['twitter:user_id'] = tweet.user_id
    output_tweet['meta']['twitter:id'] = tweet.username
    output_tweet['meta']['twitter:name'] = tweet.name
    output_tweet['meta']['twitter:link'] = tweet.link
    output_tweet['meta']['twitter:place'] = tweet.place
    output_tweet['meta']['twitter:geo'] = tweet.geo
    output_tweet['meta']['twitter:near'] = tweet.near
    output_tweet['meta']['twitter:urls'] = tweet.urls
    output_tweet['meta']['twitter:replies_count'] = tweet.replies_count
    output_tweet['meta']['twitter:retweets_count'] = tweet.retweets_count
    output_tweet['meta']['twitter:likes_count'] = tweet.likes_count
    output_tweet['meta']['twitter:source'] = tweet.source
    output_tweet['meta']['twitter:datestamp'] = tweet.datestamp
    output_tweet['meta']['twitter:timestamp'] = tweet.timestamp
    output_tweet['meta']['twitter:timezone'] = tweet.timezone

    m = hashlib.sha256()
    m.update(tweet.tweet.encode('utf-8'))
    output_tweet['data-sha256'] = m.hexdigest()
    output_tweet['data'] = base64.b64encode(gzip.compress(tweet.tweet.encode()))
    print(json.dumps(output_tweet, indent=4, sort_keys=True, default=jsonclean))
    ail_publish(data=json.dumps(output_tweet, indent=4, sort_keys=True, default=jsonclean))

    for url in urls:
        output = {}
        output['source'] = ailurlextract
        output['source-uuid'] = uuid
        output['default-encoding'] = 'UTF-8'
        output['meta'] = {}
        output['meta']['parent:twitter:tweet_id'] = tweet.id
        surl = url.split()[0]
        output['meta']['twitter:url-extracted'] = surl
        u = urlparse(surl)
        if u.hostname is not None:
            if "twitter.com" in u.hostname:
                continue
        if not validators.url(surl):
            continue
        if args.verbose:
            print("Downloading and parsing {}".format(surl), file=sys.stderr)
        signal.alarm(10)
        try:
            article = newspaper.Article(surl)
        except TimeoutException:
            print("Timeout reached for {}".format(surl), file=sys.stderr)
            continue
        else:
            signal.alarm(0)

        if r.exists("cu:{}".format(base64.b64encode(surl.encode()))):
            print("URL {} already processed".format(surl), file=sys.stderr)
            if not args.nocache:
               continue
        else:
            r.set("cu:{}".format(base64.b64encode(surl.encode())), tweet.tweet)
            r.expire("cu:{}".format(base64.b64encode(surl.encode())), cache_expire)

        try:
            article.download()
            article.parse()
        except:
            if args.verbose:
                print("Unable to download/parse {}".format(surl), file=sys.stderr)
            continue
        m = hashlib.sha256()
        m.update(article.html.encode('utf-8'))
        output['data-sha256'] = m.hexdigest()
        output['data'] = base64.b64encode(gzip.compress(article.html.encode()))
        output['meta']['newspaper:text'] = article.text
        output['meta']['newspaper:authors'] = article.authors
        try:
            article.nlp()
        except:
            if args.verbose:
                print("Unable to nlp {}".format(surl), file=sys.stderr)
            continue
        output['meta']['newspaper:keywords'] = article.keywords
        output['meta']['newspaper:publish_date'] = article.publish_date
        output['meta']['newspaper:top_image'] = article.top_image
        output['meta']['newspaper:movies'] = article.movies
        print(json.dumps(output, indent=4, sort_keys=True, default=jsonclean))
        ail_publish(data=json.dumps(output, indent=4, sort_keys=True, default=jsonclean))
