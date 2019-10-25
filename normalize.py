# encoding: utf-8
from time import time
import re
from bs4 import BeautifulSoup as Soup

from .expand_NSWs import *

charset = 'aáảàãạâấẩầẫậăắẳằẵặbcdđeéẻèẽẹêếểềễệfghiíỉìĩịjklmnoóỏòõọôốổồỗộơớởờỡợpqrstuúủùũụưứửừữựvwxyýỷỳỹỵzAÁẢÀÃẠÂẤẨẦẪẬĂẮẲẰẴẶBCDĐEÉẺÈẼẸÊẾỂỀỄỆFGHIÍỈÌĨỊJKLMNOÓỎÒÕỌÔỐỔỒỖỘƠỚỞỜỠỢPQRSTUÚỦÙŨỤƯỨỬỪỮỰVWXYÝỶỲỸỴZ'
email_regex = r'[a-z][a-z0-9_\.]{5,32}@[a-z0-9]{2,}(\.[a-z0-9]{2,4})+'
url_regex = r'((?:http(s)?:\/\/)|(www))[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&\'\(\)\*\+,;=.]+'
punc = r'\.|\,|\…|\;|\/|\(|\)|\!|\?|\'|\"|\“|\”|\:|\-|\+|\*|\\|\_|\&|\%|\^|\[|\]|\{|\}|\=|\#|\@|\`|\~|\$'
unitlist = '|'.join(UNIT_DICT.keys())
lseq_charset = '|'.join(LSEQ_DICT)

f = open(VI_WORDS_PATH, 'r', encoding='utf-8')
list_vietnamese_words = f.read().split('\n')


def split_token(text):
    """
        Tách token từ text, trả về mảng các token.
    """
    # chuyển \n thành chấm nếu cuối câu không chấm
    text = re.sub(r'\n', '.', text)
    text = re.sub(r'\.\.\.|\.\.|\. \.', '.', text)
    text = re.sub(r'\.\.\.|\.\.|\. \.', '.', text)

    # tách token
    list_tokens = text.split()
    for i, token in enumerate(list_tokens):
        # nếu là email hoặc url thì bỏ qua
        if re.match(email_regex, token) or re.match(url_regex, token):
            continue

        # tách các từ bị dính các dấu .,;/()'"
        # "đã xong.Viện" => "đã xong . Viện", "HN(Số 36)" => "HN ( Số 36)"
        split_punc = '\.|\,|\;|\/|\(|\)|\!|\?|\…'
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
    # 09 15 33 45 77 => 09.15.33.45.77, 035 164 4565 => 035.164.4565
    text = re.sub(r'(?P<id>\d+)\s+(?P<id1>\d+)( |$)',
                  lambda x: x.group('id')+'.'+x.group('id1')+' ', text)
    text = re.sub(r'(?P<id>\d+)\s+(?P<id1>\d+)( |$)',
                  lambda x: x.group('id')+'.'+x.group('id1') + ' ', text)

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


def filter_candidate_NSWs(list_tokens):
    """gán thẻ w cho các token là NSW"""
    result = []
    for token in list_tokens:
        if token.lower() not in list_vietnamese_words:
            # token là NSW
            token = '<w>'+token+'</w>'
        else:
            token = token.lower()

        result.append(token)
    return ' '.join(result)


def split_compound_NSWs(text):
    """
        Tách các NSW phức tạp cho vào thẻ split\n
        `vào lúc 10h30` => `vào lúc <split><w>10</w><w>h</w><w>30</w>`
    """
    tokens = text.split()
    for i, token in enumerate(tokens):
        # nếu token trong thẻ w
        if re.match(r'^<w>(\w|\d|{})+</w>$'.format(punc), token):
            # lấy token từ thẻ w
            token = re.sub(
                r'^<w>(?P<id>(\w|\d|{})+)</w>$'.format(punc), lambda x: x.group('id'), token)

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
                
                # thêm thẻ split
                new_token = ''
                for j, sub_token in enumerate(token.split()):
                    new_token += '<sub>' + sub_token + '</sub>'
                tokens[i] = '<split>' + new_token + '</split>'

    return ' '.join(tokens)


def add_fulltext_for_tag(tagged_text):
    soup = Soup(tagged_text, 'lxml')
    # xét thẻ split
    for split_tag in soup.findAll('split'):
        w_tags = split_tag.children
        tokens = []
        for w_tag in w_tags:
            tokens.append(w_tag.string)
        token_string = ' '.join(tokens)
        try:
            token_string = replace_NSWs(token_string)
        except:
            token_string = ' '
        split_tag.attrs['fulltext'] = token_string

    for i, w_tag in enumerate(soup.findAll('w')):
        token_string = w_tag.string
        try:
            token_string = replace_NSWs(token_string)
        except:
            token_string = ' '
        w_tag['fulltext'] = token_string

    return soup


def replace_NSWs(token_string):
    # chuyển urle
    token_string = re.sub(r'(?P<id>{}|{})'.format(email_regex, url_regex),
                          lambda x: URLE2words(x.group('id')), token_string)
    # chuyển ngày/tháng/năm
    token_string = re.sub(r'(?P<id>(^| )((0)?[1-9]|[1-2][0-9]|(3)[0-1])( |)(\/)( |)(((0)?[0-9])|((1)[0-2]))( |)(\/)( |)(\d{4}|\d{2})( |$))',
                          lambda x: ' ' + NDAT2words(''.join(x.group('id').split())) + ' ', token_string)
    # chuyển ngày/tháng
    token_string = re.sub(r'(?P<id>(^| )((0)?[1-9]|[1-2][0-9]|(3)[0-1])( |)(\/)( |)(((0)?[0-9])|((1)[0-2]))( |$))',
                          lambda x: ' ' + NDAY2words(''.join(x.group('id').split())) + ' ', token_string)
    # chuyển tháng/năm
    token_string = re.sub(r'(?P<id>(^| )(((0)?[0-9])|((1)[0-2]))( |)(\/)( |)(\d{4}|\d{2})( |$))',
                          lambda x: ' ' + NMONT2words(''.join(x.group('id').split())) + ' ', token_string)
    # chuyển số kèm đơn vị
    token_string = re.sub(r'(?P<id>(\d+\.)*\d+(\,\d+| \, \d+)?) (?P<id1>{})(?P<id2> |$)'.format(unitlist),
                          lambda x: NNUM2words(''.join(x.group('id').split(
                          ))) + ' ' + UNIT_DICT[x.group('id1')] + x.group('id2'),
                          token_string)
    # chuyển tiền tệ
    token_string = re.sub(r'(?P<id>(\d+ \. )*\d+( \, \d+)? ({}))( |$)'.format(currency_list),
                        lambda x: MONY2words(''.join(x.group('id').split(' '))) + ' ',
                        token_string)
    # chuyển giờ
    token_string = re.sub(r'(?P<id>(((0|1)?[0-9]|(2)[0-3]):([0-5]?[0-9]):([0-5]?[0-9]))|(((0|1)?[0-9]|(2)[0-3]):([0-5]?[0-9])))',
                          lambda x: NTIME2words(x.group('id')),
                          token_string)
    # chuyển số điện thoại
    token_string = re.sub(r'(?P<id> |^)(?P<id1>(0)(\d|\.){9,14})(?P<id2> |$)',
                          lambda x: x.group(
                              'id') + NTEL2words(x.group('id1')) + x.group('id2'),
                          token_string)
    # chuyển phần trăm
    token_string = re.sub(r'(?P<id>( |^)\d+(\,\d+| \, \d+)?(( |)\-( |)\d+(\,\d+| \, \d+)?)?(%| %)( |$))',
                          lambda x: ' ' +
                          NPER2words(''.join(x.group('id').split())) + ' ',
                          token_string)
    # chuyển range
    token_string = re.sub(r'(?P<id>( |^)\d+(\,\d+| \, \d+)?( |)\-( |)\d+(\,\d+| \, \d+)?( |$))',
                          lambda x: NRNG2words(''.join(x.group('id').split())),
                          token_string)
    # chuyển phân số
    token_string = re.sub(r'(?:^| )(?P<id>\d+( |)\/( |)\d+)(?: |$)',
                          lambda x: NFRC2words(''.join(x.group('id').split())), token_string)
    # nếu hai từ nối nhau bởi dấu - thì chuyển dấu trừ thành khoảng trắng
    token_string = re.sub(r'(?P<id>[{}]+) \- (?P<id1>[{}]+)'.format(
        charset, charset), lambda x: x.group('id') + ' '+x.group('id1'), token_string)

    # chuyển các trường hợp khác
    sub_tokens = token_string.split()

    for i, sub_token in enumerate(sub_tokens):
        if sub_token.lower() not in list_vietnamese_words:
            # chuyển từ mã gồm chuỗi chữ cái và số
            if (i < len(sub_tokens)-1) and re.match(r'^({})+$'.format(lseq_charset), sub_tokens[i].upper()) \
                    and re.match(r'\d+', sub_tokens[i+1]):
                sub_token = LSEQ2words(sub_tokens[i])
                sub_tokens[i] = sub_token + ' ' + NDIG2words(sub_tokens[i+1])
                sub_tokens[i+1] = ''
                continue
            elif len(sub_token) == 1 and sub_token.upper() in LSEQ_DICT.keys():
                # nếu chỉ một chữ cái riêng biệt
                sub_token = LSEQ2words(sub_token)

            elif LWRD2words(sub_token.lower()):
                # nếu có trong tiếng anh
                sub_token = LWRD2words(sub_token.lower())
            elif sub_token in ABB_DICT:
                # chuyển từ viết tắt
                sub_token = re.sub('(?P<id>({})+)'.format(lseq_charset),
                                   lambda x: LABB2words(x.group('id')), sub_token)
            else:
                # chuyển LSEQ
                sub_token = re.sub('(?P<id>({})+)'.format(lseq_charset),
                                   lambda x: LSEQ2words(x.group('id')), sub_token.upper())

            # chuyển số
            sub_token = re.sub(
                r'(?P<id>(\d+\.)*\d+(\,\d+)?)', lambda x: NNUM2words(''.join(x.group('id').split('.')))+' ', sub_token)
            # chuyển punctuation
            sub_token = re.sub(r'(?P<id>{})'.format(punc),
                               lambda x: ' ' + PUNC2words(x.group('id')) + ' ', sub_token)
        else:
            sub_token = sub_token.lower()

        sub_tokens[i] = sub_token

    token_string = ' '.join(sub_tokens)

    return token_string


def get_text_from_soup(soup):
    """Lấy ra text từ đối tượng BeautifulSoup chứa các thẻ"""
    split_tags = soup.findAll('split')
    # xóa các thẻ w trong thẻ split (chỉ lấy fulltext của thẻ split)
    for split_tag in split_tags:
        sub_w_tags = split_tag.findAll('w')
        for sub_w_tag in sub_w_tags:
            sub_w_tag.extract()
        split_tag.string = ''

    # thay thế các thẻ bằng full text
    # để lại một số punctuation
    tags = soup.findAll(['split', 'w'])
    for tag in tags:
        if tag.string in ['.', ',', '?', ';', '!', '…']:
            pass
        elif re.match(r'{}'.format(punc), tag.string):

            tag.string.replace_with('')
        else:
            tag.string.replace_with(tag['fulltext'])

    text = ''.join(soup.strings)
    text = ' '.join(text.split())
    return text


def normalize(text):
    list_tokens = split_token(text)
    tagged_text = filter_candidate_NSWs(list_tokens)
    tagged_text = split_compound_NSWs(tagged_text)
    soup = add_fulltext_for_tag(tagged_text)
    normalized_text = get_text_from_soup(soup)
    return normalized_text

t0 = time()
ex_file = os.path.join(CURDIR, 'vidu.txt')
text = open(ex_file).read()
print(normalize(text))
print(time()-t0)
