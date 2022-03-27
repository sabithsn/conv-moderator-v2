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


X_train = []
Y_train = []
with open ("olid-training-v1.0.tsv", "r", encoding = "utf-8") as f:
	c = 1
	for line in f:
		if c == 1:
			c = 0
			continue

		row = line.strip().split("\t")
		X_train.append(row[1])
		Y_train.append(row[2])

test_dict = {}
with open ("testset-levela.tsv", "r", encoding = "utf-8") as f:
	c = 1
	for line in f:
		if c == 1:
			c = 0
			continue

		row = line.strip().split("\t")
		test_dict[row[0]] = [row[1]]

with open ("labels-levela.csv", "r", encoding = "utf-8") as f:
	for line in f:
		row = line.strip().split(",")
		test_dict[row[0]].append(row[1])

X_test, Y_test = [],[]

for key in test_dict:
	try:
		X_test.append(test_dict[key][0])
		Y_test.append(test_dict[key][1])
	except:
		print (key, test_dict[key])

print (len(X_train), len(Y_train))
print (len(X_test), len(Y_test))

# for i in range (10):
# 	print (X_test[i], Y_test[i])


X_val = X_test
Y_val = Y_test

# print (X_train.shape, X_val.shape, X_test.shape)
cats = ["OFF", "NOT"]

t = text.Transformer(MODEL_NAME, maxlen=100, class_names=cats)
print ("MODEL", MODEL_NAME)

trn = t.preprocess_train(X_train, Y_train)

val = t.preprocess_test(X_val, Y_val)

model = t.get_classifier()
learner = ktrain.get_learner(model, train_data=trn, val_data=val, batch_size=8)
learner.fit_onecycle(8e-5, 3)
print ("getting predictor")
predictor = ktrain.get_predictor(learner.model, preproc=t)
test_preds = predictor.predict(X_test)
test_scores = predictor.predict_proba(X_test)

# get results
print ("test results", print_evaluation(Y_test, test_preds))
print ("auc_under_roc:", roc_auc_score(Y_test, test_scores[:, 1]))

predictor.save("../../off-models/bert-off-olid")