from utils import common_member
from checker import match_nsw, only_alpha, is_nsw
from config import ABB_DICT, EN2VI_DICT,\
    NTIM_regex, NDAT_regex, NDAY_regex, NMON_regex, NFRC_regex, NTEL_regex,\
    NRNG_regex, NPER_regex, NADD_regex, NDIG_regex, NNUM_regex, MONY_regex, CSEQ_regex,\
    email_regex, url_regex, keep_punc_regex, speakable_punc_regex, remove_punc_regex,\
    NDAY_contexts_before, NDAT_contexts_before, NADD_contexts_before, NFRC_contexts_before,\
    NMON_contexts_before, NRNG_contexts_before, NSCR_contexts_before,\
    NNUM_contexts_after, NNUM_contexts_before, NDIG_contexts_before


def get_context_before(ind, list_words):
    """get context before the nsw with index ind in list_words\n
    return: the list have 2 elements (2 tokens before nsw)\n
    if is not vietnamese word, the element is `None`)
    """
    len_context = 2
    context_before = [None] * len_context

    i = 1

    while i <= len_context and ind - i >= 0:
        token = list_words[ind - i].lower()
        # if token in list_vietnamese_words:
        context_ind = len_context - i
        context_before[context_ind] = token
        i += 1

    return context_before


def get_context_after(ind, list_words):
    """get context after the nsw with index ind in list_words\n
    return: the list have 2 elements (2 tokens after nsw)\n
    if is not vietnamese word, the element is `None`)
    """
    len_context = 2
    context_after = [None] * len_context

    i = 1

    while i <= len_context and ind + i < len(list_words):
        token = list_words[ind + i].lower()
        # if token in list_vietnamese_words:
        context_ind = i - 1
        context_after[context_ind] = token
        i += 1
    return context_after


def run_clfLETTERS(tagged_dic, list_words):
    """Classify nsw of group LETTERS, return dictionary with added tag 
        LWRD, LSEQ, LABB
    tagged_dic: dictionary entry where key is index of word in origin text,
    value is tuple with the nsw and the tag (LETTERS, NUMBERS, OTHERS).

    The dictionary returned has the same entries with the tuple extended with
    a more specific number tag assigned to it by the classifier.
    """
    LETTERS_dict = {ind: (nsw, tag) for ind, (nsw, tag) in tagged_dic.items()
                    if tag == 'LETTERS'}

    out = {}

    for (ind, (nsw, tag)) in LETTERS_dict.items():
        if nsw in ABB_DICT:
            out.update({ind: (nsw, 'LETTERS', 'LABB')})
        elif nsw in EN2VI_DICT:
            out.update({ind: (nsw, 'LETTERS', 'LWRD')})
        elif str(nsw).isupper():
            out.update({ind: (nsw, 'LETTERS', 'LSEQ')})
        else:
            out.update({ind: (nsw, 'LETTERS', 'LWRD')})

    return out


def run_clfNUMBERS(tagged_dic, list_words):
    """Classify nsw of group NUMBERS, return dictionary with added tag 
        NTIM, NDAT, NDAY, NMON, NNUM, NTEL, NDIG, NSCR, NRNG, NPER, NFRC, NADD
    tagged_dic: dictionary entry where key is index of word in origin text,
    value is tuple with the nsw and the tag (LETTERS, NUMBERS, OTHERS).

    The dictionary returned has the same entries with the tuple extended with
    a more specific number tag assigned to it by the classifier.
    """
    NUMBERS_dict = {ind: (nsw, tag) for ind, (nsw, tag) in tagged_dic.items()
                    if tag == 'NUMBERS'}

    out = {}

    for (ind, (nsw, tag)) in NUMBERS_dict.items():
        if match_nsw(nsw, NTIM_regex):
            out.update({ind: (nsw, 'NUMBERS', 'NTIM')})
        elif match_nsw(nsw, NDAT_regex):
            # may be NDAT or NADD
            context_before = get_context_before(ind, list_words)
            if common_member(context_before, NDAT_contexts_before):
                out.update({ind: (nsw, 'NUMBERS', 'NDAT')})
            elif common_member(context_before, NADD_contexts_before):
                out.update({ind: (nsw, 'NUMBERS', 'NADD')})
            else:
                out.update({ind: (nsw, 'NUMBERS', 'NDAT')})

        elif match_nsw(nsw, NDAY_regex):
            # may be NDAY or NFRC or NADD
            context_before = get_context_before(ind, list_words)
            if common_member(context_before, NDAY_contexts_before):
                out.update({ind: (nsw, 'NUMBERS', 'NDAY')})
            elif common_member(context_before, NFRC_contexts_before):
                out.update({ind: (nsw, 'NUMBERS', 'NFRC')})
            elif common_member(context_before, NADD_contexts_before):
                out.update({ind: (nsw, 'NUMBERS', 'NADD')})
            else:
                out.update({ind: (nsw, 'NUMBERS', 'NDAY')})

        elif match_nsw(nsw, NMON_regex):
            # maybe NMON or NFRC or NADD
            context_before = get_context_before(ind, list_words)
            if common_member(context_before, NMON_contexts_before):
                out.update({ind: (nsw, 'NUMBERS', 'NMON')})
            elif common_member(context_before, NFRC_contexts_before):
                out.update({ind: (nsw, 'NUMBERS', 'NFRC')})
            elif common_member(context_before, NADD_contexts_before):
                out.update({ind: (nsw, 'NUMBERS', 'NADD')})
            else:
                out.update({ind: (nsw, 'NUMBERS', 'NMON')})
        elif match_nsw(nsw, NFRC_regex):
            out.update({ind: (nsw, 'NUMBERS', 'NFRC')})
        elif match_nsw(nsw, NTEL_regex):
            out.update({ind: (nsw, 'NUMBERS', 'NTEL')})
        elif match_nsw(nsw, NRNG_regex):
            # may be NRNG or NSCR
            context_before = get_context_before(ind, list_words)
            if common_member(context_before, NRNG_contexts_before):
                out.update({ind: (nsw, 'NUMBERS', 'NRNG')})
            elif common_member(context_before, NSCR_contexts_before):
                out.update({ind: (nsw, 'NUMBERS', 'NSCR')})
            else:
                out.update({ind: (nsw, 'NUMBERS', 'NRNG')})

        elif match_nsw(nsw, NPER_regex):
            out.update({ind: (nsw, 'NUMBERS', 'NPER')})
        elif match_nsw(nsw, NADD_regex):
            out.update({ind: (nsw, 'NUMBERS', 'NADD')})
        elif match_nsw(nsw, NDIG_regex):
            # may be NDIG or NNUM
            context_before = get_context_before(ind, list_words)
            context_after = get_context_after(ind, list_words)
            if len(nsw) > 20:
                out.update({ind: (nsw, 'NUMBERS', 'NDIG')})
            elif common_member(context_before, NNUM_contexts_before):
                out.update({ind: (nsw, 'NUMBERS', 'NNUM')})
            elif common_member(context_after, NNUM_contexts_after):
                out.update({ind: (nsw, 'NUMBERS', 'NNUM')})
            elif common_member(context_before, NDIG_contexts_before):
                out.update({ind: (nsw, 'NUMBERS', 'NDIG')})
            else:
                out.update({ind: (nsw, 'NUMBERS', 'NNUM')})

        elif match_nsw(nsw, NNUM_regex):
            out.update({ind: (nsw, 'NUMBERS', 'NNUM')})

        elif match_nsw(nsw, MONY_regex):
            out.update({ind: (nsw, 'OTHERS', 'MONY')})
        elif match_nsw(nsw, CSEQ_regex):
            out.update({ind: (nsw, 'OTHERS', 'CSEQ')})
        else:
            out.update({ind: (nsw, 'OTHERS', 'NONE')})
    return out


def run_clfOTHERS(tagged_dic, list_words):
    """Classify nsw of group OTHERS, return dictionary with added tag
            URLE, PUNC, CSEQ, MONY, NONE
        tagged_dic: dictionary entry where key is index of word in origin text,
        value is tuple with the nsw and the tag (LETTERS, NUMBERS, OTHERS).

        The dictionary returned has the same entries with the tuple extended with
        a more specific number tag assigned to it by the classifier.
    """
    OTHERS_dict = {ind: (nsw, tag) for ind, (nsw, tag) in tagged_dic.items()
                   if tag == 'OTHERS'}

    out = {}

    for (ind, (nsw, tag)) in OTHERS_dict.items():
        if match_nsw(nsw, email_regex) or match_nsw(nsw, url_regex):
            out.update({ind: (nsw, 'OTHERS', 'URLE')})
        elif match_nsw(nsw, keep_punc_regex):
            out.update({ind: (nsw, 'OTHERS', 'DURA')})
        elif match_nsw(nsw, remove_punc_regex):
            out.update({ind: (nsw, 'OTHERS', 'NONE')})
        elif match_nsw(nsw, speakable_punc_regex):
            context_before = get_context_before(ind, list_words)
            context_after = get_context_after(ind, list_words)
            if only_alpha(context_before[-1]) and only_alpha(context_after[0])\
                and nsw in ['-', '–', '_'] and not is_nsw(context_after[-1]):
                out.update({ind: (nsw, 'OTHERS', 'NONE')})
            else:
                out.update({ind: (nsw, 'OTHERS', 'PUNC')})
        elif match_nsw(nsw, MONY_regex):
            out.update({ind: (nsw, 'OTHERS', 'MONY')})
        elif match_nsw(nsw, CSEQ_regex):
            out.update({ind: (nsw, 'OTHERS', 'CSEQ')})
        else:
            out.update({ind: (nsw, 'OTHERS', 'NONE')})

    return out


def classify(tagged_dic, list_tokens):
    """Classify nsw, return a dictionary with tag (is class of nsw)
            LWRD, LSEQ, LABB, NTIM, NDAT, NDAY, NMON, NNUM, NTEL, NDIG, NSCR, NRNG, NPER, NFRC, NADD,
            URLE, PUNC, DURA, CSEQ, MONY, NONE
        tagged_dic: dictionary entry where key is index of word in origin text,
        value is tuple with the nsw and the tag (LETTERS, NUMBERS, OTHERS).

        The dictionary returned has the same entries with the tuple extended with
        a more specific number tag assigned to it by the classifier.
    """
    result = {}

    out = run_clfLETTERS(tagged_dic, list_tokens)
    result.update(out)

    out = run_clfNUMBERS(tagged_dic, list_tokens)
    result.update(out)

    out = run_clfOTHERS(tagged_dic, list_tokens)
    result.update(out)

    return result
