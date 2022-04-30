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
MODEL_NAME = "bert-base-multilingual-uncased"



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


subreddits = ["antifeminists", "AskReddit", "MensRights", "unpopularopinion", "ChangeMyView", "AmITheAsshole", "Conservative", "FemaleDatingStrategy", "PoliticalCompassMemes",
 "offmychest", "askscience", "AskHistorians", "explainlikeimfive", "politics", "PoliticalHumor", "conspiracy", "socialism", "Anarcho_Capitalism"
]

ar_subs = ["arabs", "saudiarabia", "egypt"]
ru_subs = ["russia", "russian", "AskARussian"]
fr_subs = ["French", "france"]

# subreddits = [ "AskReddit", "AskHistorians", "askscience", "explainlikeimfive"]

# subreddits = ["Conservative"]

# subreddits = ["antifeminists"]
def read_other_lang (sublist):
    X = []
    Y = []
    existing_X = []
    existing_Y = []
    print ("reading files")
    for subname in sublist:
        with open ("../scraping/data/reddit/removed_comments_other_langs/" + subname + ".tsv", "r", encoding = "utf-8") as rem_f:
            with open ("../scraping/data/reddit/existing_comments_other_langs/" + subname + ".tsv", "r", encoding = "utf-8") as existing_f:

                i = 0
                for line in rem_f:
                    if i == 0:
                        i += 1
                        continue
                    comment = line.split("\t")[1]
                    X.append(comment)
                    Y.append("removed")

                i = 0

                for line in existing_f:
                    i += 1
                    if i == 1:
                        continue
                    if (i == 5000):
                        break
                    comment = line.split("\t")[1]
                    existing_X.append(comment)
                    existing_Y.append("existing")

    existing_limit = 2*len(X)
    print ("limit:", existing_limit)
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

    return (X,Y)

def get_results (lang, model):
    if lang == "french":
        sublist = fr_subs
    elif lang == "arabic":
        sublist = ar_subs
    else:
        sublist = ru_subs

    print (lang, sublist)

    X_test, Y_test = read_other_lang(sublist)


    test_preds = predictor.predict(X_test)
    test_scores = predictor.predict_proba(X_test)

    # get results
    print ("test results", print_evaluation(Y_test, test_preds))
    print ("auc_under_roc:", roc_auc_score(Y_test, test_scores[:, 1]))

    # for i in range (10):
    #     print (Y_test[i], test_scores[i])
    # print (test_scores[:10])
    # print(predictor.classes_)


    with open ("predictions/preds-" + lang + ".tsv", "w", encoding = "utf-8") as f:
        f.write("text\ttruth\tpred\tscore\n")
        for i in range (X_test.shape[0]):
            f.write (X_test[i] + "\t" + Y_test[i] + "\t" + test_preds[i] + "\t" + str(test_scores[i]) + "\n")
    # print ("AUC under ROC:", roc_auc_score(y, test_scores[:, 1]))

    print (Counter(test_preds))
    print ("________________________________________________________________________________")
    return


X = []
Y = []
existing_limit = 2*15500
existing_X = []
existing_Y = []
print ("reading files")
for subname in subreddits:
    with open ("../scraping/data/reddit/removed_comments/" + subname + ".tsv", "r", encoding = "utf-8") as rem_f:
        with open ("../scraping/data/reddit/existing_comments/" + subname + ".tsv", "r", encoding = "utf-8") as existing_f:

            i = 0
            for line in rem_f:
                if i == 0:
                    i += 1
                    continue
                comment = line.split("\t")[1]
                X.append(comment)
                Y.append("removed")

            i = 0

            for line in existing_f:
                i += 1
                if i == 1:
                    continue
                if (i == 5000):
                    break
                comment = line.split("\t")[1]
                existing_X.append(comment)
                existing_Y.append("existing")


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
# for i in range (10):
#     print (X[i], Y[i])

# train-dev-test split
# X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=1)
X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.10, random_state=1) # 0.125 x 0.8 = 0.1

print (X_train.shape, X_val.shape)
cats = ["removed", "existing"]

t = text.Transformer(MODEL_NAME, maxlen=100, class_names=cats)
print ("MODEL", MODEL_NAME)

trn = t.preprocess_train(X_train, Y_train)

val = t.preprocess_test(X_val, Y_val)

model = t.get_classifier()
learner = ktrain.get_learner(model, train_data=trn, val_data=val, batch_size=16)
learner.fit_onecycle(8e-5, 3)
print ("getting predictor")
predictor = ktrain.get_predictor(learner.model, preproc=t)

X_test = X_val
Y_test = Y_val

test_preds = predictor.predict(X_test)
test_scores = predictor.predict_proba(X_test)

# get results
print ("test results", print_evaluation(Y_test, test_preds))
print ("auc_under_roc:", roc_auc_score(Y_test, test_scores[:, 1]))

langs = ["arabic", "french", "russian"]
for lang in langs:
    get_results(lang, predictor)


# test_preds = predictor.predict(X_test)
# test_scores = predictor.predict_proba(X_test)

# # get results
# print ("test results", print_evaluation(test_preds, Y_test))

# from sklearn.metrics import roc_auc_score
# for i in range (10):
#     print (Y_test[i], test_scores[i])
# # print (test_scores[:10])
# # print(predictor.classes_)


# with open ("predictions/preds-all-subreddits.tsv", "w", encoding = "utf-8") as f:
#     f.write("text\ttruth\tpred\tscore\n")
#     for i in range (X_test.shape[0]):
#         f.write (X_test[i] + "\t" + Y_test[i] + "\t" + test_preds[i] + "\t" + str(test_scores[i]) + "\n")
# # print ("AUC under ROC:", roc_auc_score(y, test_scores[:, 1]))

# print (Counter(test_preds))
