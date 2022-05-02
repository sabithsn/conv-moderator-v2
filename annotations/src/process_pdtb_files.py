'''Fields for pipe-delimited PDTB files can be found here: https://github.com/WING-NUS/pdtb-parser'''

import csv
import os

PDTB_DIR = "../data/comments/output"
RAW_TEXT_DIR = "../data/comments"

def get_spanlists(arg1_span, arg2_span):
    '''Takes in offsets in string form and returns list of ranges in the form 
    [[range1_begin, range1_end], [range2_begin, range2_end], ...] for each argument'''
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

    return arg1_ranges, arg2_ranges

def get_senses_and_offsets(filename):
    '''Returns list of dicts containing sense types and character offsets for each
    discourse relation in the file'''
    senses_and_offsets = []
    with open(filename) as f:
        relations = csv.reader(f, delimiter="|")
        for relation in relations:
            relation_type = relation[0]
            if relation_type != "Explicit" and relation_type != "Implicit":
                continue
            discourse_sense = relation[11]
            arg1_offset = relation[22]
            arg2_offset = relation[22]
            arg1_spanlist, arg2_spanlist = get_spanlists(arg1_offset, arg2_offset)
            senses_and_offsets.append({"filename": filename,
                                       "relation_type": relation_type,
                                       "discourse_sense": discourse_sense,
                                       "arg1_spanlist": arg1_spanlist,
                                       "arg2_spanlist": arg2_spanlist
                                       })
    return senses_and_offsets


def main():
    for filename in os.listdir(PDTB_DIR):
        if not filename.endswith(".pipe"):
            continue
        senses_and_offsets = get_senses_and_offsets(os.path.join(PDTB_DIR, filename))
        print(senses_and_offsets)


if __name__ == "__main__":
    main()