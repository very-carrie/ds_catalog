import yaml
import pandas as pd
import Levenshtein
from datetime import datetime as dt
import random
import numpy as np


def retrieve_entry_by_id(entry_id):
    stream = open("catalog.yaml", 'r')
    dictionary = yaml.safe_load(stream)
    this_entry = dictionary[entry_id]
    print("title: ", this_entry["title"])
    print("link: ", this_entry["link"])
    print("summary: ", this_entry["summary"])
    print("content type: ", this_entry["content_type"])
    print("keywords: ", this_entry["keywords"])
    print("lanid: ", this_entry["lanid"])
    print("timestamp: ", this_entry["timestamp"])


def retrieve_entry_by_title(title):
    pass


def list_keywords():
    keyword_list = []
    for entry_id, entry_info in dictionary.items():
        for entry_keywords in entry_info["keywords"]:
            keyword_list.append(entry_keywords)
    df = pd.Series(keyword_list)
    # print(df.value_counts())
    return df


def entries_by_keyword(keyword):
    for entry_id, entry_info in dictionary.items():
        if keyword in entry_info["keywords"]:
            retrieve_entry_by_id(entry_id)


# TODO: this only handles keywords that don't have internal spaces
# TODO: be cautious of case
# TODO: if keywords is empty [] request keywords?
def suggest_additional_keywords(new_title, new_summary, new_keywords):
    existing_keywords = list_keywords().unique().tolist()
    words = new_title.split() + new_summary.split()
    suggested_keywords = []
    for word in words:
        word = word.lower()
        if (word in existing_keywords) and (word not in new_keywords):
            suggested_keywords.append(word)
    if suggested_keywords == []:
        return False
    else:
        print("You might be interested in adding the following keywords: ", suggested_keywords)
        return True


# TODO: what if I want to reject the first suggestion but see the rest of them?
def spell_check_keywords(new_keywords):
    existing_keywords = list_keywords().unique().tolist()
    made_suggestion = False
    for new_word in new_keywords:
        for existing_word in existing_keywords:
            d = Levenshtein.distance(new_word, existing_word)
            if (d <= 3) and (d > 0):
                made_suggestion = True
                print("You wrote ", new_word, ", did you mean ", existing_word, "?")
    if made_suggestion:
        return True
    else:
        return False


# TODO: be careful about the case of the keywords
def add_new_entry(new_title, new_link, new_content_type, new_keywords, new_summary, new_lanid,
                  suggest_keywords=True, spell_checker=True):
    now = dt.now()
    entry_id = "entry_" + now.strftime('%Y%m%d%H%M%S%f')
    new_yaml_data_dict = {entry_id: {"title": new_title, "link": new_link, "content_type": new_content_type,
                                     "keywords": new_keywords, "summary": new_summary, "lanid": new_lanid,
                                     "timestamp": now.strftime("%Y/%m/%d %H:%M:%S")}}
    if suggest_keywords:
        made_suggestions = suggest_additional_keywords(new_title, new_summary, new_keywords)
        if made_suggestions:
            print("If you are not interested in these suggestions, add the arg suggest_keywords=False")
            return
    if spell_checker:
        made_suggestions = spell_check_keywords(new_keywords)
        if made_suggestions:
            print("To turn off the spell checker, add the arg spell_checker=False")
            return
    with open('catalog.yaml', 'r') as yamlfile:
        my_yaml = yaml.safe_load(yamlfile)  # Note the safe_load
        my_yaml.update(new_yaml_data_dict)
    if my_yaml:
        with open('catalog.yaml', 'w') as yamlfile:
            yaml.safe_dump(my_yaml, yamlfile)


# TODO: might not be necessary to re-open catalog.yaml
def delete_entry(entry_id, positive=False):
    with open('catalog.yaml', 'r') as yamlfile:
        my_yaml = yaml.safe_load(yamlfile)  # Note the safe_load
        if positive == False:
            print('Are you positive you want to delete this entry?  If yes, add the arg "positive=True"')
        else:
            del my_yaml[entry_id]
    if my_yaml:
        with open('catalog.yaml', 'w') as yamlfile:
            yaml.safe_dump(my_yaml, yamlfile)


def browse_stacks(number_of_titles):
    # return number_of_titles of titles with entry numbers for later searching
    stream = open("catalog.yaml", 'r')
    dictionary = yaml.safe_load(stream)
    length_of_catalog = len(dictionary)
    titles = np.arange(length_of_catalog)
    random.shuffle(titles)
    key_list = list(dictionary.keys())
    #print(key_list[0])
    for title in titles[:min(number_of_titles, length_of_catalog)]:
        print(dictionary[key_list[title]]["title"])


if __name__ == '__main__':
    stream = open("catalog.yaml", 'r')
    dictionary = yaml.safe_load(stream)
    spell_check_keywords(["Levenstein distance", "gitt"])
    # print(dictionary)
    # retrieve_entry_by_id("entry0001")
    # keywords_list = list_keywords()
    # print(keywords_list.value_counts())
    # retrieve_entry("entry0001")
    # entries_by_keyword("git")
    # add_new_entry("test title", "test_link", ["test_content_type"], ["nummpy",
    #               "test_keyword2"], "test_summary", "cmmx")
    # add_new_entry("Visual Guide to Numpy",
    #               "https://medium.com/better-programming/numpy-illustrated-the-visual-guide-to-numpy-3b1d4976de1d",
    #               ["article"], ["numpy", "tutorial"], "visual guide to numpy", "lwmg")
    # delete_entry("entry0006")
    # delete_entry("entry0006", positive=True)
    # suggest_additional_keywords("a git title", "new numpy summary", ["numpy"])
    browse_stacks(10)

# fix add_new_entry()
# timestamps
# pge_author
# check if the link or title is already in the library
# provide summary lists of content_type, lanid, and pge_author
# Fix part of an existing entry?  Like adding keywords, capitalizing title words, etc
# Spell checker using Levenshtein distance: https://towardsdatascience.com/calculating-string-similarity-in-python-276e18a7d33a (spell_checker = False if you want your version)
# Cosine distance for title search
# Keyword suggestions from summary and title and nearness to other keywords (keyword_suggestions = True. Again can use string similarity)
# Summary length checker (thorough_summary = False)
# Sam error handling
# Tag for published by pge so JP can track thought leadership
