import os
import pandas as pd


def main():
    annotations = pd.read_csv("../data/annotation_data.csv").to_dict('records')
    for entry in annotations:
        paraphrase = entry['Custom']
        ID = entry['annotation_id']
        comment = entry['Removed Comment']
        
        with open(os.path.join('../data/comments_annotation_ids', str(ID)), "w+") as f:
            f.write(comment)
        if pd.isnull(paraphrase):
            continue
        with open(os.path.join('../data/paraphrases', str(ID)), "w+") as f:
            f.write(paraphrase)
        
    

if __name__ == "__main__":
    main()