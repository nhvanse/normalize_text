# encoding: utf-8

def load_dict(dict_path):
    """ Load dictionary \n 
    File dict: key|value\n
    Return dict
    """
    dict_ = {}
    with open(dict_path, 'r', encoding='utf-8') as file_:
        content = file_.read()
        rows = content.split('\n')
        for row in rows:
            if row == '':
                continue
            key = row.split('|')[0].strip()
            value = row.split('|')[1].strip()
            dict_[key] = value

    return dict_


def common_member(list1, list2):
    """Check if list1 and list2 have at-least 1 element common"""
    set1 = set(list1)
    set2 = set(list2)
    if (set1 & set2):
        return True
    else:
        return False

