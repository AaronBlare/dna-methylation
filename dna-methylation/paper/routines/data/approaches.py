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
            'GSE40279': 'bf0b9f92e948a257329262816ce3d202',
            'GSE87571': '7c468ca8212428806c727d3e2a836662',
            'EPIC': 'a64c0b99b7e097c668e8300e29ad693f',
            'GSE55763': '01f9edb1330453690b493c5a17624c6c',
            'liver': 'c86106e13eebe67dca94d658cd652860',
            'GSE74193': '9e47f0a1c102e177ac5183455d72d1c4'
        }
    else:
        raise ValueError(f'{dataset.type} is not supported')

    return hash[dataset.name]


def get_approach_4_hash(dataset):
    if dataset.type == 'betas':
        hash = {
            'GSE40279': 'bc82f74dd244bca21ed33d708bd61b85',
            'GSE87571': 'c098dc79338657b0b9c35f55a8441e80',
            'EPIC': '753bc3a13dfb1e22841bb140a3236dad',
            'GSE55763': '635cc3bbde1154509bd4c5a564c7f37d'
        }
    elif dataset.type == 'residuals':
        hash = {
            'GSE40279': '4d1b7f192ea49142732bb2b1374c8ff7',
            'GSE87571': 'fde5819ae46149e63fbea22a9d973f30',
            'EPIC': 'b004131b7d5a5657c26ff68dd22d35da',
            'GSE55763': 'dab3ec0ec397a78a3436c88a4cad6552'
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
            'GSE40279': 'f6796cdb',
            'GSE87571': '960bd640',
            'EPIC': '1a502535',
            'GSE55763': 'fb0b2483',
            'liver': '5c56208b',
            'GSE74193': '3f115b3c'
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
            'GSE55763': 'c7e956c1',
            'liver': 'b1f058b7',
            'GSE74193': '342dd046'
        }
    else:
        raise ValueError(f'{dataset.type} is not supported')

    return hash[dataset.name]

def get_hs_f_hash(dataset):
    if dataset.type == 'betas':
        hash = {
            'GSE40279': '2a12fab5',
            'GSE87571': '25dcc690',
            'EPIC': '8344b456',
            'GSE55763': 'a11d5a4c'
        }
    elif dataset.type == 'residuals':
        hash = {
            'GSE40279': '457bdead',
            'GSE87571': 'eb866188',
            'EPIC': '97c90927',
            'GSE55763': 'c566b57e'
        }
    else:
        raise ValueError(f'{dataset.type} is not supported')

    return hash[dataset.name]

def get_hs_m_hash(dataset):
    if dataset.type == 'betas':
        hash = {
            'GSE40279': '69dc0516',
            'GSE87571': '00f7ba4d',
            'EPIC': '23556bb7',
            'GSE55763': '96e527d6'
        }
    elif dataset.type == 'residuals':
        hash = {
            'GSE40279': 'c0e359de',
            'GSE87571': 'df920bdb',
            'EPIC': '82704c0a',
            'GSE55763': 'e05b4633'
        }
    else:
        raise ValueError(f'{dataset.type} is not supported')

    return hash[dataset.name]