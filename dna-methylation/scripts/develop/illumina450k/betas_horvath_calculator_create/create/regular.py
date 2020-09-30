import pydnameth as pdm
from scripts.develop.routines import *

data = pdm.Data(
    path='E:/YandexDisk/Work/pydnameth/tissues/brain(DLPFC)',
    base='GSE74193'
)

data_params = get_data_params(data.base)

pdm.betas_horvath_calculator_create_regular(
    data=data,
    data_params=data_params
)
