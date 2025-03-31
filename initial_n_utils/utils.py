import re


def check_float(s):
    if s == '':
        s = 0
    return float(s)


def tention_math(tns, arg):  # TODO: Предусмотреть плотность для 2 фонтур
    tentions = {'': 0, '*': 1, '**': 2}
    number = int(re.match(r'\d+', tns).group(0))
    tention = number * 3 + tentions[tns[len(str(number)):]]
    tention = max(min(tention + arg, 30), 0)
    tention = str(tention // 3) + '*' * (tention % 3)
    return tention

def stitch_grammar(stitches):
    if 9 < stitches < 21:
        return 'петель'
    else:
        return ['петель', 'петля', 'петли', 'петли', 'петли', 'петель', 'петель', 'петель', 'петель', 'петель'][
            stitches % 10]


def row_grammar(rows):
    if 5 < rows < 21:
        return 'рядов'
    else:
        return ['рядов', 'ряд', 'ряда', 'ряда', 'ряда', 'рядов', 'рядов', 'рядов', 'рядов', 'рядов'][
            rows % 10]


# print(tention_math('1**', 1))
