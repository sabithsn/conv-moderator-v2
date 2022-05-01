import math
import pandas as pd


def main():
    for metric in ['rst_span_score', 'rst_relation_score']:
        print("-------{}------".format(metric))
        annotation_data = pd.read_csv('../data/annotations_with_scores.csv')
        kate_rst_scores = [row[metric] for _, row in annotation_data.iterrows() if row['Annotator'] == 'Kate' and not pd.isnull(row[metric])]
        ilana_rst_scores = [row[metric] for _, row in annotation_data.iterrows() if row['Annotator'] == 'Ilana' and not pd.isnull(row[metric])]
        pantho_rst_scores = [row[metric] for _, row in annotation_data.iterrows() if row['Annotator'] == 'Pantho' and not pd.isnull(row[metric])]
        all_rst_scores = [row[metric] for _, row in annotation_data.iterrows() if not pd.isnull(row[metric])]
        print("Number of Kate's annotations: {}".format(len(kate_rst_scores)))
        print("Number of Ilana's annotations: {}".format(len(ilana_rst_scores)))
        print("Number of Pantho's annotations: {}".format(len(pantho_rst_scores)))
        print("Average F1 score - Kate: {}".format(sum(kate_rst_scores)/len(kate_rst_scores)))
        print("Average F1 score - Ilana: {}".format(sum(ilana_rst_scores)/len(ilana_rst_scores)))
        print("Average F1 score - Pantho: {}".format(sum(pantho_rst_scores)/len(pantho_rst_scores)))
        print("Average F1 score - All: {}".format(sum(all_rst_scores)/len(all_rst_scores)))


if __name__ == "__main__":
    main()