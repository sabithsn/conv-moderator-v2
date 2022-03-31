
from nltk.translate.bleu_score import sentence_bleu
from bert_score import BERTScorer
import statistics
import pandas as pd 

df = pd.read_csv("../data/style-transfer-annotation.tsv", sep = "\t")
df = df[["Removed Comment", "Custom", "Annotator"]]
df = df.dropna()
df["Removed Comment"] = list(map(lambda x: x.lower(), df['Removed Comment']))
df["Custom"] = list(map(lambda x: x.lower(), df['Custom']))

df_list = df.values.tolist()
annotations = {"Pantho": {"OG" : [], "PP": []}, "Kate": {"OG" : [], "PP": []}, "Ilana": {"OG" : [], "PP": []}}
print (df_list[:5])

scorer = BERTScorer(lang = "en", rescale_with_baseline=True)

_, _, full_bert = scorer.score(df["Custom"].values.tolist(), df["Removed Comment"].values.tolist())
print ("full bert score:", full_bert.mean())

bleus = []
for i in range (len(df_list)):
    x = df_list[i][0]
    y = df_list[i][1]
    reference = [x]
    candidate = y
    BLEU = sentence_bleu(reference, candidate)
    bleus.append(BLEU)
BLEU = statistics.mean(bleus)
print ("full BLEU:", BLEU)

for i in range (len(df_list)):
    row = df_list[i]
    annotations[row[2]]["PP"].append(row[1])
    annotations[row[2]]["OG"].append(row[0])


for key in annotations:
    _,_, bert = scorer.score(annotations[key]["PP"], annotations[key]["OG"])
    bert = bert.mean().item()
    bleus = []
    for i in range (len(annotations[key]["OG"])):
        x = annotations[key]["OG"][i]
        y = annotations[key]["PP"][i]
        reference = [x]
        candidate = y
        BLEU = sentence_bleu(reference, candidate)
        bleus.append(BLEU)
    BLEU = statistics.mean(bleus)
    
    print ("Annotator ", key, " Scores:")
    print ("BLEU:", round(BLEU*100,2))
    print ("BERT-score:", round(bert*100,2))


scorer = BERTScorer(lang = "en", rescale_with_baseline=True)

lines = []
with open ("../data/style-transfer-annotation.tsv", "r", encoding = "utf-8") as f:
    for line in f:
        lines.append(line.strip())


# scorer = BERTScorer(lang = "en")
with open ("../data/style-transfer-annotation+similarity.tsv", "w", encoding = "utf-8") as f:
    for i in range (len(lines)):
        line = lines[i]
        if i == 0:
            f.write(line + "\tBERT_score\tBLEU_score\n")
            continue
        if (i%100 == 0):
            print(i)
        row = line.split("\t")
        custom = row[7].lower()
        og = row[0].lower()
        if len(custom) == 0:
            f.write(line + "\t??????\t??????\n")
            continue

        reference = [og]
        candidate = custom
        BLEU = str(sentence_bleu(reference, candidate)*100)

        reference = [og]
        candidate = [custom]
        _,_, bert = scorer.score(candidate, reference)
        bert = str(round(bert.mean().item()*100,2))

        f.write(line + "\t" + bert + "\t" + BLEU + "\n")