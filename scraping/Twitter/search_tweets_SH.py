''' 
SH
code adapted from https://towardsdatascience.com/an-extensive-guide-to-collecting-tweets-from-twitter-api-v2-for-academic-research-using-python-3-518fcb71df2a
'''

import argparse
import requests
import os
import json
import pandas as pd
import csv
import datetime
import dateutil.parser
import unicodedata
#To add wait time between requests
import time

BEARER_TOKEN = os.getenv('BEARER_TOKEN')

'''
create header for API calls
'''
def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

'''
create payload for API calls
'''
def create_payload(query, start_date, end_date, max_results = 10):
    
    search_url = "https://api.twitter.com/2/tweets/search/all" 

    query_params = {'query': query,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    'expansions': 'author_id,in_reply_to_user_id,attachments.media_keys,geo.place_id',
                    'tweet.fields': 'id,text,entities,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'next_token': {}}
    return (search_url, query_params)

'''
make API call
'''
def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    headers = create_headers(BEARER_TOKEN)
    parser = argparse.ArgumentParser(description='Get search terms.')
    parser.add_argument('--search_terms_file', type=str,
                        help='path of file with search terms')
    args = parser.parse_args()
    search_terms_file = args.search_terms_file

    # read keywords from file and create query
    search_keywords = []
    with open(search_terms_file) as f:
        search_keywords = f.readlines()

    search_keywords = [x.strip() for x in search_keywords]
    search_keywords = " OR ".join(search_keywords)
    query = "-is:retweet (" + search_keywords + ")"
    print("QUERY:", query)


    # start and end date
    start_time = "2021-07-01T00:00:00.000Z"
    end_time = "2021-12-28T00:00:00.000Z"

    # max num results per request
    max_results = 500
    #Total number of tweets we collected from the loop
    total_tweets = 0

    count = 0 # Counting tweets per time period
    max_count = 1000000 # Max tweets per time period (1M atm)
    flag = True
    first = True
    next_token = None
    full_response = {}
        
    # Check if flag is true
    while flag:
        # Check if max_count reached
        if count >= max_count:
            break

        print("-------------------")
        print("Token: ", next_token)
        payload = create_payload(query, start_time, end_time, max_results)
        json_response = connect_to_endpoint(payload[0], headers, payload[1], next_token)
        result_count = json_response['meta']['result_count']

        if 'next_token' in json_response['meta']:
            # Save the token to use for next call
            next_token = json_response['meta']['next_token']
            print("Next Token: ", next_token)
        else:
            #Since this is the final request, turn flag to false to move to the next time period.
            flag = False
            next_token = None

        # update counts and dictionary
        if result_count is not None and result_count > 0:
            count += result_count
            total_tweets += result_count
            print("Total # of Tweets added: ", total_tweets)
            print("-------------------")

            # merge json response with previous response
            if first:
                full_response = json_response
                first = False
            else:
                #  merge data and users with previous iteration
                full_response['data'].extend(json_response['data'])
                full_response['includes']['users'].extend(json_response['includes']['users'])

                # merge meta info
                if int(full_response['meta']['newest_id']) < int(json_response['meta']['newest_id']):
                    full_response['meta']['newest_id'] = json_response['meta']['newest_id']

                if int(full_response['meta']['oldest_id']) > int(json_response['meta']['oldest_id']):
                    full_response['meta']['newest_id'] = json_response['meta']['oldest_id']

                full_response['meta']['result_count'] = full_response['meta']['result_count'] + result_count

                if 'next_token' in json_response['meta']:
                    full_response['meta']['next_token'] = json_response['meta']['next_token']


        time.sleep(5)


    print("Total number of results: ", total_tweets)

    print("saving json")
    # output json file is named according to search terms, start date and end date
    with open(search_terms_file.split("\\")[-1].split(".")[0] + "#" + start_time.split("T")[0] + "@@" + end_time.split("T")[0] + ".json", 'w') as f:
        json.dump(full_response, f)



if __name__ == "__main__":
    main()