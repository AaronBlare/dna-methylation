import pandas as pd

geo_file_path = 'E:/YandexDisk/pydnameth/script_datasets/GPL21145/'
geo_file_name = 'GPL21145_gsm_table_22_09_20.xlsx'

file = geo_file_path + geo_file_name
table_header = pd.read_excel(file, header=None).iat[0, 0]
df_geo = pd.read_excel(file, header=0)

source_name = list(df_geo['source_name_ch1'])
characteristics = list(df_geo['characteristics_ch1'])
protocol = list(df_geo['extract_protocol_ch1'])

bad_words = ['tumor', 'Tumor', 'fetal', 'Fetal', 'metastasis', 'Metastasis', 'glioma', 'Glioma', 'glioblastoma',
             'Glioblastoma', 'age (in years): -', 'gestational', 'Gestational', 'injury', 'Injury', 'cancer', 'Cancer']
good_words = ['brain', 'Brain', 'neuron', 'Neuron', 'cortex', 'Cortex', 'cerebellum', 'Cerebellum', 'hippocampus',
              'Hippocampus', 'lobe', 'Lobe', 'DLPFC', 'glia', 'Glia', 'gyrus', 'Gyrus', 'astrocyte', 'Astrocyte']

source_name_good_indexes = []
source_name_bad_indexes = []
for i in range(0, len(source_name)):
    item = source_name[i]
    if isinstance(item, str):
        for good_word in good_words:
            if good_word in item:
                for bad_word in bad_words:
                    if bad_word in item:
                        source_name_bad_indexes.append(i)
                        break
                if i in source_name_bad_indexes:
                    break
                source_name_good_indexes.append(i)
                break

characteristics_good_indexes = []
characteristics_bad_indexes = []
for i in range(0, len(characteristics)):
    item = characteristics[i]
    if isinstance(item, str):
        for good_word in good_words:
            if good_word in item:
                for bad_word in bad_words:
                    if bad_word in item:
                        characteristics_bad_indexes.append(i)
                        break
                if i in source_name_bad_indexes or i in characteristics_bad_indexes:
                    break
                characteristics_good_indexes.append(i)
                break

indexes = list(set(source_name_good_indexes + characteristics_good_indexes))
indexes.sort()
df_brain = df_geo.loc[indexes, :]

file_result = geo_file_path + 'brain_03_03_20.xlsx'
writer = pd.ExcelWriter(file_result, engine='xlsxwriter')
df_brain.to_excel(writer, index=False, startrow=0)
worksheet = writer.sheets['Sheet1']
writer.save()

datasets_codes = list(df_brain['series_id'])
datasets = []
for item in datasets_codes:
    codes = item.split(',')
    datasets.extend(codes)
datasets = list(set(datasets))

with open(geo_file_path + 'brain_03_03_20_gse.txt', 'w') as f:
    for item in datasets:
        f.write("%s\n" % item)
