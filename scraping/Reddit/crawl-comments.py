import praw
from psaw import PushshiftAPI
import time
import pandas as pd
import datetime as dt
import os
import json

api = PushshiftAPI()
reddit = praw.Reddit(
    client_id="oBYI_wZFIzZNSngQYrDGUQ",
    client_secret="LuRblKfUyu0cfvtPPhDFQmACb3U3jA",
    user_agent="Sabit Hassan",
    username = "paper_crow",
)


subreddit = "antifeminists"

ts_after = int(dt.datetime(2021, 10, 1).timestamp())
ts_before = int(dt.datetime(2021, 12, 28).timestamp())

gen = api.search_comments(subreddit = subreddit)


max_response_cache =100
all_comments = []
deleted_comments = []

i = 0
deleted_count = 0
for comment in gen:
    i += 1
    print (i)
    if (i % 10 == 0):
        print (i)

    atts = comment.d_
    # print (atts['author'], atts['body'])
    praw_comment = reddit.comment(id = atts['id'])
    # print (praw_comment.author, praw_comment.body)
    # print (praw_comment)
    all_comments.append(atts)
    if praw_comment.author is None or praw_comment.body.lower() == "[deleted]" or praw_comment.body.lower() == "[removed]":
        print (atts['body'])
        print (praw_comment.body)
        deleted_comments.append(atts)
        deleted_count += 1

        print ("seen so far, %d, deleted so far %d" (i,deleted_count))


    # Omit this test to actually return all results. Wouldn't recommend it though: could take a while, but you do you.
    if i >= max_response_cache:
        break

print ("saving json")

with open("deleted#" + subreddit + "#2021-10-1@@2021-12-28.json", 'w') as f:
    json.dump(deleted_comments, f)

with open("all#" + subreddit + "#2021-10-1@@2021-12-28.json", 'w') as f:
    json.dump(all_comments, f)