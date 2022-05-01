import pandas as pd
import pickle
import regex as re
import uuid


PARENT_FILE = "../data/Reddit-Comment-Parent-Pairs.csv"

def main():
    rst_relations = pickle.load(open("../data/top_level_relations.pkl", "rb"))
    print(rst_relations.keys())
    comment_data = pd.read_csv(PARENT_FILE)
    comment_data["rst_rel"] = [rst_relations[row["ID"]] if row["ID"] in rst_relations else None for _, row in comment_data.iterrows()]
    comment_data.to_csv('../data/Reddit-Comment-Parent-Pairs-RST.csv')

if __name__ == "__main__":
    main()