import math
from collections import OrderedDict

import pandas as pd
from initial_n_utils.vocabs import sts_or_row, convert_to_sts
from initial_n_utils.utils import curved_line, concave_line
from Stitches.technique import hem_func


class TankTop:
    main_stitch = ['stockinette']
    adjustments = ['waist', 'hips', 'bust', 'neck']
    technique = ['ribber', 'hem']

    def __init__(self, name, stitches_size, measures):  # TODO: В планах: передавать экземпляр Owner (person)
        self.name = name
        self.measurements_adjustments = self.mes_and_adj_preparation(measures) if len(measures) > 1 else measures[0]
        self.stitches_size = stitches_size
        self.back = Back(self.measurements_adjustments, self.stitches_size)
        self.front = Front(self.measurements_adjustments, self.stitches_size)

    @staticmethod
    def rows_sts(number, row_or_sts, stitches_size, stitch=0):
        '''Конвертирует см в количество рядов/петель
        number: мерка в см
        row_or_sts: row или stitch. Передается в словарь sts_or_row, который содержит название столбцов в pandas.DataFrame self.stitches_size
        stitch: строка в pandas.DataFrame self.stitches_size (актуально, если self.stitches_size содержит более одного вида переплетения'''

        if isinstance(stitch, str):
            stitch = stitches_size[stitch].index
        return number * stitches_size.iloc[stitch][sts_or_row[row_or_sts]]

    def mes_and_adj_preparation(self, args):
        '''Сводит все мерки и моделирование в один DataFrame, подсчитывает суммы по строкам'''
        garment_measurements, garment_adjustments, garment_design = args
        mes_adj = pd.concat([garment_measurements.join(garment_adjustments), garment_design]).rename(
            columns={0: 'design'})
        mes_adj['sum'] = mes_adj.sum(axis=1)
        return mes_adj


    @staticmethod
    def round_to_base(number, base):
        return int(base * (round(number / base)))


    def front(self):
        pass

    def finishing(self):
        pass


class Back:

    def __init__(self, measures, stitches_size, armhole_coef = 1.5):
        self.armhole_coef=armhole_coef
        self.cloth_part=self.__class__.__name__.lower()
        self.main_measures_set = self.back_main_set(measures, stitches_size)
        self.fitted = self.fitted()
        self.waist = self.waist()
        self.side_line = self.side_line()
        self.bottom = self.bottom(stitches_size)
        self.armhole = self.armhole()
        self.neck = self.neck()


    def back_main_set(self, measures, stitches_size):
        '''Основные мерки для спинки'''
        const = measures.loc['ribber'][
            'sum'] if 'ribber' in measures.index else 0
        back_meas = {'TBL': [measures.loc['TBL']['sum'].item()],
                     'back_length_till_waist': [
                         measures.loc['back_length_till_waist']['sum'].item()],
                     'waist': [measures.loc['waist']['sum'].item() / 2],
                     'hips': [measures.loc['hips']['sum'].item() / 2],
                     'bust': [(measures.loc['bust']['measures'].item() + measures.loc['bust'][
                         'adjustments'].item() / 3) / 2],

                     f'{self.cloth_part}_neck_depth': [measures.loc[f'{self.cloth_part}_neck_depth']['sum'].item() +
                                                       measures.loc[f'{self.cloth_part}_neck_lowing']['sum'].item()],
                     'neck_width': [measures.loc['neck']['measures'].item() / 3 + measures.loc['neck'][
                         'adjustments'].item() * 2 + 0.5],
                     'shoulder_width': [measures.loc['shoulder_width']['sum'].item() - const],
                     f'{self.cloth_part}_plain_part': [measures.loc[f'{self.cloth_part}_neck_plain']['sum'].item()],
                     'armhole_height': [measures.loc['bust']['measures'].item() / 6 + 5 + self.armhole_coef +
                                        measures.loc['armscye_lowing']['sum'].item() + const]}

        back_meas['armhole_depth'] = [
            (back_meas['bust'][0] - back_meas['neck_width'][0] - back_meas['shoulder_width'][0] * 2) / 2]
        back_meas['armhole_starts_at'] = [
            back_meas['TBL'][0] - back_meas['armhole_height'][0] + back_meas[f'{self.cloth_part}_neck_depth'][0]]
        back_meas['width'] = [max(back_meas['waist'][0], back_meas['hips'][0], back_meas['bust'][0])]
        if self.cloth_part== 'front':
            back_meas['dart_width']= [back_meas['bust'][0] - measures.loc['lower_bust'][
                'sum'].item() / 2 + 2]
            back_meas['dart_length']= [(back_meas['width'][0] - measures.loc['bust_separation']['sum'].item()) / 2]
            back_meas['bust_height'] = [measures.loc['bust_height']['sum'].item()]
        if 'ribber' in measures.index:
            back_meas['ribber'] = [measures.loc['ribber']['sum'].item()]
            back_meas['armhole_starts_at'] = [back_meas['armhole_starts_at'][0] - back_meas['ribber'][0]]
        else:
            back_meas['hem'] = [measures.loc['hem']['sum'].item()]
            back_meas['armhole_starts_at'] = [back_meas['armhole_starts_at'][0] - back_meas['hem'][0]]

        back = pd.DataFrame.from_dict(back_meas, orient='index', columns=['sm'])

        app_units = OrderedDict()
        units_to_knit = {}
        for i in sorted(back.index):

            if i not in ['fitted', 'dart']: #Возможно, их и нет в back?
                app_units[i] = [
                    TankTop.rows_sts(back.loc[i]['sm'].item(), ['row', 'sts'][i in convert_to_sts], stitches_size)]
                if i not in ['hem', 'ribber', 'armhole_starts_at']:
                    units_to_knit[i] = [int(TankTop.round_to_base(app_units[i][0], 2))]
                elif i in ['hem']:

                    units_to_knit[i] = [round(app_units[i][0])]
                elif i in ['ribber']:
                    app_units[i] = [
                        TankTop.rows_sts(back.loc[i]['sm'].item(), ['row', 'sts'][i in convert_to_sts], stitches_size,
                                         stitch=i)]
                    units_to_knit[i] = [round(app_units[i][0])]
                elif i == 'armhole_starts_at':
                    units_to_knit[i] = [round(app_units[i][0]) - (
                            units_to_knit['armhole_height'][0] - math.floor(app_units['armhole_height'][0]))]

        back = back.join(pd.DataFrame.from_dict(app_units, orient='index', columns=['app_units']))
        back = back.join(pd.DataFrame.from_dict(units_to_knit, orient='index', columns=['units_to_knit']))
        # print(back)
        return back

    def bottom(self, stitches_size):
        half = self.main_measures_set.loc['width']['units_to_knit'].item() // 4
        sts_to_decrease = half + 1
        length = int(TankTop.round_to_base(TankTop.rows_sts(1, 'row', stitches_size), 2) / 2)
        sts_per_row = pd.DataFrame([half] + curved_line(sts_to_decrease, length), index=[i * 2 for i in range(3)],
                                   columns=['bottom']).rename_axis(index='counter')
        return sts_per_row

    def fitted(self):

        lower_length = int(min(round(self.main_measures_set.loc['back_length_till_waist']['units_to_knit'].item() / 2),
                               self.main_measures_set.loc['TBL']['units_to_knit'].item() -
                               self.main_measures_set.loc['hem']['units_to_knit'].item() -
                               self.main_measures_set.loc['back_length_till_waist']['units_to_knit'].item()))

        direct_part = 0
        if lower_length == self.main_measures_set.loc['back_length_till_waist']['units_to_knit'].item() / 2:
            direct_part = int(
                self.main_measures_set.loc['TBL']['units_to_knit'].item() - self.main_measures_set.loc['hem'][
                    'units_to_knit'].item() - self.main_measures_set.loc['back_length_till_waist'][
                    'units_to_knit'].item() - lower_length)
        upper_length = int(self.main_measures_set.loc['armhole_starts_at'][
                               'units_to_knit'].item() - lower_length - direct_part)

        lower_sts_to_decrease = int((self.main_measures_set.loc['hips']['units_to_knit'].item() -
                                     self.main_measures_set.loc['waist']['units_to_knit'].item()) / 2)

        if lower_sts_to_decrease != 0:
            lower_decrease_every_rows = int(
                lower_length // lower_sts_to_decrease)
            lower_rows_remains = lower_length % lower_sts_to_decrease

        else:
            lower_decrease_every_rows = 0
            lower_rows_remains = 0

        upper_sts_to_decrease = int((self.main_measures_set.loc['waist']['units_to_knit'].item() -
                                     self.main_measures_set.loc['bust']['units_to_knit'].item()) / 2)

        if upper_sts_to_decrease != 0:
            upper_decrease_every_rows = int(upper_length // (upper_sts_to_decrease))
            upper_rows_remains = upper_length % (upper_sts_to_decrease)
        else:
            upper_decrease_every_rows = 0
            upper_rows_remains = 0

        waist_line = pd.DataFrame.from_dict(
            {'lower': [direct_part, lower_length, lower_sts_to_decrease, lower_decrease_every_rows, lower_rows_remains],
             'upper': [None, upper_length, upper_sts_to_decrease, upper_decrease_every_rows, upper_rows_remains]},
            orient='index', columns=['direct_part', 'length', 'sts_to_decrease', 'decrease_every_row', 'row_remainder'])
        return waist_line

    def waist(self):

        direct_part, lower_length, lower_sts_to_decrease, lower_decrease_every_row, lower_row_remainder = list(
            map(int, self.fitted.loc['lower']))
        upper_length, upper_sts_to_decrease, upper_decrease_every_row, upper_row_remainder = list(
            map(int, self.fitted.loc['upper'][1:]))

        lower_direct = pd.DataFrame([direct_part], index=['lower_direct_part'], columns=['fitted_waist'], dtype=int)

        lower_curv = pd.DataFrame([1] * (lower_sts_to_decrease),
                                  index=[direct_part + i * lower_decrease_every_row for i in
                                         range(lower_sts_to_decrease)], columns=['fitted_waist'], dtype=int)

        waist = lower_row_remainder + upper_row_remainder if (
                                                                     lower_row_remainder + upper_row_remainder) != 0 else upper_decrease_every_row // 2
        upper = upper_decrease_every_row if (
                                                    lower_row_remainder + upper_row_remainder) != 0 else upper_decrease_every_row - waist

        upper_curv = pd.DataFrame([1] * upper_sts_to_decrease,
                                  index=[lower_curv.index[
                                             -1] + waist + lower_decrease_every_row + i * upper_decrease_every_row for i
                                         in
                                         range(upper_sts_to_decrease)], columns=['fitted_waist'], dtype=int)

        waist = pd.DataFrame([waist + lower_decrease_every_row], index=['knit_directly'], columns=['fitted_waist'],
                             dtype=int)
        upper_direct = pd.DataFrame([upper], index=['upper_direct_part'], columns=['fitted_waist'], dtype=int)
        waist_line = pd.concat([lower_direct, lower_curv, waist, upper_curv, upper_direct], axis=0)

        return waist_line

    def side_line(self):  # если не приталено
        lenght = int(self.fitted['length'].sum())
        sts_to_decrease = int((self.main_measures_set.loc['hips']['units_to_knit'] -
                               self.main_measures_set.loc['bust']['units_to_knit']) / 2)
        decrease_every_row = int(lenght // sts_to_decrease)
        row_remainder = int(lenght % sts_to_decrease) + int(decrease_every_row // 2 + decrease_every_row % 2)
        side_line = pd.DataFrame([self.fitted.loc['lower']['direct_part'] + decrease_every_row // 2],
                                 index=['direct_at_start'],
                                 columns=['not_fitted'], dtype=int)
        curv = pd.DataFrame([1] * sts_to_decrease,
                            index=[int(self.fitted.loc['lower']['direct_part']) + int(i * decrease_every_row) + int(
                                decrease_every_row // 2) for i
                                   in range(sts_to_decrease)], columns=['not_fitted'], dtype=int)
        direct_at_end = pd.DataFrame([row_remainder], index=['direct_at_end'], columns=['not_fitted'], dtype=int)
        side_line = pd.concat([side_line, curv, direct_at_end], axis=0).rename_axis(index=['counter'])

        return side_line

    def armhole(self):

        one_fourth = self.main_measures_set.loc['armhole_depth']['units_to_knit'].item() // 4
        one_time_decrease = int(one_fourth + self.main_measures_set.loc['armhole_depth']['units_to_knit'].item() % 4)
        armhole = pd.DataFrame([one_time_decrease], index=[0], columns=['armhole'])
        for sts in (2, 1, 0.9):
            curv = curved_line(one_fourth, int(one_fourth // round(sts)))
            if sts >= 1:
                mult = 2
            else:
                mult = 3
            part = pd.DataFrame(curv, index=[armhole.index[-1] + mult + i * mult for i in range(len(curv))],
                                columns=['armhole'])
            armhole = pd.concat([armhole, part], axis=0)

        armhole = pd.concat(
            [armhole, pd.DataFrame([armhole['armhole'].sum()], index=['total sts'], columns=['armhole'])],
            axis=0).rename_axis(index=['counter'])

        return armhole

    def neck(self):
        plain_part = self.main_measures_set.loc[f'{self.cloth_part}_plain_part']['units_to_knit'].item() / 2
        neck_curve = (self.main_measures_set.loc['neck_width']['units_to_knit'].item() / 2) - plain_part
        one_fourth = (neck_curve // 4)
        one_time_decrease = one_fourth + neck_curve % 4+plain_part
        number_of_decs = int((self.main_measures_set.loc[f'{self.cloth_part}_neck_depth']['units_to_knit'].item() - 2) // 2)
        neck_line = curved_line(
            self.main_measures_set.loc['neck_width']['units_to_knit'].item() // 2 - one_time_decrease, number_of_decs)
        neck_line = pd.DataFrame([one_time_decrease]+ neck_line, dtype=int, index=[i * 2 for i in range(len(neck_line) + 1)],
                                 columns=['neck']).rename_axis(index=['counter'])
        return neck_line


class Front(Back):

    def __init__(self, measures, stitches_size, armhole_coef = 0):
        super().__init__(measures, stitches_size, armhole_coef)
        self.dart = self.dart() if measures.loc['dart']['sum'].item() == 1 else None
    #
    def dart(self):
        half_dart_width=TankTop.round_to_base(self.main_measures_set.loc['dart_width']['units_to_knit'].item()/2,2)
        number_of_decs=int(half_dart_width/2)
        dart_line_forw=concave_line(self.main_measures_set.loc['dart_length']['units_to_knit'].item(),number_of_decs)
        dart_line_back=dart_line_forw[::-1]
        dart_line_back[0], dart_line_back[-1]=dart_line_back[0]//2, dart_line_back[-1]+dart_line_back[0]//2
        dart_line_forw.extend([i for i in dart_line_back])
        # print(dart_line_back, dart_line_forw)
        dart_line=pd.DataFrame(dart_line_forw, dtype=int, index=[i*2 for i in range(len(dart_line_forw))], columns=['dart']).rename_axis(index=['counter'])
        dart_line['dec/inc']=['dec']*len(dart_line_forw)
        for i in dart_line.index:
            dart_line=dart_line.replace('dec','inc') if i>=len(dart_line_forw) else None


        # dart_line=(dart_line,dart_line[::-1])
        return dart_line

#
    # def neck(self):
    #     plain_part = self.main_measures_set.loc[f'{self.cloth_part}_plain_part']['units_to_knit'].item() / 2
    #     print(plain_part)
    #     neck_curve = (self.main_measures_set.loc['neck_width']['units_to_knit'].item() / 2) - plain_part
    #     one_fourth = (neck_curve // 4)
    #     one_time_decrease = one_fourth + neck_curve % 4
    #     print(one_time_decrease)
    #     number_of_decs = int((self.main_measures_set.loc['front_neck_depth']['units_to_knit'].item() - 2) // 2)
    #     neck_line = curved_line(
    #         self.main_measures_set.loc['neck_width']['units_to_knit'].item() // 2 - one_time_decrease, number_of_decs)
    #     neck_line = pd.DataFrame([plain_part] + neck_line, dtype=int, index=[i * 2 for i in range(len(neck_line) + 1)],
    #                              columns=['neck']).rename_axis(index=['counter'])
    #     return neck_line
