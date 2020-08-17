import pydnameth as pdm
from scripts.develop.routines import *

data = pdm.Data(
    path='',
    base='E-MTAB-7309-FILTERED'
)

data_params = get_data_params(data.base)

pdm.betas_horvath_calculator_create_regular(
    data=data,
    data_params=data_params
)
