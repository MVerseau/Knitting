from texts import ribber
from initial_n_utils.utils import stitch_grammar, row_grammar


class Ribber:

    def __init__(self, name: str):
        self.name = name

    # Каждая резинка - дочерний класс?
    @staticmethod  # Временно, т.к. при создании экземпляра элемента одежды будет создаваться и экземпляр резинки
    def two_through_one(stitches, rows, tention=2):
        name = '2х2 через иглу'
        if stitches % 3 != 0:
            stitches = (stitches // 3 + 1) * 3
        return ribber.format(stitches, stitch_grammar(stitches), name, rows, row_grammar(rows), tention+1)


# class TwoThroughOne(Ribber):
#     name = '2х2 через иглу'
#
#     def __init__(self, stitches, rows, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.stitches = self.stitches_adjustment(stitches) #(stitches // 3 + 1) * 3 if stitches%3!=0 else stitches
#         self.rows = rows
#
#     def stitches_adjustment(self, stitches):
#         if stitches % 3 != 0:
#             return (stitches // 3 + 1) * 3
#         return stitches
#
#     def two_through_one(self):
#         return ribber.format(stitches, stitch_grammar(stitches), name, rows, row_grammar(rows))
