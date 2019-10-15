from routines.nuage.otu_counts import load_otu_counts
from routines.nuage.subjects import load_subject_info, T0_T1_subject_separation
from tqdm import tqdm
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_validate, cross_val_predict
import plotly
import plotly.graph_objs as go
from scipy.stats import spearmanr


def plot_scatter(x, y, title):
    figure_file_path = 'D:/Aaron/Bio/NU-Age/Figures/'
    trace = go.Scatter(
        x=x,
        y=y,
        mode='lines+markers',
        marker=dict(
            size=8,
            line=dict(
                width=0.5
            ),
            opacity=0.8
        )
    )
    layout = go.Layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        ),
        title=go.layout.Title(
            text=title,
            xref="paper",
            x=0
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text="Number of OTUs",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                )
            ),
            #range=[min(min(x), min(y)) - 5, max(max(x), max(y)) + 5]
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text="MAE",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                )
            ),
            #range=[min(min(x), min(y)) - 5, max(max(x), max(y)) + 5]
        )
    )

    fig = go.Figure(data=trace, layout=layout)

    plotly.offline.plot(fig, filename=figure_file_path + 'scater_' + title + '.html', auto_open=False, show_link=True)
    plotly.io.write_image(fig, figure_file_path + 'scatter_' + title + '.png')
    plotly.io.write_image(fig, figure_file_path + 'scatter_' + title + '.pdf')

def plot_random_forest(x, y, title):
    figure_file_path = 'D:/Aaron/Bio/NU-Age/Figures/'
    trace = go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=dict(
            size=8,
            line=dict(
                width=0.5
            ),
            opacity=0.8
        )
    )
    layout = go.Layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        ),
        title=go.layout.Title(
            text=title,
            xref="paper",
            x=0
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text="Actual adherence",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                )
            ),
            #range=[min(min(x), min(y)) - 5, max(max(x), max(y)) + 5]
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text="Predicted adherence",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                )
            ),
            #range=[min(min(x), min(y)) - 5, max(max(x), max(y)) + 5]
        )
    )

    fig = go.Figure(data=trace, layout=layout)

    plotly.offline.plot(fig, filename=figure_file_path + 'rf_' + title + '.html', auto_open=False, show_link=True)
    plotly.io.write_image(fig, figure_file_path + 'rf_' + title + '.png')
    plotly.io.write_image(fig, figure_file_path + 'rf_' + title + '.pdf')

def plot_heatmap(data, names):
    figure_file_path = 'D:/Aaron/Bio/NU-Age/Figures/'
    trace = go.Heatmap(
        z=[data],
        x=names)

    fig = go.Figure(data=trace)

    plotly.offline.plot(fig, filename=figure_file_path + 'heatmap.html', auto_open=False, show_link=True)
    plotly.io.write_image(fig, figure_file_path + 'heatmap.png')
    plotly.io.write_image(fig, figure_file_path + 'heatmap.pdf')

def plot_hist(data, names, colors, suffix):
    figure_file_path = 'D:/Aaron/Bio/NU-Age/Figures/'
    fig = go.Figure(go.Bar(
        x=data,
        y=names,
        orientation='h',
        marker_color=colors
    ))

    plotly.offline.plot(fig, filename=figure_file_path + suffix + '_hist.html', auto_open=False, show_link=True)
    plotly.io.write_image(fig, figure_file_path + suffix + '_hist.png')
    plotly.io.write_image(fig, figure_file_path + suffix + '_hist.pdf')


data_file_path = 'D:/Aaron/Bio/NU-Age/Data'

fn_subject_info = data_file_path + '/' + 'correct_subject_info.tsv'
subject_info_dict = load_subject_info(fn_subject_info)
T0_subject_dict, T1_subject_dict = T0_T1_subject_separation(subject_info_dict)
fn_otu_counts = data_file_path + '/' + 'OTUcounts.tsv'
otu_counts = load_otu_counts(fn_otu_counts)

subject_row_dict_T0 = otu_counts.subject_row_dict_T0
subject_row_dict_T1 = otu_counts.subject_row_dict_T1

common_otus = list(set(otu_counts.otu_col_dict_T0.keys()).intersection(set(otu_counts.otu_col_dict_T1.keys())))

common_otu_t0 = np.zeros((len(list(subject_row_dict_T0.keys())), len(common_otus)), dtype=np.float32)
common_otu_t1 = np.zeros((len(list(subject_row_dict_T1.keys())), len(common_otus)), dtype=np.float32)

otu_id = 0
otu_col_dict = {}
for key in otu_counts.otu_col_dict_T0:
    if key in otu_counts.otu_col_dict_T1:
        otu_col_dict[key] = otu_id
        common_otu_t0[:, otu_id] = otu_counts.normalized_T0[:, otu_counts.otu_col_dict_T0[key]]
        common_otu_t1[:, otu_id] = otu_counts.normalized_T1[:, otu_counts.otu_col_dict_T1[key]]
        otu_id += 1

adherence_key = 'compliance160'
adherence_key_t0 = 'adherence_t0'
adherence_key_t1 = 'adherence_t1'
adherence_dict = {adherence_key_t0: [], adherence_key_t1: []}

common_subjects = list(set(subject_row_dict_T0.keys()).intersection(set(subject_row_dict_T1.keys())))
subjects_wo_adherence = []
for code in common_subjects:
    index = T0_subject_dict['CODE'].index(code)

    curr_adherence_t0 = T0_subject_dict[adherence_key][index]
    curr_adherence_t1 = T1_subject_dict[adherence_key][index]

    if curr_adherence_t0 == '' or curr_adherence_t1 == '':
        subjects_wo_adherence.append(code)
        continue

    adherence_dict[adherence_key_t0].append(curr_adherence_t0 * 100.0 / 160.0)
    adherence_dict[adherence_key_t1].append(curr_adherence_t1 * 100.0 / 160.0)

if len(subjects_wo_adherence) > 0:
    for elem in subjects_wo_adherence:
        common_subjects.remove(elem)

otu_t0 = np.zeros((len(common_subjects), len(common_otus)), dtype=np.float32)
otu_t1 = np.zeros((len(common_subjects), len(common_otus)), dtype=np.float32)

for sub_id, sub in tqdm(enumerate(common_subjects)):
    curr_otu_t0 = common_otu_t0[subject_row_dict_T0[sub], :]
    curr_otu_t1 = common_otu_t1[subject_row_dict_T1[sub], :]

    otu_t0[sub_id, :] = curr_otu_t0
    otu_t1[sub_id, :] = curr_otu_t1

otu_t0_df = pd.DataFrame(otu_t0, common_subjects, list(otu_col_dict.keys()))
otu_t1_df = pd.DataFrame(otu_t1, common_subjects, list(otu_col_dict.keys()))

clf_t0 = RandomForestRegressor(n_estimators=5, min_samples_split=100)

output_t0 = cross_validate(clf_t0, otu_t0_df, adherence_dict[adherence_key_t0], cv=2, scoring='neg_mean_absolute_error',
                           return_estimator=True)
output_t0_pred = cross_val_predict(clf_t0, otu_t0_df, adherence_dict[adherence_key_t0], cv=2)
accuracy_t0 = np.mean(output_t0['test_score'])
#plot_random_forest(adherence_dict[adherence_key_t0], output_t0_pred, 'T0')

features_dict_t0 = dict((key, []) for key in list(otu_col_dict.keys()))
for idx, estimator in enumerate(output_t0['estimator']):
    feature_importances = pd.DataFrame(estimator.feature_importances_,
                                       index=list(otu_col_dict.keys()),
                                       columns=['importance']).sort_values('importance', ascending=False)

    features_names = list(feature_importances.index.values)
    features_values = list(feature_importances.values)
    for id in range(0, len(features_names)):
        features_dict_t0[features_names[id]].append(features_values[id][0])

for key in features_dict_t0.keys():
    features_dict_t0[key] = np.mean(features_dict_t0[key])
features_dict_t0 = {k: v for k, v in sorted(features_dict_t0.items(), reverse=True, key=lambda x: x[1])}

accuracy_list = []
num_features_list = []
for experiment_id in range(1, 1):
    if experiment_id % 10 == 0:
        print('T0 experiment #', str(experiment_id))
    features_list_len = 5 * experiment_id
    features_list = list(features_dict_t0.keys())[0:features_list_len]
    new_df_t0 = otu_t0_df[features_list].copy()
    clf_t0 = RandomForestRegressor(n_estimators=500, min_samples_split=100)

    output_t0 = cross_validate(clf_t0, new_df_t0, adherence_dict[adherence_key_t0], cv=2,
                               scoring='neg_mean_absolute_error',
                               return_estimator=True)
    output_t0_pred = cross_val_predict(clf_t0, new_df_t0, adherence_dict[adherence_key_t0], cv=2)
    accuracy_t0 = np.mean(output_t0['test_score'])
    accuracy_list.append(accuracy_t0)
    num_features_list.append(features_list_len)
#plot_scatter(num_features_list, accuracy_list, 'T0')

num_features = 0
top_features_t0 = []
top_features_imp_t0 = []
for key in features_dict_t0.keys():
    if num_features < 75:
        top_features_t0.append(key)
        top_features_imp_t0.append(features_dict_t0[key])
        num_features += 1

f = open(data_file_path + '/t0_otus.txt', 'w')
f.write('MAE: ' + str(accuracy_t0) + '\n')
for item in top_features_t0:
    f.write(item + '\n')
f.close()

clf_t1 = RandomForestRegressor(n_estimators=5, min_samples_split=100)

output_t1 = cross_validate(clf_t1, otu_t1_df, adherence_dict[adherence_key_t1], cv=2, scoring='neg_mean_absolute_error',
                           return_estimator=True)
output_t1_pred = cross_val_predict(clf_t1, otu_t1_df, adherence_dict[adherence_key_t1], cv=2)
accuracy_t1 = np.mean(output_t1['test_score'])
#plot_random_forest(adherence_dict[adherence_key_t1], output_t1_pred, 'T1')

features_dict_t1 = dict((key, []) for key in list(otu_col_dict.keys()))
for idx, estimator in enumerate(output_t1['estimator']):
    feature_importances = pd.DataFrame(estimator.feature_importances_,
                                       index=list(otu_col_dict.keys()),
                                       columns=['importance']).sort_values('importance', ascending=False)

    features_names = list(feature_importances.index.values)
    features_values = list(feature_importances.values)
    for id in range(0, len(features_names)):
        features_dict_t1[features_names[id]].append(features_values[id][0])

for key in features_dict_t1.keys():
    features_dict_t1[key] = np.mean(features_dict_t1[key])
features_dict_t1 = {k: v for k, v in sorted(features_dict_t1.items(), reverse=True, key=lambda x: x[1])}

accuracy_list = []
num_features_list = []
for experiment_id in range(1, 1):
    if experiment_id % 10 == 0:
        print('T1 experiment #', str(experiment_id))
    features_list_len = 5 * experiment_id
    features_list = list(features_dict_t1.keys())[0:features_list_len]
    new_df_t1 = otu_t1_df[features_list].copy()
    clf_t1 = RandomForestRegressor(n_estimators=500, min_samples_split=100)

    output_t1 = cross_validate(clf_t1, new_df_t1, adherence_dict[adherence_key_t1], cv=2,
                               scoring='neg_mean_absolute_error',
                               return_estimator=True)
    output_t1_pred = cross_val_predict(clf_t1, new_df_t1, adherence_dict[adherence_key_t1], cv=2)
    accuracy_t1 = np.mean(output_t1['test_score'])
    accuracy_list.append(accuracy_t1)
    num_features_list.append(features_list_len)
#plot_scatter(num_features_list, accuracy_list, 'T1')

num_features = 0
top_features_t1 = []
top_features_imp_t1 = []
for key in features_dict_t1.keys():
    if num_features < 75:
        top_features_t1.append(key)
        top_features_imp_t1.append(features_dict_t1[key])
        num_features += 1

f = open(data_file_path + '/t1_otus.txt','w')
f.write('MAE: ' + str(accuracy_t1) + '\n')
for item in top_features_t1:
    f.write(item + '\n')
f.close()

top_features_merged = list(set(top_features_t0 + top_features_t1))
top_features_intersection_imp = []
for id in range(0, len(top_features_merged)):
    name = top_features_merged[id]
    curr_imp = []
    if name in top_features_t0:
        index_t0 = top_features_t0.index(name)
        imp_t0 = top_features_imp_t0[index_t0]
        curr_imp.append(imp_t0)
    if name in top_features_t1:
        index_t1 = top_features_t1.index(name)
        imp_t1 = top_features_imp_t1[index_t1]
        curr_imp.append(imp_t1)
    if len(curr_imp) == 1:
        top_features_intersection_imp.append(curr_imp[0])
    else:
        top_features_intersection_imp.append(np.mean(curr_imp))

top_features_art = []
otu_file = data_file_path + '/' + 'otu_random_forest.txt'
f = open(otu_file)
for line in f:
    top_features_art.append(line.replace(' \n', ''))
f.close()

top_features_common_with_art = list(set(top_features_merged).intersection(set(top_features_art)))
print('Number of common OTUs: ', str(len(top_features_common_with_art)))

new_df_t0 = otu_t0_df[top_features_merged].copy()
new_df_t1 = otu_t1_df[top_features_merged].copy()
new_df = new_df_t0.append(new_df_t1)
new_adherence = adherence_dict[adherence_key_t0] + adherence_dict[adherence_key_t1]

corr_coeffs = []
for i in range(0, len(top_features_merged)):
    corr_coeff, p_val = spearmanr(list(new_df.iloc[:,i]), new_adherence)
    corr_coeffs.append(corr_coeff)
coeff_range = [min(corr_coeffs), max(corr_coeffs)]

data, names = map(list, zip(*sorted(zip(corr_coeffs, top_features_merged), reverse=False)))
#plot_heatmap(data, list(range(1, len(top_features_int))))

name_list = []
bact_list = []
fn_otus_info = data_file_path + '/' + 'Spingo_classified_TaxaTable.tsv'
f = open(fn_otus_info)
header = f.readline()
for line in f:
    line = line.split('\t')
    name = line[0]
    bact = line[-2]
    name_list.append(name)
    bact_list.append(bact)
f.close()

for name_id in range(0, len(top_features_merged)):
    name = top_features_merged[name_id]
    index = name_list.index(name)
    top_features_merged[name_id] = name + '_' + bact_list[index]

diet_positive_names = []
diet_positive_imp = []
diet_negative_names = []
diet_negative_imp = []
for id in range(0, len(corr_coeffs)):
    curr_coeff = corr_coeffs[id]
    if curr_coeff > 0:
        diet_positive_names.append(top_features_merged[id])
        diet_positive_imp.append(top_features_intersection_imp[id])
    else:
        diet_negative_names.append(top_features_merged[id])
        diet_negative_imp.append(top_features_intersection_imp[id])

diet_positive_imp, diet_positive_names = map(list, zip(*sorted(zip(diet_positive_imp, diet_positive_names), reverse=False)))
colors_positive = ['lightslategray',] * len(diet_positive_names)
for id in range(0, len(diet_positive_names)):
    otu_name_list = diet_positive_names[id].split('_')
    otu_name = otu_name_list[0] + '_' + otu_name_list[1]
    if otu_name in top_features_common_with_art:
        colors_positive[id] = 'crimson'
diet_negative_imp, diet_negative_names = map(list, zip(*sorted(zip(diet_negative_imp, diet_negative_names), reverse=False)))
colors_negative = ['lightslategray',] * len(diet_negative_names)
for id in range(0, len(diet_negative_names)):
    otu_name_list = diet_negative_names[id].split('_')
    otu_name = otu_name_list[0] + '_' + otu_name_list[1]
    if otu_name in top_features_common_with_art:
        colors_negative[id] = 'crimson'
plot_hist(diet_positive_imp, diet_positive_names, colors_positive, 'positive')
plot_hist(diet_negative_imp, diet_negative_names, colors_negative, 'negative')


