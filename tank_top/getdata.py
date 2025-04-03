from initial_n_utils.vocabs import measures_vocab, stitches_size_approach, adjustments_vocab
from tank_top_person import Owner
from tanktop import TankTop
import pandas as pd
from initial_n_utils.utils import check_float


def find_measurements(name) -> pd.DataFrame or None:
    try:

        garment_measurements = pd.read_csv(name, sep=';', index_col=0)
        print(f'{name} in the directory')
        return garment_measurements
    except:
        print(f'File {name} is empty')
        print('Файл с мерками пустой или его нет')
        return


def get_design(size) -> pd.DataFrame:
    new_finishing = input('Заменить отделку на резинку (сейчас подгиб)? ')
    if new_finishing.lower() in 'lfда':
        finishing = 'ribber'
    else:
        finishing = 'hem'

    garment_design = {'armscye_lowing': None, 'back_neck_plain': None, 'front_neck_plain': None,
                      'back_neck_lowing': None, 'front_neck_lowing': None, finishing: None}
    print('\nМОДЕЛИРОВАНИЕ')
    for k, v in garment_design.items():
        garment_design[k] = [check_float((input(f'{measures_vocab[k]}: ')))]

    fit = input('Приталенный силуэт? (да/нет): ')
    if fit in 'нетytn':
        garment_design['fitted'] = [0]
    else:
        garment_design['fitted'] = [1]

    if size / 2 >= 54:
        garment_design['dart'] = [1]
    else:
        dart = input('Делать нагрудную вытачку? (да/нет): ')
        if dart in 'ytnнет':
            garment_design['dart'] = [0]
        else:
            garment_design['dart'] = [1]
    # print(garment_design)
    return pd.DataFrame.from_dict(garment_design, orient='index')


def get_measurements(name):  # зачем DataFrames?

    garment_measurements = find_measurements(name.title() + '.csv')  # проверить, достаточно ли мерок в файле
    garment_adjustments = {}

    if garment_measurements is None:
        garment_measurements = {}
        for k in Owner.measurements:
            garment_measurements[k] = [check_float(input(f'{measures_vocab[k]}: '))]
            if k in TankTop.adjustments:
                garment_adjustments[k] = [check_float(input(f'{adjustments_vocab[k]}: '))]

        garment_measurements = pd.DataFrame.from_dict(garment_measurements, orient='index').rename(
            columns={0: 'measures'})
    else:
        for k in TankTop.adjustments:
            garment_adjustments[k] = [check_float(input(f'{adjustments_vocab[k]}: '))]
            if k=='neck':
                garment_adjustments[k]=garment_adjustments[k]*2
    garment_adjustments = pd.DataFrame.from_dict(garment_adjustments, orient='index').rename(
        columns={0: 'adjustments'})
    garment_measurements.to_csv(name.title() + '.csv', sep=';', index=True, encoding='utf-8')

    garment_design = get_design(garment_measurements.loc['bust'].item())

    return garment_measurements, garment_adjustments, garment_design


def set_stitches_size() -> pd.DataFrame:
    print("\nДАННЫЕ ПРОБНИКА")
    stitches_size = pd.DataFrame(columns=['sts in sm', 'rows in sm'])
    # print(stitches_size)
    for st in TankTop.main_stitch:
        tension = input('Плотность (для 2 фонтур указать черзе "/": ')
        stitches = int(input("Количество петель: "))
        rows = int(input("Количество рядов: "))
        sm_in_stitches = 0
        sm_in_rows = 0
        a = 0
        while a < 3:
            sm_in_stitches += float(input(f'См в ширину{stitches_size_approach[a]}: '))
            sm_in_rows += float(input(f"См в длину{stitches_size_approach[a]}: "))
            a += 1
            if input('Следующее измерение? (Y/N) ') not in 'ylд':
                break
        s_size = {'tension': [tension], 'sts in sm': [stitches / (sm_in_stitches / a)],
                  'rows in sm': [rows / (sm_in_rows / a)]}

        stitches_size = pd.concat([stitches_size, pd.DataFrame.from_dict(s_size).rename(index={0: st})])

    return stitches_size


def get_stitches_size(name):
    try:
        stitches_size = pd.read_csv(name.title() + ' stitches_size.csv', sep=';')
    except:
        print('Петельной пробы нет')
        stitches_size = set_stitches_size()
        stitches_size.to_csv(name + ' stitches_size.csv', sep=';', encoding='utf-8')
    return stitches_size
