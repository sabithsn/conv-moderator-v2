import argparse
import json
import os
import requests

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(keywords, language, delete):
    # You can adjust the rules if needed
    or_sep = " OR "
    print(keywords)
    print(language)
    rule = "(" + (or_sep.join(keywords)) + ")" + " lang:" + language
    print(rule)
    sample_rules = [
        {"value": rule}, #, "tag": "dog pictures"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(set, outfile):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            with open(outfile, "a+") as f:
                json_response = json.loads(response_line)
                f.write(json.dumps(json_response, indent=4, sort_keys=True))


def main():
    # parse commandline arguments
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--search_terms_file', type=str,
                        help='path of file with search terms')
    parser.add_argument('--language', type=str,
                        help='language to stream tweets for')
    parser.add_argument('--outfile', type=str,
                        help='file to write stream data to')
    args = parser.parse_args()

    # get keywords from text file
    search_keywords = []
    with open(args.search_terms_file) as f:
        search_keywords = f.readlines()
    search_keywords = [x.strip() for x in search_keywords]
    print(search_keywords)

    # stream tweets
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(search_keywords, args.language, delete)
    get_stream(set, args.outfile)


if __name__ == "__main__":
    main()