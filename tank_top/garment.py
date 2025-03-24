import pandas as pd
from initial_n_utils.vocabs import sts_or_row


class Garment:
    main_stitch = ['stockinette']
    adjustments = ['waist', 'hips', 'bust', 'neck']

    def __init__(self, name, garment_measurements, garment_adjustments, garment_design, stitches_size):
        self.name = name
        self.measurements_adjustments = pd.concat(
            [garment_measurements.join(garment_adjustments), garment_design]).rename(columns={0: 'design'})
        self.stitches_size = stitches_size
        # for a in garment_adjustments.index:
        #     setattr(self, a + '_adj', garment_adjustments.loc[a]['adjustments'])

    def rows_sts(self, number, row_or_sts, stitch=0):
        if isinstance(stitch, str):
            stitch = self.stitches_size[stitch].index
        return number * self.stitches_size.iloc[stitch][sts_or_row[row_or_sts]]

    # Возможность"на лету" менять мерки, прибавки, дизайн
