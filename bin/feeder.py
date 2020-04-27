#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import twint
from urlextract import URLExtract
import newspaper
import validators
import hashlib
import base64
import zlib
import simplejson as json
import redis
import sys
import datetime
import configparser
import argparse

def jsonclean(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

uuid = "aae656ec-d446-4a21-acf0-c88d4e09d506"
ailfeedertype = "ail-feeder-twitter"

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

twint.run.Search(c)
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
    for url in urls:
        output = {}
        output['source'] = ailfeedertype
        output['source-uuid'] = uuid
        output['default-encoding'] = 'UTF-8'
        output['meta'] = {}
        output['meta']['twitter:tweet_id'] = tweet.id
        output['meta']['twitter:user_id'] = tweet.user_id
        output['meta']['twitter:id'] = tweet.username
        output['meta']['twitter:tweet'] = tweet.tweet
        output['meta']['twitter:name'] = tweet.name
        output['meta']['twitter:link'] = tweet.link
        output['meta']['twitter:place'] = tweet.place
        output['meta']['twitter:geo'] = tweet.geo
        output['meta']['twitter:near'] = tweet.near
        output['meta']['twitter:urls'] = tweet.urls
        output['meta']['twitter:replies_count'] = tweet.replies_count
        output['meta']['twitter:retweets_count'] = tweet.retweets_count
        output['meta']['twitter:likes_count'] = tweet.likes_count
        output['meta']['twitter:source'] = tweet.source
        output['meta']['twitter:datestamp'] = tweet.datestamp
        output['meta']['twitter:timestamp'] = tweet.timestamp
        output['meta']['twitter:timezone'] = tweet.timezone
        surl = url.split()[0]
        output['meta']['twitter:url-extracted'] = surl
        if not validators.url(surl):
            continue
        if args.verbose:
            print("Downloading and parsing {}".format(surl), file=sys.stderr)
        article = newspaper.Article(surl)
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
        output['data'] = base64.b64encode(zlib.compress(article.html.encode()))
        output['meta']['newspaper:text'] = article.text
        output['meta']['newspaper:authors'] = article.authors
        article.nlp()
        output['meta']['newspaper:keywords'] = article.keywords
        output['meta']['newspaper:publish_date'] = article.publish_date
        output['meta']['newspaper:top_image'] = article.top_image
        output['meta']['newspaper:movies'] = article.movies
        print(json.dumps(output, indent=4, sort_keys=True, default=jsonclean))

