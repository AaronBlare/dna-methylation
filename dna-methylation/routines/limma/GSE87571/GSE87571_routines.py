import pandas as pd


def get_line_list(line):
    line_list = line.split('\t')
    for val_id in range(0, len(line_list)):
        line_list[val_id] = line_list[val_id].replace('"', '').rstrip()
    return line_list


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def save_table_dict_xlsx(fn, table_dict):
    fn_xlsx = fn + '.xlsx'
    df = pd.DataFrame(table_dict)
    writer = pd.ExcelWriter(fn_xlsx, engine='xlsxwriter')
    writer.book.use_zip64()
    df.to_excel(writer, index=False)
    writer.save()


path = 'E:/YandexDisk/Work/pydnameth/GSE87571'

f = open(f'{path}/betas.txt')
line = f.readline()
line_list = get_line_list(line)
f.close()

names = line_list[1::]

f = open(f'{path}/observables.txt')
key_line = f.readline()
keys = key_line.split('\t')
keys = [x.rstrip() for x in keys]

observables_dict = {}
for key in keys:
    observables_dict[key] = []

for line in f:
    values = line.split('\t')
    for key_id in range(0, len(keys)):
        key = keys[key_id]
        value = values[key_id].rstrip()
        if is_float(value):
            value = float(value)
            if value.is_integer():
                observables_dict[key].append(int(value))
            else:
                observables_dict[key].append(float(value))
        else:
            observables_dict[key].append(value)
f.close()

observables_dict['geo_accession'] = names

save_table_dict_xlsx(f'{path}/obs', observables_dict)

a = 1
