

measures_vocab = {'waist': 'ОТ', 'hips': "ОБ", 'bust': "ОГ", 'back_length_till_waist': "ДИ до талии", 'neck': 'ОШ',
                  'TBL': "ДИ", 'hem': "Ширина отделки низа (подгиба)", 'shoulder_width': "ШП", 'bust_separation': "ЦГ",
                  'back_neck_depth': "Глубина горловины по спинке (дети: 2-2,5 см, взрослые: 3-3,5 см)",
                  'front_neck_depth': "Глубина горловины по переду (дети: 5-6 см, взрослые: 7-8 см)",
                  'armscye_lowing': "Занижение проймы (см)", 'back_neck_plain': "Ровная часть горловины спинки",
                  'front_neck_plain': "Ровная часть горловины переда",
                  'back_neck_lowing': "Углубление выреза горловин по спинке",
                  'front_neck_lowing': "Углубление выреза горловин по переду",
                  'ribber': 'Ширина резинки'}

adjustments_vocab = {'waist': 'прибавка к ОТ', 'hips': 'прибавка к ОБ', 'bust': 'прибавка к ОГ',
                     'neck': 'прибавка к ОШ'}
stitches_size_approach = [' в спокойном состоянии: ', ', растянутый вдоль: ', ', растянутый поперек: ']
sts_or_row = {'row': 'rows in sm', 'sts': 'sts in sm'}
# convert_to_sts_or_rows={'sts':['width','armhole_depth','neck_width','shoulder_width','plain_part'],'row':['garment_length','back_length_till_waist','hem','ribber', 'armhole_height', 'shoulder_height', 'neck_depth']}
convert_to_sts=['bust','waist','hips','armhole_depth','neck_width','shoulder_width','plain_part','width']