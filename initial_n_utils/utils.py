import re


def check_float(s):
    if s == '':
        s = 0
    s = s.replace(',', '.')
    return float(s)


def tention_math(tns:str, arg:int):  # TODO: Предусмотреть плотность для 2 фонтур
    tentions = {'': 0, '*': 1, '**': 2}
    number = int(re.match(r'\d+', tns).group(0))
    tention = number * 3 + tentions[tns[len(str(number)):]]
    tention = max(min(tention - arg, 30), 0)
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


def curved_line(sts_to_dec,
                number_of_rows):  # выгнутая линия _/``` например, окат рукава. Когда сначала быстрые убавки, потом маленькие
    base_sts = int(sts_to_dec // number_of_rows)
    sts_remainder = int(sts_to_dec % number_of_rows)
    sts_per_row = [base_sts] * number_of_rows
    sts_to_add = [1] * sts_remainder + [0] * (number_of_rows - sts_remainder)
    sts_per_row = [a + b for a, b in zip(sts_per_row, sts_to_add)]
    return sts_per_row


def concave_line(sts_to_dec,
                 number_of_decs):  # вогнутая линия ___/` например, горловина спинки. Когда сначала маленькие убавки, потом быстрые
    base_sts = int(sts_to_dec // number_of_decs)
    sts_remainder = int(sts_to_dec % number_of_decs)
    sts_per_row = [base_sts] * number_of_decs
    sts_to_add = [0] * (number_of_decs - sts_remainder) + [1] * sts_remainder
    sts_per_row = [a + b for a, b in zip(sts_per_row, sts_to_add)]
    return sts_per_row


# print(tention_math('1**', 1))

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def binary_sort(arr, target):
    if arr[-1] > target:
        left = 0
        right = len(arr)
        while left <= right:
            mid = (left + right) / 2
            if arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        for j in range(target, left, -1):
            return arr[left]
    else:
        return arr[arr.columns[-1]].sum()
