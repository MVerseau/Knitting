import tank_top_person
from initial_n_utils.vocabs import measures_vocab


def get_measurements():
    garment_measurements = {'waist': None, 'hips': None, 'bust': None, 'back_length_till_waist': None,
                            'garment_length': None, 'hem': None, 'shoulder_width': None, 'bust_separation': None,
                            'back_neck_depth': None, 'front_neck_depth': None}
    for k, v in garment_measurements.items():
        garment_measurements[k] = float(input(f'{measures_vocab[k]}: '))
    garment_design = {'armscye_lowing': None, 'back_neck_plain': None, 'front_neck_plain': None,
                      'back_neck_lowing': None, 'front_neck_lowing': None}
    for k, v in garment_design.items():
        garment_design[k] = float(input(f'{measures_vocab[k]}: '))
    return garment_measurements,garment_design



def get_stitches_size():
    pass


get_measurements()
