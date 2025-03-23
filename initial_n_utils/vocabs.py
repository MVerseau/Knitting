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

measures_vocab={'waist':'ОТ', 'hips':"ОБ", 'bust':"ОГ", 'back_length_till_waist':"ДИ до талии",'neck': 'ОШ', 'garment_length':"ДИ", 'hem':"Ширина отделки низа", 'shoulder_width':"ШП", 'bust_separation':"ЦГ",
                    'back_neck_depth':"Глубина горловины по спинке (дети: 2-2,5 см, взрослые: 3-3,5 см)", 'front_neck_depth':"Глубина горловины по переду (дети: 5-6 см, взрослые: 7-8 см)", 'armscye_lowing':"Занижение проймы (см)", 'back_neck_plain': "Ровная часть горловины спинки", 'front_neck_plain':"Ровная часть горловины переда", 'back_neck_lowing':"Углубление выреза горловин по спинке", 'front_neck_lowing':"Углубление выреза горловин по переду"}

adjustments_vocab={'waist': 'прибавка к ОТ', 'hips': 'прибавка к ОБ', 'bust': 'прибавка к ОБ', 'neck': 'прибавка к ОШ'}
stitches_size_approach=[' в спокойном состоянии: ',', растянутый вдоль: ',', растянутый поперек: ']