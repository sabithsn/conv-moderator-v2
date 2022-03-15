import time
import sys  # Need to have acces to sys.stdout
import os
import praw
import json
import threading

from knockknock import slack_sender


webhook_url = "https://hooks.slack.com/services/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"

# different reddit auths. to reduce load on one key
reddit1 = praw.Reddit(
    client_id="g_5TADErbq49hr9PDByTBw",
    client_secret="d0p1t8Yr75H-5pJ401NBKYD_G4C1yg",
    user_agent="Conversational Moderator",
    username = "DebateTime5118",
)

reddit2 = praw.Reddit(
    client_id="CeH_bJZluREDNEv4uOBe4g",
    client_secret="0zdQ_uZ1gTEa539A27t0ntQ_7O2Efg",
    user_agent="Conversational Moderator",
    username = "PossiblyMundane31",
)

reddit3 = praw.Reddit(
    client_id="n82NxGGLfiVR9gXmllQ1kw",
    client_secret="zJ-h1VOD1Hi2dMYsvY6JiPw0xiGS_Q",
    user_agent="Conversational Moderator",
    username = "Imaginary_North_5376",
)

reddit4 = praw.Reddit(
    client_id="ttRKLeozxm67Rr87Jv-jEw",
    client_secret="bQPZGya5tXzXbv1nHM27nm00KkU9gg",
    user_agent="Conversational Moderator",
    username = "Empty-Cartographer78",
)

redditAPIs = [reddit1, reddit2, reddit3, reddit4]


''' stream new reddit comments and write to file '''
def stream_reddit(threadID, subreddit, writefile):

    i = 0
    for post in subreddit.stream.submissions():
        i += 1
        print (threadID + " streamed: ", i)

        # parse comment object
        try:
            author = post.author.id
        except: 
            author = "None"
        body = post.selftext.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        created = str(post.created_utc)
        c_id = str(post.id)
        permalink = str(post.permalink)
        title = str(post.title)
        row = [author, body, created, c_id, permalink, title]
        line = "\t".join(row) + "\n"
        
        # some lines may throw error when writing to file
        try:
            writefile.write(line)
        except:
            continue

        time.sleep(0.5)

'''create thread for streaming each subreddit'''
@slack_sender(webhook_url=webhook_url, channel="#conversational-moderator")
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

    subreddits = ["AskReddit", "MensRights", "antifeminists", "unpopularopinion", "ChangeMyView", "AmITheAsshole", "Conservative", "FemaleDatingStrategy", "PoliticalCompassMemes",
    "offmychest", "askscience", "AskHistorians", "explainlikeimfive", "politics", "PoliticalHumor", "conspiracy", "socialism", "Anarcho_Capitalism",
    "arabs", "egypt", "saudiarabia", "russian", "russia", "AskARussian", "French", "france"
    ]
    threads = []
    writefiles = []

    # spawn thread for each subreddit
    for i in range(len(subreddits)):
        subreddit = subreddits[i]
        api = redditAPIs[i%3]
        try:
            wf = open("../data/reddit/post_stream/" + subreddit +".tsv", 'a', encoding = "utf-8")
        except:
            wf = open("../data/reddit/post_stream/" + subreddit +".tsv", 'w', encoding = "utf-8")

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

        
