import nltk
import numpy as np
import os
import pickle
import torch

from nltk.tokenize import sent_tokenize
from scipy.special import softmax
from transformers import XLNetForSequenceClassification, XLNetTokenizer

from process_pdtb_files import get_senses_and_offsets, get_spanlists

PDTB_DIR = "../data/comments/output"
RAW_TEXT_DIR = "../data/comments"
PRETRAINED_MODEL_DIR = "/home/kaa1391/pdtb-parsers/pdtb3/scripts/output/fold_2_xlnet_large"
PDTB_LABELS = ['Temporal.Asynchronous', 'Temporal.Synchrony', 'Contingency.Cause',
               'Contingency.Pragmatic cause', 'Contingency.Condition.', 'Comparison.Contrast', 'Comparison.Concession',
               'Expansion.Conjunction', 'Expansion.Instantiation', 'Expansion.Restatement',
               'Expansion.Alternative','Expansion.List']
DEVICE = "cuda"


def _truncate_seq_pair(tokens_a, tokens_b, max_length):
    """Truncates a sequence pair in place to the maximum length."""

    # This is a simple heuristic which will always truncate the longer sequence
    # one token at a time. This makes more sense than truncating an equal percent
    # of tokens from each, since if one sequence is very short then each token
    # that's truncated likely contains more information than a longer sequence.
    while True:
        total_length = len(tokens_a) + len(tokens_b)
        if total_length <= max_length:
            break
        if len(tokens_a) > len(tokens_b):
            tokens_a.pop()
        else:
            tokens_b.pop()


def get_args_from_spanlists(arg1_ranges, arg2_ranges, text):
    arg1_list = []
    for argrange in arg1_ranges:
        beginning = int(argrange[0])
        end = int(argrange[1])
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


def tokenize_args(arg1, arg2, max_seq_length,
                  tokenizer,
                  cls_token_at_end=False, pad_on_left=False,
                  cls_token='[CLS]', sep_token='[SEP]', pad_token=0,
                  sequence_a_segment_id=0, sequence_b_segment_id=1,
                  cls_token_segment_id=1, pad_token_segment_id=0,
                  mask_padding_with_zero=True):
    tokens_a = tokenizer.tokenize(arg1)

    tokens_b = None
    if arg2:
        tokens_b = tokenizer.tokenize(arg2)
        # Modifies `tokens_a` and `tokens_b` in place so that the total
        # length is less than the specified length.
        # Account for [CLS], [SEP], [SEP] with "- 3"
        _truncate_seq_pair(tokens_a, tokens_b, max_seq_length - 3)
    else:
        # Account for [CLS] and [SEP] with "- 2"
        if len(tokens_a) > max_seq_length - 2:
            tokens_a = tokens_a[:(max_seq_length - 2)]

    # The convention in BERT is:
    # (a) For sequence pairs:
    #  tokens:   [CLS] is this jack ##son ##ville ? [SEP] no it is not . [SEP]
    #  type_ids:   0   0  0    0    0     0       0   0   1  1  1  1   1   1
    # (b) For single sequences:
    #  tokens:   [CLS] the dog is hairy . [SEP]
    #  type_ids:   0   0   0   0  0     0   0
    #
    # Where "type_ids" are used to indicate whether this is the first
    # sequence or the second sequence. The embedding vectors for `type=0` and
    # `type=1` were learned during pre-training and are added to the wordpiece
    # embedding vector (and position vector). This is not *strictly* necessary
    # since the [SEP] token unambiguously separates the sequences, but it makes
    # it easier for the model to learn the concept of sequences.
    #
    # For classification tasks, the first vector (corresponding to [CLS]) is
    # used as as the "sentence vector". Note that this only makes sense because
    # the entire model is fine-tuned.
    tokens = tokens_a + [sep_token]
    segment_ids = [sequence_a_segment_id] * len(tokens)

    if tokens_b:
        tokens += tokens_b + [sep_token]
        segment_ids += [sequence_b_segment_id] * (len(tokens_b) + 1)

    if cls_token_at_end:
        tokens = tokens + [cls_token]
        segment_ids = segment_ids + [cls_token_segment_id]
    else:
        tokens = [cls_token] + tokens
        segment_ids = [cls_token_segment_id] + segment_ids

    input_ids = tokenizer.convert_tokens_to_ids(tokens)

    # The mask has 1 for real tokens and 0 for padding tokens. Only real
    # tokens are attended to.
    input_mask = [1 if mask_padding_with_zero else 0] * len(input_ids)

    # Zero-pad up to the sequence length.
    padding_length = max_seq_length - len(input_ids)

    if pad_on_left:
        input_ids = ([pad_token] * padding_length) + input_ids
        input_mask = ([0 if mask_padding_with_zero else 1] * padding_length) + input_mask
        segment_ids = ([pad_token_segment_id] * padding_length) + segment_ids
    else:
        input_ids = input_ids + ([pad_token] * padding_length)
        input_mask = input_mask + ([0 if mask_padding_with_zero else 1] * padding_length)
        segment_ids = segment_ids + ([pad_token_segment_id] * padding_length)

    assert len(input_ids) == max_seq_length, "{}, {}".format(len(input_ids), len(s1_input_ids))
    assert len(input_mask) == max_seq_length
    assert len(segment_ids) == max_seq_length

    return torch.tensor(input_ids).to(DEVICE), torch.tensor(input_mask).to(DEVICE), torch.tensor(segment_ids).to(DEVICE)


def run_inference(model, tokenizer, arg1_text, arg2_text):
    # encodings = tokenizer.encode_plus(arg1_text,
    #                                   arg2_text,
    #                                   add_special_tokens=True, max_length=128, 
    #                                   return_tensors='pt', 
    #                                   return_token_type_ids=True, 
    #                                   return_attention_mask=True, 
    #                                   pad_to_max_length=True)
    
    
    #input_ids = encodings['input_ids']
    #attention_mask = encodings['attention_mask']
    #token_type_ids = encodings['token_type_ids']
    input_ids, attention_mask, token_type_ids = tokenize_args(arg1_text, arg2_text, 128, tokenizer)
    input_ids = torch.unsqueeze(input_ids, dim=0)
    attention_mask = torch.unsqueeze(attention_mask, dim=0)
    token_type_ids = torch.unsqueeze(token_type_ids, dim=0)

    inputs = {'input_ids':      input_ids,
              'attention_mask': attention_mask,
              'token_type_ids': token_type_ids}
    output = model(**inputs)
    pred = np.argmax(output[0].detach().cpu().numpy(), axis=1)
    probs = softmax(output[0].detach().cpu().numpy(), axis=1)
    return PDTB_LABELS[pred.item()], probs


def get_sentences(text):
    sentences = sent_tokenize(text)
    return sentences


def main():
    model = XLNetForSequenceClassification.from_pretrained(PRETRAINED_MODEL_DIR).to(DEVICE)
    model.eval()
    tokenizer = XLNetTokenizer.from_pretrained("xlnet-large-cased")
    for filename in os.listdir(PDTB_DIR):
        if not filename.endswith(".pipe"):
            continue
        filepath = os.path.join(PDTB_DIR, filename)
        senses_and_offsets = get_senses_and_offsets(os.path.join(PDTB_DIR, filename))

        with open(os.path.join(RAW_TEXT_DIR, filename.replace(".pipe", "")), "r") as f:
            text = f.read()

            ### run implicit sense classifier (and append to file) ###
            with open(os.path.join(PDTB_DIR, filename), "a") as g:
                sentences_to_check = get_sentences(text)
                probabilities = []
                # check each pair of adjacent sentences
                for i in range(len(sentences_to_check) - 1):
                    arg1_text = sentences_to_check[i]
                    arg2_text = sentences_to_check[i+1]
                    predicted_label, probs = run_inference(model, tokenizer, arg1_text, arg2_text)   
                    print("Implicit" + ("|" * 11) + predicted_label + ("|" * 13) + arg1_text + ("|" * 10) + arg2_text + ("|" * 13))
                    g.write("\n" + "Implicit" + ("|" * 11) + predicted_label + ("|" * 13) + arg1_text + ("|" * 10) + arg2_text + ("|" * 13))   
                    probabilities.append(probs)  

                pickle.dump(probabilities, open(os.path.join(PDTB_DIR, filename.replace(".pipe", "-implicit-probs.pkl")), "wb"))

if __name__ == "__main__":
    main()