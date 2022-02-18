if __name__ == '__main__':

    # subreddits = ["antifeminists", "AskReddit", "MensRights", "unpopularopinion", "ChangeMyView", "AmITheAsshole", "Conservative", "FemaleDatingStrategy", "PoliticalCompassMemes"]
    # subreddits = subreddits + ["offmychest", "askscience", "AskHistorians", "explainlikeimfive", "politics", "PoliticalHumor", "conspiracy", "socialism", "Anarcho_Capitalism"]
    subreddits = ["Conservative", "ChangeMyView"]



    for subname in subreddits:
        print (subname)
        existing_lines = []
        deleted_lines = []
        removed_lines = []
        with open ("../scraping/data/reddit/deleted_comments/" + subname + ".tsv", "r", encoding = "utf-8") as del_f:
            with open ("../scraping/data/reddit/removed_comments/" + subname + ".tsv", "r", encoding = "utf-8") as rem_f:
                with open ("../scraping/data/reddit/existing_comments/" + subname + ".tsv", "r", encoding = "utf-8") as existing_f:

                    for line in del_f:
                        if line not in deleted_lines:
                            deleted_lines.append(line)
                    for line in rem_f:
                        if line not in removed_lines:
                            removed_lines.append(line)
                    for line in existing_f:
                        if line not in existing_lines:
                            existing_lines.append(line)               

        with open ("../scraping/data/reddit/deleted_comments/" + subname + ".tsv", "w", encoding = "utf-8") as del_f:
            with open ("../scraping/data/reddit/removed_comments/" + subname + ".tsv", "w", encoding = "utf-8") as rem_f:
                with open ("../scraping/data/reddit/existing_comments/" + subname + ".tsv", "w", encoding = "utf-8") as existing_f:

                    for line in deleted_lines:
                        del_f.write(line)
                    for line in removed_lines:
                        rem_f.write(line)
                    for line in existing_lines:
                        existing_f.write(line)
