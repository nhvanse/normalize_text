# encoding: utf-8
import re

from config import punc_with_number, charset, \
    punc, email_regex, url_regex, vn_words_dict


def match_nsw(nsw, regex):
    "Check if nsw match regex"
    if re.match(regex, nsw):
        return True
    else:
        return False


def is_nsw(token):
    """Return 'True' if  token is nsw"""
    return token.lower() not in vn_words_dict


def is_digit_based(nsw):
    """Return 'True' if nsw is based around digits."""
    return bool(re.match(r'^(\d|{})*\d(\d|{})*$'.format(punc_with_number, punc_with_number), nsw))


def only_alpha(nsw):
    """Return 'True' if nsw is only based on alphabetic characters."""
    return bool(re.match(r'^[{}]+$'.format(charset), nsw))


def has_alpha(nsw):
    """Return 'True' if nsw has at-least an alphabetic character."""
    return bool(re.search(r'[{}]+'.format(charset), nsw))


def has_digit(nsw):
    """Return 'True' if nsw has at-least a digit."""
    return bool(re.search(r'\d+', nsw))


def has_punc(nsw):
    """Return 'True' if nsw has at-least a punctuation."""
    return bool(re.search(r'({})+'.format(punc), nsw))


def is_url(nsw):
    """Return 'True' if nsw is url"""
    return bool(re.match(url_regex, nsw))


def is_email(nsw):
    """Return 'True' if nsw is email"""
    return bool(re.match(email_regex, nsw))

