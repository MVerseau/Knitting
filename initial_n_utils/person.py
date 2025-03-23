import datetime


class Person:
    def __init__(self, name, measures):
        self.name = name
        self.date = datetime.date.today()
        self.waist = measures.loc['waist'] if not measures.loc['waist'].empty else None
        self.hips = measures.loc['hips'] if not measures.loc['hips'].empty else None
        self.bust = measures.loc['bust'] if not measures.loc['bust'].empty else None
        self.back_length_till_waist = measures.loc['back_length_till_waist'] if not measures.loc[
            'back_length_till_waist'].empty else None
        self.garment_length = measures.loc['garment_length'] if not measures.loc['garment_length'].empty else None
        self.hem = measures.loc['hem'] if not measures.loc['hem'].empty else None
        self.shoulder_width = measures.loc['shoulder_width'] if not measures.loc['shoulder_width'].empty else None
        self.bust_separation = measures.loc['bust_separation'] if not measures.loc['bust_separation'].empty else None
        self.back_neck_depth = measures.loc['back_neck_depth'] if not measures.loc['back_neck_depth'].empty else None
        self.front_neck_depth = measures.loc['front_neck_depth'] if not measures.loc['front_neck_depth'].empty else None

    def __str__(self):
        return f'{self.name} @ {self.date}'
