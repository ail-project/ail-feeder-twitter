# AIL - feeder from Twitter

This AIL feeder is a generic software to extract specific urls from Twitter, collect and feed AIL via ZMQ.

# Usage

~~~shell
adulau@dobbertin:~/git/ail-feeder-twitter/bin$ python3 feeder.py --help
usage: feeder.py [-h] [--verbose] [--nocache] [--tweetlimit TWEETLIMIT] query

positional arguments:
  query                 query to search on Twitter to feed AIL

optional arguments:
  -h, --help            show this help message and exit
  --verbose             verbose output
  --nocache             disable cache
  --tweetlimit TWEETLIMIT
                        maximum number of tweet to fetch
~~~

# JSON output format to AIL

~~~~json
{
    "data": "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",
    "data-sha256": "3398ba5ddfd05ffd7c45f1711759321c6183d4312dfd5a327c34212694e31592",
    "default-encoding": "UTF-8",
    "meta": {
        "newspaper:authors": [],
        "newspaper:keywords": [
            "open",
            "exchange",
            "threat"
        ],
        "newspaper:movies": [],
        "newspaper:publish_date": null,
        "newspaper:text": "",
        "newspaper:top_image": "https://otx.alienvault.com/assets/images/otx-logo-twitter-square.png",
        "twitter:datestamp": "2020-04-27",
        "twitter:geo": "",
        "twitter:id": "ozuma5119",
        "twitter:likes_count": "1",
        "twitter:link": "https://twitter.com/ozuma5119/status/1254705226973450240",
        "twitter:name": "Osumi, Yusuke\ud83d\ude07",
        "twitter:near": "",
        "twitter:place": "",
        "twitter:replies_count": "0",
        "twitter:retweets_count": "1",
        "twitter:source": "",
        "twitter:timestamp": "11:33:32",
        "twitter:timezone": "CEST",
        "twitter:tweet": "#Phishing Alert\u26a0 www\\.support-01\\.info\nhxxp://au-jjg[.]com/\nIP: 154.202.14[.]62 (CloudInnovation,SC&CN) #AfriNIC\nRegistrant: dugattreubertf6sb6@{yahoo^.co^.jp,gmail^.com}\n  https://pastebin.com/gut5rdj2\u00a0\nBrand: au KDDI (Japan)\n\n https://urlscan.io/result/b0307a8a-35a5-407d-9d33-23b8f4fe0c1f/\u00a0\u2026\n#MoqHao  https://otx.alienvault.com/pulse/5de7e1b56675ecc611a42504\u00a0\u2026 pic.twitter.com/VDUVmTmKm0",
        "twitter:tweet_id": 1254705226973450240,
        "twitter:url-extracted": "https://otx.alienvault.com/pulse/5de7e1b56675ecc611a42504",
        "twitter:urls": [
            "https://pastebin.com/gut5rdj2",
            "https://urlscan.io/result/b0307a8a-35a5-407d-9d33-23b8f4fe0c1f/",
            "https://otx.alienvault.com/pulse/5de7e1b56675ecc611a42504"
        ],
        "twitter:user_id": 79207749
    },
    "source": "ail-feeder-twitter",
    "source-uuid": "aae656ec-d446-4a21-acf0-c88d4e09d506"
}

~~~~

 - `source` is the name of the AIL feeder module
 - `source-uuid` is the UUID of the feeder (unique per feeder)
 - `data` is the base64 encoded value of the gziped data
 - `data-sha256` is the SHA256 value of the uncompress data
 - `meta` is the generic field where feeder can add the metadata collected

