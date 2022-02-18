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

subreddit = "unpopularopinion"
subrule = [
"1. Your post must be an unpopular opinion Your post must be an opinion. Not a question. Not a showerthought. Not a rant. Not a proposal. Not a fact. An opinion. One opinion. A subjective statement about your position on some topic. Please have a clear, self contained opinion as your post title, and use the text field to elaborate and expand on why you think/feel this way. Your opinion must be unpopular. Unpopularity is a bit like an onion. It has layers. Be specific as to where you believe your opinion is unpopular.",
"2. Do not post low effort/satirical/troll posts. We get it, you all think this sub is garbage and is just for popular opinions, and you want to be funny and post 'going to be downvoted to oblivion here, but I think racism is bad.' We enjoy the memes, but please keep them off the sub. If your post is just one sentence it will be removed. Please try and elaborate on your opinion and justify your position. Any opinion that is not well thought out, incoherent, internally contradictory or otherwise nonsensical is subject to removal.' Included in this rule are vaccine related posts and new variants related posts.",
"3. Do not post opinions that are heavily posted/have been on the front page recently. Recent reposts and opinions that are constantly posted here are not allowed. No response posts about upvoted posts here. Posts relating to highly popular topics aren't allowed outside of the relevant megathreads. You can find a list of the topics and their respective megathreads in a post on the top of the sub. POSTS ABOUT POLITICS ARE NOT ALLOWED. POSTS DIRECTLY ABOUT THIS SUBREDDIT ARE NOT ALLOWED OUTSIDE THE MEGATHREAD",
"4. Be Civil This applies for both your behaviour on the sub, and the opinions which you post. Obey the sitewide rules and reddiquette. No racism, sexism, homophobia, transphobia, or general bigotry. Some opinions are so inappropriate/offensive that they'll be removed as hate posts. These posts are usually, but not exclusively, those that target a particular sex, race, sexual orientation, etc, when the user in question is hostile, vulgar or aggressive towards said group.",
"5. No Political Posts Our users have voted for no political posts in this sub, and this rule will not be changed until the majority votes otherwise. It's very unlikely your political post is an unpopular opinion. Feel free to use the Politics Megathread pinned to the front page.",
"6. No Covid posts or posts in relation Due the pandemic and its out pour of misinformation and pseudoscience. It has been decided that no covid posts may be posted. Included in this rule are vaccine related posts and new variants related posts."
]

subrule = "@@@###@@@".join(subrule)


removed_file = "removed_comments/" + subreddit + ".tsv"
similar_file = "similar-paired-removed/" + subreddit + ".tsv"

pps = {}
with open (similar_file, "r", encoding = "utf-8") as f:
    flag = 1
    for line in f:
        if flag:
            flag = 0
            continue
        row = line.strip().split("\t")
        body = row[0]
        pp = row[1]
        if body in pps:
            pps[body] += [pp]
        else:
            pps[body] = [pp]

authors = []
u_ids = []
texts = []
subreddits = []
submission_texts = []
parent_texts = []
subrules = []
p1s = []
p2s = []
p3s = []
p4s = []
p5s = []
permalinks = []


with open (removed_file, "r", encoding = "utf-8") as f:
    flag = 0
    for line in f:
        flag += 1
        if flag == 1:
            continue
        row = line.strip().split("\t")
        author = row[0]
        authors.append(author)

        body = row[1]
        texts.append(body)
        subreddits.append(subreddit)
        subrules.append(subrule)

        if body not in pps:
            print ("not found", flag)
            continue

        candidates = pps[body]
        if len(candidates) != 5:
            print ("not enough cands", flag)
            print (body)
            print (candidates)
            continue

        p1s.append(candidates[0])
        p2s.append(candidates[1])
        p3s.append(candidates[2])
        p4s.append(candidates[3])
        p5s.append(candidates[4])


        created_at = row[2]
        c_id = "t1_" + row[3]
        s_id = row[4]
        p_id = row[5]
        permalink = row[6]
        permalinks.append(permalink)

        u_id = subreddit + "_" + c_id
        u_ids.append(u_id)

        c_ids = [c_id]

        parent_text = "text_not_found"
        submission_text = "text_not_found"

        comment = reddit.info(c_ids)
        for c in comment:
            s_id = c.link_id[3:]
            try:
                parent_submission = reddit.submission(id = s_id)
                submission_text = parent_submission.selftext.replace("\n", " ").replace("\r"," ")

                print (flag)

                parent_comment = reddit.comment(id = c.parent_id)
                parent_text = parent_comment.body.replace("\n", " ").replace("\r"," ")
            except:
                continue

        submission_texts.append(submission_text)
        parent_texts.append(parent_text)

with open ("annotation_files/" + subreddit + ".tsv", "w", encoding = "utf-8") as f:
    for i in range (len(parent_texts)):
        row = [authors[i], u_ids[i], subreddits[i], subrules[i], texts[i], submission_texts[i], parent_texts[i], p1s[i], p2s[i], p3s[i], p4s[i], p5s[i], permalinks[i]]
        line = "\t".join(row) + "\n"
        f.write(line)
