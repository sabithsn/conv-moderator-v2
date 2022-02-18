import argparse
import datetime
import json
import os
import requests
import sys
import time

from datetime import timezone

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
#bearer_token = os.environ.get("BEARER_TOKEN")
bearer_token = 'AAAAAAAAAAAAAAAAAAAAACxmPwEAAAAAacEMQfc2DpZEkDPQpVN5hqfRYf4%3DFsl1gwLjllavgDUmT0Nwn27ZSdntTzaum5dY6vEQAVmRKAIb6e'

search_url = "https://api.twitter.com/2/tweets/search/all"


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", search_url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def main():
    headers = create_headers(bearer_token)
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--search_terms_file', type=str,
                        help='path of file with search terms')

    args = parser.parse_args()

    start_date = datetime.datetime(2019, 12, 1, 0, 0, 0, 0, timezone.utc).astimezone()
    end_date = datetime.datetime(2019, 12, 31, 0, 0, 0, 0, timezone.utc).astimezone()

    search_keywords = []
    with open(args.search_terms_file) as f:
        search_keywords = f.readlines()

    search_keywords = [x.strip for x in search_keywords]
    print(search_keywords)

    query_params = {'tweet.fields': 'author_id,created_at,geo,lang,public_metrics,referenced_tweets',
                    "max_results": "500"
                    }

    delta = datetime.timedelta(days=1)

    while start_date <= end_date:
        date_since = start_date.isoformat()
        date_until = (start_date + delta).isoformat()
        print(date_since + " - " + date_until)
        query_params["start_time"] = date_since
        query_params["end_time"] = date_until
        for keyword in search_keywords:
            query_params["query"] = keyword
            tweets = []
            print(keyword)
            while True:
                try:
                    json_response = connect_to_endpoint(search_url, headers, query_params)
                except:
                    print("Exceeded rate limit")
                    time.sleep(10)

                try:
                    for tweet in json_response["data"]:
                        tweets.append(tweet)
                except:
                    pass

                if "next_token" in json_response["meta"]:
                    next_token = json_response["meta"]["next_token"]
                    query_params["next_token"] = next_token
                else:
                    break

            if "next_token" in query_params:
                query_params.pop('next_token')
            
            filename = date_since + "_" + date_until + "_" + keyword + ".txt"
            with open(filename, 'w') as filehandle:
                filehandle.write(json.dumps(tweets))

        start_date += delta

if __name__ == "__main__":
    main()