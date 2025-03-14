from texts import ribber
from vocabs import stitch_grammar, row_grammar


class Ribber:

    def __init__(self, name: str):
        self.name = name

    @staticmethod  # Временно, т.к. при создании экземпляра элемента одежды будет создаваться и экземпляр резинки
    def two_through_one(stitches, rows):
        if stitches % 3 != 0:
            stitches = (stitches // 3 + 1) * 3
        return ribber.format(stitches, stitch_grammar(stitches), 'NAME', rows, row_grammar(rows))
