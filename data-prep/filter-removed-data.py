from nltk import word_tokenize
import ktrain
from ktrain import text
from collections import Counter

def contains_30_or_fewer_tokens(text):
    tokens = word_tokenize(text)
    if len(tokens) < 30:
        return True
    else:
        return False

def contains_3_or_more_tokens(text):
    tokens = word_tokenize(text)
    if len(tokens) > 2:
        return True
    else:
        return False

texts = []
subs = []
with open ("../scraping/data/all-removed-comments.tsv", "r", encoding = "utf-8") as f:
	for line in f:
		row = line.strip().split("\t")
		texts.append(row[1])
		subs.append(row[0])

predictor = ktrain.load_predictor("../../off-models/bert-off-olid")
text_preds = predictor.predict(texts)

print (Counter(text_preds))

filtered = []

for i in range (len(texts)):
	
	text = texts[i]
	sub = subs[i]
	label = text_preds[i]

	# print (text, sub, label)
	if (contains_3_or_more_tokens(text) and contains_30_or_fewer_tokens(text) and label == "OFF"):
		filtered.append(text + "\t" + sub + "\t" + label + "\n")

print (len(filtered))
with open ("../scraping/data/filtered-removed-comments.tsv", "w", encoding = "utf-8") as f:
	for line in filtered:
		f.write(line)