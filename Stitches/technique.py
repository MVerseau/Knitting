from texts import hem
from initial_n_utils.utils import row_grammar


def hem_func(tention, rows):
    return hem.format(tention - 2, rows, row_grammar(rows))

def dart():
    pass


# tention = 5
# rows = 5
# print(hem_func(5, 5))
