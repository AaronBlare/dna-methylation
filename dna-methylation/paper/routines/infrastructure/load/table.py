import os.path
import pickle
import pandas as pd
from paper.routines.infrastructure.save.table import save_table_dict_pkl


def load_table_dict(fn):
    if os.path.isfile(fn + '.pkl'):
        table_dict = load_table_dict_pkl(fn + '.pkl')
    else:
        table_dict = load_table_dict_xlsx(fn + '.xlsx')
        save_table_dict_pkl(fn, table_dict)
    return table_dict


def load_table_dict_xlsx(fn):
    if os.path.isfile(fn):
        df = pd.read_excel(fn)
        tmp_dict = df.to_dict()
        table_dict = {}
        for key in tmp_dict:
            curr_dict = tmp_dict[key]
            table_dict[key] = list(curr_dict.values())
        return table_dict
    else:
        raise IOError(f'No such file: {fn}')


def load_table_dict_by_key_xlsx(fn, main_key):
    table_dict = load_table_dict_xlsx(fn)
    table_dict_by_key = {key:{} for key in table_dict}

    for item_id, item in enumerate(table_dict[main_key]):
        for key in table_dict:
            table_dict_by_key[key][item] = table_dict[key][item_id]

    return table_dict_by_key


def load_table_dict_pkl(fn):
    if os.path.isfile(fn):
        f = open(fn, 'rb')
        table_dict = pickle.load(f)
        f.close()
        return table_dict
    else:
        raise IOError(f'No such file: {fn}')

