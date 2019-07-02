import pandas as pd
import csv
from itertools import zip_longest

data_path = 'D:/Aaron/Bio/variance/v2/'
data_files = ['GSE40279.xlsx', 'GSE87571.xlsx', 'EPIC.xlsx', 'GSE55763.xlsx']

data_m = []
data_f = []
data_mean = []
data_min = []
data_max = []
data_area = []
data_i = []

for data_file in data_files:
    print(data_file[:-5])
    curr_data = pd.read_excel(data_path + data_file)
    curr_r2_m = list(curr_data.best_R2_gender_F)
    curr_r2_f = list(curr_data.best_R2_gender_M)
    curr_r2_mean = list(curr_data.r2_mean)
    curr_r2_min = list(curr_data.r2_min)
    curr_r2_max = list(curr_data.r2_max)
    curr_area = list(curr_data.area_intersection_rel_box_common)
    curr_i = list(curr_data.increasing_1_box_common)

    for id in range(0, len(curr_r2_m)):
        if curr_r2_m[id] == -1:
            curr_r2_m[id] = 0.0
        if curr_r2_f[id] == -1:
            curr_r2_f[id] = 0.0
        if curr_r2_mean[id] == -1:
            curr_r2_mean[id] = 0.0
        if curr_r2_min[id] == -1:
            curr_r2_min[id] = 0.0
        if curr_r2_max[id] == -1:
            curr_r2_max[id] = 0.0
        if curr_i[id] == 0:
            curr_i[id] = 1.0

    data_m.append([data_file[:-5]] + curr_r2_m)
    data_f.append([data_file[:-5]] + curr_r2_f)
    data_mean.append([data_file[:-5]] + curr_r2_mean)
    data_min.append([data_file[:-5]] + curr_r2_min)
    data_max.append([data_file[:-5]] + curr_r2_max)
    data_area.append([data_file[:-5]] + curr_area)
    data_i.append([data_file[:-5]] + curr_i)

with open(data_path + "R2_F.csv","w", newline='') as f:
    writer = csv.writer(f)
    for values in zip_longest(*data_f):
        writer.writerow(values)

with open(data_path + "R2_M.csv","w", newline='') as f:
    writer = csv.writer(f)
    for values in zip_longest(*data_m):
        writer.writerow(values)

with open(data_path + "R2_mean.csv","w", newline='') as f:
    writer = csv.writer(f)
    for values in zip_longest(*data_mean):
        writer.writerow(values)

with open(data_path + "R2_min.csv","w", newline='') as f:
    writer = csv.writer(f)
    for values in zip_longest(*data_min):
        writer.writerow(values)

with open(data_path + "R2_max.csv","w", newline='') as f:
    writer = csv.writer(f)
    for values in zip_longest(*data_max):
        writer.writerow(values)

with open(data_path + "Area.csv","w", newline='') as f:
    writer = csv.writer(f)
    for values in zip_longest(*data_area):
        writer.writerow(values)

with open(data_path + "I.csv","w", newline='') as f:
    writer = csv.writer(f)
    for values in zip_longest(*data_i):
        writer.writerow(values)