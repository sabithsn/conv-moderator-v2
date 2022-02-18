import sys
import praw
import timeit

# auth
reddit = praw.Reddit(
    client_id="nIPvIISM35QMMygjPVhPzw",
    client_secret="vLPYCQMVskhu9zTDT0xn6-j86uf5Hw",
    user_agent="SH4",
    username = "paper_scraper",
    password = "Darpa2021"
)

c_ids = ["t1_hqn4y9b"]

comment = reddit.info(c_ids)
for c in comment:
    print (c)
    print (c.link_id)
    s_id = c.link_id[3:]
    print (s_id)
    parent_submission = reddit.submission(id = s_id)
    print (parent_submission)
    print (parent_submission.title)

    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    parent_comment = reddit.comment(id = c.parent_id)
    print (parent_comment.body)
    print ("ahohaisd")
    # print (parent_comment.replies)

    # comment_queue = parent_submission.comments[:]  # Seed with top-level
    # while comment_queue:
    #     comment = comment_queue.pop(0)
    #     print(comment.body)
    #     print ("......................")
    #     comment_queue.extend(comment.replies)

    parent_submission.comments.replace_more(limit=None)
    for comment in parent_submission.comments.list():
        print(comment.id, comment.body)
        print ("_________________________________")


