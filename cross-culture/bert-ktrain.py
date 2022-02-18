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

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID";
os.environ["CUDA_VISIBLE_DEVICES"]="0";
MODEL_NAME = "bert-base-multilingual-cased"



def print_evaluation(gold_labels, predicted_labels):

    '''Prints accuracy, precision, recall, f1 score'''

    accuracy = accuracy_score(gold_labels, predicted_labels) * 100
    f1 = f1_score(gold_labels, predicted_labels, average = "macro") * 100
    recall = recall_score(gold_labels, predicted_labels, average = "macro") * 100
    precision = precision_score(gold_labels, predicted_labels, average = "macro") * 100
  

    a = [accuracy, precision, recall, f1]
    for i in range (4):
        a[i] = round(a[i],2)

    return a

def readfile(filename):
    texts = []
    targets = []
    groups = []
    flag = 1
    n_count = 0
    n_max = 2000
    with open (filename, "r", encoding = "utf-8") as f:
        for line in f:
            if flag:
                flag = 0
                continue
            row = line.strip().split("\t")
            if len(row) < 7:
                continue
            if row[0] == "NULL":
                n_count += 1
                if n_count > n_max:
                    continue

            texts.append(row[1])
            targets.append(row[5])
            groups.append(row[6])

    return (texts, targets, groups)


train_texts, train_targets, train_groups = readfile("data/training_data.tsv")
test_texts, test_targets, test_groups = readfile("data/test_data.tsv")

print ("__________________")
print (Counter(train_targets))
print (Counter(test_targets))
print ("__________________")
print (Counter(train_groups))
print (Counter(test_groups))
print ("__________________")

target_cats = list(set(train_targets))
group_cats = list(set(train_groups))

task = "target"
# task = "group"

X_train = train_texts
X_test = test_texts

if task == "target":
    Y_train = train_targets
    Y_test = test_targets
    t = text.Transformer(MODEL_NAME, maxlen=50, class_names=target_cats)
else:
    Y_train = train_groups
    Y_test = test_groups
    t = text.Transformer(MODEL_NAME, maxlen=50, class_names=group_cats)



print ("MODEL", MODEL_NAME)

trn = t.preprocess_train(X_train, Y_train)

val = t.preprocess_test(X_test, Y_test)

model = t.get_classifier()
learner = ktrain.get_learner(model, train_data=trn, val_data=val, batch_size=16)
learner.fit_onecycle(8e-5, 3)
print ("getting predictor")
predictor = ktrain.get_predictor(learner.model, preproc=t)
predictor.save("../../cross-models/"+task+"_mbert2")

test_preds = predictor.predict(X_test)

# get results
print (task + " test results", print_evaluation(test_preds, Y_test))

print (Counter(test_preds))









