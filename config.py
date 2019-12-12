# encoding : utf-8
import os.path
import re
from utils import load_dict

CURDIR = os.path.dirname(__file__)

LSEQ_DICT_PATH = os.path.join(CURDIR, 'dicts/LSEQ_DICT.txt')
EN2VI_DICT_PATH = os.path.join(CURDIR, 'dicts/EN2VI_DICT.txt')
ABB_DICT_PATH = os.path.join(CURDIR, 'dicts/ABB_DICT.txt')
PUNC_DICT_PATH = os.path.join(CURDIR, 'dicts/PUNC_DICT.txt')
CURRENCY_DICT_PATH = os.path.join(CURDIR, 'dicts/CURRENCY_DICT.txt')
UNIT_DICT_PATH = os.path.join(CURDIR, 'dicts/UNIT_DICT.txt')
VI_WORDS_PATH = os.path.join(CURDIR, 'dicts/vietnamese_words.txt')

LSEQ_DICT = load_dict(LSEQ_DICT_PATH)
EN2VI_DICT = load_dict(EN2VI_DICT_PATH)
ABB_DICT = load_dict(ABB_DICT_PATH)
PUNC_DICT = load_dict(PUNC_DICT_PATH)
CURRENCY_DICT = load_dict(CURRENCY_DICT_PATH)
UNIT_DICT = load_dict(UNIT_DICT_PATH)

currency_list_regex = '|'.join(CURRENCY_DICT.keys())
currency_list_regex = re.sub('(?P<id>\$|\£|\€)', lambda x: '\\' +x.group('id'),
                             currency_list_regex)


_f = open(VI_WORDS_PATH, 'r', encoding='utf-8')
list_vietnamese_words = _f.read().split('\n')
vn_words_dict = dict.fromkeys(list_vietnamese_words, 0)
_f.close()

charset = 'aáảàãạâấẩầẫậăắẳằẵặbcdđeéẻèẽẹêếểềễệfghiíỉìĩịjklmnoóỏòõọôốổồỗộơớởờỡợpqrstuúủùũụưứửừữựvwxyýỷỳỹỵzAÁẢÀÃẠÂẤẨẦẪẬĂẮẲẰẴẶBCDĐEÉẺÈẼẸÊẾỂỀỄỆFGHIÍỈÌĨỊJKLMNOÓỎÒÕỌÔỐỔỒỖỘƠỚỞỜỠỢPQRSTUÚỦÙŨỤƯỨỬỪỮỰVWXYÝỶỲỸỴZ'
change_phone_dict = {'òa': 'oà', 'óa': 'oá', 'ọa': 'oạ', 'õa': 'oã', 'ỏa': 'oả',
                         'òe': 'oè', 'óe': 'oé', 'ọe': 'oẹ', 'õe': 'oẽ', 'ỏe': 'oẻ',
                         'ùy': 'uỳ', 'úy': 'uý', 'ụy': 'uỵ', 'ũy': 'uỹ', 'ủy': 'uỷ'}



punc = r'\.|\,|\…|\;|\/|\(|\)|\!|\?|\'|\"|\“|\”|\:|\-|\+|\<|\>|\*|\\|\_|\&|\%|\^|\[|\]|\{|\}|\=|\#|\@|\`|\~|\$|\–|\°|\€|\£'
remove_punc_regex = r'^\(|\)|\'|\"|\“|\”|\[|\]|\{|\}|\`$'
keep_punc_regex = r'^\.|\,|\…|\;|\!|\?|\:$'
speakable_punc_regex = r'^\/|\-|\+|\*|\\|\_|\&|\%|\^|\=|\#|\@|\<|\>|\~|\$|\–|\°|\€|\£$'
not_end_of_number_punc = r'\(|\)|\'|\"|\“|\”|\[|\]|\{|\}|\`|\.|\,|\…|\;|\!|\?|\:|^\/|\-|\+|\*|\\|\_|\&|\^|\=|\#|\@|\<|\>|\~|\–'
punc_with_number = '\/|\.|\,|\-|\–|\%|\:|\°|\$|\€|\£'



email_regex = r'[a-z][a-z0-9_\.]{5,32}@[a-z0-9]{2,}(\.[a-z0-9]{2,4})+'
url_regex = r'((?:http(s)?:\/\/)|(www))[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&\'\(\)\*\+,;=.]+'
short_url = r'([\w.-]+(?:\.[\w\.-]+)+)?[\w\-\._~:/?#[\]@!\$&\'\(\)\*\+,;=.]+(\.(com|gov|vn|com|org|info|io|net|edu))+'
url_regex += '|' + short_url



NTIM_regex = r'^((((0|1)?[0-9]|(2)[0-3]):([0-5]?[0-9]):([0-5]?[0-9]))|(((0|1)?[0-9]|(2)[0-3]):([0-5]?[0-9])))$'
NDAT_regex = r'^((0)?[1-9]|[1-2][0-9]|(3)[0-1])(\/)(((0)?[0-9])|((1)[0-2]))(\/)(\d{4}|\d{2})$'
NDAY_regex = r'^((0)?[1-9]|[1-2][0-9]|(3)[0-1])(\/)(((0)?[0-9])|((1)[0-2]))$'
NMON_regex = r'^(((0)?[0-9])|((1)[0-2]))( |)(\/)( |)(\d{4}|\d{2})$'
NFRC_regex = r'^\d+\/\d+$'
NTEL_regex = r'^(0|\+\d{2})(\d|\.\d){5,14}$'
NRNG_regex = r'^((\d+\.)*\d+(\,\d+)?)\-((\d+\.)*\d+(\,\d+)?)$'
NPER_regex = r'^((\d+\.)*\d+(\,\d+)?)(\-((\d+\.)*\d+(\,\d+)?))?\%$'
NADD_regex = r'^\d+(\/\d+)+$'
NDIG_regex = r'^\d+$'
NNUM_regex = r'^(\d+\.)*\d+(\,\d+)?$'
MONY_regex = r'^(\d+\.)*\d+(\,\d+)?({})$'.format(currency_list_regex)
CSEQ_regex = r'^(\d|{})+'.format(speakable_punc_regex[1:-1])



NDAT_contexts_before = ['ngày', 'hôm', 'nay',
                        'sáng', 'chiều', 'trưa', 'tối', 'mai']
NADD_contexts_before = ['địa', 'chỉ', 'số', 'nhà']
NDAY_contexts_before = ['ngày', 'hôm', 'nay',
                        'sáng', 'chiều', 'trưa', 'tối', 'mai']
NFRC_contexts_before = ['chiếm']
NMON_contexts_before = ['tháng']
NFRC_contexts_before = ['chiếm', 'trên', 'dưới']
NRNG_contexts_before = ['từ', 'khoảng']
NSCR_contexts_before = ['tỷ', 'số']
NNUM_contexts_before = ['thứ', 'khoảng', 'còn', 'trên', 'dưới']
NNUM_contexts_after = ['điểm', ]
NDIG_contexts_before = ['số', 'mã', 'dãy']
