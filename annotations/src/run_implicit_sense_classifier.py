import nltk
import numpy as np
import os

from nltk.tokenize import sent_tokenize

from transformers import XLNetForSequenceClassification

from process_pdtb_files import get_senses_and_offsets, get_spanlists

PDTB_DIR = "../data/comments/output"
RAW_TEXT_DIR = "../data/comments"
PRETRAINED_MODEL_DIR = "/home/kaa1391/pdtb-parsers/pdtb3/scripts/output/fold_2_xlnet_large"
PDTB_LABELS = ['Temporal.Asynchronous', 'Temporal.Synchrony', 'Contingency.Cause',
               'Contingency.Pragmatic cause', 'Contingency.Condition.', 'Comparison.Contrast', 'Comparison.Concession',
               'Expansion.Conjunction', 'Expansion.Instantiation', 'Expansion.Restatement',
               'Expansion.Alternative','Expansion.List']
DEVICE = "cuda"

def get_args_from_spanlists(arg1_ranges, arg2_ranges, text):
    arg1_list = []
    for argrange in arg1_ranges:
        beginning = int(argrange[0])
        end = int(argrange[1])
        #if filename == "talk_1978_en.txt":
        #    beginning += 2
        #    end += 2
        arg1_list.append(text[beginning:end])

    arg2_list = []
    for argrange in arg2_ranges:
        beginning = int(argrange[0])
        end = int(argrange[1])
        #if filename == "talk_1978_en.txt":
        #    beginning += 2
        #    end += 2
        arg2_list.append(text[beginning:end])

    arg1 = " ".join(arg1_list)
    arg2 = " ".join(arg2_list)

    return arg1, arg2


def run_inference(model, tokenizer, arg1_text, arg2_text):
    encodings = tokenizer.encode_plus(arg1_text,
                                      arg2_text,
                                      add_special_tokens=True, max_length=128, 
                                      return_tensors='pt', 
                                      return_token_type_ids=True, 
                                      return_attention_mask=True, 
                                      pad_to_max_length=True)
    
    input_ids = encodings['input_ids']
    attention_mask = encodings['attention_mask']
    token_type_ids = encodings['token_type_ids']
    inputs = {'input_ids':      input_ids,
              'attention_mask': attention_mask,
              'token_type_ids': token_type_ids}
    output = model(**inputs)
    pred = np.argmax(output['logits'].detach().cpu().numpy(), axis=1)
    return PDTB_LABELS[pred]


def get_sentences_and_offsets(text):
    sentences = sent_tokenize(text)
    sentences_and_offsets = [(sentence, (text.find(sentence), text.find(sentence) + len(sentence))) for sentence in sentences]
    return sentences_and_offsets


def sentence_pair_is_explicit(sentence1, sentence2):



def main():
    model = XLNetForSequenceClassification.from_pretrained(PRETRAINED_MODEL_DIR).to(DEVICE)
    model.eval()
    tokenizer = XLNetForSequenceClassification.from_pretrained("xlnet-large-cased")
    for filename in os.listdir(PDTB_DIR):
        if not filename.endswith(".pipe"):
            continue
        filepath = os.path.join(PDTB_DIR, filename)
        senses_and_offsets = get_senses_and_offsets(os.path.join(PDTB_DIR, filename))
        
        for i, relation in enumerate(senses_and_offsets):
            print(relation)
            relation_type = relation['relation_type']
            if relation_type != "Implicit":
                continue

            text = ""
            with open(os.path.join(RAW_TEXT_DIR, filename.replace(".pipe", ".txt"))) as f:
                text = f.read()
            arg1_text, arg2_text = get_args_from_spanlists(relation["arg1_spanlist"], relation["arg2_spanlist"], text)
            
            predicted_label = run_inference(model, tokenizer, arg1_text, arg2_text)


if __name__ == "__main__":
    main()