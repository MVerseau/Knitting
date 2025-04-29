from texts import hem, start_with_waist_yarn
from initial_n_utils.utils import row_grammar, stitch_grammar
from initial_n_utils.utils import tention_math

def start_func(sts):
    return start_with_waist_yarn.format(int(sts),stitch_grammar(int(sts)))

def hem_func(tention, rows):
    rows = int(rows)
    tention = tention_math(tention, 2)
    return hem.format(tention, rows, row_grammar(rows))




def technique(tank_top):
    # START
    print(start_func(tank_top.back.main_measures_set.loc['width']['units_to_knit']))
    # HEM
    print(hem_func(str(tank_top.stitches_size.iloc[0]['tension']),
                   tank_top.back.main_measures_set.loc['hem']['units_to_knit']))
