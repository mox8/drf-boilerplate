import os
from datetime import datetime

import xml.etree.cElementTree as et


def get_n_items_from_iterable(dataset: list, amount: int) -> list:
    if amount <= 1:
        amount = 2
    if len(dataset) < amount:
        return dataset
    step = len(dataset) // (amount - 1)
    index_list = list(range(0, dataset.index(dataset[-1]), step))
    index_list.append(dataset.index(dataset[-1]))
    return list(map(lambda x: dataset[x], index_list))


def is_svg(file):
    file.seek(0)
    tag = None
    try:
        for event, el in et.iterparse(file, ('start',)):
            tag = el.tag
            break
    except et.ParseError:
        pass
    file.seek(0)
    return tag == '{http://www.w3.org/2000/svg}svg'


def get_env_variables_list(env_name: str) -> list:
    env_string = os.environ.get(env_name, '')
    env_string = env_string.replace(' ', '')
    env_list = list(set(list(filter(None, env_string.split(',')))))
    return env_list


class StrColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


def timeit(func):
    def wrapper(*args, **kwargs):
        color_pattern = f'{StrColors.OKGREEN}{StrColors.BOLD} [{func.__name__}] -> '
        start = datetime.now()
        print(f'{color_pattern}Start time: {start.strftime("%H:%M:%S")}{StrColors.ENDC}\n')
        result = func(*args, **kwargs)
        finish = datetime.now()
        print(f'\n{color_pattern}Finish time: {finish.strftime("%H:%M:%S")}{StrColors.ENDC}')
        print(f'{color_pattern}Duration: {finish - start}{StrColors.ENDC}')
        return result
    return wrapper
