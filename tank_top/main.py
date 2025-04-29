import datetime
import os
import re

import pandas as pd

#
# from Stitches.ribber import Ribber
# from texts import ribber_to_knit
from getdata import get_measurements, get_stitches_size
# from tank_top_person import Owner
from tanktop import TankTop
from technique import technique


def main():
    name = input('Имя: ')
    measures=None
    file_exists=None
    for file in os.listdir(os.getcwd()):
        if f'{name.title()} tank_top' in file:
            file_exists=True
            measures = [pd.read_csv(file,sep=';', index_col=0)] #->pd.DataFrame
            break
    if measures is None:
        measures = get_measurements(name) #->tuple

    stitches_size = get_stitches_size(name) #->pd.DataFrame
    # print(len(measures))
    tank_top = TankTop(name, stitches_size, measures)
    # print(tank_top.measurements_adjustments)
    if not file_exists:
        tank_top.measurements_adjustments.to_csv(f'{tank_top.name.title()} tank_top.{datetime.date.today()}.csv', sep=';', index=True, encoding='utf-8')
    # print(tank_top.back.main_measures_set)
    # print(tank_top.back.fitted)
    # print(tank_top.back.waist)
    # print(tank_top.back.side_line)
    # print(tank_top.stitches_size)
    # print(f'{tank_top.back.bottom}')
    # print(f'{tank_top.back.armhole}')
    # print(f'{tank_top.back.neck}')
    # print(tank_top.front.main_measures_set)
    # print(tank_top.front.armhole)
    # print(tank_top.front.neck)
    # print(tank_top.front.dart)
    technique(tank_top)



if __name__ == '__main__':
    main()
