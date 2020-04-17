# AIL - feeder from Twitter

This AIL feeder is a generic software to extract specific urls from Twitter, collect and feed AIL via ZMQ.

# JSON output format to AIL

~~~~json
{
        "source": "ail-feeder-twitter",
        "source-uuid": "f790c3da-0238-4be4-9e28-edbe25e58ad9",
        "data": "My44IiwKICAgICJMaWNlbnNlIDo6IE9TSSBBcHByb3ZlZCA6OiBHTlUgQWZmZXJvIEdlbmVyYWwg"
        "data-sha256": "0f77b3d9c0ea1f15ec7d68703a4e4b3926e52c9c37e02b39b0ad0b1783128ff1",
        "meta": {
                "twitter-id": "adulau",
                "tweet-id": "1251033245724086272"        
                
        }
}
~~~~

 - `source` is the name of the AIL feeder module
 - `source-uuid` is the UUID of the feeder (unique per feeder)
 - `data` is the base64 encoded value of the gziped data
 - `data-sha256` is the SHA256 value of the uncompress data
 - `meta` is the generic field where feeder can add the metadata collected

