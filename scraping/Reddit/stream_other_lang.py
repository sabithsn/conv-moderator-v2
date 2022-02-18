import time
import sys  # Need to have acces to sys.stdout
import os
import praw
import json
import threading


# different reddit auths. to reduce load on one key
reddit1 = praw.Reddit(
    client_id="oBYI_wZFIzZNSngQYrDGUQ",
    client_secret="LuRblKfUyu0cfvtPPhDFQmACb3U3jA",
    user_agent="SH1",
    username = "paper_crow",
)

reddit2 = praw.Reddit(
    client_id="Of2n4lF-DEnwLeVH6BBkrA",
    client_secret="C0HhaNoggtRt1mS8j3louIHOTuD5ZA",
    user_agent="SH2",
    username = "paper_rain_",
)

reddit3 = praw.Reddit(
    client_id="paqHNMpcHa2eA6VrgPBEsQ",
    client_secret="U_cepXEaDb_ya1aLF6iytv_8BL7-TQ",
    user_agent="SH3",
    username = "paper_hat_64",
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

    subreddits = ["arabs", "egypt", "saudiarabia", "russian", "russia", "AskARussian", "French", "france", "mangafr"]
    threads = []
    writefiles = []

    # spawn thread for each subreddit
    for i in range(len(subreddits)):
        subreddit = subreddits[i]
        api = redditAPIs[i%3]
        try:
            wf = open("../data/reddit/other_lang_stream/" + subreddit +".tsv", 'a', encoding = "utf-8")
        except:
            wf = open("../data/reddit/other_lang_stream/" + subreddit +".tsv", 'w', encoding = "utf-8")

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

        
