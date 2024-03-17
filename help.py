import json
import random

def p(text, *args):
    print(text, *args, sep=' / ', end='\n')

def pcolor(text_code, color_num = 2):
    print(f'\033[3{color_num}m{text_code}\033[0m', end='\n')

def wtf(html, pg):
    with open(f'./html/html{pg}.txt', "w", encoding='utf8') as f:
        f.write(html)

def lf(filename):
    with open(filename, 'r') as f:
        return f.read()

def write_json(data, path):
    with open(path, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)  

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_description_index(unit_code):
    ''' return index '''
    unit = unit_code.replace('.', '')

    nids = {
        'ед':0,
        'гр':1, 
        'кг':2,
        'мл':3,
        'л':4, 'литра':4,
        'см':5,
        'м':6,
        'мин':7,
        'ч':8,
        'шт':9, 'штук':9,
        'порц':10,
    }

    return (str(nids[unit]) if unit in nids.keys() else '')

def get_id():
    return random.randrange(1992, 3999)

def get_maximun_m(t):
    if t == 'radio':
        return str(1)
    
    if t == 'checkbox':
        return str(10)

def get_type_m(t):
    if t == 'radio':
        return 'one_one'

    if t == 'checkbox':
        return 'all_one'

def get_list_gid(m_groups):
    g_arr = []
    for g_ in m_groups:
        g_arr.append(g_['gid'])
    
    return set(g_arr)