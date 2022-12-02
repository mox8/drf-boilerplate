def get_n_items_from_iterable(dataset: list, amount: int) -> list:
    if amount <= 1:
        amount = 2
    if len(dataset) < amount:
        return dataset
    step = len(dataset) // (amount - 1)
    index_list = list(range(0, dataset.index(dataset[-1]), step))
    index_list.append(dataset.index(dataset[-1]))
    return list(map(lambda x: dataset[x], index_list))
