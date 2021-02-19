import yaml
import pandas as pd
import Levenshtein


def retrieve_entry(entry_id):
    entry_instance = dictionary[entry_id].items()
    for key, value in entry_instance:
        print(key + " : " + str(value))


def list_keywords():
    keyword_list = []
    for entry_id, entry_info in dictionary.items():
        for entry_keywords in entry_info["keywords"]:
            keyword_list.append(entry_keywords)
    df = pd.Series(keyword_list)
    #print(df.value_counts())
    return df


def entries_by_keyword(keyword):
    for entry_id, entry_info in dictionary.items():
        if keyword in entry_info["keywords"]:
            retrieve_entry(entry_id)


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
        pass
    else:
        print("You might be interested in adding the following keywords: ", suggested_keywords)
        print("If you are not interested in these suggestions, add the arg suggest_keywords=False")


# TODO: what if I want to reject the first suggestion but see the rest of them?
def spell_check_keywords(new_keywords):
    existing_keywords = list_keywords().unique().tolist()
    made_suggestion = False
    for new_word in new_keywords:
        for existing_word in existing_keywords:
            d = Levenshtein.distance(new_word, existing_word)
            if (d <= 3) and (d > 0):
                made_suggestion=True
                print("You wrote ", new_word, ", did you mean ", existing_word, "?")
    if made_suggestion:
        print("To turn off the spell checker, add the arg spell_checker=False")


# TODO: be careful about the case of the keywords
def add_new_entry(new_title, new_link, new_content_type, new_keywords, new_summary, new_lanid,
                  suggest_keywords=True, spell_checker=True):
    new_yaml_data_dict = {"entry0006": {"title": new_title, "link": new_link, "content_type": new_content_type,
                           "keywords": new_keywords, "summary": new_summary, "lanid": new_lanid}}
    if suggest_keywords:
        suggest_additional_keywords(new_title, new_summary, new_keywords)
        return
    if spell_checker:
        spell_check_keywords(new_keywords)
        return
    with open('bib.yaml', 'r') as yamlfile:
        my_yaml = yaml.safe_load(yamlfile)  # Note the safe_load
        my_yaml.update(new_yaml_data_dict)
    if my_yaml:
        with open('bib.yaml', 'w') as yamlfile:
            yaml.safe_dump(my_yaml, yamlfile)


# TODO: might not be necessary to re-open bib.yaml
def delete_entry(entry_id, positive=False):
    with open('bib.yaml', 'r') as yamlfile:
        my_yaml = yaml.safe_load(yamlfile)  # Note the safe_load
        if positive == False:
            print('Are you positive you want to delete this entry?  If yes, add the arg "positive=True"')
        else:
            del my_yaml[entry_id]
    if my_yaml:
        with open('bib.yaml', 'w') as yamlfile:
            yaml.safe_dump(my_yaml, yamlfile)

def browse_stacks(number_of_titles):
    # return number_of_titles of titles with entry numbers for later searching
    pass

if __name__ == '__main__':

    stream = open("bib.yaml", 'r')
    dictionary = yaml.safe_load(stream)
    # spell_check_keywords(["Levenstein distance", "gitt"])
    # print(dictionary)
    # retrieve_entry("entry0001")
    # list_keywords()
    # retrieve_entry("entry0001")
    # entries_by_keyword("test_keyword1")
    # add_new_entry("test title", "test_link", ["test_content_type"], ["nummpy",
    #               "test_keyword2"], "test_summary", "cmmx")

    # add_new_entry("Visual Guide to Numpy",
    #               "https://medium.com/better-programming/numpy-illustrated-the-visual-guide-to-numpy-3b1d4976de1d",
    #               ["article"], ["numpy", "tutorial"], "visual guide to numpy", "lwmg")
    # delete_entry("entry0006")
    # delete_entry("entry0006", positive=True)
    # suggest_additional_keywords("a git title", "new numpy summary", ["numpy"])


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
