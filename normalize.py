# encoding: utf-8
from spliter import split_tokens
from tagger import create_NSWs_dict, tagify
from classifier import classify
from expander import expand

def replace_nsw(expanded_dic, list_tokens):
    """Get expanded_dic of NSWs and list_tokens\n
        expanded_dic: a dictionary with keys are indices of nsw in list_tokens,
        value are tuples contain (nsw,tag, class, fulltext) of nsw
    Return: Normalized text with NSWs is replaced by its fulltext
    """
    for ind, (nsw, tag, class_, fulltext) in expanded_dic.items():
        list_tokens[ind] = fulltext
    list_words = ' '.join(list_tokens).split()
    normalized_text =  ' '.join(list_words).lower()


def normalise(text):
    list_tokens = split_tokens(text)
    NSWs_dict = create_NSWs_dict(list_tokens)
    tagged_dic = tagify(NSWs_dict)
    classified_dic = classify(tagged_dic, list_tokens)
    expanded_dic = expand(classified_dic, list_tokens)
    normalized_text = replace_nsw(expanded_dic, list_tokens)
    return normalized_text

# text = open('./vidu.txt').read()
# print(normalise(text))