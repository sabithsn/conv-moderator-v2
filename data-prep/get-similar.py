import sys
import timeit
import scipy
from sentence_transformers import SentenceTransformer
import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

measure = "bert"
# measure = "MiniLM"

if measure == "bert":
    model = SentenceTransformer('bert-base-nli-mean-tokens')
else:
    model = SentenceTransformer('all-MiniLM-L6-v2')

def read_dump(filename):
    texts = []
    with open (filename, "r", encoding = "utf-8") as f:
        for line in f:
            row = line.strip().split("\t")
            if len(row) == 1 or len(row) == 10:
                texts.append(row[0])
    return texts [1:]

''' just reads a file '''
def readfile(filename):
    texts = []
    with open (filename, "r", encoding = "utf-8") as f:
        for line in f:
            row = line.strip().split("\t")
            texts.append(row[1])

    return texts [1:]


''' for each embedding in queries, gets the top n most similar embeddings in the corpus'''
def get_most_similar(filename, query_embeddings, corpus_embeddings, closest_n):
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
                try:
                    f.write(r + "\t" + existing_texts[idx].strip() + "\t" + str(round((1-distance),3)) + "\n")
                except:
                    continue


if __name__ == '__main__':

    start = timeit.default_timer()
    # subreddits = ["antifeminists", "AskReddit", "MensRights", "unpopularopinion", "ChangeMyView", "AmITheAsshole", "Conservative", "FemaleDatingStrategy", "PoliticalCompassMemes"]
    subreddits = [ "ChangeMyView"]
    print ("measure:", measure)
    # generate top n similar sentences for each subreddit 
    for subname in subreddits:

        print ("doing SUB:", subname)

        removed = "../scraping/data/reddit/removed_comments/" + subname + ".tsv"
        deleted = "../scraping/data/reddit/deleted_comments/" + subname + ".tsv"
        existing = "../../reddit-dump/" + subname + ".tsv"
        paired_deleted = "../scraping/data/reddit/similar-paired-deleted/" + subname + "_" + measure + ".tsv"
        paired_removed = "../scraping/data/reddit/similar-paired-removed/" + subname + "_" + measure + ".tsv"

        top_n = 1

        removed_texts = readfile(removed)
        deleted_texts = readfile(deleted)
        existing_texts = read_dump(existing)

        print (subname, " dump size ", len(existing_texts))

        print ("loading existing embeddings")
        existing_embeddings = model.encode(existing_texts)
        print ("corpus embeddings loaded")

        print ("loading removed embeddings")
        removed_embeddings = model.encode(removed_texts)
        print ("removed embeddings loaded")

        # print ("loading deleted embeddings")
        # deleted_embeddings = model.encode(deleted_texts)
        # print ("deleted embeddings loaded")


        # get_most_similar(paired_deleted, deleted_embeddings, existing_embeddings, top_n)
        get_most_similar(paired_removed, removed_embeddings, existing_embeddings, top_n)


        stop = timeit.default_timer()
        print('Time: ', stop - start)


