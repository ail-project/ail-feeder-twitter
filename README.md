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
    "data-sha256": "e7ef2750b22359af0e9ddf251e6babcf10f84b5516563a9a6b22332a67c4ced5",
    "default-encoding": "UTF-8",
    "meta": {
        "newspaper:authors": [],
        "newspaper:keywords": [
            "buffer",
            "printf",
            "cs50h",
            "jpeg",
            "camera",
            "512",
            "stdioh",
            "stdinth",
            "stdlibh",
            "include",
            "c",
            "count",
            "int",
            "0xff",
            "img"
        ],
        "newspaper:movies": [],
        "newspaper:publish_date": null,
        "newspaper:text": "Untitled a guest Apr 28th, 2020 27 Never a guest27Never\n\nNot a member of Pastebin yet? Sign Up , it unlocks many cool features!\n\nrawdownloadcloneembedreportprint C 1.94 KB #include <stdio.h> #include <stdlib.h> #include <cs50.h> #include <stdint.h> //a jpeg starts with 0xff, 0xd8,0xff, and 0xe(x) int main ( int argc , char * argv [ ] ) { char picName [ 10 ] ; int count = 0 ; int block = 0 ; if ( argc != 2 ) { printf ( \"Usage: ./recover image\" ) ; return 1 ; } FILE * camera = fopen ( argv [ 1 ] , \"r\" ) ; uint8_t buffer [ 512 ] ; FILE * img ; //read a byte with size 1, with there being 512 bytes. Store in buffer while ( fread ( buffer , 1 , 512 , camera ) == 512 ) //keep reading the card, each block is 512 bytes { if ( buffer [ 0 ] == 0xff && buffer [ 1 ] == 0xd8 && buffer [ 2 ] == 0xff ) { //checking to see if 4th byte is jpeg header valid if ( buffer [ 3 ] >= 0xe0 && buffer [ 3 ] <= 0xef ) { printf ( \"%x\n\n\" , buffer [ 0 ] ) ; printf ( \"%x\n\n\" , buffer [ 1 ] ) ; printf ( \"%x\n\n\" , buffer [ 2 ] ) ; printf ( \"%x\n\n\" , buffer [ 3 ] ) ; count += 1 ; //count is number of jpegs found //closing jpeg if it is not the first if ( count > 1 ) { fclose ( img ) ; } printf ( \"pictures found: %i\" , count ) ; sprintf ( picName , \"%03i.jpg\" , count - 1 ) ; img = fopen ( picName , \"w\" ) ; fwrite ( buffer , 1 , 512 , img ) ; while ( true ) { fread ( buffer , 1 , 512 , camera ) ; //write into img until the next jpeg is encountered if ( buffer [ 0 ] == 0xff && buffer [ 1 ] == 0xd8 && buffer [ 2 ] == 0xff ) { if ( buffer [ 3 ] >= 0xe0 && buffer [ 3 ] <= 0xef ) { break ; } } fwrite ( buffer , 1 , 512 , img ) ; } } } } }\n\nRAW Paste Data\n\n#include <stdio.h> #include <stdlib.h> #include <cs50.h> #include <stdint.h> //a jpeg starts with 0xff, 0xd8,0xff, and 0xe(x) int main(int argc, char *argv[]) { char picName[10]; int count = 0; int block = 0; if (argc != 2) { printf(\"Usage: ./recover image\"); return 1; } FILE *camera = fopen(argv[1], \"r\"); uint8_t buffer[512]; FILE *img; //read a byte with size 1, with there being 512 bytes. Store in buffer while(fread(buffer, 1, 512, camera) == 512) //keep reading the card, each block is 512 bytes { if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff) { //checking to see if 4th byte is jpeg header valid if (buffer[3] >= 0xe0 && buffer[3] <= 0xef) { printf(\"%x\n\n\", buffer[0]); printf(\"%x\n\n\", buffer[1]); printf(\"%x\n\n\", buffer[2]); printf(\"%x\n\n\", buffer[3]); count += 1; //count is number of jpegs found //closing jpeg if it is not the first if (count > 1) { fclose(img); } printf(\"pictures found: %i\", count); sprintf(picName, \"%03i.jpg\", count - 1); img = fopen(picName, \"w\"); fwrite(buffer, 1, 512, img); while (true) { fread(buffer, 1, 512, camera); //write into img until the next jpeg is encountered if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff) { if (buffer[3] >= 0xe0 && buffer[3] <= 0xef) { break; } } fwrite(buffer, 1, 512, img); } } } } }",
        "newspaper:top_image": "https://pastebin.com/i/facebook.png",
        "twitter:datestamp": "2020-04-28",
        "twitter:geo": "",
        "twitter:id": "fuckingfaiiure",
        "twitter:likes_count": "0",
        "twitter:link": "https://twitter.com/fuckingfaiIure/status/1255111711142506498",
        "twitter:name": "\ud835\ude96\ud835\ude8a\ud835\ude97\ud835\udea0\ud835\ude98\ud835\ude95",
        "twitter:near": "",
        "twitter:place": "",
        "twitter:replies_count": "0",
        "twitter:retweets_count": "0",
        "twitter:source": "",
        "twitter:timestamp": "14:28:45",
        "twitter:timezone": "CEST",
        "twitter:tweet": " https://pastebin.com/ZkW49rmr\u00a0",
        "twitter:tweet_id": 1255111711142506498,
        "twitter:url-extracted": "https://pastebin.com/ZkW49rmr",
        "twitter:urls": [
            "https://pastebin.com/ZkW49rmr"
        ],
        "twitter:user_id": 1134504082759045120
    },
    "source": "ail_feeder_twitter",
    "source-uuid": "aae656ec-d446-4a21-acf0-c88d4e09d506"
}
~~~~

 - `source` is the name of the AIL feeder module
 - `source-uuid` is the UUID of the feeder (unique per feeder)
 - `data` is the base64 encoded value of the gziped data
 - `data-sha256` is the SHA256 value of the uncompress data
 - `meta` is the generic field where feeder can add the metadata collected
