import sys
import timeit
import scipy
from sentence_transformers import SentenceTransformer
import tensorflow as tf
import pandas as pd
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))


# model = SentenceTransformer('all-mpnet-L6-v2')
# model = SentenceTransformer('all-MiniLM-L6-v2')

model = SentenceTransformer('all-mpnet-base-v2')


def read_dump(filename):
    data = pd.read_csv(filename, sep="\t")
    data = data["body"].values.tolist()
    return data


data = read_dump("../../reddit-dump/cleaned-and-filtered/AmITheAsshole.tsv")
print (data[:10])


''' just reads a file '''
def readfile(filename):
    texts = []
    with open (filename, "r", encoding = "utf-8") as f:
        for line in f:
            row = line.strip().split("\t")
            texts.append(row[1])

    return texts [1:]


def get_most_similar(filename, removed_texts, existing_texts, query_embeddings, corpus_embeddings, closest_n, subname):
    print ("WRITING TO: ", filename)
    with open (filename, "w", encoding = "utf-8") as f:
        f.write("original\tcandidate\tscore\n")
        k = 0
        for r, query_embedding in zip(removed_texts, query_embeddings):
            k += 1
            print (k)
            distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]

            results = zip(range(len(distances)), distances)
            results = sorted(results, key=lambda x: x[1])

            print("\n\n======================\n\n")
            print("Query:", r)
            print("\nTop 5 most similar sentences in corpus:")

            for idx, distance in results[0:closest_n]:
                print(existing_texts[idx].strip(), "(Score: %.4f)" % (1-distance))
                # try:
                f.write(r.replace("\t"," ").replace("\n", " ").replace("\r", " ") + "\t" + existing_texts[idx].replace("\t"," ").replace("\n", " ").replace("\r", " ") + "\t" + str(round((1-distance),3)) + "\t" + subname + "\n")


current_sub = ""

sublist = ["AmITheAsshole", "AskScience", "Conspiracy", "ExplainLikeImFive", "OffMyChest", "PoliticalHumor", "UnpopularOpinion"]

top_n = 1
with open ("../scraping/data/filtered-removed-comments.tsv", "r", encoding = "utf-8") as g:
    cur_removed = []
    cur_existing = []
    flag = True
    for line in g:
        row = line.strip().split("\t")
        sub = row[1]
        text = row[0]
        if sub not in sublist:
            continue

        if sub != current_sub:
            if flag:
                flag = False
                current_sub = sub
                cur_removed.append(text)
                continue
            else:
                print ("DOING SUB:", current_sub)
                cur_existing = read_dump("../../reddit-dump/cleaned-and-filtered/" + current_sub + ".tsv")
                existing_embeddings = model.encode(cur_existing)
                removed_embeddings = model.encode(cur_removed)
                get_most_similar("../scraping/data/style-candidates/mpnet_" + current_sub + ".tsv", cur_removed, cur_existing, removed_embeddings, existing_embeddings, top_n, current_sub)
                cur_removed = []
                cur_removed.append(text)
                current_sub = sub
        else:
            cur_removed.append(text)

    print ("DOING SUB:", current_sub)
    cur_existing = read_dump("../../reddit-dump/cleaned-and-filtered/" + current_sub + ".tsv")
    existing_embeddings = model.encode(cur_existing)
    removed_embeddings = model.encode(cur_removed)
    get_most_similar("../scraping/data/style-candidates/mpnet_" + current_sub + ".tsv", cur_removed, cur_existing, removed_embeddings, existing_embeddings, top_n, current_sub)
