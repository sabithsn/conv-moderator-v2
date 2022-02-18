import praw

reddit = praw.Reddit(
    client_id="oBYI_wZFIzZNSngQYrDGUQ",
    client_secret="LuRblKfUyu0cfvtPPhDFQmACb3U3jA",
    user_agent="Sabit Hassan",
)


print ("hello world")
print(reddit.read_only)


subname = "antifeminists"

# assume you have a reddit instance bound to variable `reddit`
subreddit = reddit.subreddit(subname)
print(subreddit.display_name)
# Output: redditdev
print(subreddit.title)
# Output: reddit development
print(subreddit.description)
# Output: a subreddit for discussion of ...
print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

# assume you have a Subreddit instance bound to variable `subreddit`
i = 0
deleted = 0
with open (subname + ".tsv", "w") as f:
    for submission in subreddit.new(limit=None):
        if (i == 2000):
            break
        i += 1
        if (i % 100 == 0):
            print (i)
    ##    print(submission.title)
    ##    print (submission.author)
        if (submission.author is None):
            print ("holla", submission.url)
            f.write(submission.id + "\t" + submission.title + "\t" + submission.url + submission.selftext.replace("\n", " ").replace("\r", " ") + "\n")
            deleted += 1
        # Output: the submission's title
    ##    print(submission.score)
        # Output: the submission's score
    ##    print(submission.id)
        # Output: the submission's ID
    ##    print(submission.url)
        # Output: the URL the submission points to or the submission's URL if it's a self post
        
print ("posts crawled", i)
print ("deleted comments", deleted)

