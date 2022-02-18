'''Uses PRAW to scrape reddit posts. Note: using this endpoint results in a limit of 1000 posts'''

import argparse
import pandas as pd
import praw
import sys
import threading
import time


def get_submissions(reddit, subreddit_name):
    """Store info from all submissions into a Pandas dataframe"""
    submissions = []
    subreddit = reddit.subreddit(subreddit_name)

    for submission in subreddit.top(limit=100):
        submissions.append([submission.title, submission.score, submission.id, submission.subreddit, submission.url,
                            submission.num_comments, submission.selftext, submission.created])

    subreddit_posts = pd.DataFrame(submissions,
                         columns=['author', 'body', 'created', 'c_id', 's_id', 'p_id', 'permalink'])
    return subreddit_posts


def get_comments(threadID, subreddit, writefile):
    """Store info from all comments for each submission into a Pandas dataframe"""
    i=0
    for submission in subreddit.top(limit=1000):
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            i += 1
            print(threadID + " streamed: ", i)
            try:
                author = comment.author.id
            except:
                #occurs if author is deleted
                author = "N/A"
            body = comment.body.replace("\n", " ").replace("\r", " ").replace("\t", " ")
            created = str(comment.created_utc)
            c_id = str(comment.id)
            s_id = str(comment.link_id)
            p_id = str(comment.parent_id)
            permalink = str(comment.permalink)
            row = [author, body, created, c_id, s_id, p_id, permalink]
            line = "\t".join(row) + "\n"
        
            # some lines may throw error when writing to file
            try:
                writefile.write(line)
            except:
                continue

        time.sleep(0.5)


def run_thread(thread_ID, subreddit, redditAPI, writefile):
    '''create thread for streaming each subreddit'''
    while True:
        print ("Subreddit:", subreddit)
        subreddit = redditAPI.subreddit(subreddit)
        get_comments(thread_ID, subreddit, writefile)    


'''thread class'''
class myThread (threading.Thread):
   def __init__(self, threadID, subreddit, redditAPI, writefile):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.subreddit = subreddit
      self.redditAPI = redditAPI
      self.writefile = writefile

   def run(self):
      print ("Starting " + str(self.threadID) + " - " + self.subreddit)
      run_thread(self.threadID, self.subreddit, self.redditAPI, self.writefile)
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

    subreddits = ["AskReddit", "MensRights", "antifeminists", "unpopularopinion", "ChangeMyView", "AmITheAsshole", "Conservative", "FemaleDatingStrategy", "PoliticalCompassMemes"]
    threads = []
    writefiles = []

    # spawn thread for each subreddit
    for i in range(len(subreddits)):
        subreddit = subreddits[i]
        try:
            wf = open(args.out_dir + subreddit + ".tsv", 'a', encoding = "utf-8")
        except:
            wf = open(args.out_dir + subreddit + ".tsv", 'w', encoding = "utf-8")

        reddit = praw.Reddit(client_id=args.client_id, client_secret=args.client_secret, user_agent=args.user_agent, )

        writefiles.append(wf)

        thread = myThread(str(i) + "-" + subreddit, subreddit, reddit, wf)
        thread.daemon = True
        threads.append(thread)
        thread.start()
    
    # catch keyboard interruption, close threads and files
    try:
        while (True):
            time.sleep(.1)
    except KeyboardInterrupt:
        print('Interrupted, attempting to close all threads and files')

        for wf in writefiles:
            wf.close()
        print ("all files closed")
        
        for t in threads:
            t.join()

        print ("all threads joined")
        sys.exit(1)

if __name__ == "__main__":
    main()
