import numpy as np 
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from collections import Counter
import random
from sklearn.model_selection import train_test_split
import ktrain
from ktrain import text
import os
from collections import Counter


def readfile(filename):
	texts = []
	with open (filename, "r", encoding = "utf-8") as f:
		flag = 1
		for line in f:
			if flag:
				flag = 0
				continue

			row = line.strip().split("\t")
			texts.append(row[1])

	return texts

def writefile(filename, texts, predictions):
	with open (filename, "w", encoding = "utf-8") as f:
		for i in range (len(texts)):
			line = texts[i] + "\t" + predictions[i] + "\n"
			f.write(line)
	return

task = "target"
# task = "group"

predictor = ktrain.load_predictor("../../cross-models/"+task+"_mbert2")


# en_sub_existing = readfile("../scraping/data/reddit/existing_comments/AskReddit.tsv")
# en_sub_existing = random.sample(en_sub_existing, 10000)
# en_sub_removed = readfile("../scraping/data/reddit/removed_comments/AskReddit.tsv")

# en_sub_existing_preds = predictor.predict(en_sub_existing)
# writefile("predictions2/"+task+"AskReddit-existing.tsv", en_sub_existing, en_sub_existing_preds)

# en_sub_removed_preds = predictor.predict(en_sub_removed)
# writefile("predictions2/"+task+"AskReddit-removed.tsv", en_sub_removed, en_sub_removed_preds)

# print ("DONE ENGLISH")

ar_sub_existing = readfile("../scraping/data/reddit/existing_comments_other_langs/saudiarabia.tsv")
ar_sub_removed = readfile("../scraping/data/reddit/removed_comments_other_langs/saudiarabia.tsv")

ar_sub_existing_preds = predictor.predict(ar_sub_existing)
writefile("predictions2/"+task+"-saudiarabia-existing.tsv", ar_sub_existing, ar_sub_existing_preds)

ar_sub_removed_preds = predictor.predict(ar_sub_removed)
writefile("predictions2/"+task+"-saudiarabia-removed.tsv", ar_sub_removed, ar_sub_removed_preds)

