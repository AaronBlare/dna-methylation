import os.path
import pickle


def load_annotations_dict(fn):
    fn_txt = fn + '.txt'
    fn_pkl = fn + '.pkl'

    if os.path.isfile(fn_pkl):

        f = open(fn_pkl, 'rb')
        annotations_dict = pickle.load(f)
        f.close()

    else:

        f = open(fn_txt)
        key_line = f.readline()
        keys = key_line.split('\t')
        keys = [x.rstrip() for x in keys]

        annotations_dict = {}
        for key in keys:
            annotations_dict[key] = []

        for line in f:
            values = line.split('\t')
            for key_id, key in enumerate(keys):
                values_for_key = values[key_id].rstrip()
                if values_for_key == '':
                    annotations_dict[key].append([])
                else:
                    values_for_key = values_for_key.split(';')
                    values_for_key = list(set(values_for_key))
                    annotations_dict[key].append(values_for_key)
        f.close()

        f = open(fn_pkl, 'wb')
        pickle.dump(annotations_dict, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    return annotations_dict