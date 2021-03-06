subreddit = "unpopularopinion"
subrules = [
"1. Your post must be an unpopular opinion Your post must be an opinion. Not a question. Not a showerthought. Not a rant. Not a proposal. Not a fact. An opinion. One opinion. A subjective statement about your position on some topic. Please have a clear, self contained opinion as your post title, and use the text field to elaborate and expand on why you think/feel this way. Your opinion must be unpopular. Unpopularity is a bit like an onion. It has layers. Be specific as to where you believe your opinion is unpopular.",
"2. Do not post low effort/satirical/troll posts. We get it, you all think this sub is garbage and is just for popular opinions, and you want to be funny and post 'going to be downvoted to oblivion here, but I think racism is bad.' We enjoy the memes, but please keep them off the sub. If your post is just one sentence it will be removed. Please try and elaborate on your opinion and justify your position. Any opinion that is not well thought out, incoherent, internally contradictory or otherwise nonsensical is subject to removal.' Included in this rule are vaccine related posts and new variants related posts.",
"3. Do not post opinions that are heavily posted/have been on the front page recently. Recent reposts and opinions that are constantly posted here are not allowed. No response posts about upvoted posts here. Posts relating to highly popular topics aren't allowed outside of the relevant megathreads. You can find a list of the topics and their respective megathreads in a post on the top of the sub. POSTS ABOUT POLITICS ARE NOT ALLOWED. POSTS DIRECTLY ABOUT THIS SUBREDDIT ARE NOT ALLOWED OUTSIDE THE MEGATHREAD",
"4. Be Civil This applies for both your behaviour on the sub, and the opinions which you post. Obey the sitewide rules and reddiquette. No racism, sexism, homophobia, transphobia, or general bigotry. Some opinions are so inappropriate/offensive that they'll be removed as hate posts. These posts are usually, but not exclusively, those that target a particular sex, race, sexual orientation, etc, when the user in question is hostile, vulgar or aggressive towards said group.",
"5. No Political Posts Our users have voted for no political posts in this sub, and this rule will not be changed until the majority votes otherwise. It's very unlikely your political post is an unpopular opinion. Feel free to use the Politics Megathread pinned to the front page.",
"6. No Covid posts or posts in relation Due the pandemic and its out pour of misinformation and pseudoscience. It has been decided that no covid posts may be posted. Included in this rule are vaccine related posts and new variants related posts."
]

subrulemap = {subreddit:subrules}

with open ("subrules.tsv", "w", encoding = "utf-8") as f:
	for sub in subrulemap:
		rules = ("@@@###@@@").join(subrulemap[sub]).replace("\n"," ").replace("\r", " ")
		f.write(sub + "\t" + rules + "\n")

