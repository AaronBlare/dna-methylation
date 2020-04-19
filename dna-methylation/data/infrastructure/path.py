from enum import Enum
import socket
import os


class DataPath(Enum):
    local_1 = 'D:/YandexDisk/Work/pydnameth/script_datasets'
    local_2 = 'E:/YandexDisk/Work/pydnameth/script_datasets'
    local_3 = 'C:/Users/User/YandexDisk/pydnameth/script_datasets'


def get_data_path():
    host_name = socket.gethostname()

    if host_name == 'MSI':
        path = DataPath.local_1.value
    elif host_name == 'DESKTOP-K9VO2TI':
        path = DataPath.local_2.value
    elif host_name == 'DESKTOP-4BEQ7MS':
        path = DataPath.local_3.value
    else:
        raise ValueError("Unsupported host_name: " + host_name)

    return path


def make_dir(path):
    try:
        os.makedirs(path)
        print("Directory ", path, " Created ")
    except FileExistsError:
        print("Directory ", path, " already exists")