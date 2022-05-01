import pandas as pd
import pickle
import regex as re


PREDICTION_FILE = "/home/kaa1391/conv-moderator-v2/annotations/data/style-transfer-predictions - dialogpt.csv"

def main():
    annotation_data = pd.read_csv("/home/kaa1391/conv-moderator-v2/annotations/data/style-transfer-predictions - dialogpt.csv")
    for metric in 'anno_pred', 'orig_pred':
        span_results = pickle.load(open('../data/span_results_{}_dialogpt.pkl'.format(metric), 'rb'))
        relation_results = pickle.load(open('../data/relation_results_{}_dialogpt.pkl'.format(metric), 'rb'))
        annotation_data['rst_span_score_{}'.format(metric)] = [span_results[row['annotation_id']] if row['annotation_id'] in span_results else None for _, row in annotation_data.iterrows()]
        annotation_data['rst_relation_score_{}'.format(metric)] = [relation_results[row['annotation_id']] if row['annotation_id'] in relation_results else None for _, row in annotation_data.iterrows()]
        annotation_data.to_csv('../data/prediction_data_with_rst_scores_dialogpt.csv')

    annotation_data = pd.read_csv("/home/kaa1391/conv-moderator-v2/annotations/data/style-transfer-predictions - BART.csv")
    for metric in 'anno_pred', 'orig_pred':
        span_results = pickle.load(open('../data/span_results_{}_bart.pkl'.format(metric), 'rb'))
        relation_results = pickle.load(open('../data/relation_results_{}_bart.pkl'.format(metric), 'rb'))
        annotation_data['rst_span_score_{}'.format(metric)] = [span_results[row['annotation_id']] if row['annotation_id'] in span_results else None for _, row in annotation_data.iterrows()]
        annotation_data['rst_relation_score_{}'.format(metric)] = [relation_results[row['annotation_id']] if row['annotation_id'] in relation_results else None for _, row in annotation_data.iterrows()]
        annotation_data.to_csv('../data/prediction_data_with_rst_scores_bart.csv')

if __name__ == "__main__":
    main()