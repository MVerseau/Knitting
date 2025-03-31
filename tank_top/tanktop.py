import math
from collections import OrderedDict

import pandas as pd
from initial_n_utils.vocabs import sts_or_row, convert_to_sts
from Stitches.technique import hem_func


class TankTop:
    main_stitch = ['stockinette']
    adjustments = ['waist', 'hips', 'bust', 'neck']
    technique = ['ribber', 'hem']

    def __init__(self, name, garment_measurements, garment_adjustments, garment_design,
                 stitches_size):  # TODO: В планах: передавать экземпляр Owner (person)
        self.name = name
        self.measurements_adjustments = self.mes_and_adj_preparation(garment_measurements, garment_adjustments,
                                                                     garment_design)
        self.stitches_size = stitches_size

    def rows_sts(self, number, row_or_sts, stitch=0):
        '''Конвертирует см в количество рядов/петель
        number: мерка в см
        row_or_sts: row или stitch. Передается в словарь sts_or_row, который содержит название столбцов в pandas.DataFrame self.stitches_size
        stitch: строка в pandas.DataFrame self.stitches_size (актуально, если self.stitches_size содержит более одного вида переплетения'''

        if isinstance(stitch, str):
            stitch = self.stitches_size[stitch].index
        return number * self.stitches_size.iloc[stitch][sts_or_row[row_or_sts]]

    def mes_and_adj_preparation(self, garment_measurements, garment_adjustments, garment_design):
        '''Сводит все мерки и моделирование в один DataFrame, подсчитывает суммы по строкам'''

        mes_adj = pd.concat([garment_measurements.join(garment_adjustments), garment_design]).rename(
            columns={0: 'design'})
        mes_adj['sum'] = mes_adj.sum(axis=1)
        return mes_adj

    @staticmethod
    def round_to_base(number, base):
        return int(base * round(number / base))

    def back_main_set(self):
        '''Основные мерки для спинки'''
        back_meas = {'TBL': [self.measurements_adjustments.loc['TBL']['sum'].item()],
                     'back_length_till_waist': [
                         self.measurements_adjustments.loc['back_length_till_waist']['sum'].item()],
                     'waist': [self.measurements_adjustments.loc['waist']['sum'].item() / 2],
                     'hips': [self.measurements_adjustments.loc['hips']['sum'].item() / 2],
                     'bust': [self.measurements_adjustments.loc['bust']['sum'].item() / 2],
                     'neck_depth': [self.measurements_adjustments.loc['back_neck_depth']['sum'].item() +
                                    self.measurements_adjustments.loc['back_neck_lowing']['sum'].item()],
                     'neck_width': [self.measurements_adjustments.loc['neck']['sum'].item()],
                     'shoulder_width': [self.measurements_adjustments.loc['shoulder_width']['sum'].item()],
                     'plain_part': [self.measurements_adjustments.loc['back_neck_plain']['sum'].item()],
                     'armhole_height': [self.measurements_adjustments.loc['bust']['measures'].item() / 6 + 5 + 1.5 +
                                        self.measurements_adjustments.loc['armscye_lowing']['sum'].item()]}

        const = self.measurements_adjustments.loc['ribber'][
            'sum'] if 'ribber' in self.measurements_adjustments.index else 0
        back_meas['armhole_depth'] = [
            max(back_meas['waist'][0], back_meas['hips'][0], back_meas['bust'][0]) - back_meas['neck_width'][0] - (
                    (back_meas['shoulder_width'][0] - const) * 2) / 2]
        back_meas['armhole_starts_at'] = [
            back_meas['TBL'][0] - back_meas['armhole_height'][0] + back_meas['neck_depth'][0]]
        if 'ribber' in self.measurements_adjustments.index:
            back_meas['ribber'] = [self.measurements_adjustments.loc['ribber']['sum'].item()]
            back_meas['armhole_starts_at'] = [back_meas['armhole_starts_at'][0] - back_meas['ribber'][0]]
        else:
            back_meas['hem'] = [self.measurements_adjustments.loc['hem']['sum'].item()]
            back_meas['armhole_starts_at'] = [back_meas['armhole_starts_at'][0] - back_meas['hem'][0]]
        back = pd.DataFrame.from_dict(back_meas, orient='index', columns=['sm'])

        app_units = OrderedDict()
        units_to_knit = {}
        for i in sorted(back.index):
            app_units[i] = [self.rows_sts(back.loc[i]['sm'].item(), ['row', 'sts'][i in convert_to_sts])]
            if i not in ['hem', 'ribber', 'armhole_starts_at']:
                units_to_knit[i] = [int(self.round_to_base(app_units[i][0], 2))]
            elif i in ['hem', 'ribber']:
                units_to_knit[i] = [round(app_units[i][0])]
            elif i == 'armhole_starts_at':
                units_to_knit[i] = [round(app_units[i][0]) - (units_to_knit['armhole_height'][0] - math.floor(app_units['armhole_height'][0]))]

        back = back.join(pd.DataFrame.from_dict(app_units, orient='index', columns=['app_units']))
        back = back.join(pd.DataFrame.from_dict(units_to_knit, orient='index', columns=['units_to_knit']))

        return back

    def front(self):
        pass

    def finishing(self):
        pass
