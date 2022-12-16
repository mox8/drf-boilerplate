import os
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
