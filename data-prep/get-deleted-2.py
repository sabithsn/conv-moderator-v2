import sys
import praw
import timeit

# auth
reddit = praw.Reddit(
    client_id="nIPvIISM35QMMygjPVhPzw",
    client_secret="vLPYCQMVskhu9zTDT0xn6-j86uf5Hw",
    user_agent="SH4",
    username = "paper_scraper",
    password = "Darpa2021"
)


if __name__ == '__main__':

    # subreddits = ["offmychest", "askscience", "AskHistorians", "explainlikeimfive", "politics", "PoliticalHumor", "conspiracy", "socialism", "Anarcho_Capitalism"]
    # subreddits = ["AmITheAsshole", "Conservative", "FemaleDatingStrategy", "PoliticalCompassMemes"]
    subreddits = ["Conservative", "ChangeMyView"]

    with open ("../scraping/data/reddit/info.tsv", "a") as g:
        for subname in subreddits:
            start = timeit.default_timer()


            print ("DOING SUB: ", subname)
            print ("#############################################################")
            
            # read file corresponding to the sub
            filename = "../scraping/data/reddit/comment_stream3/" + subname + ".tsv"
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
            with open ("../scraping/data/reddit/deleted_comments/" + subname + ".tsv", "a", encoding = "utf-8") as del_f:
                with open ("../scraping/data/reddit/removed_comments/" + subname + ".tsv", "a", encoding = "utf-8") as rem_f:
                    with open ("../scraping/data/reddit/existing_comments/" + subname + ".tsv", "a", encoding = "utf-8") as existing_f:

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

                                if (len (comment.mod_reports) > 0):
                                    print ("MOD REPORT:", comment.mod_reports)
                                    line = line + "\t" + " ##MOD## " + "*$*".join(comment.mod_reports)
                                if (len (comment.user_reports) > 0):
                                    print ("USER REPORT:", comment.user_reports)
                                    line = line + "\t" + " ##USER## " + "*$*".join(comment.user_reports)

                                line = c_dict[comment.id]
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

                                # print ("MOD REPORT!!!!")
                                # print (comment.mod_reports)
                                # print ("USER REPORT!!!!")
                                # print (comment.user_reports)
                                
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



