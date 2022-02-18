import argparse
import json
import tweepy

from tweepy import OAuthHandler

access_token = '1158580111660048384-LZ37eHV7Cgm8KknXVA25ZksM99mJSA'
access_token_secret = 'e5UV689XAPC1r5OkQuRDCtazMitDKSaNLOhyGizWTp6sL'

consumer_key = 'CrS9sXoZSr54ywlQibL0BnvZ' 
consumer_secret = 'MP8XxsZxYNHlWDD4YuawPq3JoXVFx40ZL6MxwCzdpevSa0a5mY'

# parse commandline arguments
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--search_terms_file', type=str,
                        help='path of file with search terms')
parser.add_argument('--language', type=str,
                        help='language to stream tweets for')
parser.add_argument('--outfile', type=str,
                        help='file to write stream data to')
args = parser.parse_args()


class StreamWriter(tweepy.Stream):

    def on_status(self, status):
        with open(args.outfile, "a+") as f:
            #json_response = json.loads(status)
            #print(json_response)
            f.write(json.dumps(status._json, indent=4, sort_keys=True))

    def on_error(self, status):
        print(status)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

stream = StreamWriter(
    'GVCKgmhswa6o4iBQIgG93WWTG',
    'ov8CywamGgZhEYpP0Y4DkvEwPeBgLNjlsYYl4e26L4U6j9B3dm',
    '1158580111660048384-LZ37eHV7Cgm8KknXVA25ZksM99mJSA',
    'e5UV689XAPC1r5OkQuRDCtazMitDKSaNLOhyGizWTp6sL'
)

def main():
    # get keywords from text file
    search_keywords = []
    with open(args.search_terms_file) as f:
        search_keywords = f.readlines()
    search_keywords = [x.strip() for x in search_keywords]

    stream.filter(track=search_keywords, languages=[args.language])

if __name__ == "__main__":
    main()