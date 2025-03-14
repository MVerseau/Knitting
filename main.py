from ribber import Ribber
from texts import ribber_to_knit
import os
import pandas as pd



def get_stitches_size():
    stitches_size = 'stitches_size.csv'
    if stitches_size in os.listdir(os.getcwd()):
        try:
            stitches_size = pd.read_csv(stitches_size)
        except pd.errors.EmptyDataError:
            stitches_size = 'Петельной пробы нет'
    else:
        stitches_size = "Петельной пробы нет"
    return stitches_size


def get_measurements():
    measures = 'measures.csv'
    if measures in os.listdir(os.getcwd()):
        try:
            measures = pd.read_csv(measures)
        except pd.errors.EmptyDataError:
            measures = 'Файл с мерками пустой'
    else:
        measures = 'Мерок нет'
    return measures


def main():
    measurements = get_measurements()  # DataFrame or str
    stitches_size = get_stitches_size()  # DaraFrame or str
    print(Ribber.two_through_one(5, 15))
    print(ribber_to_knit.format(20))
    print(stitches_size)
    print(measurements)


if __name__ == '__main__':
    main()
