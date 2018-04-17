from ml_metrics import mapk


def getList(filename):
    with open(filename) as input:
        return [line[:-1].split(',')[1:] for line in input]


print mapk(getList('train_data.csv')[:1000], getList('answer11')[:1000], 3)
