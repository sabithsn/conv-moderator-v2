import pandas as pd
import regex as re


ANNOTATION_FILE = "../data/annotation_data.csv"
PREDICTION_FILES = ["/home/kaa1391/conv-moderator-v2/annotations/data/style-transfer-predictions - BART.csv", "/home/kaa1391/conv-moderator-v2/annotations/data/style-transfer-predictions - dialogpt.csv"]

def main():
    annotation_data = pd.read_csv(ANNOTATION_FILE)
    for filepath in PREDICTION_FILES:
        prediction_data = pd.read_csv(filepath)
        prediction_data['annotation_id'] = [annotation_data[annotation_data['Removed Comment'].str.match(re.escape(row['source']))]['annotation_id'].values[0] for _, row in prediction_data.iterrows()]
        prediction_data.to_csv(filepath)

if __name__ == "__main__":
    main()