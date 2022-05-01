import csv
import os
import spacy
import torch
import torch.nn
import torch.utils.data

from copy import deepcopy
from spacy.matcher import PhraseMatcher
from typing import List, Dict

from transformers import BertTokenizer

from spacy.matcher import PhraseMatcher
from spacy.lang.en import English

class PDTB2DatasetHAN(torch.utils.data.Dataset):
    def __init__(
            self,
            max_sent_length: int,
            max_doc_length: int,
            num_classes: int,
            tokenizer: BertTokenizer,
            window_size: int
    ):
        self.tokenizer = tokenizer
        self.max_doc_length = max_doc_length
        self.max_sent_length = max_sent_length
        self.num_classes = num_classes
        self.window_size = window_size

        self.tokenizer.add_special_tokens({'additional_special_tokens': ['[ACLS]', '[BCLS]', '[ASEP]', '[BSEP]']})
        print("tokenizer length:", len(tokenizer))
        self.nlp = English()
        #self.nlp.add_pipe(self.nlp.create_pipe('sentencizer'))
        self.nlp.add_pipe("sentencizer")
        
        
        PDTB_DIR = "./data_pdtb/pdtb2_pipe"
        RAW_TEXT_DIR = "./data_pdtb/pdtb_v2/data/raw/wsj"
        PDTB_RELATIONS = {"Temporal.Synchrony": 0, "Temporal.Asynchronous": 1, "Contingency.Cause": 2,
            "Contingency.Pragmatic cause": 3, "Contingency.Condition": 4, "Contingency.Pragmatic condition": 5,
            "Comparison.Contrast": 6, "Comparison.Pragmatic contrast": 7, "Comparison.Concession": 8, 
            "Comparison.Pragmatic concession": 9, "Expansion.Conjunction": 10, "Expansion.Instantiation": 11,
            "Expansion.Restatement": 12, "Expansion.Alternative": 13, "Expansion.Exception": 14, "Expansion.List": 15
        }
        labels = []
        arg_pairs = []
        documents = []
        arg_spans = []
        #print(os.getcwd())
        for directory in os.listdir(PDTB_DIR):
            for filename in os.listdir(PDTB_DIR + os.sep + directory):
                with open(PDTB_DIR + os.sep + directory + os.sep + filename, encoding='latin-1') as csvfile:
                    relations = csv.reader(csvfile, delimiter='|', quoting=csv.QUOTE_NONE)
                    for relation in relations:
                        relation_type = relation[0]
                        if relation_type != "Implicit":
                            continue
    
                        discourse_sense = ".".join(relation[11].split(".")[:2])
                        if discourse_sense.count(".") < 1:
                            continue
    
                        try:
                            arg_pairs.append((relation[24], relation[34]))
                            arg_spans.append((relation[22], relation[32]))
                        except:
                            print(relation)
                            print(filename)
                            print("Error; no argument found")
                            exit()
                        labels.append(PDTB_RELATIONS[discourse_sense])
                        
                        with open(RAW_TEXT_DIR + os.sep + directory + os.sep + filename[:-5], encoding='latin-1') as f:
                            text = f.read()
                            documents.append(text)

        self.documents = documents
        self.arg_pairs = arg_pairs
        self.labels = labels
        self.arg_spans = arg_spans
        
        self.dataset_size = len(labels)
        self.dataset_size = len(labels)

    def _pad_single_sentence_for_bert(self, tokens: List[str], cls: bool = True):
        if cls:
            return [self.tokenizer.cls_token] + tokens + [self.tokenizer.sep_token]
        else:
            return tokens + [self.tokenizer.sep_token]
            
    def _pad_argument_for_bert(self, doc, sentences: List[str], sentences_orig: List[str], terms: str = "", arg1: bool = True):
        # Only run nlp.make_doc to speed things up
        patterns = [self.nlp.make_doc(text) for text in terms]
        patterns_w_period = [self.nlp.make_doc(text + ".") for text in terms]
        matcher = PhraseMatcher(self.nlp.vocab, validate=True)
        matcher.add("TerminologyList", patterns)#, validate=True
        matcher.add("TerminologyListWPeriod", patterns)#, validate=True
        matches = matcher(doc)
        arg_index = -1
        new_sentences = deepcopy(sentences)
                 
        #edge cases where PhraseMatcher doesn't produce matches       
        if arg_index == -1:
            arg_sents = []
            for text in terms:
                #handling edge case
                if text.startswith("("):
                    text = text[1:]
                term_doc = self.nlp(text)
                for sent in term_doc.sents:
                    arg_sents.append(sent.text)
                    arg_sents.append(sent.text + ".")
                
            arg_tokenized = [[token.text for token in self.nlp(text)] for text in arg_sents]
            
            for i, sentence_orig in enumerate(sentences_orig):
                sentence = new_sentences[i]
                token_inserted_in_sentence = 0
                if any([" ".join(arg) in " ".join(sentence_orig) for arg in arg_tokenized]):
                    if arg1:
                        first_token_position_in_sent = -1
                        end_token_position_in_sent = -1
                        for arg in arg_tokenized:
                            indices_list = [i for i in range(len(sentence_orig)-len(arg)+1) if arg == sentence_orig[i:i+len(arg)]]
                            if len(indices_list) > 0:
                                first_token_position_in_sent = indices_list[0]
                                end_token_position_in_sent = indices_list[0] + len(arg)
                            
                        sentence.insert(first_token_position_in_sent, '[ACLS]')
                        sentence.insert(end_token_position_in_sent + 1, '[ASEP]')
                    else:
                        first_token_position_in_sent = -1
                        end_token_position_in_sent = -1
                        for arg in arg_tokenized:
                            indices_list = [i for i in range(len(sentence_orig)-len(arg)+1) if arg == sentence_orig[i:i+len(arg)]]
                            if len(indices_list) > 0:
                                first_token_position_in_sent = indices_list[0]
                                end_token_position_in_sent = indices_list[0] + len(arg)

                        sentence.insert(first_token_position_in_sent, '[BCLS]')
                        sentence.insert(end_token_position_in_sent + 1, '[BSEP]')
                    new_sentences[i] = sentence
                    arg_index = i
                    token_inserted_in_sentence = 1
                    
        if arg_index == -1:
            print("is arg1:", arg1)
            print("arg_index is -1")
            print("terms:", terms)
            print("patterns:", patterns)
            print("patterns_w_period:", patterns_w_period)
            print("matches:", matches)
            arg_tokenized = [" ".join([token.text for token in self.nlp(text)]) for text in terms]
            print("arg_tokenized:", arg_tokenized)
            print("sentences tokenized:", [" ".join(sentence_orig) for sentence_orig in sentences_orig])
            print(sentences)

        return new_sentences, arg_index

    def _pad_sequence_for_bert_batch(self, tokens_lists, max_len: int):
        pad_id = self.tokenizer.pad_token_id
        assert max_len <= self.max_sent_length
        toks_ids = []
        att_masks = []
        tok_type_lists = []
        for item_toks in tokens_lists:
            padded_item_toks = item_toks + [pad_id] * (max_len - len(item_toks))
            toks_ids.append(padded_item_toks)

            _att_mask = [1] * len(item_toks) + [0] * (max_len - len(item_toks))
            att_masks.append(_att_mask)

            first_sep_id = padded_item_toks.index(self.tokenizer.sep_token_id)
            assert first_sep_id > 0
            _tok_type_list = [0] * (first_sep_id + 1) + [1] * (max_len - first_sep_id - 1)
            tok_type_lists.append(_tok_type_list)
        return toks_ids, att_masks, tok_type_lists

    def _transform_text(self, doc, arg1, arg2):
        # encode document with max sentence length and max document length (maximum number of sentences)
        sentences = [[token.text for token in sent] for sent in doc.sents]
        text: List[List[str]] = sentences
        
        sentences_1, arg1_index = self._pad_argument_for_bert(doc, sentences, sentences, arg1, True)
        sentences_2, arg2_index = self._pad_argument_for_bert(doc, sentences_1, sentences, arg2, False)
        #TODO: figure out edge case where arg1 or arg2 index equals -1
        final_sentences = sentences_2[(arg1_index-self.window_size) % len(sentences): arg2_index+self.window_size+1]
        
        docs = []
        sent_index = 0
        for sentence in final_sentences:
            if sent_index == 0:
                bert_sentence = self._pad_single_sentence_for_bert(sentence, cls=True)
            else:
                bert_sentence = self._pad_single_sentence_for_bert(sentence, cls=False)
            if len(bert_sentence) <= self.max_sent_length:
                docs.append(bert_sentence)
            sent_index += 1
        docs = docs[:self.max_doc_length]
        num_sents = min(len(docs), self.max_doc_length)

        # skip erroneous ones
        if not num_sents:
            return None, -1, None

        num_words = [min(len(sent), self.max_sent_length) for sent in docs][:self.max_doc_length]

        return docs, num_sents, num_words

    def __getitem__(self, i):
        doc = self.nlp(self.documents[i])
        
        arg1, arg2 = get_arg_list_from_spans(self.arg_spans[i][0], self.arg_spans[i][1], self.documents[i])
        doc, num_sents, num_words = self._transform_text(doc, arg1, arg2)

        if num_sents == -1:
            return None

        return doc, self.labels[i], num_sents, num_words

    def __len__(self):
        return self.dataset_size

    def bert_collate_fn(self, batch):
        batch = filter(lambda x: x is not None, batch)
        docs, labels, doc_lengths, sent_lengths = list(zip(*batch))

        docs = [[self.tokenizer.convert_tokens_to_ids(sentence) for sentence in doc] for doc in docs]

        bsz = len(labels)
        batch_max_doc_length = max(doc_lengths)
        batch_max_sent_length = max([max(sl) if sl else 0 for sl in sent_lengths])

        docs_tensor = torch.zeros((bsz, batch_max_doc_length, batch_max_sent_length), dtype=torch.long)
        batch_att_mask_tensor = torch.zeros((bsz, batch_max_doc_length, batch_max_sent_length), dtype=torch.long)
        token_type_ids_tensor = torch.zeros((bsz, batch_max_doc_length, batch_max_sent_length), dtype=torch.long)
        sent_lengths_tensor = torch.zeros((bsz, batch_max_doc_length))

        for doc_idx, doc in enumerate(docs):
            padded_token_lists, att_mask_lists, tok_type_lists = self._pad_sequence_for_bert_batch(
                doc, batch_max_sent_length
            )

            doc_length = doc_lengths[doc_idx]
            sent_lengths_tensor[doc_idx, :doc_length] = torch.tensor(sent_lengths[doc_idx], dtype=torch.long)

            for sent_idx, (padded_tokens, att_masks, tok_types) in enumerate(
                    zip(padded_token_lists, att_mask_lists, tok_type_lists)):
                docs_tensor[doc_idx, sent_idx, :] = torch.tensor(padded_tokens, dtype=torch.long)
                batch_att_mask_tensor[doc_idx, sent_idx, :] = torch.tensor(att_masks, dtype=torch.long)
                token_type_ids_tensor[doc_idx, sent_idx, :] = torch.tensor(tok_types, dtype=torch.long)

        return (
            docs_tensor,
            torch.tensor(labels, dtype=torch.long),
            torch.tensor(doc_lengths, dtype=torch.long),
            sent_lengths_tensor,
            dict(attention_masks=batch_att_mask_tensor, token_type_ids=token_type_ids_tensor),
        )
        
def get_arg_list_from_spans(arg1_span, arg2_span, text):
    arg1_ranges_str = arg1_span.split(";")
    arg2_ranges_str = arg2_span.split(";")
    arg1_ranges = []
    for argrange in arg1_ranges_str:
        if argrange != "":
            arg1_ranges.append(argrange.split(".."))

    arg2_ranges = []
    for argrange in arg2_ranges_str:
        if argrange!= "":
            arg2_ranges.append(argrange.split(".."))

    arg1_list = []
    for argrange in arg1_ranges:
        beginning = int(argrange[0])
        end = int(argrange[1])
        arg1_list.append(text[beginning:end])

    arg2_list = []
    for argrange in arg2_ranges:
        beginning = int(argrange[0])
        end = int(argrange[1])
        arg2_list.append(text[beginning:end])

    return arg1_list, arg2_list