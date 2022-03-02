import nltk
import os
import pandas as pd

from knockknock import slack_sender
from nltk import word_tokenize
from tqdm import tqdm


tqdm.pandas()

DATA_DIR = "../data/reddit/historical_comments_pushshift"
CLEANED_DIR = "cleaned"
OUT_DIR = "cleaned_and_filtered"
webhook_url = "https://hooks.slack.com/services/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"

def contains_30_or_fewer_tokens(text):
    if pd.isnull(text):
        return True
    tokens = word_tokenize(text)
    if len(tokens) < 30:
        return True
    else:
        return False

def contains_3_or_more_tokens(text):
    if pd.isnull(text):
        return False
    tokens = word_tokenize(text)
    if len(tokens) > 2:
        return True
    else:
        return False

@slack_sender(webhook_url=webhook_url, channel="#conversational-moderator")
def main():
    cleaned_data_dir = os.path.join(DATA_DIR, CLEANED_DIR)
    dir_to_write = os.path.join(DATA_DIR, OUT_DIR)
    if not os.path.isdir(dir_to_write):
        os.mkdir(dir_to_write)
    for filename in os.listdir(cleaned_data_dir):
        filepath = os.path.join(cleaned_data_dir, filename)
        if os.path.isdir(filepath):
            continue
        if os.path.isfile(os.path.join(dir_to_write, filename)):
            continue
        data = pd.read_csv(filepath, sep="\t")
        #data["body"] = data[(contains_3_or_more_tokens(data["body"])) & (contains_30_or_fewer_tokens(data["body"]))]
        data['30_or_fewer_tokens'] = data.progress_apply(lambda row: contains_30_or_fewer_tokens(row['body']), axis=1)
        data['3_or_more_tokens'] = data.progress_apply(lambda row: contains_3_or_more_tokens(row['body']), axis=1)
        print("------Data------")
        print(len(data))
        print(data['30_or_fewer_tokens'].head(20))
        print("------Data Filtered------")
        data_filtered = data[data['30_or_fewer_tokens'] == True]
        print(len(data_filtered))
        print(data_filtered['30_or_fewer_tokens'].head(20))
        data_filtered = data_filtered[data_filtered['3_or_more_tokens'] == True]
        print(len(data_filtered))
        print(data_filtered['3_or_more_tokens'].head(20))
        data_filtered.to_csv(os.path.join(dir_to_write, filename), sep="\t")

if __name__ == "__main__":
    main()