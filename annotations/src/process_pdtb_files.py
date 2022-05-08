'''Fields for pipe-delimited PDTB files can be found here: https://github.com/WING-NUS/pdtb-parser'''
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
import csv
import os
import pandas as pd
PDTB_DIR = "../data/comments/output"
RAW_TEXT_DIR = "../data/comments"

def get_spanlists(arg1_span, arg2_span):
    '''Takes in offsets in string form and returns list of ranges in the form 
    [[range1_begin, range1_end], [range2_begin, range2_end], ...] for each argument'''
    arg1_ranges_str = arg1_span.split(";")
    arg2_ranges_str = arg2_span.split(";")
    arg1_ranges = []
    for argrange in arg1_ranges_str:
        if argrange != "":
            arg1_ranges.append(argrange.split(".."))

    arg2_ranges = []
    for argrange in arg2_ranges_str:
        if argrange!= "":
            arg2_ranges.append(argrange.split(".."))

    return arg1_ranges, arg2_ranges

def get_senses_and_offsets(filename):
    '''Returns list of dicts containing sense types and character offsets for each
    discourse relation in the file'''
    senses_and_offsets = []
    with open(filename,  encoding = "utf-8") as f:
        relations = csv.reader(f, delimiter="|")
        # print (relations)
        for relation in relations:
            if len(relation) == 0:
                continue
            relation_type = relation[0]
            if relation_type != "Explicit" and relation_type != "Implicit":
                continue
            discourse_sense = relation[11]
            arg1_offset = relation[22]
            try:
                arg2_offset = relation[32]
            except:
                print ("--------------------------------------------------------------")
                print ("\t".join(relation))
                print (filename)
                print ("--------------------------------------------------------------")
                exit()
            arg1_spanlist, arg2_spanlist = get_spanlists(arg1_offset, arg2_offset)
            senses_and_offsets.append({"filename": filename,
                                       "relation_type": relation_type,
                                       "discourse_sense": discourse_sense,
                                       "arg1_spanlist": arg1_spanlist,
                                       "arg2_spanlist": arg2_spanlist
                                       })
    return senses_and_offsets


def insert_tag(original, tag, index):
    inserted = original[:index] + tag + original[index:]
    inserted = inserted.split(tag)
    inserted = (" " + tag + " ").join(inserted)
    inserted = inserted.replace("  ", " ").strip()
    # if index == 0:
    #     inserted = tag + " " 
    return inserted

def merge(original, sent1, sent2):
    # print ("sent1", sent1)
    # print ("sent2", sent2)
    new_str = []
    # original_split = original.split(" ")
    sent1_split = word_tokenize(sent1)
    sent2_split = word_tokenize(sent2)
    # print (sent1_split)
    # print (sent2_split)
    i = 0
    j = 0
    k = 0
    while i < len (sent1_split):

        if sent1_split[i] == sent2_split[j]:
            if j < len(sent2_split) - 1:
                j += 1
            i += 1
            continue
        if sent1_split[i] not in sent2_split:
            sent2_split = sent2_split[:j] + [sent1_split[i]] + sent2_split[j:]
            i += 1
            if j < len(sent2_split) - 1:
                j += 1
            continue
        if j < len(sent2_split) - 1:
            j += 1
        else:
            sent2_split = sent2_split + [sent1_split[i]]
            i += 1

    # match = original_split[0]
    # while True:
    #     print (new_str)
    #     print (i,j,k)
    #     while j < len (sent1_split) and sent1_split[j] != match:
    #         new_str.append(sent1_split[j])
    #         j += 1

    #     while k < len (sent2_split) and sent2_split[k] != match:
    #         new_str.append(sent2_split[k])
    #         k += 1

    #     if i < len(original_split):
    #         new_str.append(original_split[i])
    #     i += 1
    #     if i < len(original_split):
    #         match = original_split[i]

    #     if j >= len(sent1_split) and k >= len(sent2_split):
    #         break

    # print ("original:", original_split)
    # print ("new:", new_split)
    # original_index = 0
    # cur = original_split[original_index]

    # for i in range (len(new_split)):
    #     if new_split[i] != cur:
    #         new_str.append(new_split[i])
    #     else:
    #         new_str.append(new_split[i])
    #         original_index += 1
    #         if original_index >= len(original_split):
    #             continue
    #         cur = original_split[original_index]
    return TreebankWordDetokenizer().detokenize(sent2_split)
    # return (" ".join(sent2_split))


def main():

    df = pd.read_csv("../Data/Comment-Parent - Pairs.csv")
    subs = df["subreddit"].values.tolist()
    comments = df["comment"].values.tolist()
    parents = df["parent"].values.tolist()
    IDs = df["ID"].values.tolist()

    dictionary = {}
    for i in range (len(IDs)):
        dictionary[IDs[i]] = (subs[i], comments[i], parents[i])

    new_tokens = []
    inserts = []
    with open ("EI-PDTB-discourse-annotation.tsv", "w", encoding = "utf-8") as h:
        h.write("subreddit\tparent\tcomment\tpdtb-comment\n")
        for filename in os.listdir(PDTB_DIR):
            if not filename.endswith(".pipe"):
                continue
            print (filename)
            file_id = filename.split(".")[0]
            s,comment,p = dictionary[file_id]
            copy_comment = str(comment)
            senses_and_offsets = get_senses_and_offsets(os.path.join(PDTB_DIR, filename))
            print (senses_and_offsets)
            new_strings = []
            inserts = []

            for x in senses_and_offsets:
                sense = x["discourse_sense"]
                sense_arg1_begin = "<" + sense + ">"
                sense_arg1_end = "<" + sense + "/> "

                sense_arg2_begin = "<" + sense + ">"
                sense_arg2_end = "<" + sense + "/> "

                print (sense)
                if sense_arg1_begin not in new_tokens:
                    new_tokens.append(sense_arg1_begin)
                    new_tokens.append(sense_arg1_end)
                    new_tokens.append(sense_arg2_begin)
                    new_tokens.append(sense_arg2_end)


                a1_spans = x["arg1_spanlist"]
                a2_spans = x["arg2_spanlist"]


                for a1_span in a1_spans:
                    start = int(a1_span[0])
                    end = int(a1_span[1])
                    inserts.append((start,sense_arg1_begin))
                    inserts.append((end,sense_arg1_end))

                    # start_added = insert_tag(comment, sense_arg1_begin, start)
                    # end_added = insert_tag(comment, sense_arg1_end, end)
                    # new_strings.append(start_added)
                    # new_strings.append(end_added)
                for a2_span in a2_spans:
                    start = int(a2_span[0])
                    end = int(a2_span[1])
                    inserts.append((start,sense_arg2_begin))
                    inserts.append((end,sense_arg2_end))

                    # start_added = insert_tag(comment, sense_arg2_begin, start)
                    # end_added = insert_tag(comment, sense_arg2_end, end)
                    # new_strings.append(start_added)
                    # new_strings.append(end_added)

            inserts.sort(key = lambda y: y[0])
            inserts.reverse()
            for (index, tag) in inserts:
                copy_comment = copy_comment[:index] + tag + copy_comment[index:]
            for token in new_tokens:
                copy_comment = copy_comment.replace(token, " " + token + " ")

            copy_comment = copy_comment.replace("  ", " ").replace("\t", " ").strip()
            print (inserts)
            print (copy_comment)

            row = [str(s),str(p),str(comment),str(copy_comment)]
            h.write("\t".join(row)+"\n")
            # h.write(str(senses_and_offsets) + "\n")
            # h.write("_______________________________________\n")
            # print(senses_and_offsets)
            # print (cur)
            # break

    new_tokens = list(set(new_tokens))
    with open ("new-tokens4.txt", "w") as k:
        for x in new_tokens:
            k.write(x+"\n")
if __name__ == "__main__":
    main()