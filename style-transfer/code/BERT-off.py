import numpy as np 
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from sklearn.metrics import roc_auc_score

from collections import Counter
import random
from sklearn.model_selection import train_test_split
import ktrain
from ktrain import text
import os
import pandas as pd 

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID";
os.environ["CUDA_VISIBLE_DEVICES"]="0";
MODEL_NAME = "bert-base-uncased"



def print_evaluation(gold_labels, predicted_labels):

    '''Prints accuracy, precision, recall, f1 score'''

    accuracy = accuracy_score(gold_labels, predicted_labels) * 100
    f1 = f1_score(gold_labels, predicted_labels, average = "macro") * 100
    recall = recall_score(gold_labels, predicted_labels, average = "macro") * 100
    precision = precision_score(gold_labels, predicted_labels, average = "macro") * 100
  

    a = [("accuracy",accuracy), ("precision",precision), ("recall", recall), ("f1-macro", f1)]
    for i in range (4):
        a[i] = (a[i][0], round(a[i][1],2))
    return a


predictor = ktrain.load_predictor('../../../off-models/bert-off-olid')
print ("predictor loaded")

df = pd.read_csv("../data/style-transfer-annotation.tsv", sep = "\t")
df = df[["Removed Comment", "Custom", "Annotator"]]
df = df.dropna()
df_list = df.values.tolist()
print (len(df_list))
for i in range (10):
	print (df_list[i])

annotations = {"Pantho": [], "Kate": [], "Ilana": [], "Original": []}
for i in range (len(df_list)):
	row = df_list[i]
	annotations["Original"].append(row[0])
	annotations[row[2]].append(row[1])

for key in annotations:
	preds = predictor.predict(annotations[key])
	print ("Annotator ", key, " Distribution:")
	dist = Counter(preds)
	print (dist)
	for dist_key in dist:
		print (dist_key, dist[dist_key], round( dist[dist_key]*100.0/sum(dist.values()), 2)) 


lines = []
paraphrases = []
with open ("../data/style-transfer-annotation.tsv", "r", encoding = "utf-8") as f:
	for line in f:
		lines.append(line.strip())
		row = line.strip().split("\t")
		custom = row[7]
		paraphrases.append(custom)

preds = predictor.predict(paraphrases)

with open ("../data/style-transfer-annotation+off_preds.tsv", "w", encoding = "utf-8") as f:
	print (len(lines), len(preds))
	for i in range (len(lines)):
		line = lines[i]
		row = line.split("\t")
		custom = row[7]
		pred = preds[i]

		if len(custom) == 0:
			f.write(line + "\tNOT_DONE_YET\n")
		else:
			f.write(line + "\t" + pred + "\n")


