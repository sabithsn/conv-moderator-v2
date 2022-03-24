# segment EDUs
python3 run_segbot.py

# generate XML files using Stanford parser
/usr/bin/java -mx2g -cp "/home/kaa1391/stanford-corenlp-4.1.0/*" edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse -filelist ../file_list_children.txt -outputDirectory ../../annotations/data/comments -outputExtension '.xml' -outputFormat 'xml'

# preprocess data
python3 preprocess.py --data_dir ../../annotations/data/comments --corenlp_dir ../../../stanford-corenlp-4.1.0/