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
import statistics
from bert_score import BERTScorer
from nltk.translate.bleu_score import sentence_bleu


os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID";
os.environ["CUDA_VISIBLE_DEVICES"]="0";
MODEL_NAME = "bert-base-uncased"
class_names = ["anger", "anticipation", "disgust", "fear", "joy", "love", "optimism", "pessimism", "sadness", "surprise" , "trust"]

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

filename = "../data/predictions/dialogpt-style-preds.tsv"
# filename = "../data/predictions/predictions_BART.txt"

removed = []
annotated = []
predicted = []

with open (filename, "r", encoding = "utf-8") as f:
    flag = 0
    for line in f:
        if flag == 0:
            flag = 1
            continue
        row = line.strip().split("\t")
        removed.append(row[0])
        annotated.append(row[1])
        predicted.append(row[2])


off_predictor = ktrain.load_predictor('../../../pred-models/bert-off-olid')
emo_predictor = ktrain.load_predictor("../../../pred-models/emotion-bert")

print ("Predicting removed")
removed_off_preds = off_predictor.predict(removed)
removed_emo_preds = emo_predictor.predict(removed)

print ("Predicting annotated")
annotated_off_preds = off_predictor.predict(annotated)
annotated_emo_preds = emo_predictor.predict(annotated)

print ("Predicting predicted")
predicted_off_preds = off_predictor.predict(predicted)
predicted_emo_preds = emo_predictor.predict(predicted)



# OVERALL BERT SCORE
scorer = BERTScorer(lang = "en", rescale_with_baseline=True)
_, _, bert_predicted_removed = scorer.score(predicted, removed)
print ("predicted_removed_bert_score:", bert_predicted_removed.mean())
_, _, bert_predicted_annotated = scorer.score(predicted, annotated)
print ("predicted_annotated_bert_score:", bert_predicted_annotated.mean())


# OVERALL BLEU SCORE
bleus = []
for i in range (len(removed)):
    x = removed[i]
    y = predicted[i]
    reference = [x]
    candidate = y
    BLEU = sentence_bleu(reference, candidate)
    bleus.append(BLEU)
BLEU_predicted_removed = statistics.mean(bleus)
print ("predicted_removed_BLEU:", BLEU_predicted_removed)

bleus = []
for i in range (len(annotated)):
    x = annotated[i]
    y = predicted[i]
    reference = [x]
    candidate = y
    BLEU = sentence_bleu(reference, candidate)
    bleus.append(BLEU)
BLEU_predicted_annotated = statistics.mean(bleus)
print ("predicted_annotated_BLEU:", BLEU_predicted_annotated)

retained_dist = {}
removed_dist = {}
added_dist = {}

scorer = BERTScorer(lang = "en", rescale_with_baseline=True)
with open ("dialogpt-analysis-with-removed.tsv", "w", encoding = "utf-8") as f:
    f.write("predicted_removed_bert_score: " + str(round(bert_predicted_removed.mean().item()*100,2)) + "\n")
    f.write("predicted_removed_BLEU: " + str(round(BLEU_predicted_removed*100,2)) + "\n")
    f.write("removed\tpredicted\tbert-score\tBLEU-score\tremoved-offensive?\tpredicted-offensive?\tremoved-emotions\tpredicted-emotions\temotions-removed\temotions-retained\temotions-added\n")
    for i in range (len(removed)):
        rem = removed[i]
        pred = predicted[i]

        reference = [rem]
        candidate = [pred]
        _,_, bert = scorer.score(candidate, reference)
        bert = str(round(bert.mean().item()*100,2))

        reference = [rem]
        candidate = pred
        BLEU = str(round(sentence_bleu(reference, candidate)*100,2))

        rem_off_pred = removed_off_preds[i]
        pred_off_pred = predicted_off_preds[i]

        og_pred = get_emo(removed_emo_preds[i])
        pp_pred = get_emo(predicted_emo_preds[i])

        emo_removed = []
        emo_retained = []
        emo_added = []
        for x in og_pred:
            if x not in pp_pred:
                emo_removed.append(x)
                if x in removed_dist:
                    removed_dist[x] += 1
                else:
                    removed_dist[x] = 1
            else:
                emo_retained.append(x)
                if x in retained_dist:
                    retained_dist[x] += 1
                else:
                    retained_dist[x] = 1

        for x in pp_pred:
            if x not in og_pred:
                emo_added.append(x)
                if x in added_dist:
                    added_dist[x] += 1
                else:
                    added_dist[x] = 1
        row = [rem, pred, bert, BLEU, rem_off_pred, pred_off_pred, ",".join(og_pred), ",".join(pp_pred), ",".join(emo_removed), ",".join(emo_retained), ",".join(emo_added)]
        f.write("\t".join(row) + "\n")
    
    f.write ("REMOVED_EMO DISTRIBUTION\n")
    print ("Removed distribution:")
    for key in removed_dist:
        row = [key, str(removed_dist[key]), str(round( removed_dist[key]*100.0/sum(removed_dist.values()), 2))]
        print (row)
        f.write("\t".join(row) + "\n")

    f.write ("RETAINED_EMO DISTRIBUTION\n")
    print ("Retained distribution:")
    for key in retained_dist:
        row = [key, str(retained_dist[key]), str(round( retained_dist[key]*100.0/sum(retained_dist.values()), 2))]
        print (row)
        f.write("\t".join(row) + "\n")

    f.write ("ADDED_EMO DISTRIBUTION\n")
    print ("Added distribution:")
    for key in added_dist:
        row = [key, str(added_dist[key]), str(round( added_dist[key]*100.0/sum(added_dist.values()), 2))]
        print (row)
        f.write("\t".join(row) + "\n")

    f.write ("OFF_REMOVED_DISTRIBUTION\n")
    dist = Counter(removed_off_preds)
    for dist_key in dist:
        row = [dist_key, str(dist[dist_key]), str(round( dist[dist_key]*100.0/sum(dist.values()), 2))]
        f.write ("\t".join(row) + "\n")

    f.write ("OFF_PREDICTED_DISTRIBUTION\n")
    dist = Counter(predicted_off_preds)
    for dist_key in dist:
        row = [dist_key, str(dist[dist_key]), str(round( dist[dist_key]*100.0/sum(dist.values()), 2))]
        f.write ("\t".join(row) + "\n")


scorer = BERTScorer(lang = "en", rescale_with_baseline=True)
with open ("dialogpt-analysis-with-annotated.tsv", "w", encoding = "utf-8") as f:
    f.write("predicted_removed_bert_score: " + str(round(bert_predicted_annotated.mean().item()*100,2)) + "\n")
    f.write("predicted_removed_BLEU: " + str(round(BLEU_predicted_annotated*100,2)) + "\n")
    f.write("annotated\tpredicted\tbert-score\tBLEU-score\tannotated-offensive?\tpredicted-offensive?\tannotated-emotions\tpredicted-emotions\temotions-removed\temotions-retained\temotions-added\n")
    for i in range (len(annotated)):
        anno = annotated[i]
        pred = predicted[i]

        reference = [anno]
        candidate = [pred]
        _,_, bert = scorer.score(candidate, reference)
        bert = str(round(bert.mean().item()*100,2))

        reference = [anno]
        candidate = pred
        BLEU = str(sentence_bleu(reference, candidate)*100)

        anno_off_pred = annotated_off_preds[i]
        pred_off_pred = predicted_off_preds[i]

        og_pred = get_emo(annotated_emo_preds[i])
        pp_pred = get_emo(predicted_emo_preds[i])

        emo_removed = []
        emo_retained = []
        emo_added = []
        for x in og_pred:
            if x not in pp_pred:
                emo_removed.append(x)
                if x in removed_dist:
                    removed_dist[x] += 1
                else:
                    removed_dist[x] = 1
            else:
                emo_retained.append(x)
                if x in retained_dist:
                    retained_dist[x] += 1
                else:
                    retained_dist[x] = 1

        for x in pp_pred:
            if x not in og_pred:
                emo_added.append(x)
                if x in added_dist:
                    added_dist[x] += 1
                else:
                    added_dist[x] = 1
        row = [anno, pred, bert, BLEU, anno_off_pred, pred_off_pred, ",".join(og_pred), ",".join(pp_pred), ",".join(emo_removed), ",".join(emo_retained), ",".join(emo_added)]
        f.write("\t".join(row) + "\n")

    f.write ("REMOVED_EMO DISTRIBUTION\n")
    print ("Removed distribution:")
    for key in removed_dist:
        row = [key, str(removed_dist[key]), str(round( removed_dist[key]*100.0/sum(removed_dist.values()), 2))]
        print (row)
        f.write("\t".join(row) + "\n")

    f.write ("RETAINED_EMO DISTRIBUTION\n")
    print ("Retained distribution:")
    for key in retained_dist:
        row = [key, str(retained_dist[key]), str(round( retained_dist[key]*100.0/sum(retained_dist.values()), 2))]
        print (row)
        f.write("\t".join(row) + "\n")

    f.write ("ADDED_EMO DISTRIBUTION\n")
    print ("Added distribution:")
    for key in added_dist:
        row = [key, str(added_dist[key]), str(round( added_dist[key]*100.0/sum(added_dist.values()), 2))]
        print (row)
        f.write("\t".join(row) + "\n")


    f.write ("OFF_ANNOTATED_DISTRIBUTION\n")
    dist = Counter(annotated_off_preds)
    for dist_key in dist:
        row = [dist_key, str(dist[dist_key]), str(round( dist[dist_key]*100.0/sum(dist.values()), 2))]
        f.write ("\t".join(row) + "\n")

    f.write ("OFF_PREDICTED_DISTRIBUTION\n")
    dist = Counter(predicted_off_preds)
    for dist_key in dist:
        row = [dist_key, str(dist[dist_key]), str(round( dist[dist_key]*100.0/sum(dist.values()), 2))]
        f.write ("\t".join(row) + "\n")


