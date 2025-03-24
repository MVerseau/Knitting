from Stitches.ribber import Ribber
from texts import ribber_to_knit
from getdata import get_measurements, get_stitches_size
from tank_top_person import Owner
from garment import Garment


def main():
    name, measurements, garment_adjustments, garment_design = get_measurements()  # DataFrame or str.
    stitches_size = get_stitches_size(name)  # DaraFrame or str
    # print(Ribber.two_through_one(5, 15))
    # print(ribber_to_knit.format(20))
    # print(stitches_size)
    # print(f'{measurements}')
    # print(garment_design)
    # person = Owner(name, measurements) #здесь проверить все необходимые мерки?
    # print(person.measurements)
    # print(garment_adjustments.loc['waist']['adjustments'])
    tank_top = Garment(name, measurements, garment_adjustments, garment_design,
                       stitches_size)
    print(tank_top.stitches_size)
    # print(type(person.waist))


# TODO: to continue from here

if __name__ == '__main__':
    main()
