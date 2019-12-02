# encoding: utf-8
from time import time
import re
import unicodedata
from .expand_NSWs import *

charset = 'aáảàãạâấẩầẫậăắẳằẵặbcdđeéẻèẽẹêếểềễệfghiíỉìĩịjklmnoóỏòõọôốổồỗộơớởờỡợpqrstuúủùũụưứửừữựvwxyýỷỳỹỵzAÁẢÀÃẠÂẤẨẦẪẬĂẮẲẰẴẶBCDĐEÉẺÈẼẸÊẾỂỀỄỆFGHIÍỈÌĨỊJKLMNOÓỎÒÕỌÔỐỔỒỖỘƠỚỞỜỠỢPQRSTUÚỦÙŨỤƯỨỬỪỮỰVWXYÝỶỲỸỴZ'
email_regex = r'[a-z][a-z0-9_\.]{5,32}@[a-z0-9]{2,}(\.[a-z0-9]{2,4})+'
url_regex = r'((?:http(s)?:\/\/)|(www))[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&\'\(\)\*\+,;=.]+'
short_url = r'([\w.-]+(?:\.[\w\.-]+)+)?[\w\-\._~:/?#[\]@!\$&\'\(\)\*\+,;=.]+(\.(com|gov|vn|com|org|info|io|net|edu))+'
url_regex += '|' + short_url
punc = r'\.|\,|\…|\;|\/|\(|\)|\!|\?|\'|\"|\“|\”|\:|\-|\+|\*|\\|\_|\&|\%|\^|\[|\]|\{|\}|\=|\#|\@|\`|\~|\$'
unitlist = '|'.join(UNIT_DICT.keys())
lseq_charset = '|'.join(LSEQ_DICT)

f = open(VI_WORDS_PATH, 'r', encoding='utf-8')
list_vietnamese_words = f.read().split('\n')

classes = ['NTIM', 'NDAT', 'NDAY', 'NMON', 'NNUM', 'NTEL', 'NDIG', 'NSCR', 'NRNG', 'NPER', 'NFRC', 'NADD',
               'LWRD', 'LSEQ', 'LABB',
               'PUNC', 'URLE', 'MONY', 'CSEQ', 'DURA', 'NONE'
    ]

def split_token(text):
    """
        Tách token từ text, trả về mảng các token.
    """
    # chuyển \n thành chấm nếu cuối câu không chấm
    text = re.sub(r'\n', ' . ', text)
    text = re.sub(r'(\s*)(\.|\,|\…|\;)(\s*)\.', ' .', text)
    text = re.sub(r'(\s*)(\.|\,|\…|\;)(\s*)\.', ' .', text)

    # tách token
    list_tokens = text.split()
    for i, token in enumerate(list_tokens):
        # nếu là email hoặc url thì bỏ qua
        if re.match(email_regex, token) or re.match(url_regex, token):
            print(token)
            continue

        # tách các từ bị dính các dấu .,;/()'"
        # "đã xong.Viện" => "đã xong . Viện", "HN(Số 36)" => "HN ( Số 36)"
        split_punc = '\.|\,|\;|\/|\(|\)|\!|\?|\…|\:'
        token = re.sub(r'(?P<id>[{}])(?P<id1>{})(?P<id2>[{}])'.format(charset, split_punc, charset),
                       lambda x: x.group('id') + ' ' + x.group('id1') + ' ' + x.group('id2'), token)
        token = re.sub(r'(?P<id>[{}]|\d+)(?P<id1>{})'.format(charset, split_punc),
                       lambda x: x.group('id') + ' ' + x.group('id1'), token)
        token = re.sub(r'(?P<id>{})(?P<id1>[{}]|\d+)'.format(split_punc, charset),
                       lambda x: x.group('id') + ' ' + x.group('id1'), token)
        
        # tách các punctuation liền nhau
        token = re.sub(r'(?P<id>{})(?P<id1>{})'.format(punc, punc),
                       lambda x: x.group('id') + ' ' + x.group('id1'), token)
        token = re.sub(r'(?P<id>{})(?P<id1>{})'.format(punc, punc),
                       lambda x: x.group('id') + ' ' + x.group('id1'), token)

        list_tokens[i] = token

    text = ' '.join(list_tokens)

    
    # chuyển số  về dạng chuẩn: 1 .000.000, 1. 000.000, 1  . 000. 000 => 1.000.000
    text = re.sub(r'(?P<id>( |^|\.)\d+)(\s+\.|\.\s+|\s+\.\s+)(?P<id1>\d)',
                  lambda x: x.group('id')+'.'+x.group('id1'), text)
    text = re.sub(r'(?P<id>( |^|\.)\d+)(\s+\.|\.\s+|\s+\.\s+)(?P<id1>\d)',
                  lambda x: x.group('id')+'.'+x.group('id1'), text)
    
    # # 09 15 33 45 77 => 09.15.33.45.77, 035 164 4565 => 035.164.4565
    text = re.sub(r'(?P<id>\d+)\s+(?P<id1>\d+)( |$)',
                  lambda x: x.group('id')+'.'+x.group('id1')+' ', text)
    text = re.sub(r'(?P<id>\d+)\s+(?P<id1>\d+)( |$)',
                  lambda x: x.group('id')+'.'+x.group('id1') + ' ', text)
    
    # chuyển ngày.giờ  21 / 10 / 2019.23 : 59 => 21 / 10 / 2019 23 : 59
    text = re.sub(r'(?P<id>\d{2} \/ \d{2} \/ \d{4})\.(?P<id1>\d+ \: \d+)',
                  lambda x: x.group('id')+' '+x.group('id1'), text)


    # 2/ 3, 2 /3, 2 / 3 => 2/3

    text = re.sub(r'(?P<id>\d+)(\s+\/|\/\s+|\s+\/\s+)(?P<id1>\d+)',
                  lambda x: x.group('id')+'/'+x.group('id1'), text)
    text = re.sub(r'(?P<id>\d+)(\s+\/|\/\s+|\s+\/\s+)(?P<id1>\d+)',
                  lambda x: x.group('id')+'/'+x.group('id1'), text)
    # 2 : 30 => 2:30, 12 : 30 : 59 => 12:30:59
    text = re.sub(r'(?P<id>\d+)(\s+\:|\:\s+|\s+\:\s+)(?P<id1>\d+)',
                  lambda x: x.group('id')+':'+x.group('id1'), text)
    text = re.sub(r'(?P<id>\d+)(\s+\:|\:\s+|\s+\:\s+)(?P<id1>\d+)',
                  lambda x: x.group('id')+':'+x.group('id1'), text)
    
    # 2 , 63 => 2,63
    text = re.sub(r'(?P<id>\d+)(\s+\,|\,\s+|\s+\,\s+)(?P<id1>\d+)(?P<id2> |%|-|{})'.format('\$|S\$|SGD|VNĐ'),
                  lambda x: x.group('id')+','+x.group('id1')+x.group('id2'), text)
    
    # chuyển tiền tệ và dạng đơn vị ở cuối: $ 1000, $1000, 1000 $ => 1000$
    text = re.sub(r'(?P<id>{})\s*(?P<id1>(\d+ \. )*\d+( \, \d+)?)'.format('\$|S\$|SGD|VNĐ'),
                  lambda x: ''.join((x.group('id1') + x.group('id')).split()), text)
    text = re.sub(r'(?P<id>(\d+ \. )*\d+(\,\d+| \, \d+)?)\s*(?P<id1>{})'.format('\$|S\$|SGD|VNĐ'),
                  lambda x:  ''.join((x.group('id') +  x.group('id1')).split()), text)
    
    # loại bỏ các dấu không cần đọc
    text = re.sub(r'\(|\)|\'|\"|\[|\]|\{|\}|\“|\”|\|', ' ', text)
    # chỉnh sửa một số âm , ví dụ òa thành oà
    change_phone_dict = {'òa': 'oà', 'óa': 'oá', 'ọa': 'oạ', 'õa': 'oã', 'ỏa': 'oả',
                         'òe': 'oè', 'óe': 'oé', 'ọe': 'oẹ', 'õe': 'oẽ', 'ỏe': 'oẻ',
                         'ùy': 'uỳ', 'úy': 'uý', 'ụy': 'uỵ', 'ũy': 'uỹ', 'ủy': 'uỷ'}
    text = re.sub(r'(?P<id>{})'.format('|'.join(change_phone_dict.keys())),
                  lambda x: change_phone_dict[x.group('id')], text)

    list_tokens = text.split()

    return list_tokens



def split_compound_NSWs(list_tokens):
    for i, token in enumerate(list_tokens):
        # nếu token là NSW
        if token.lower() not in vn_words_dict:
            # nếu là email hoặc url thì bỏ qua
            if re.match(email_regex, token) or re.match(url_regex, token):
                continue

            # nếu không phải punctuation, word riêng lẻ hoặc lớp số thì phân tách
            if not re.match(r'^({}|[{}]+|\d+|((\d+({}))+\d+))$'.format(punc, charset, punc), token):
                token = re.sub(r'(?P<id>{})'.format(punc),
                               lambda x: ' ' + x.group('id') + ' ', token)
                token = re.sub(r'(?P<id>(\D\d)|(\d\D))',
                               lambda x: x.group('id')[0]+' '+x.group('id')[1], token)
                token = re.sub(r'(?P<id>(\D\d)|(\d\D))',
                               lambda x: x.group('id')[0]+' '+x.group('id')[1], token)
                token = re.sub(r'(?P<id>(\d[{}]))'.format(charset),
                               lambda x: x.group('id')[0]+' '+x.group('id')[1], token)
                
                token = ' '.join(token.split())
                list_tokens[i] = token

    return ' '.join(list_tokens)

def replace(text):
    '''Chuyển text đã tách token về dạng chuẩn hóa cho tiếng Việt'''
    # dict đếm số lần xuất hiện của các nhóm NSWs
    nswcounter = dict.fromkeys(classes, 0)

    # chuyển urle
    text, count = re.subn(r'(?P<id>{}|{})'.format(email_regex, url_regex),
                          lambda x: URLE2words(x.group('id')), text)
    nswcounter['URLE'] += count
    
    # chuyển ngày/tháng/năm
    text, count = re.subn(r'(?P<id>(^| )((0)?[1-9]|[1-2][0-9]|(3)[0-1])( |)(\/)( |)(((0)?[0-9])|((1)[0-2]))( |)(\/)( |)(\d{4}|\d{2})( |$))',
                          lambda x: ' ' + NDAT2words(''.join(x.group('id').split())) + ' ', text)
    nswcounter['NDAT'] += count
    
    # chuyển ngày/tháng
    text, count = re.subn(r'(?P<id>(^| )((0)?[1-9]|[1-2][0-9]|(3)[0-1])( |)(\/)( |)(((0)?[0-9])|((1)[0-2]))( |$))',
                          lambda x: ' ' + NDAY2words(''.join(x.group('id').split())) + ' ', text)
    nswcounter['NDAY'] += count
    
    # chuyển tháng/năm
    text, count = re.subn(r'(?P<id>(^| )(((0)?[0-9])|((1)[0-2]))( |)(\/)( |)(\d{4}|\d{2})( |$))',
                          lambda x: ' ' + NMONT2words(''.join(x.group('id').split())) + ' ', text)
    nswcounter['NMON'] += count
    
    # chuyển số kèm đơn vị
    text, count = re.subn(r'(?P<id1>{}) \/ (?P<id2>{})(?P<id3> |$)'.format(unitlist, unitlist),
                          lambda x: UNIT_DICT[x.group('id1')] + ' trên ' + UNIT_DICT[x.group('id2')]+ x.group('id3'),
                          text)
    nswcounter['LABB'] += count

    text, count = re.subn(r'(?P<id>(\d+\.)*\d+(\,\d+| \, \d+)?) (?P<id1>{})(?P<id2> |$)'.format(unitlist),
                          lambda x: NNUM2words(''.join(x.group('id').split(
                          ))) + ' ' + UNIT_DICT[x.group('id1')] + x.group('id2'),
                          text)
    nswcounter['NNUM'] += count
    nswcounter['LABB'] += count
    
    # chuyển tiền tệ
    text, count = re.subn(r'(?P<id>(\d+ \. )*\d+( \, \d+)? ({}))( |$)'.format(currency_list),
                        lambda x: MONY2words(''.join(x.group('id').split(' '))) + ' ',
                        text)
    nswcounter['MONY'] += count
    
    # chuyển giờ
    text, count = re.subn(r'(?P<id>(((0|1)?[0-9]|(2)[0-3]):([0-5]?[0-9]):([0-5]?[0-9]))|(((0|1)?[0-9]|(2)[0-3]):([0-5]?[0-9])))',
                          lambda x: NTIME2words(x.group('id')),
                          text)
    nswcounter['NTIM'] += count                          
    
    # chuyển số điện thoại
    text, count = re.subn(r'(?P<id> |^)(?P<id1>(0)(\d|\.){9,14})(?P<id2> |$)',
                          lambda x: x.group(
                              'id') + NTEL2words(x.group('id1')) + x.group('id2'),
                          text)
    nswcounter['NTEL'] += count                          
    
    # chuyển phần trăm
    text, count = re.subn(r'(?P<id>( |^)\d+(\,\d+| \, \d+)?(( |)\-( |)\d+(\,\d+| \, \d+)?)?(%| %)( |$))',
                          lambda x: ' ' +
                          NPER2words(''.join(x.group('id').split())) + ' ',
                          text)
    nswcounter['NPER'] += count
    
    # chuyển range
    text, count = re.subn(r'(?P<id>( |^)\d+(\,\d+| \, \d+)?( |)\-( |)\d+(\,\d+| \, \d+)?( |$))',
                          lambda x: ' ' + NRNG2words(''.join(x.group('id').split())) + ' ',
                          text)
    nswcounter['NRNG'] += count
    
    # chuyển phân số
    text, count = re.subn(r'(?:^| )(?P<id>\d+( |)\/( |)\d+)(?: |$)',
                          lambda x: NFRC2words(''.join(x.group('id').split())), text)
    nswcounter['NFRC'] += count
    
    # nếu hai từ nối nhau bởi dấu - thì chuyển dấu trừ thành khoảng trắng
    text, count = re.subn(r'(?P<id>[{}]+) \- (?P<id1>[{}]+)'.format(
        charset, charset), lambda x: x.group('id') + ' '+x.group('id1'), text)
    nswcounter['PUNC'] += count

    

    # chuyển các trường hợp khác
    sub_tokens = text.split()

    for i, sub_token in enumerate(sub_tokens):
        if sub_token.lower() not in vn_words_dict:
            # chuyển từ mã gồm chuỗi chữ cái và số
            if (i < len(sub_tokens)-1) and re.match(r'^({})+$'.format(lseq_charset), sub_tokens[i].upper()) \
                    and re.match(r'\d+', sub_tokens[i+1]):
                sub_token = LSEQ2words(sub_tokens[i])
                sub_tokens[i] = sub_token + ' ' + NDIG2words(sub_tokens[i+1])
                sub_tokens[i+1] = ''
                nswcounter['LSEQ'] += 1
                nswcounter['NDIG'] += 1
                continue
            elif len(sub_token) == 1 and sub_token.upper() in LSEQ_DICT.keys():
                # nếu chỉ một chữ cái riêng biệt
                sub_token = LSEQ2words(sub_token)
                nswcounter['LSEQ'] += count
            elif sub_token in ABB_DICT:
                # chuyển từ viết tắt
                sub_token, count = re.subn('(?P<id>({})+)'.format(lseq_charset),
                                   lambda x: LABB2words(x.group('id')), sub_token)
                nswcounter['LABB'] += count
            elif sub_token.isupper():
                # chuyển LSEQ
                sub_token, count = re.subn('(?P<id>({})+)'.format(lseq_charset),
                                lambda x: LSEQ2words(x.group('id')), sub_token.upper()) 
                nswcounter['LSEQ'] += count
            elif LWRD2words(sub_token.lower()):
                # nếu có trong tiếng anh
                sub_token = LWRD2words(sub_token.lower())
                nswcounter['LWRD'] += 1
            elif re.match(r'({})+'.format('|'.join(charset)), sub_token):
                # thường là tên latin
                sub_token = latin_name2words(sub_token.lower())
                nswcounter['LWRD'] += 1

            # chuyển số
            sub_token, count = re.subn(
                r'(?P<id>(\d+\.)*\d+(\,\d+)?)', lambda x: NNUM2words(''.join(x.group('id').split('.')))+' ', sub_token)
            nswcounter['NNUM'] += count
            # chuyển punctuation
            # đọc một số punctuation
            sub_token, count = re.subn(r'(?P<id>{})'.format(r'\/'),
                               lambda x: ' ' + PUNC2words(x.group('id')) + ' ', sub_token)
            nswcounter['PUNC'] += count

            # bỏ một số punctuation không đọc
            sub_token, count = re.subn(r'(?P<id>{})'.format(r'\(|\)|\'|\"|\“|\”|\-|\+|\*|\\|\_|\&|\%|\^|\[|\]|\{|\}|\=|\#|\@|\`|\~|\$'),
                               lambda x: '', sub_token)
            nswcounter['PUNC'] += count

            # giữ lại các dấu ngắt nghỉ
            sub_token, count = re.subn(r'(?P<id>{})'.format('\.|\,|\;|\?|\!|\…|\:'),
                               lambda x: x.group('id'), sub_token)
            nswcounter['DURA'] += count

            # loại bỏ các thành phần không đọc được như các icon,...
            sub_token, count = re.subn(r'(?P<id>[^({})])'.format('|'.join(charset) + '|\.|\,|\;|\?|\!|\…|\:'),
                               lambda x: ' ', sub_token)
            nswcounter['NONE'] += count               
        else:
            sub_token = sub_token.lower()

        sub_tokens[i] = sub_token

    text = ' '.join(sub_tokens)
    normalized_text = ' '.join(text.split())

    return normalized_text, nswcounter

def count_NSWs(text):
    list_tokens = split_token(text)
    text = split_compound_NSWs(list_tokens)
    normalized_text, nswcounter = replace(text)

    return nswcounter

def normalize(text):
    # text = unicodedata.normalize('NFKC', text)
    list_tokens = split_token(text)
    text = split_compound_NSWs(list_tokens)
    normalized_text, nswcounter = replace(text)

    return normalized_text