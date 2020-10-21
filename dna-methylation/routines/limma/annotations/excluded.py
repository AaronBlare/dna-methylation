import os.path
import pickle


def load_excluded(fn):
    exclude_dict = {}

    fn_txt = fn + '.txt'
    fn_pkl = fn + '.pkl'

    if os.path.isfile(fn_pkl):

        f = open(fn_pkl, 'rb')
        exclude_dict = pickle.load(f)
        f.close()

    else:
        f = open(fn_txt)
        exclude_list = f.readlines()
        f.close()
        for x in exclude_list:
            exclude_dict[x.rstrip()] = True

        f = open(fn_pkl, 'wb')
        pickle.dump(exclude_dict, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    return exclude_dict