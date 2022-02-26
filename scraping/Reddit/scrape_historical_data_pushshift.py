'''Uses Pushshift to scrape reddit posts. This will allow you to get all historical posts without a limit'''
'''Based on this tutorial: https://medium.com/swlh/how-to-scrape-large-amounts-of-reddit-data-using-pushshift-1d33bde9286'''

import argparse
import pandas as pd
import pmaw
import praw
import sys
import threading
import time

from pmaw import PushshiftAPI
from tqdm import tqdm


def get_comments_from_top_n_submissions(threadID, subreddit, api, writefile):
    submission_ids = list(api.search_submissions(
        subreddit = subreddit,        
        limit = 1000,
    ))
    for submission_id in tqdm(submission_ids):  
        comment_ids = api.search_submission_comment_ids(ids=submission_id)
        for comment in tqdm(api.search_comments(ids=comment_ids)):
            print(comment)


def get_comments(threadID, subreddit, api, writefile):
    comments = api.search_comments(subreddit=subreddit)
    comments_df = pd.DataFrame(comments)
    comments_df.to_csv(writefile, header=True, index=False, columns=list(comments_df.axes[1]))
    

'''create thread for streaming each subreddit'''
def run_thread(thread_ID, subreddit, api, writefile):
    while True:
        print ("Subreddit:", subreddit)
        get_comments(thread_ID, subreddit, api, writefile)    


'''thread class'''
class myThread (threading.Thread):
   def __init__(self, threadID, subreddit, api, writefile):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.subreddit = subreddit
      self.api = api
      self.writefile = writefile

   def run(self):
      print ("Starting " + str(self.threadID) + " - " + self.subreddit)
      run_thread(self.threadID, self.subreddit, self.api, self.writefile)
      print ("Exiting " + str(self.threadID) + " - " + self.subreddit)


def main():
    parser = argparse.ArgumentParser(description='Credentials and output info')
    parser.add_argument('--client_id', type=str,
                        help='client ID')
    parser.add_argument('--client_secret', type=str,
                        help='client secret')
    parser.add_argument('--user_agent', type=str,
                        help='user agent')
    parser.add_argument('--out_dir', type=str,
                        help='directory to write stream data to')
    args = parser.parse_args()

    #subreddits = ["AskReddit", "MensRights", "antifeminists", "unpopularopinion", "ChangeMyView", "AmITheAsshole", "Conservative", "FemaleDatingStrategy", "PoliticalCompassMemes"]
    subreddits = ["AmITheAsshole", "AskHistorians", "AskReddit", "AskScience", "ChangeMyView", "Conspiracy"]#, "ExplainLikeImFive", "OffMyChest", "PoliticalHumor", "UnpopularOpinion"]
    threads = []
    writefiles = []

    reddit = praw.Reddit(client_id=args.client_id, client_secret=args.client_secret, user_agent=args.user_agent)
    api = PushshiftAPI(praw=reddit)

    # spawn thread for each subreddit
    for i in range(len(subreddits)):
        subreddit = subreddits[i]
        print(subreddit)
        # try:
        #     wf = open(args.out_dir + subreddit + ".tsv", 'a', encoding = "utf-8")
        # except:
        #     wf = open(args.out_dir + subreddit + ".tsv", 'w', encoding = "utf-8")

        # writefiles.append(wf)

        # submission_ids = list(api.search_submissions(
        #     subreddit = subreddit,        
        #     limit = 1000,
        # ))
        # for submission_id in tqdm(submission_ids):  
        #     comment_ids = api.search_submission_comment_ids(ids=submission_id)
        #     for comment in tqdm(api.search_comments(ids=comment_ids)):
        #         print(comment)

        comments = api.search_comments(subreddit=subreddit, limit=1000000)
        comments_df = pd.DataFrame(comments)
        comments_df.to_csv(args.out_dir + subreddit + ".tsv", header=True, index=False, columns=list(comments_df.axes[1]), sep="\t")

        # thread = myThread(str(i) + "-" + subreddit, subreddit, api, wf)
        # thread.daemon = True
        # threads.append(thread)
        # thread.start()
    
    # catch keyboard interruption, close threads and files
    # try:
    #     while (True):
    #         time.sleep(.1)
    # except KeyboardInterrupt:
    #     print('Interrupted, attempting to close all threads and files')

    #     for wf in writefiles:
    #         wf.close()
    #     print ("all files closed")
        
    #     for t in threads:
    #         t.join()

    #     print ("all threads joined")
    #     sys.exit(1)

if __name__ == "__main__":
    main()
