import os
import pandas as pd


def main():
    for filepath in ["/home/kaa1391/conv-moderator-v2/annotations/data/style-transfer-predictions - BART.csv"]:
        annotations = pd.read_csv(filepath).to_dict('records')
        for entry in annotations:
            ID = entry['annotation_id']
            prediction = entry['prediction']
            
            with open(os.path.join('../data/predictions-bart', str(ID)), "w+") as f:
                f.write(prediction)
    

if __name__ == "__main__":
    main()