class DataObject(object):

    def __init__(self, features_list):
        self.features = features_list
        self.first_nominal_feature = features_list[0]
        self.second_nominal_feature = features_list[1]
        self.third_nominal_feature = features_list[2]
        self.ordinal_feature = features_list[3]
        self.absolute_feature = features_list[4]
        self.sum_distance = 0