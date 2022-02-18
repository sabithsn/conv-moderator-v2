import time
import sys  # Need to have acces to sys.stdout
import os
import praw
import json
import threading


# different reddit auths. to reduce load on one key
reddit1 = praw.Reddit(
    client_id="p0Zc36SNOM2JSp9N6X2TGg",
    client_secret="_kSgueqBRuvQ1qk1eaqgHmqnDXmWjQ",
    user_agent="SH4",
    username = "paper_cycle",
)

reddit2 = praw.Reddit(
    client_id="G7E26vvmd0Dc0j9qKCA6yQ",
    client_secret="ZR4O2cBBmDcykyGAGfC4iyo7MbfetA",
    user_agent="SH5",
    username = "paper_ring",
)

reddit3 = praw.Reddit(
    client_id="aq0X1TQf99TO9OgI5I-SoA",
    client_secret="QndINhrLpYAjL3lZOZl7-BvlVxpRpg",
    user_agent="SH6",
    username = "paper_basket",
)

redditAPIs = [reddit1, reddit2, reddit3]


''' stream new reddit comments and write to file '''
def stream_reddit(threadID, subreddit, writefile):

    i = 0
    for comment in subreddit.stream.comments():
        i += 1
        print (threadID + " streamed: ", i)

        # parse comment object
        author = comment.author.id
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

'''create thread for streaming each subreddit'''
def run_thread(thread_ID, subreddit, redditAPI, writefile):
    while True:
        print ("Subreddit:", subreddit)
        subreddit = redditAPI.subreddit(subreddit)
        stream_reddit(thread_ID, subreddit, writefile)    


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



if __name__ == '__main__':

    subreddits = ["AskReddit", "MensRights", "antifeminists", "unpopularopinion", "ChangeMyView", "AmITheAsshole", "Conservative", "FemaleDatingStrategy", "PoliticalCompassMemes"]
    threads = []
    writefiles = []

    # spawn thread for each subreddit
    for i in range(len(subreddits)):
        subreddit = subreddits[i]
        api = redditAPIs[i%3]
        try:
            wf = open("../data/reddit/comment_stream2/" + subreddit +".tsv", 'a', encoding = "utf-8")
        except:
            wf = open("../data/reddit/comment_stream2/" + subreddit +".tsv", 'w', encoding = "utf-8")

        writefiles.append(wf)

        thread = myThread(str(i) + "-" + subreddit, subreddit, api, wf)
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

        
