def get_approach_1_hash(dataset):
    if dataset.type == 'betas':
        hash = {
            'GSE40279': '7875dff3886829397f5fbbbf9aaae009',
            'GSE87571': '8c357499960c0612f784ca7ed3fedb2c',
            'EPIC': '23298d48a2fbeb252cfdcb90cfa004a3',
            'GSE55763': '67553bd9c9801d1eeeba0dc2776db156'
        }
    else:
        raise ValueError(f'{dataset.type} is not supported')

    return hash[dataset.name]


def get_approach_3_hash(dataset):
    if dataset.type == 'residuals':
        hash = {
            'GSE40279': 'd7d1e0acca27c1974c16942a917320ac',
            'GSE87571': 'c859f04f18c43296cb61b3151ab53adc',
            'EPIC': '7adee9f94aa1dee9e79cc1dbfe940ae6',
            'GSE55763': '1350b1840f9c4bd1cf72023195a29fde'
        }
    else:
        raise ValueError(f'{dataset.type} is not supported')

    return hash[dataset.name]


def get_linreg_female_hash(dataset):
    if dataset.type == 'betas':
        hash = {
            'GSE40279': '6e5e9526',
            'GSE87571': '31efe635',
            'EPIC': '7383db3e',
            'GSE55763': '6a7442e0'
        }
    else:
        raise ValueError(f'{dataset.type} is not supported')

    return hash[dataset.name]


def get_linreg_male_hash(dataset):
    if dataset.type == 'betas':
        hash = {
            'GSE40279': '40e12959',
            'GSE87571': '3dd80109',
            'EPIC': '191c0e80',
            'GSE55763': '0a75a8f8'
        }
    else:
        raise ValueError(f'{dataset.type} is not supported')

    return hash[dataset.name]


def get_polygon_hash(dataset):
    if dataset.type == 'betas':
        hash = {
            'GSE40279': 'ebc9f2bd',
            'GSE87571': 'c5e6999a',
            'EPIC': 'f410e129',
            'GSE55763': 'fa723546'
        }
    else:
        raise ValueError(f'{dataset.type} is not supported')

    return hash[dataset.name]


def get_ss_hash(dataset):
    if dataset.type == 'residuals':
        hash = {
            'GSE40279': 'd794817d',
            'GSE87571': 'c4a8606d',
            'EPIC': 'c2355c6e',
            'GSE55763': 'f3a53c1a'
        }
    else:
        raise ValueError(f'{dataset.type} is not supported')

    return hash[dataset.name]


def get_ar_hash(dataset):
    if dataset.type == 'residuals':
        hash = {
            'GSE40279': '5c6afd44',
            'GSE87571': '6af05523',
            'EPIC': '018fad6b',
            'GSE55763': 'c7e956c1'
        }
    else:
        raise ValueError(f'{dataset.type} is not supported')

    return hash[dataset.name]