
class Annotations:

    def __init__(self,
                 name='annotations',
                 type='450k',
                 exclude=None,
                 select_dict=None
                 ):
        self.name = name
        self.type = type
        self.exclude = exclude
        self.select_dict = select_dict

        self.missed_values = ['NA', 'nan']

        self.positive_dict = {}
        self.negative_dict = {}

        if self.select_dict is not None:
            if isinstance(self.select_dict, dict):
                for key, values in self.select_dict.items():
                    if isinstance(values, list):
                        positive_list = []
                        negative_list = []
                        for value in values:
                            if value[0] == '-':
                                negative_list.append(value[1::])
                            else:
                                positive_list.append(value)
                        if len(positive_list) > 0:
                            self.positive_dict[key] = positive_list
                        if len(negative_list) > 0:
                            self.negative_dict[key] = negative_list
                    else:
                        raise ValueError('Each value from Annotations.select_dict.values() must be list')
            else:
                raise ValueError('Annotations.select_dict must be dict')

        if self.type == '450k':
            self.id_name = 'ID_REF'
        elif self.type == 'ht12':
            self.id_name = 'PROBE_ID'
        elif self.type == 'epityper':
            self.id_name = 'ID_REF'
        else:
            raise ValueError('Unsupported annotations type')

    def __str__(self):
        name = 'type(' + self.type + ')' + '_exclude(' + self.exclude + ')'
        if self.select_dict is not None:
            if isinstance(self.select_dict, dict):
                keys = list(self.select_dict.keys())
                keys.sort()
                str_list = []
                for key in keys:
                    values = self.select_dict[key]
                    if isinstance(values, list):
                        values.sort()
                        str_list.append(key + '(' + str(values) + ')')
                    else:
                        raise ValueError('Each value from Annotations.select_dict.values() must be list')
                if len(str_list) > 0:
                    name += '_' + '_'.join(str_list)
            else:
                raise ValueError('Annotations.select_dict must be dict')
        return name
