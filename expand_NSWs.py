# encoding : utf-8
import re

from num2words import num2words

from config import EN2VI_DICT, vn_words_dict, ABB_DICT, LSEQ_DICT,\
    PUNC_DICT, CURRENCY_DICT, currency_list_regex, punc


# hàm bignumread để xử lý số lớn mà thu viện num2words không xử lý được
def bignumread(numberstring, index=0):
    '''đọc số tự nhiên lớn (>10^9), index:độ lớn hàng tỷ cần xét'''

    if len(numberstring) <= 9:
        return smallnumread(numberstring)
    else:
        index += 1
        big = numberstring[:-9]
        small = numberstring[-9:]
        return bignumread(big, index + 1) + ' ' + 'tỷ ' * index + ', ' + smallnumread(small)


def smallnumread(numberstring):
    '''đọc số tự nhiên nhỏ có chỉnh sửa từ thư viện num2words'''

    result = ""
    number = int(numberstring)
    if number <= 1000 or number % 1000 == 0:
        result = num2words(number, lang='vi')
    else:
        result = num2words(number // 100 * 100, lang='vi')
        if ((number // 100) % 10 == 0):
            result += " không trăm"
        if number % 100 < 10:
            result += " lẻ " + num2words(number % 100, lang='vi')
        else:
            result += " " + num2words(number % 100, lang='vi')

    return result


def decimal2words(numberstring):
    """đọc số tự nhiên"""
    if len(numberstring) <= 9:
        return smallnumread(numberstring)
    else:
        return bignumread(numberstring)


def NNUM2words(num_string):
    """đọc số tự nhiên, có thể có phân tách . và số thập phân"""
    num_string = re.sub(r'\.', '', str(num_string))
    arr = num_string.split(',')
    if len(arr) == 1:
        # số tự nhiên
        return decimal2words(num_string)
    elif len(arr) == 2:
        # số thực có phần thập phân ngăn bởi dấu phẩy
        return decimal2words(arr[0]) + ' phẩy ' + NDIG2words(arr[1])
    else:
        return ''


def NDIG2words(dig_string):
    "3925"
    result = ''
    for digit in dig_string:
        if digit.isdigit():
            result += num2words(int(digit), lang='vi') + ' '
    result = result.strip()
    return result


def NTIM2words(time_string):
    try:
        time_arr = time_string.split(':')
        if len(time_arr) == 2:
            h = time_arr[0]
            m = time_arr[1]
            return NNUM2words(h) + " giờ " + NNUM2words(m) + " phút"
        elif len(time_arr) == 3:
            h = time_arr[0]
            m = time_arr[1]
            s = time_arr[2]
            return NNUM2words(h) + " giờ " + NNUM2words(m) + " phút " \
                   + NNUM2words(s) + " giây"
    except:
        return ""


def NDAT2words(date_string):
    """ngày/tháng/năm"""
    separator = '/'
    date_arr = date_string.split(separator)
    d, m, y = date_arr[0], date_arr[1], date_arr[2]

    # đọc ngày
    dstring = ""
    if int(d) < 10:
        dstring = "mồng " + NNUM2words(d)
    else:
        dstring = NNUM2words(d)

    # đọc năm
    ystring = ""
    y = int(y)
    if y <= 1000 or y % 1000 == 0:
        ystring = NNUM2words(y)
    else:
        ystring = NNUM2words(y // 100 * 100)
        if ((y // 100) % 10 == 0):
            ystring += " không trăm"
        if y % 100 < 10:
            ystring += " lẻ " + NNUM2words(y % 100)
        else:
            ystring += " " + NNUM2words(y % 100)

    return dstring + " tháng " + NNUM2words(m) \
           + " năm " + ystring


def NDAY2words(day_string):
    """ngày/tháng"""
    separator = '/'
    day_arr = day_string.split(separator)
    d, m = day_arr[0], day_arr[1]

    # đọc ngày
    dstring = ""
    if int(d) < 10:
        dstring = "mồng " + NNUM2words(d)
    else:
        dstring = NNUM2words(d)

    return dstring + " tháng " + NNUM2words(m)


def NMON2words(mont_string):
    """tháng/năm"""
    separator = '/'
    mont_arr = mont_string.split(separator)
    m, y = mont_arr[0], mont_arr[1]

    # đọc năm
    ystring = ""
    y = int(y)
    if y <= 1000 or y % 1000 == 0:
        ystring = NNUM2words(y)
    else:
        ystring = NNUM2words(y // 100 * 100)
        if (y // 100 % 10 == 0):
            ystring += " không trăm"
        if y % 100 < 10:
            ystring += " lẻ " + NNUM2words(y % 100)
        else:
            ystring += " " + NNUM2words(y % 100)

    return NNUM2words(m) + " năm " + ystring


def NTEL2words(tel_string):
    "093.156.2565, +84357121314"
    tel_string = ''.join(tel_string.split('.'))
    result = ''
    result = re.sub('\+', 'cộng ', tel_string)
    result = re.sub('(?P<id>\d)', lambda x: NNUM2words(
        x.group('id')) + ' ', result)
    return result


def NSCR2words(score_string):
    """tỷ số `2-3`"""
    arr = score_string.split('-')
    result = NNUM2words(arr[0]) + ' ' + NNUM2words(arr[1])

    return result


def NRNG2words(range_string):
    """từ `2-3`"""
    arr = range_string.split('-')
    result = NNUM2words(arr[0]) + ' đến ' + NNUM2words(arr[1])

    return result


def NPER2words(per_string):
    """30% hoặc 30-40%"""
    per_string = re.sub(r'(?P<id>\d+)\-(?P<id1>\d+)',
                        lambda x: x.group('id') + ' đến ' + x.group('id1'), per_string)
    per_string = re.sub(
        r'(?P<id>\d+)\%', lambda x: x.group('id') + ' phần trăm', per_string)
    per_string = re.sub(
        r'(?P<id>\d+(\,\d+)?)', lambda x: NNUM2words(x.group('id')), per_string)

    return per_string


def NADD2words(add_string):
    "12/7"
    add_string = re.sub(r'\/', ' trên ', add_string)
    add_string = re.sub(r'(?P<id>\d+)', lambda x: NNUM2words(x.group('id')))
    return add_string

def NFRC2words(frac_string):
    """3/4"""
    frac_string = re.sub(r'\/', lambda x: ' phần ', frac_string)
    frac_string = re.sub(
        r'(?P<id>\d+)', lambda x: NNUM2words(x.group('id')), frac_string)

    return frac_string


def LWRD2words(word):
    try:
        result = EN2VI_DICT[word.lower()]
    except:
        # nếu word không có trong từ điển tiếng Anh
        return latin_name2words(word)

    return result


def LSEQ2words(seq_string):
    result = ''
    for char in seq_string:
        if char.upper() in LSEQ_DICT.keys():
            result += LSEQ_DICT[char.upper()] + ' '
    result = result.strip()
    return result


def LABB2words(abb_string):
    """ĐHBKHN"""
    result = ''
    abb_string = abb_string.strip()
    result = ABB_DICT[abb_string].split(',')[0]

    return result


def PUNC2words(punc_string):
    result = ''
    if punc_string in PUNC_DICT:
        result = PUNC_DICT[punc_string]

    return result


def URLE2words(urle_string):
    """đọc đường link và email"""
    urle_string = urle_string.lower()
    urle_string = re.sub(r'\.$', '', urle_string)
    urle_string = re.sub(r'^http', 'hát tê tê pê ', urle_string)
    urle_string = re.sub(r'.com', ' chấm com ', urle_string)
    urle_string = re.sub(r'.edu', ' chấm e đu ', urle_string)
    urle_string = re.sub(r'gmail', ' gờ meo ', urle_string)
    urle_string = re.sub(r'outlook', ' ao lúc ', urle_string)
    urle_string = re.sub(r'@', ' a còng ', urle_string)
    urle_string = re.sub(r'(?P<id>{})'.format("\\" + '|\\'.join(PUNC_DICT.keys())),
                         lambda x: ' ' + PUNC2words(x.group('id')) + ' ', urle_string)
    urle_string = re.sub(r'(?P<id>\d)', lambda x: ' ' +
                                                  NNUM2words(x.group('id')) + ' ', urle_string)
    arr = urle_string.split()
    for i, word in enumerate(arr):
        if word not in vn_words_dict:
            # nếu đọc được theo tiếng Anh
            if LWRD2words(word):
                arr[i] = LWRD2words(word)
            else:
                k = 0
                newtoken = ''
                while k < len(word):
                    # so khớp từ dài đến ngắn  xem có từ nào đọc được tiếng Việt không
                    for j in [5, 4, 3, 2, 1]:
                        if k + j <= len(word):
                            if word[k:k + j] in vn_words_dict:
                                newtoken += word[k:k + j] + ' '
                                k = k + j
                                break
                            elif j > 2 and LWRD2words(word[k:k + j]):
                                # nếu có trong tiếng anh thì đọc kiểu tiếng anh
                                newtoken += LWRD2words(word[k:k + j]) + ' '
                                k = k + j
                                break
                            elif j == 1 and word[k] != ' ':
                                # nếu có 1 chữ cái thì đọc từng chữ
                                newtoken += LSEQ2words(word[k]) + ' '
                                k += 1
                                break
                            elif j == 1 and word[k] == ' ':
                                # kí tự cách
                                newtoken += ' '
                                k += 1
                arr[i] = newtoken

    result = ' '.join(arr)
    return result.strip()


def MONY2words(money_string):
    # tách đơn vị và số, đọc đơn vị
    money_string = re.sub(r'(?P<id>\d)(?P<id1>{})'.format(currency_list_regex),
                        lambda x: x.group('id') + ' ' + CURRENCY_DICT[x.group('id1')],
                        money_string)
    # đọc số
    money_string = re.sub(r'(?P<id>(\d+\.)*\d+(\,\d+)?)',
                          lambda x: NNUM2words(''.join(x.group('id').split('.'))), money_string)
    return money_string


def latin_name2words(token):
    # sửa một số âm tiết sang tiếng việt
    phones1 = 'ai|ao|ây|oi|âu'
    phones2 = 'p|c|t|ch|n|ng|m|ph|b|d|đ|g|h|x|s|th|v|gu|l|r'
    phones3 = 'a|ă|e|i|o|ơ|ô|u|y'
    phones4 = 'ai|ao|ây|oi|âu|a|ă|e|i|o|ơ|ô|u'
    token = re.sub('(?P<id>{})(?P<id1>({})({}))'.format(phones3, phones2, phones3),
                   lambda x: x.group('id') + ' ' + x.group('id1'), token)
    token = re.sub('(?P<id>{})(?P<id1>({})({}))'.format(phones3, phones2, phones3),
                   lambda x: x.group('id') + ' ' + x.group('id1'), token)
    token = re.sub('yl', 'in', token)
    token = re.sub('(?P<id>da|di|de|du|do)',
                   lambda x: 'đ' + x.group('id')[1], token)
    token = re.sub('j|z', 'd', token)
    token = re.sub('f', 'ph', token)
    token = re.sub(r'd$', 't', token)
    token = re.sub('(?P<id>ya|ye|yo|yu)', lambda x: 'd' +
                                                    x.group('id')[1], token)
    token = re.sub('(?P<id>ka|ko|ku)', lambda x: 'c' + x.group('id')[1], token)
    token = re.sub('(?P<id>ci|ce)', lambda x: 'k' + x.group('id')[1], token)
    token = re.sub('al', 'an', token)
    token = re.sub('el', 'eo', token)
    token = re.sub('il', 'iu', token)
    token = re.sub('ol', 'on', token)
    token = re.sub('ul', 'un', token)
    token = re.sub('ue', 'oe', token)
    token = re.sub('et', 'ét', token)
    token = re.sub('ic', 'ích', token)
    token = re.sub('sh', 's', token)

    i = 0
    newtoken = ''
    while i < len(token):
        # so khớp từ dài đến ngắn  xem có từ nào không
        # nếu có thì thay thế bởi phiên âm
        for j in [5, 4, 3, 2, 1]:
            if i + j <= len(token):
                if j == 1 and token[i] not in ['a', 'e', 'i', 'o', 'u']:
                    # nếu chỉ có 1 chữ cái không phải nguyên âm thì bỏ qua
                    i += 1
                elif token[i:i + j] in vn_words_dict:
                    newtoken += token[i:i + j] + ' '
                    i = i + j
                    break
    return newtoken.strip()

def DURA2words(token):
    """giữ lại DURA"""
    return token

def CSEQ2words(token):
    token_string = re.sub(r'(?P<id>(\d+\.)*\d+(\,\d+)?)',
                          lambda x: NNUM2words(''.join(x.group('id').split('.'))) + ' ',
                          token)
    token_string = re.sub(r'(?P<id>({}))'.format(punc),
                          lambda x: PUNC_DICT[x.group('id')] + ' ',
                          token_string)
    token_string = ' '.join(token_string.split())
    return token_string
def NONE2words(token):
    return ''