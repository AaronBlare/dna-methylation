import numpy as np
import pandas as pd
from enum import Enum
from itertools import combinations
from scipy import stats
from sklearn import metrics as metrics
from sklearn.model_selection import ShuffleSplit
from statsmodels import api as sm


class ClockExogType(Enum):
    all = 'all'
    deep = 'deep'
    single = 'single'
    slide = 'slide'


class Clock:
    def __init__(self,
                 endog_data,
                 endog_names,
                 exog_data,
                 exog_names,
                 metrics_dict,
                 train_size,
                 test_size,
                 exog_num,
                 exog_num_comb,
                 num_bootstrap_runs
                 ):
        self.endog_data = endog_data
        self.endog_names = endog_names
        self.exog_data = exog_data
        self.exog_names = exog_names
        self.metrics_dict = metrics_dict
        self.train_size = train_size
        self.test_size = test_size
        self.exog_num = exog_num
        self.exog_num_comb = exog_num_comb
        self.num_bootstrap_runs = num_bootstrap_runs


def build_clock_linreg(clock):
    endog_data = clock.endog_data
    endog_name = clock.endog_names
    exog_data = clock.exog_data
    exog_names = clock.exog_names
    metrics_dict = clock.metrics_dict
    train_size = clock.train_size
    test_size = clock.test_size
    num_bootstrap_runs = clock.num_bootstrap_runs
    exog_num = clock.exog_num
    exog_num_comb = clock.exog_num_comb

    endog_dict = {endog_name: endog_data}
    endog_df = pd.DataFrame(endog_dict)

    if exog_num_comb > exog_num:
        exog_num_comb = exog_num

    exog_ids_all = combinations(list(range(0, exog_num)), exog_num_comb)

    R2_best = 0
    r_best = 0
    evs_best = 0
    mae_best = max(endog_data)

    num_comb = 0
    for exog_ids in exog_ids_all:
        num_comb += 1

        exog_dict = {}
        exog_arg_list = ['const']
        for exog_id in list(exog_ids):
            exog_dict[exog_names[exog_id]] = exog_data[exog_id]
            exog_arg_list += [exog_names[exog_id]]
        exog_df = pd.DataFrame(exog_dict)
        exog_df['const'] = 1

        reg_res = sm.OLS(endog=endog_df[endog_name], exog=exog_df[exog_arg_list]).fit()

        metrics_dict['summary'].append(reg_res.summary())

        rs = ShuffleSplit(num_bootstrap_runs, test_size, train_size)
        indexes = np.linspace(0, len(endog_data) - 1, len(endog_data), dtype=int).tolist()

        R2 = reg_res.rsquared
        r_test = 0.0
        evs_test = 0.0
        mae_test = 0.0

        bootstrap_id = 0
        for train_index, test_index in rs.split(indexes):

            endog_train_dict = {endog_name: list(np.array(endog_data)[train_index])}
            endog_train_df = pd.DataFrame(endog_train_dict)

            exog_train_dict = {}
            for exog_id in list(exog_ids):
                exog_train_dict[exog_names[exog_id]] = np.array(exog_data[exog_id]).T[train_index].T.tolist()
            exog_train_df = pd.DataFrame(exog_train_dict)
            exog_train_df['const'] = 1

            y_test = list(np.array(endog_data)[test_index])

            exog_test_dict = {}
            for exog_id in list(exog_ids):
                exog_test_dict[exog_names[exog_id]] = np.array(exog_data[exog_id]).T[test_index].T.tolist()
            exog_test_df = pd.DataFrame(exog_test_dict)
            exog_test_df['const'] = 1

            model = sm.OLS(endog=endog_train_df[endog_name], exog=exog_train_df[exog_arg_list]).fit()

            y_test_pred = model.get_prediction(exog=exog_test_df[exog_arg_list]).predicted_mean
            slope, intercept, r_value, p_value, std_err = stats.linregress(y_test_pred, y_test)
            r_test += r_value
            evs = metrics.explained_variance_score(y_test, list(y_test_pred))
            mae = metrics.mean_absolute_error(y_test, list(y_test_pred))
            evs_test += evs
            mae_test += mae

            bootstrap_id += 1

        r_test /= float(num_bootstrap_runs)
        evs_test /= float(num_bootstrap_runs)
        mae_test /= float(num_bootstrap_runs)

        if mae_test < mae_best:
            R2_best = R2
            r_best = r_test
            evs_best = evs_test
            mae_best = mae_test

        print('num_comb: ' + str(num_comb))

    metrics_dict['R2'].append(R2_best)
    metrics_dict['r_test'].append(r_best)
    metrics_dict['evs_test'].append(evs_best)
    metrics_dict['mae_test'].append(mae_best)