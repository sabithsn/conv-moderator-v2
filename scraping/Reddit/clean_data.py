from bs4 import BeautifulSoup
import os
import pandas as pd
import re

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

DATA_DIR = "../data/reddit/historical_comments_pushshift"
OUT_DIR = "cleaned"

def remove_html_tags(text):
    if pd.isnull(text):
        return ""
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def remove_html_tags_bs4(text):
    if pd.isnull(text):
        return ""
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()

def main():
    dir_to_write = os.path.join(DATA_DIR, OUT_DIR)
    if not os.path.isdir(dir_to_write):
        os.mkdir(dir_to_write)
    for filename in os.listdir(DATA_DIR):
        filepath = os.path.join(DATA_DIR, filename)
        if os.path.isdir(filepath):
            continue

        try:
            data = pd.read_csv(filepath, sep="\t", lineterminator='\n')
        except:
            print("read failed for file {}".format(filename))
            continue
        data["body"] = [remove_html_tags_bs4(text) for text in data["body"].values.tolist()]
        print(data["body"].head(10))
        data.to_csv(os.path.join(dir_to_write, filename), sep="\t")


if __name__ == "__main__":
    main()