import time
import sys  # Need to have acces to sys.stdout
import os
import praw
import json

reddit = praw.Reddit(
    client_id="oBYI_wZFIzZNSngQYrDGUQ",
    client_secret="LuRblKfUyu0cfvtPPhDFQmACb3U3jA",
    user_agent="Sabit Hassan",
    username = "paper_crow",
)

def stream_reddit(writefile,subreddit):

    i = 0
    for comment in subreddit.stream.comments():
        i += 1
        print ("streamed:", i)
        author = comment.author.id
        body = comment.body.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        time = str(comment.created_utc)
        c_id = str(comment.id)
        s_id = str(comment.link_id)
        p_id = str(comment.parent_id)
        permalink = str(comment.permalink)
        row = [author, body, time, c_id, s_id, p_id, permalink]
        line = "\t".join(row) + "\n"
        try:
            writefile.write(line)
        except:
            continue

if __name__ == '__main__':
    try:
        subreddit = sys.argv[1]
        print ("Subreddit:", subreddit)
        writefile = open(subreddit+".tsv", 'a', encoding = "utf-8")

        subreddit = reddit.subreddit(subreddit)
        print(subreddit.display_name)
        print(subreddit.title)
        print(subreddit.description)

        stream_reddit(writefile,subreddit)

    except KeyboardInterrupt:
        print('Interrupted')
        writefile.close() # to not forget to close your file
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


