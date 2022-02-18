import numpy as np 
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from collections import Counter
import random
from sklearn.model_selection import train_test_split

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


# subreddits = ["antifeminists", "AskReddit", "MensRights", "unpopularopinion", "ChangeMyView", "AmITheAsshole", "Conservative", "FemaleDatingStrategy", "PoliticalCompassMemes",
#  "offmychest", "askscience", "AskHistorians", "explainlikeimfive", "politics", "PoliticalHumor", "conspiracy", "socialism", "Anarcho_Capitalism"
# ]
subreddits = ["AmITheAsshole"]
# subreddits = [ "Conservative", "politics"]


X = []
Y = []
existing_limit = 2000
existing_X = []
existing_Y = []
print ("reading files")
for subname in subreddits:
    with open ("../scraping/data/reddit-posts/deleted_posts/" + subname + ".tsv", "r", encoding = "utf-8") as del_f:
        with open ("../scraping/data/reddit-posts/removed_posts/" + subname + ".tsv", "r", encoding = "utf-8") as rem_f:
            with open ("../scraping/data/reddit-posts/existing_posts/" + subname + ".tsv", "r", encoding = "utf-8") as existing_f:

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
                    X.append(comment)
                    Y.append("removed")

                i = 0

                for line in existing_f:
                    if i == 0:
                        i += 1
                        continue
                    comment = line.split("\t")[1]
                    existing_X.append(comment)
                    existing_Y.append("existing")


# choose subset of existing and add to data
c = list(zip(existing_X, existing_Y))

random.shuffle(c)

existing_X, existing_Y = zip(*c)
existing_X, existing_Y = list(existing_X)[:existing_limit], list(existing_Y)[:existing_limit]
# print (existing_X[:10], existing_Y[:10])

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


# choose word/char as mode and its range.
mode = "word"
ngram_range = (1,2)

# train vectorizer, transform using vectorizer 
train_vectorizer = TfidfVectorizer(ngram_range=ngram_range, analyzer = mode)
X_train = train_vectorizer.fit_transform(X_train)
X_val = train_vectorizer.transform(X_val)
X_test = train_vectorizer.transform(X_test)
print (X_train.shape, X_val.shape, X_test.shape)

# train svm
clf = LinearSVC()
clf.fit(X_train, Y_train)

val_preds = clf.predict(X_val)
test_preds = clf.predict(X_test)

# get results
print ("dev results", print_evaluation(val_preds, Y_val))
print ("test results", print_evaluation(test_preds, Y_test))

print (Counter(test_preds))




