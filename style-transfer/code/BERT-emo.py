import os
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score, jaccard_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import pickle
import scipy
import unicodecsv as csv
import ktrain
from ktrain import text
import pandas as pd

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID";
os.environ["CUDA_VISIBLE_DEVICES"]="0"; 
class_names = ["anger", "anticipation", "disgust", "fear", "joy", "love", "optimism", "pessimism", "sadness", "surprise" , "trust"]

# def evaluate(labels, predictions):
#   scores = {}
#   scores['jaccard'] = jaccard_score(labels, predictions, average="samples")
#   scores['f1'] = f1_score(labels, predictions, average="macro")
#   all_accs = []
#   for i in range(labels.shape[-1]):
#     scores[f'accuracy-{i}'] = accuracy_score(labels[:, i], predictions[:, i])
#     all_accs.append(scores[f'accuracy-{i}'])
#   scores['accuracy'] = np.mean(np.array(all_accs))
#   return scores

# def filter_data(X_train, y_train, filt):
#     length = y_train.shape[0]
#     filtered_X_train = []
#     filtered_y_train = []
#     for i in range (length):
#         if sum(y_train[i]) >= filt:
#             filtered_X_train.append(X_train[i])
#             filtered_y_train.append(y_train[i])
#     print ("filter length:", filt)
#     print ("resultant length:", len(filtered_y_train))

#     return (np.array(filtered_X_train), np.array(filtered_y_train))  

# def map_labels (arr):
#     print ("mapping labels")
#     mapped_labels = []
#     length = arr.shape[0]
#     for i in range (length):
#         row = arr[i]
#         mapped_row = []
#         for j in range (11):
#             if row[j] >= 0.5:
#                 label = 1
#             else:
#                 label = 0
#             mapped_row.append(label)
#         mapped_labels.append(mapped_row)
#     return np.array(mapped_labels)


# def readfile(filename):
#     with open (filename, "rb") as f:
#         count = 0
#         inp = []
#         labels = []
#         for line in f:
#             if count == 0:
#                 count += 1
#                 continue
#             row = line.decode("utf-8").strip().split("\t")
#             inp.append(row[1])
#             label_row = row[2:]
#             for i in range (len(label_row)):
#                 label_row[i] = int (label_row[i])
#             labels.append(label_row)
#     return (np.array(inp), np.array(labels))



# train_X, train_y = readfile ("../data/emotion-data/train.txt")
# dev_X, dev_y = readfile ("../data/emotion-data/dev.txt")
# test_X, test_y = readfile ("../data/emotion-data/test-gold.txt")

# MODEL_NAME = "bert-base-uncased"
# print ("MODEL:")
# print (MODEL_NAME)
# t = text.Transformer(MODEL_NAME, maxlen=30, class_names = class_names)
# trn = t.preprocess_train(train_X, train_y)
# val = t.preprocess_test(dev_X, dev_y)

# model = t.get_classifier()
# learner = ktrain.get_learner(model, train_data=trn, val_data=val, batch_size=8)
# learner.fit_onecycle(8e-5, 3)


# print ("getting predictor")
# clf = ktrain.get_predictor(learner.model, preproc=t)
# print ("predictor obtained")
# clf.save("../../../pred-models/emotion-bert")

# predicted_labels = clf.predict(test_X)
# hot_preds = []
# for i in range (len(predicted_labels)):
#   if len(predicted_labels[i]) != 11:
#       print ("Shouldn't happen 1")
#       exit()
#   row = []
#   for j in range (11):
#       if predicted_labels[i][j][0] != class_names[j]:
#           print (predicted_labels[i])
#           print (class_names)
#           print ("Shouldnt happen 2")
#           exit()
#       if predicted_labels[i][j][1] >= 0.5:
#           row.append(1)
#       else:
#           row.append(0)
#   hot_preds.append(row)

# hot_preds = np.array(hot_preds)

# res = evaluate(test_y, hot_preds)

# jaccard = str(round(res["jaccard"],4))
# f1 = str(round(res["f1"],4))
# print (jaccard, f1)

# ----------------------------------------------------------------------------- #

clf = ktrain.load_predictor("../../../pred-models/emotion-bert")

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
    predicted_labels = clf.predict(annotations[key])
    dist = {}
    for i in range (len(predicted_labels)):
        if len(predicted_labels[i]) != 11:
            print ("Shouldn't happen 3")
            exit()
        row = []
        for j in range (11):
            if predicted_labels[i][j][0] != class_names[j]:
                print (predicted_labels[i])
                print (class_names)
                print ("Shouldnt happen 4")
                exit()
            if predicted_labels[i][j][1] >= 0.5:
                row.append(predicted_labels[i][j][0])
                if predicted_labels[i][j][0] in dist:
                    dist[predicted_labels[i][j][0]] += 1
                else:
                    dist[predicted_labels[i][j][0]] = 1
    print ("distribution of annotator: ", key)

    for dist_key in dist:
        print (dist_key, dist[dist_key], round( dist[dist_key]*100.0/sum(dist.values()), 2)) 

def get_emo (preds):
    row = []
    for j in range (11):
        if preds[j][0] != class_names[j]:
            print (preds[i])
            print (class_names)
            print ("Shouldnt happen 4")
            exit()
        if preds[j][1] >= 0.5:
            row.append(preds[j][0])

    return row

lines = []
paraphrases = []
originals = []
with open ("../data/style-transfer-annotation.tsv", "r", encoding = "utf-8") as f:
    for line in f:
        lines.append(line.strip())
        row = line.strip().split("\t")
        paraphrases.append(row[7])
        originals.append(row[0])

pp_preds = clf.predict(paraphrases)
og_preds = clf.predict(originals)

retained_dist = {}
removed_dist = {}
added_dist = {}

with open ("../data/style-transfer-annotation+emotion_preds.tsv", "w", encoding = "utf-8") as f:
    for i in range (len(lines)):
        line = lines[i]
        if i == 0:
            f.write(line + "\tog_emotions\tpp_emotions\temotions_removed\temotions_retained\temotions_added\n")
            continue

        row = line.split("\t")
        custom = row[7]
        if len(custom) == 0:
            f.write(line + "\t??????\t??????\t??????\t??????\t??????\n")
            continue

        pp_pred = get_emo(pp_preds[i])
        og_pred = get_emo(og_preds[i])

        removed = []
        retained = []
        added = []
        for x in og_pred:
            if x not in pp_pred:
                removed.append(x)
                if x in removed_dist:
                    removed_dist[x] += 1
                else:
                    removed_dist[x] = 1
            else:
                retained.append(x)
                if x in retained_dist:
                    retained_dist[x] += 1
                else:
                    retained_dist[x] = 1

        for x in pp_pred:
            if x not in og_pred:
                added.append(x)
                if x in added_dist:
                    added_dist[x] += 1
                else:
                    added_dist[x] = 1

        # print (og_pred)
        # print (pp_pred)
        # print (removed)
        # print (retained)
        # print (added)
        new_fields = [",".join(og_pred), ",".join(pp_pred), ",".join(removed), ",".join(retained), ",".join(added)]
        f.write(line + "\t" + "\t".join(new_fields) + "\n")
print ("___________________________________________________________________________________-")
print ("Removed distribution:")
for key in removed_dist:
    print (key, removed_dist[key], round( removed_dist[key]*100.0/sum(removed_dist.values()), 2))

print ("Retained distribution:")
for key in retained_dist:
    print (key, retained_dist[key], round( retained_dist[key]*100.0/sum(retained_dist.values()), 2))

print ("Added distribution:")
for key in added_dist:
    print (key, added_dist[key], round( added_dist[key]*100.0/sum(added_dist.values()), 2))
