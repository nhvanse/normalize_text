import pronouncing
import re
import os.path
import time
from tqdm import tqdm

from .utils import load_dict

CURDIR = os.path.dirname(__file__)

POPULAR_EN2VI_DICT_PATH = os.path.join(CURDIR,  'dicts/popular_english_words.txt')
CMUPHONE2VI_DICT_PATH = os.path.join(CURDIR,  'dicts/cmu_phones.txt')
EN2VI_DICT_PATH = os.path.join(CURDIR,  'dicts/EN2VI_DICT.txt')
BRANCH_DICT_PATH = os.path.join(CURDIR,  'dicts/proper_name/BRANCH_DICT.txt')
PERSON_DICT_PATH = os.path.join(CURDIR,  'dicts/proper_name/PERSON_DICT.txt')


cmuphone2vi_dict = load_dict(CMUPHONE2VI_DICT_PATH)
popular_en2vi_dict = load_dict(POPULAR_EN2VI_DICT_PATH)
popular_branch_dict = load_dict(BRANCH_DICT_PATH)
popular_person_dict = load_dict(PERSON_DICT_PATH)

popular_en2vi_dict.update(popular_branch_dict)
popular_en2vi_dict.update(popular_person_dict)

list_enwords = pronouncing.cmudict.words()
list_enwords.extend(popular_en2vi_dict.keys())


def convert_by_rules(en_pronounce):
    """
        Chuyển theo luật phiên âm tiếng Anh từ CMU dictionary sang phiên âm tiếng Việt
    """
    list_en_phonemes = en_pronounce.split()
    for i, en_phone in enumerate(list_en_phonemes):
        # remove the digit
        if en_phone[-1].isdigit():
            list_en_phonemes[i] = en_phone[:-1]

    list_vi_phonemes = [cmuphone2vi_dict[en_phone]
                        for en_phone in list_en_phonemes]

    temp = ''.join(list_vi_phonemes)

    phones1 = 'ai|ao|ây|oi|âu'
    phones2 = 'p|c|t|ch|n|ng|m|ph|b|d|đ|g|h|x|s|th|v|gu|l|r'
    phones3 = 'a|ă|e|i|o|ơ|ô|u'
    phones4 = 'ai|ao|ây|oi|âu|a|ă|e|i|o|ơ|ô|u'

    #  tách
    temp = re.sub(r'(?P<id>{})'.format(phones1),
                  lambda x: x.group('id') + " ", temp)

    temp = re.sub(r'(?P<id>{})(?P<id1>{})'.format(phones4, phones4),
                  lambda x: x.group('id') + " " + x.group('id1'), temp)
    temp = re.sub(r'(?P<id>{})(?P<id1>{})'.format(phones4, phones4),
                  lambda x: x.group('id') + " " + x.group('id1'), temp)

    temp = re.sub(r'(?P<id>{})(?P<id1>{})(?P<id2>{})'.format(phones4, phones2, phones4),
                  lambda x: x.group('id') + " " + x.group('id1') + x.group('id2'), temp)
    temp = re.sub(r'(?P<id>{})(?P<id1>{})(?P<id2>{})'.format(phones4, phones2, phones4),
                  lambda x: x.group('id') + " " + x.group('id1') + x.group('id2'), temp)

    temp = re.sub(r'(?P<id>{})(?P<id1>{})(?P<id2>{})'.format(phones3, phones2, phones2),
                  lambda x: x.group('id') + x.group('id1') + " " + x.group('id2'), temp)

    temp = re.sub(r'(?P<id>{})(?P<id1>{})'.format(phones2, phones2),
                  lambda x: x.group('id') + " " + x.group('id1'), temp)
    temp = re.sub(r'(?P<id>{})(?P<id1>{})'.format(phones2, phones2),
                  lambda x: x.group('id') + " " + x.group('id1'), temp)

    # ghép âm
    temp = re.sub(r'(?P<id>a i|o i|i a|u ơ|i u|a o)', lambda x: x.group(
        'id')[0] + x.group('id')[2:] + ' ', temp)
    temp = re.sub(r'(?P<id>n g|c h|p h|t h|t r)',
                  lambda x: x.group('id')[:1] + x.group('id')[2:], temp)

    # tach phần lỗi khi ghép
    temp = re.sub(r'(?P<id>{})(?P<id1>{})'.format(phones1, phones4),
                  lambda x: x.group('id') + " " + x.group('id1'), temp)

    # thay đổi âm cuối của từ
    temp = re.sub(r'(?P<id>{})(?P<id1>{})'.format(
        phones4, 'đ|x|s|th'), lambda x: x.group('id')+'t', temp)
    temp = re.sub(r'(?P<id>{})(?P<id1>{})'.format(
        phones4, 'ph|b|v'), lambda x: x.group('id')+'p', temp)
    temp = re.sub(r'(?P<id>{})(?P<id1>{})'.format(
        phones4, 'd|h'), lambda x: x.group('id'), temp)
    temp = re.sub(r'(?P<id>{})(?P<id1>{})'.format(
        phones4, 'g|c|ch'), lambda x: x.group('id')+'c', temp)

    # chỉnh sửa phát âm
    temp = re.sub(r'ơ (?P<id>{})'.format(phones4),
                  lambda x: 'ơ r' + x.group('id'), temp)
    temp = re.sub(r'ơl'.format(phones2), lambda x: 'ồ', temp)

    temp = re.sub(r'gu (?P<id>{})'.format(phones4),
                  lambda x: 'gu' + x.group('id'), temp)

    temp = re.sub(r'^ơn ', lambda x: 'ăn ', temp)
    temp = re.sub(r'(?P<id>{})ơn'.format(phones2),
                  lambda x: x.group('id')+'ừn', temp)
    temp = re.sub(r'âu l |âu n ', lambda x: 'ôn ', temp)

    temp = re.sub(r'gu i l', lambda x: 'guiu l', temp)
    temp = re.sub(r'gu il', lambda x: 'guiu', temp)
    temp = re.sub(r'gu i', lambda x: 'gui', temp)
    temp = re.sub(r'gui', lambda x: 'guy', temp)
    temp = re.sub(r'guyl', lambda x: 'guiu', temp)
    temp = re.sub(r'guu ', lambda x: 'gu ', temp)
    temp = re.sub(r'guơ (?P<id>{}) '.format('m|n'),
                  lambda x: 'guơ'+x.group('id')+' ', temp)

    temp = re.sub(r'tai  m |tai  m$', lambda x: 'tham ', temp)

    temp = re.sub(r'ây (?P<id>{}) '.format('t|m|n'),
                  lambda x: 'ê'+x.group('id') + " ", temp)
    temp = re.sub(r'ây (?P<id>{})$'.format('t|m|n'),
                  lambda x: 'ê'+x.group('id'), temp)
    temp = re.sub(r'ây (?P<id>{})(?P<id1>{})'.format('t|m|n', phones4),
                  lambda x: 'ê'+x.group('id') + " "+x.group('id')+x.group('id1'), temp)
    temp = re.sub(r'c(?P<id>{})'.format('i|ê'),
                  lambda x: 'k'+x.group('id'), temp)
    temp = re.sub(r'êt', lambda x: 'ết', temp)

    temp = re.sub(r'p rơ', lambda x: 'p rô', temp)
    temp = re.sub(r'ao  n', lambda x: 'ao', temp)
    temp = re.sub(r'đơc', lambda x: 'đắc', temp)
    temp = re.sub(r'^ơ n', lambda x: 'ăn ', temp)
    temp = re.sub(r'gu ut|guut', lambda x: 'gút', temp)
    temp = re.sub(r'gu ul|guul', lambda x: 'gun', temp)
    temp = re.sub(r' c gu|^c gu', lambda x: ' qu', temp)
    temp = re.sub(r'ây ng', lambda x: 'ên', temp)

    # âm i ơ thành âm iu
    temp = re.sub(r'(?P<id>{})i ơ '.format(phones2),
                  lambda x: x.group('id') + 'iu ', temp)

    temp = re.sub(r'(?P<id>{})r t '.format(phones3),
                  lambda x: x.group('id')+'t', temp)
    temp = re.sub(r'(?P<id>{})r t$'.format(phones3),
                  lambda x: x.group('id')+'t', temp)
    temp = re.sub(r'(?P<id>{})r'.format(phones3),
                  lambda x: x.group('id'), temp)

    temp = re.sub(r'(?P<id>{})l'.format('i'),
                  lambda x: x.group('id')+'u', temp)
    temp = re.sub(r'(?P<id>{})l'.format('e'),
                  lambda x: x.group('id')+'o', temp)
    temp = re.sub(r'(?P<id>{})l'.format('u|a|o'),
                  lambda x: x.group('id')+'n', temp)

    temp = re.sub(r'(?P<id>{})c l'.format(phones3),
                  lambda x: x.group('id')+'c cồ l', temp)
    temp = re.sub(r'(?P<id>{})p l'.format(phones3),
                  lambda x: x.group('id')+' pồ l', temp)

    temp = re.sub(r'^no n'.format(phones3), lambda x: 'non ', temp)

    # loại bỏ một số âm cuối
    temp = re.sub(r' (?P<id>{})$'.format(phones2), lambda x: '', temp)
    temp = re.sub(r' (?P<id>{})$'.format(phones2), lambda x: '', temp)

    # thêm ờ cho phụ âm đứng riêng
    temp = re.sub(r'^(?P<id>{}) '.format(phones2),
                  lambda x: x.group('id')+'ờ ', temp)
    temp = re.sub(r' (?P<id>{}) '.format(phones2),
                  lambda x: ' ' + x.group('id')+'ờ ', temp)
    temp = re.sub(r' (?P<id>{}) '.format(phones2),
                  lambda x: ' ' + x.group('id')+'ờ ', temp)

    # thêm dấu
    add_prosodic_dict = {
        'at':'át', 'ăt':'ắt', 'ât':'ất', 'et':'ét', 'êt':'ết', 'it':'ít', 'ot':'ót', 'ôt':'ốt', 'ơt':'ớt', 'ut':'út', 'ưt':'ứt', 'yt':'ýt',
        'ac':'ác', 'ăc':'ắc', 'âc':'ấc', 'ec':'éc', 'êc':'ếc', 'ic':'íc', 'oc':'óc', 'ôc':'ốc', 'ơc':'ớc', 'uc':'úc', 'ưc':'ức', 'yc':'ýc',
        'ap':'áp', 'ăp':'ắp', 'âp':'ấp', 'ep':'ép', 'êp':'ếp', 'ip':'íp', 'op':'óp', 'ôp':'ốp', 'ơp':'ớp', 'up':'úp', 'ưp':'ứp', 'yp':'ýp',
        
    }
    temp = re.sub(r'(?P<id>{})'.format('|'.join(add_prosodic_dict.keys())), lambda x: add_prosodic_dict[x.group('id')], temp)

    return temp


def en2vi(en_word):
    """ 
        Chuyển 1 từ tiếng Anh sang cách đọc tiếng Việt
    """
    result = ''
    try:
        if en_word in popular_en2vi_dict:
            result = popular_en2vi_dict[en_word]
        else:
            en_pronounce = pronouncing.phones_for_word(en_word)
            # 1 từ tiếng anh có thể có >= 1 cách phát âm
            # ta dùng cách phát âm đầu tiên
            en_pronounce = en_pronounce[0]
            result = convert_by_rules(en_pronounce)
    except:
        result = None

    return result



"""Tạo từ điển phiên âm tiếng Việt cho các từ tiếng Anh"""
t0 = time.time()

with open(EN2VI_DICT_PATH, 'w') as f:
    for enword in tqdm(list_enwords):
        viword = en2vi(enword)
        if viword:
            # khác None thì ghi vào file
            f.write("{}|{}\n".format(enword, viword))

print("Time: {} s".format(time.time()-t0))
