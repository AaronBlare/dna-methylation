import pydnameth as pdm
from scripts.develop.routines import *

data = pdm.Data(
    path='',
    base='unn_epic'
)

data_params = get_data_params(data.base)
data_params['part'] = 'raw'

pdm.betas_horvath_calculator_create_regular(
    data=data,
    data_params=data_params
)
