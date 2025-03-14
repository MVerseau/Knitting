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
