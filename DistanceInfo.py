class DistanceInfo(object):

    def __init__(self, object1_index, object2_index, distance_value):
        self.object1_index = object1_index
        self.object2_index = object2_index
        self.distance = distance_value

    def print_distance(self):
        print("first object", self.object1_index, "second object", self.object2_index, "distance", self.distance)