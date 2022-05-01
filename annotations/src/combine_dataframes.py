import pandas as pd
import regex as re
import uuid


PARENT_FILE = "../data/Reddit-Comment-Parent-Pairs.csv"
ANNOTATION_FILE = "../data/Style-transfer-annotation.csv"

def main():
    parent_data = pd.read_csv(PARENT_FILE)
    annotation_data = pd.read_csv(ANNOTATION_FILE)
    annotation_data['parent_sheet_id'] = [parent_data[parent_data['comment'].str.match(re.escape(row['Removed Comment']))]['ID'].values for _, row in annotation_data.iterrows()]
    annotation_data['annotation_id'] = [uuid.uuid1() for _, row in annotation_data.iterrows()]
    annotation_data.to_csv('annotation_data.csv')

if __name__ == "__main__":
    main()