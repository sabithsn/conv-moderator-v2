import random

# gets the most similar sentence in the file
def readfile(filename):
	lines = []
	current = ""
	flag = True
	with open (filename, 'r', encoding = "utf-8") as f:
		for line in f:
			# skip the first line
			if flag:
				flag = False
				continue
			row = line.strip().split("\t")
			# if the original has changed:
			if row[0] != current:
				current = row[0]
				lines.append(line)
	return lines

def writefile(filename, lines):
	with open(filename, "w", encoding = "utf-8") as f:
		f.write("input_text\ttarget_text\tscore\n")
		for line in lines:
			f.write(line)

# subreddits = ["antifeminists", "AskReddit", "MensRights", "unpopularopinion", "ChangeMyView", "AmITheAsshole", "Conservative", "FemaleDatingStrategy", "PoliticalCompassMemes"]
subreddits = ["Conservative", "ChangeMyView"]

measure = "bert"
# measure = "MiniLM"

for sub in subreddits:
	deleted_lines = readfile("../scraping/data/reddit/similar-paired-deleted/" + sub + "_" + measure + ".tsv")
	removed_lines = readfile("../scraping/data/reddit/similar-paired-removed/" + sub + "_" + measure + ".tsv")

	random.shuffle(deleted_lines)
	random.shuffle(removed_lines)

	del_len = len(deleted_lines)
	rem_len = len(removed_lines)

	train_ratio = 0.8

	del_train_lim = int(del_len*train_ratio)
	rem_train_lim = int(rem_len*train_ratio)

	del_train, del_eval = deleted_lines[:del_train_lim], deleted_lines[del_train_lim:]
	rem_train, rem_eval = removed_lines[:rem_train_lim], removed_lines[rem_train_lim:]

	# writefile("../scraping/data/reddit/train/deleted/" + sub + "_" + measure + ".tsv", del_train)
	writefile("../scraping/data/reddit/train/removed/" + sub + "_" + measure + ".tsv", rem_train)
	# writefile("../scraping/data/reddit/eval/deleted/" + sub + "_" + measure + ".tsv", del_eval)
	writefile("../scraping/data/reddit/eval/removed/" + sub + "_" + measure + ".tsv", rem_eval)






