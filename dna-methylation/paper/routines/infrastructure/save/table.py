import pandas as pd
import pickle
import os


def save_table_dict_xlsx(fn, table_dict, is_rewrite=True):
    fn_xlsx = fn + '.xlsx'
    if not is_rewrite:
        if os.path.exists(fn_xlsx):
            is_save = False
        else:
            is_save = True
    else:
        is_save = True

    if is_save:
        df = pd.DataFrame(table_dict)
        writer = pd.ExcelWriter(fn_xlsx, engine='xlsxwriter')
        writer.book.use_zip64()
        df.to_excel(writer, index=False)
        writer.save()

def save_table_dict_pkl(fn, table_dict):
    fn_pkl = fn + '.pkl'
    f = open(fn_pkl, 'wb')
    pickle.dump(table_dict, f, pickle.HIGHEST_PROTOCOL)
    f.close()
