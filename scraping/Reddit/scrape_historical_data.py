'''Queries the Reddit API directly for posts. Note: using this endpoint results in a limit of 1000 posts'''
'''Based on this tutorial: https://medium.com/geekculture/utilizing-reddits-api-8d9f6933e192'''

import argparse
import pandas as pd
import requests
import sys
import threading
import time


def get_comments(threadID, subreddit_name, headers, writefile):
    '''get all historical comments in a subreddit'''
    api = 'https://oauth.reddit.com'
    df = pd.DataFrame({'name': [], 'title': [], 'selftext': [], 'score': []})
    res = requests.get('{}/r/{}/new'.format(api, subreddit_name), headers=headers, params={'limit': '100'})

    for post in res.json()['data']['children']:
        df = df.append({
            'name': post['data']['name'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'score': post['data']['score']}, ignore_index=True)

    i = 0
    while True:
        i += len(res.json()['data']['children'])
        print (threadID + " streamed: ", i)
        print("after:", df['name'].iloc[len(df) - 1])
        res = requests.get('{}/r/{}/new'.format(api, subreddit_name),headers=headers, params={'limit': '100','after': df['name'].iloc[len(df) - 1]})
        if len(res.json()['data']['children']) == 0:
            print('No more posts found')
            break
        for post in res.json()['data']['children']:
            df = df.append({
            'name': post['data']['name'], 
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'score': post['data']['score']}, ignore_index=True)

    df.to_csv(writefile)


def run_thread(thread_ID, subreddit, headers, writefile):
    '''create thread for streaming each subreddit'''
    print ("Subreddit:", subreddit)
    get_comments(thread_ID, subreddit, headers, writefile)    


'''thread class'''
class myThread (threading.Thread):
   def __init__(self, threadID, subreddit, headers, writefile):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.subreddit = subreddit
      self.headers = headers
      self.writefile = writefile

   def run(self):
      print ("Starting " + str(self.threadID) + " - " + self.subreddit)
      run_thread(self.threadID, self.subreddit, self.headers, self.writefile)
      print ("Exiting " + str(self.threadID) + " - " + self.subreddit)


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--client_id', type=str,
                        help='client ID')
    parser.add_argument('--client_secret', type=str,
                        help='client secret')
    parser.add_argument('--user_agent', type=str,
                        help='user agent')
    parser.add_argument('--out_dir', type=str,
                        help='directory to write stream data to')
    args = parser.parse_args()

    auth = requests.auth.HTTPBasicAuth(args.client_id, args.client_secret)

    reddit_username = 'grad-student12345'
    reddit_password = 'catsareaw3some'
    data = {
        'grant_type': 'password',
        'username': reddit_username,
        'password': reddit_password
    }

    headers = {'User-Agent': args.user_agent}
    res = requests.post('https://www.reddit.com/api/v1/access_token',
    auth=auth, data=data, headers=headers)

    token = res.json()['access_token']
    headers['Authorization'] = 'bearer {}'.format(token)

    subreddits = ["AskReddit", "MensRights", "antifeminists", "unpopularopinion", "ChangeMyView", "AmITheAsshole", "Conservative", "FemaleDatingStrategy", "PoliticalCompassMemes"]
    threads = []
    writefiles = []

    # spawn thread for each subreddit
    for i in range(len(subreddits)):
        subreddit = subreddits[i]
        # try:
        #     wf = open(args.out_dir + subreddit + ".tsv", 'a', encoding = "utf-8")
        # except:
        #     wf = open(args.out_dir + subreddit + ".tsv", 'w', encoding = "utf-8")

        # writefiles.append(wf)
        wf = args.out_dir + subreddit + ".tsv"

        thread = myThread(str(i) + "-" + subreddit, subreddit, headers, wf)
        thread.daemon = True
        threads.append(thread)
        thread.start()
    
    # catch keyboard interruption, close threads and files
    try:
        while (True):
            time.sleep(.1)
    except KeyboardInterrupt:
        print('Interrupted, attempting to close all threads and files')

        # for wf in writefiles:
        #     wf.close()
        # print ("all files closed")
        
        for t in threads:
            t.join()

        print ("all threads joined")
        sys.exit(1)

if __name__ == "__main__":
    main()
