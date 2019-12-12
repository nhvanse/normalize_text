# encoding: utf-8
import re
from unicodedata import normalize as nml

from checker import is_email, is_url, is_nsw, only_alpha
from config import punc, charset, not_end_of_number_punc, change_phone_dict


def split_tokens(text):
    """Split text to list_tokens by spaces.
    """
    text = nml('NFKC', text)  # đưa về chuẩn NFKC

    # thêm dấu chấm cho chỗ xuống dòng nếu chưa có
    text = re.sub(r'(\s*\n+\s*)+',
                  ' . ', text)
    text = re.sub(r'\. \. ', ' . ', text)

    list_tokens = text.split()
    for i, token in enumerate(list_tokens):
        if len(token) > 1 and is_nsw(token) and not only_alpha(token) \
                and (not is_url(token)) and (not is_email(token)):
            # tách chữ với số liền nhau, chữ với punc liền nhau
            token = re.sub(r'(?P<id>[{}]+)(?P<id1>(\d+|{}))'.format(charset, punc),
                           lambda x: x.group('id') + ' ' + x.group('id1'),
                           token)
            token = re.sub(r'(?P<id>(\d+|{}))(?P<id1>[{}]+)'.format(punc, charset),
                           lambda x: x.group('id') + ' ' + x.group('id1'),
                           token)

            # tách token chứa số kết thúc(hoặc bắt đầu) bởi một số punc như (,"...
            token = re.sub(r'(?P<id>\d)(?P<id1>{})$'.format(not_end_of_number_punc),
                           lambda x: x.group('id') + ' ' + x.group('id1'),
                           token)
            token = re.sub(r'^(?P<id>{})(?P<id1>\d)'.format(not_end_of_number_punc),
                           lambda x: x.group('id') + ' ' + x.group('id1'),
                           token)

            # tách hai punc liền nhau
            token = re.sub(r'(?P<id>{})(?P<id1>{})'.format(punc, punc),
                           lambda x: x.group('id') + ' ' + x.group('id1'),
                           token)

            # chỉnh sửa môt số âm , ví dụ òa thành oà
            token = re.sub(r'(?P<id>{})'.format('|'.join(change_phone_dict.keys())),
                           lambda x: change_phone_dict[x.group('id')], token)

            list_tokens[i] = token

    list_tokens = ' '.join(list_tokens).split()
    return list_tokens
