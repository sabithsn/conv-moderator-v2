import sys
import praw
import timeit

# auth
reddit = praw.Reddit(
    client_id="oYQthMoMvL2ERdGzAYPIlQ",
    client_secret="V0Gub34VCxchLp6ZxujTd38hReEPew",
    user_agent="SH8",
    username = "paper_band",
)


if __name__ == '__main__':

    subreddits = ["arabs", "egypt", "saudiarabia", "russian", "russia", "AskARussian", "French", "france", "mangafr"]
    # subreddits = ["AmITheAsshole", "Conservative", "FemaleDatingStrategy", "PoliticalCompassMemes"]
    with open ("../scraping/data/reddit/info-other-langs.tsv", "w") as g:
        for subname in subreddits:
            start = timeit.default_timer()


            print ("DOING SUB: ", subname)
            print ("#############################################################")
            
            # read file corresponding to the sub
            filename = "../scraping/data/reddit/other_lang_stream/" + subname + ".tsv"
            all_lines = []
            c_ids = []
            c_dict = {}
            with open (filename, "r", encoding = "utf-8") as f:
                for line in f:
                    all_lines.append(line)
                    row = line.strip().split("\t")
                    c_id = "t1_" + row[3]
                    c_dict[row[3]] = line
                    c_ids.append(c_id)



            deleted_count = 0
            removed_count = 0
            all_count = 0
            with open ("../scraping/data/reddit/deleted_comments_other_langs/" + subname + ".tsv", "w", encoding = "utf-8") as del_f:
                with open ("../scraping/data/reddit/removed_comments_other_langs/" + subname + ".tsv", "w", encoding = "utf-8") as rem_f:
                    with open ("../scraping/data/reddit/existing_comments_other_langs/" + subname + ".tsv", "w", encoding = "utf-8") as existing_f:

                        # write headers
                        g.write("subname\tall\tdeleted\tremoved\n")
                        row = ["author", "body", "created_at", "c_id", "s_id", "p_id", "permalink"]
                        line = "\t".join(row) + "\n"
                        del_f.write(line)
                        rem_f.write(line)
                        existing_f.write(line)

                        # check every comment on reddit
                        for comment in reddit.info(c_ids):
                            all_count += 1
                            if all_count % 2000 == 0:
                                print ("checked so far, ", all_count)
                                print ("deleted so far, ", deleted_count)
                                print ("removed so far, ", removed_count)
                            body = comment.body.replace("\n", " ").replace("\r", " ").replace("\t", " ")

                            if "[deleted]" in body:
                                line = c_dict[comment.id]

                                if (len (comment.mod_reports) > 0):
                                    print ("MOD REPORT:", comment.mod_reports)
                                    line = line + "\t" + " ##MOD## " + "*$*".join(comment.mod_reports)
                                if (len (comment.user_reports) > 0):
                                    print ("USER REPORT:", comment.user_reports)
                                    line = line + "\t" + " ##USER## " + "*$*".join(comment.user_reports)
                                    
                                try:
                                    del_f.write(line)
                                    deleted_count += 1
                                    # print ("deleted so far", deleted_count)
                                except:
                                    continue

                            elif "[removed]" in body:
                                line = c_dict[comment.id]

                                if (len (comment.mod_reports) > 0):
                                    print ("MOD REPORT:", comment.mod_reports)
                                    line = line + "\t" + " ##MOD## " + "*$*".join(comment.mod_reports)
                                if (len (comment.user_reports) > 0):
                                    print ("USER REPORT:", comment.user_reports)
                                    line = line + "\t" + " ##USER## " + "*$*".join(comment.user_reports)
                                
                                try:
                                    rem_f.write(line)
                                    removed_count += 1
                                    # print ("removed so far", removed_count)
                                except:
                                    continue

                            else:
                                try:
                                    line = c_dict[comment.id]
                                    existing_f.write(line)
                                except:
                                    continue

                        print ("SUB: ", subname)
                        print ("deleted: ", deleted_count)
                        print ("removed: ", removed_count)
                        print ("all: ", all_count)

                        g.write(subname + "\t" + str(all_count) + "\t" + str(deleted_count) + "\t" + str(removed_count) + "\n")

                        stop = timeit.default_timer()
                        print('Time: ', stop - start)

                        print ("*********************************************************") 



