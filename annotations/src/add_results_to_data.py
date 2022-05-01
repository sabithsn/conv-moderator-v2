import pandas as pd
import pickle
import regex as re
import uuid


PARENT_FILE = "../data/Reddit-Comment-Parent-Pairs.csv"
ANNOTATION_FILE = "../data/annotation_data.csv"

def main():
    annotation_data = pd.read_csv(ANNOTATION_FILE)
    span_results = pickle.load(open('../data/span_results.pkl', 'rb'))
    relation_results = pickle.load(open('../data/relation_results.pkl', 'rb'))
    annotation_data['rst_span_score'] = [span_results[row['annotation_id']] if row['annotation_id'] in span_results else None for _, row in annotation_data.iterrows()]
    annotation_data['rst_relation_score'] = [relation_results[row['annotation_id']] if row['annotation_id'] in relation_results else None for _, row in annotation_data.iterrows()]
    annotation_data.to_csv('../data/annotation_data_with_rst_scores.csv')

if __name__ == "__main__":
    main()