subreddits = ["antifeminists", "AskReddit", "MensRights", "unpopularopinion", "ChangeMyView", "AmITheAsshole", "Conservative", "FemaleDatingStrategy", "PoliticalCompassMemes"]
subreddits += ["offmychest", "askscience", "AskHistorians", "explainlikeimfive", "politics", "PoliticalHumor", "conspiracy", "socialism", "Anarcho_Capitalism"]


all_lines = []

for subname in subreddits:
	with open ("../scraping/data/reddit/removed_comments/" + subname + ".tsv", "r", encoding = "utf-8") as rem_f:
		c = 0
		for line in rem_f:
			if c == 0:
				c = 1
				continue

			row = line.strip().split("\t")
			all_lines.append (subname + "\t" + row[1] + "\n")

with open ("../scraping/data/all-removed-comments.tsv", "w", encoding = "utf-8") as f:
	for line in all_lines:
		f.write(line)



