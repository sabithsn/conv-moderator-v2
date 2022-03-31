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
MODEL_NAME = "bert-base-cased"



def print_evaluation(gold_labels, predicted_labels):

    '''Prints accuracy, precision, recall, f1 score'''

    accuracy = accuracy_score(gold_labels, predicted_labels) * 100
    f1 = f1_score(gold_labels, predicted_labels, average = "macro") * 100
    recall = recall_score(gold_labels, predicted_labels, average = "macro") * 100
    precision = precision_score(gold_labels, predicted_labels, average = "macro") * 100
  

    a = [("accuracy",accuracy), ("precision",precision), ("recall", recall), ("f1-macro", f1)]
    for i in range (4):
        a[i] = (a[i][0], round(a[i][1],2))
    print (a)
    s = [round(accuracy, 2), round(precision, 2), round(recall, 2), round(f1, 2)]
    return s


# subreddits = ["antifeminists", "AskReddit", "MensRights", "unpopularopinion", "ChangeMyView", "AmITheAsshole", "Conservative", "FemaleDatingStrategy", "PoliticalCompassMemes",
#  "offmychest", "askscience", "AskHistorians", "explainlikeimfive", "politics", "PoliticalHumor", "conspiracy", "socialism", "Anarcho_Capitalism"
# ]

# subreddits = ["AskHistorians", "askscience", "AskReddit"]
# subreddits = ["AskReddit"]
subreddits = ["politics","PoliticalHumor","Conservative"]

# subreddits = ["Conservative"]

# subreddits = ["antifeminists"]

X = []
Y = []
# existing_limit = 15500
existing_X = []
existing_Y = []
print ("reading files")
for subname in subreddits:
    with open ("../scraping/data/reddit/deleted_comments/" + subname + ".tsv", "r", encoding = "utf-8") as del_f:
        with open ("../scraping/data/reddit/removed_comments/" + subname + ".tsv", "r", encoding = "utf-8") as rem_f:
            with open ("../scraping/data/reddit/existing_comments/" + subname + ".tsv", "r", encoding = "utf-8") as existing_f:

                # i = 0
                # for line in del_f:
                #     if i == 0:
                #         i += 1
                #         continue
                #     comment = line.split("\t")[1]
                #     X.append(comment)
                #     Y.append("deleted")

                i = 0
                for line in rem_f:
                    if i == 0:
                        i += 1
                        continue
                    comment = line.split("\t")[1]
                    # if len (comment.split(" ")) > 30 or len(comment.split(" ")) < 3:
                    #     continue
                    X.append(comment)
                    Y.append("removed")
                    i += 1
                print ("removed ", subname, ": ", i)

                i = 0

                for line in existing_f:
                    if i == 0:
                        i += 1
                        continue
                    if (i == len(X)):
                        break
                    comment = line.split("\t")[1]
                    # if len (comment.split(" ")) > 30 or len(comment.split(" ")) < 3:
                    #     continue
                    existing_X.append(comment)
                    existing_Y.append("existing")
                    i += 1


existing_limit = len(X)
# choose subset of existing and add to data
inds = [x for x in range (len(existing_X))]
random.shuffle(inds)
inds = inds[:existing_limit]

existing_X = list(np.array(existing_X)[inds])
existing_Y = list(np.array(existing_Y)[inds])

X = X + existing_X
Y = Y + existing_Y

# shuffle 
X = np.array(X)
Y = np.array(Y)
inds = [x for x in range (len(X))]
random.shuffle(inds)
X, Y = X[inds], Y[inds]

print ("DISTRIBUTION:")
print (Counter(Y))
print ("______________________________")

# check
for i in range (10):
    print (X[i], Y[i])

# train-dev-test split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=1)
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.125, random_state=1) # 0.125 x 0.8 = 0.1

print (X_train.shape, X_val.shape, X_test.shape)
cats = ["removed", "existing"]

t = text.Transformer(MODEL_NAME, maxlen=30, class_names=cats)
print ("MODEL", MODEL_NAME)

trn = t.preprocess_train(X_train, Y_train)

val = t.preprocess_test(X_val, Y_val)

model = t.get_classifier()
learner = ktrain.get_learner(model, train_data=trn, val_data=val, batch_size=16)
learner.fit_onecycle(8e-5, 3)
print ("getting predictor")
predictor = ktrain.get_predictor(learner.model, preproc=t)
test_preds = predictor.predict(X_test)
test_scores = predictor.predict_proba(X_test)

# get results
print ("test results", print_evaluation(Y_test, test_preds))
print ("auc_under_roc:", round(roc_auc_score(Y_test, test_scores[:, 1])*100, 2))

# for i in range (10):
#     print (Y_test[i], test_scores[i])
# print (test_scores[:10])
# print(predictor.classes_)


with open ("predictions/preds-conservative.tsv", "w", encoding = "utf-8") as f:
    f.write("text\ttruth\tpred\tscore\n")
    for i in range (X_test.shape[0]):
        f.write (X_test[i] + "\t" + Y_test[i] + "\t" + test_preds[i] + "\t" + str(test_scores[i]) + "\n")
# print ("AUC under ROC:", roc_auc_score(y, test_scores[:, 1]))

print (Counter(test_preds))









