# encoding: utf-8
from checker import is_nsw, is_email, is_url, only_alpha, \
    has_alpha, has_digit, is_digit_based, has_punc


def create_NSWs_dict(list_token):
    "Create dictionary of NSWs in list_token: keys are indices, values NSWs"
    NSWs_dict = {i: list_token[i] for i in range(
        len(list_token)) if is_nsw(list_token[i])}
    return NSWs_dict


def tagify(NSWs_dict):
    """Return dictionary with added tag. <NUMBERS, LETTERS, OTHERS>\n
    NSWs_dic: dictionary entry where key is index of word in origin text, value
         is the nsw
    The dictionary returned has the same keys with the values being a tuple
    with nsw and its assigned tag.
    """
    out = {}
    for ind, nsw in NSWs_dict.items():
        if is_url(nsw) or is_email(nsw):
            # group OTHERS
            out.update({ind: (nsw, 'OTHERS')})
        elif is_digit_based(nsw):
            # group NUMBERS
            out.update({ind: (nsw, 'NUMBERS')})
        elif only_alpha(nsw):
            # group LETTERS
            out.update({ind: (nsw, 'LETTERS')})
        elif has_alpha(nsw) and (has_digit(nsw) or has_punc(nsw)):
            # group SPLITS
            out.update({ind: (nsw, 'SPLITS')})
        else:
            # group OTHERS
            out.update({ind: (nsw, 'OTHERS')})

    return out
