import pandas as pd
import pickle
import csv


def save_table_dict_xlsx(fn, table_dict):
    fn_xlsx = fn
    df = pd.DataFrame(table_dict)
    writer = pd.ExcelWriter(fn_xlsx, engine='xlsxwriter')
    writer.book.use_zip64()
    df.to_excel(writer, index=False)
    writer.save()


def save_table_dict_pkl(fn, table_dict):
    fn_pkl = fn
    f = open(fn_pkl, 'wb')
    pickle.dump(table_dict, f, pickle.HIGHEST_PROTOCOL)
    f.close()


def save_table_dict_csv(fn, table_dict):
    fn_csv = fn + '.csv'
    with open(fn_csv, 'w') as csvfile:
        writer = csv.DictWriter(csvfile,
                                fieldnames=table_dict.keys(),
                                lineterminator='\n')
        writer.writeheader()
        for id in range(0, len(list(table_dict.values())[0])):
            tmp_dict = {}
            for key, values in table_dict.items():
                tmp_dict[key] = values[id]
            writer.writerow(tmp_dict)