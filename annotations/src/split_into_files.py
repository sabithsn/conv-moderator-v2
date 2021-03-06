import os
import pandas as pd


def main():
    comment_parent_pairs = pd.read_csv("../data/Comment-Parent - Pairs.csv").to_dict('records')
    for entry in comment_parent_pairs:
        comment = entry['comment']
        parent = entry['parent']
        ID = entry['ID']
        print(ID)

        with open(os.path.join('../data/comments', str(ID)), "w+") as f:
            f.write(comment)
        with open(os.path.join('../data/comments', str(ID) + '.txt'), "w+") as f:
            f.write(comment)
        if pd.isnull(parent):
            continue
        with open(os.path.join('../data/parent_comments', str(ID)), "w+") as f:
            f.write(parent)
        with open(os.path.join('../data/comments_with_parents_final', str(ID)), "w+") as f:
            if not (parent.endswith(".") or parent.endswith("?") or parent.endswith("!")):
                parent = parent + "."
            parent_as_paragraph = parent.replace("\n", "")
            child_as_paragraph = comment.replace("\n", "")
            f.write(parent_as_paragraph + "\n" + "\n" + child_as_paragraph)
        # with open(os.path.join('../data/comments_with_parents_final', str(ID) + ".edus"), "w+") as f:
        #     with open(os.path.join('../data/parent_comments', str(ID) + ".edus")) as g:
        #         parent_edus = g.read()
        #     with open(os.path.join('../data/comments', str(ID) + ".edus")) as h:
        #         child_edus = h.read()
        #     f.write(parent_edus + "\n" + child_edus)

        
    

if __name__ == "__main__":
    main()