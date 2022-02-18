import time
import sys  # Need to have acces to sys.stdout
import os
import praw
import json
import threading


# different reddit auths. to reduce load on one key
reddit1 = praw.Reddit(
    client_id="4QiCBaZbQ_ofO5gl1P8BBA",
    client_secret="IAXh5qQIbRMKaYd4OGHvFCtaKj2epQ",
    user_agent="SH7",
    username = "paper_fern",
)

reddit2 = praw.Reddit(
    client_id="oYQthMoMvL2ERdGzAYPIlQ",
    client_secret="V0Gub34VCxchLp6ZxujTd38hReEPew",
    user_agent="SH8",
    username = "paper_band",
)

reddit3 = praw.Reddit(
    client_id="3k9BarswvGXgHmru21--Rg",
    client_secret="XLWXFLK3CCgvJxnqHVxlRtx4eh4B1g",
    user_agent="SH9",
    username = "paper_frodo",
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

    subreddits = ["offmychest", "askscience", "AskHistorians", "explainlikeimfive", "politics", "PoliticalHumor", "conspiracy", "socialism", "Anarcho_Capitalism"]
    threads = []
    writefiles = []

    # spawn thread for each subreddit
    for i in range(len(subreddits)):
        subreddit = subreddits[i]
        api = redditAPIs[i%3]
        try:
            wf = open("../data/reddit/comment_stream3/" + subreddit +".tsv", 'a', encoding = "utf-8")
        except:
            wf = open("../data/reddit/comment_stream3/" + subreddit +".tsv", 'w', encoding = "utf-8")

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

        
