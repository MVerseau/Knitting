from initial_n_utils.person import Person


class Owner(Person):
    measurements = ['waist', 'hips', 'bust', 'back_length_till_waist', 'TBL', 'neck', 'shoulder_width', 'bust_separation',
                    'back_neck_depth', 'front_neck_depth']

    def __init__(self,name, measures):
        super().__init__(name, measures)
