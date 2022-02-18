'''
Fine-tune BART on removed reddit data.
run the program with command line argument of subname.
change lines 23,24 to run on deleted reddit data
'''

'''
python fine-tune-BART.py Conservative bert
python fine-tune-BART.py Conservative MiniLM
python fine-tune-BART.py ChangeMyView bert
python fine-tune-BART.py ChangeMyView MiniLM
'''

import os
from datetime import datetime
import logging
import sys

import pandas as pd
from sklearn.model_selection import train_test_split
from simpletransformers.seq2seq import Seq2SeqModel, Seq2SeqArgs

# from utils import load_data, clean_unnecessary_spaces


def main():
    logging.basicConfig(level=logging.INFO)
    transformers_logger = logging.getLogger("transformers")
    transformers_logger.setLevel(logging.ERROR)


    train_directory = "../scraping/data/reddit/train/removed/"
    eval_directory = "../scraping/data/reddit/eval/removed/"
    
    # measure = "bert"
    # measure = "MiniLM"

    subname = sys.argv[1]
    measure = sys.argv[2]

    # Google Data
    train_df = pd.read_csv(train_directory + subname + "_" + measure + ".tsv", sep="\t").astype(str)
    eval_df = pd.read_csv(eval_directory + subname + "_" + measure + ".tsv", sep="\t").astype(str)


    train_df = train_df[["input_text", "target_text"]]
    train_df = train_df.apply(lambda x: x.str.slice(0, 2000))
    eval_df = eval_df[["input_text", "target_text"]]
    eval_df = eval_df.apply(lambda x: x.str.slice(0, 2000))

    train_df["prefix"] = "paraphrase"
    eval_df["prefix"] = "paraphrase"


    train_df = train_df.dropna()
    eval_df = eval_df.dropna()

    print(train_df)

    model_args = Seq2SeqArgs()
    model_args.eval_batch_size = 2
    model_args.evaluate_during_training = True
    model_args.evaluate_during_training_steps = 2500
    model_args.evaluate_during_training_verbose = True
    model_args.fp16 = False
    model_args.learning_rate = 5e-5
    model_args.max_seq_length = 128
    model_args.num_train_epochs = 3
    model_args.overwrite_output_dir = True
    model_args.reprocess_input_data = True
    model_args.save_eval_checkpoints = False
    model_args.save_steps = -1
    model_args.train_batch_size = 2
    model_args.use_multiprocessing = False

    model_args.do_sample = True
    model_args.num_beams = 2
    model_args.num_return_sequences = 3
    model_args.max_length = 128
    model_args.top_k = 50
    model_args.top_p = 0.95

    model_args.wandb_project = "Paraphrasing with BART"


    model = Seq2SeqModel(
        encoder_decoder_type="bart",
        encoder_decoder_name="facebook/bart-base",
        args=model_args,
    )

    model.train_model(train_df, eval_data=eval_df)

    to_predict = [
        prefix + ": " + str(input_text)
        for prefix, input_text in zip(
            eval_df["prefix"].tolist(), eval_df["input_text"].tolist()
        )
    ]
    truth = eval_df["target_text"].tolist()

    preds = model.predict(to_predict)

    # Saving the predictions if needed
    # os.makedirs("../scraping/data/reddit/predictions/removed", exist_ok=True)

    with open("../scraping/data/reddit/predictions/removed/" + subname + "_predictions_" + measure + "_BART.txt", "w", encoding = "utf-8") as f:
        for i, text in enumerate(eval_df["input_text"].tolist()):
            try:
                f.write(str(text.replace("\n"," ").replace("\r", " ")) + "\t" + truth[i].replace("\n"," ").replace("\r", " ") + "\t" + preds[i][0].replace("\n"," ").replace("\r", " ") + "\n")

            except:
                f.write (text.replace("\n"," ").replace("\r", " ") + "\t" + "UNKNOWN" + "\t" + "UNKNOWN" + "\n")
                continue

if __name__ == "__main__":
        main()