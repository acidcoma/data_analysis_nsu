import math

from DataObject import DataObject
from DistanceInfo import DistanceInfo


class Analyser:

    def __init__(self, dataframe):
        self.absolute_maximum = max(dataframe.iloc[:,4])
        self.absolute_minimum = min(dataframe.iloc[:,4])
        self.pre_ordinal_list = set(dataframe.iloc[:,3])
        self.nominal_list_first = dataframe.iloc[:,0]
        self.nominal_list_second = dataframe.iloc[:,1]
        self.nominal_list_third = dataframe.iloc[:,2]
        objects_list = []
        all_features_list = dataframe.values.tolist()
        for object_features in all_features_list:
            data_object = DataObject(object_features)
            objects_list.append(data_object)
        self.objects_list = objects_list
        self.ordinal_list = []
        self.distances = []
        self.distances_matrix = []
        # print(self.absolute_maximum, self.absolute_minimum)

    def form_ordinal_list(self):
        print("Existing ordinal values:", self.pre_ordinal_list)
        print("Choose the order of ordinal values. For this, list them with commas please:")
        print("Выберите порядок ординальных значений. Для этого перечислите их через запятую, пожалуйста:")
        print("Example of input:value1, value2, value3, value4, value5, ... valueN")
        order = []
        input_str = input().split(", ")
        for i in input_str:
            order.append(i)
        self.ordinal_list = order
        print("Now the order is: ", self.ordinal_list, "\n")

    @staticmethod
    # сильная шкала
    def calculate_absolute_measure(value1, value2, max, min):
        norm = (math.fabs(value1 - value2))/(max - min)
        return norm

    @staticmethod
    # шкала порядка
    def calculate_ordinal_measure(value1, value2, values_list):
        # if value1 == "mass market":
        #     value1_ind = 1
        # elif value1 == "middle":
        #     value1_ind = 2
        # else:
        #     value1_ind = 3
        #
        # if value2 == "mass market":
        #     value2_ind = 1
        # elif value2 == "middle":
        #     value2_ind = 2
        # else:
        #     value2_ind = 3
        norm = 0
        n = len(values_list)
        value1_ind = values_list.index(value1) #порядковое значение -> его иденкс в упорядоченном списке порядквых значений
        value2_ind = values_list.index(value2)
        # for k in [1, 2, 3]:
        for k in range(n):
            if (value1_ind < k and value2_ind < k) or (value1_ind > k and value2_ind > k) or (value1_ind == k) & (k == value2_ind):
                norm += 0
            elif (value1_ind < k and value2_ind > k) or (value1_ind > k and value2_ind < k):
                norm += 1
            elif (value1_ind == k and (value2_ind < k or value2_ind > k)) or ((value1_ind < k or value1_ind > k) and value2_ind == k):
                norm += 0.5
            else:
                print("error")

        result_norm = 0.5 * norm
        return result_norm

    @staticmethod
    # шкала наименований
    def calculate_nominal_measure(value1, value2, all_values_list):
        norm = 0
        for value in all_values_list:
            if (value1 == value and value2 == value) or (value1 != value and value2 != value):
                norm += 0
            elif (value1 == value and value2 != value) or (value1 != value and value2 == value):
                norm += 1
            else:
                print("error")
        result_norm = 1/10 * norm
        return result_norm

    @staticmethod
    # общее расстояние
    def calculate_distance_between_objects(self):
        for i in range(9):
            for j in range(i, 10):
                object1 = self.objects_list[i]
                object2 = self.objects_list[j]
                absolute_norm = Analyser.calculate_absolute_measure(object1.absolute_feature,
                                                                    object2.absolute_feature,
                                                                    self.absolute_maximum,
                                                                    self.absolute_minimum)
                ordinal_norm = Analyser.calculate_ordinal_measure(object1.ordinal_feature, object2.ordinal_feature, self.ordinal_list)
                nominal_norm_first = Analyser.calculate_nominal_measure(object1.first_nominal_feature,
                                                                        object2.first_nominal_feature,
                                                                        self.nominal_list_first)
                nominal_norm_second = Analyser.calculate_nominal_measure(object1.second_nominal_feature,
                                                                         object2.second_nominal_feature,
                                                                         self.nominal_list_second)
                nominal_norm_third = Analyser.calculate_nominal_measure(object1.third_nominal_feature,
                                                                        object2.third_nominal_feature,
                                                                        self.nominal_list_third)
                distance = (1 / math.sqrt(10)) * math.sqrt(
                    absolute_norm ** 2 + ordinal_norm ** 2 + nominal_norm_first ** 2
                    + nominal_norm_second ** 2 + nominal_norm_third ** 2)
                distance = float("%.2f" % distance)
                distance_info = DistanceInfo(self.objects_list.index(object1)+1, self.objects_list.index(object2)+1,
                                             distance)
                self.distances.append(distance_info)

    def print_triples(self):
        for triple in self.distances:
            triple.print_distance()

    def make_and_print_distances_matrix(self):
        matrix = [[0.00 for a in range(11)] for b in range(11)]
        matrix[0][0] = " "

        for x in range(1, 11):
            matrix[x][0] = str(x)
        for y in range(1, 11):
            matrix[0][y] = str(y) + " "

        for d in self.distances:
            i = d.object1_index
            j = d.object2_index
            val = d.distance
            matrix[i][j] = val
            matrix[j][i] = val

        self.distances_matrix = matrix
        print("\n Distances matrix: \n")
        for row in matrix:
            print(row)

    def calculate_sum_distances(self):
        for z in range(9):
            for d in self.distances:
                if (d.object1_index-1) == z:
                    sum_d = 0
                    i = d.object1_index - 1
                    sum_d += d.distance
                    for x in range(i + 1, 10 + i):
                        sum_d += self.distances[x].distance
                    sum_d = float("%.2f" % sum_d)
                    self.objects_list[i].sum_distance = sum_d
                    i = 0
                    z += 1

        # for 10th object
        sum_d_for_last = 0
        for dis in self.distances:
            if dis.object2_index == 10:
                sum_d_for_last += dis.distance
        sum_d_for_last = float("%.2f" % sum_d_for_last)
        self.objects_list[9].sum_distance = sum_d_for_last

        sum_distances_list = []
        for obje in self.objects_list:
            sum_distances_list.append(obje.sum_distance)
            print("\n Sum distance for object number", self.objects_list.index(obje)+1, "is: ", obje.sum_distance)

        number = 0
        min_distance = 0
        for q in self.objects_list:
                if q.sum_distance == min(sum_distances_list):
                   number = self.objects_list.index(q)+1
                   min_distance = q.sum_distance

        print("\n RESULT: the closest to all other objects is the object number", number, "with sum distance =", min_distance)
        print("\n")

    def calculate_distance_between_nominal_features(self):
        norm_between_first_and_second = 0
        norm_between_first_and_third = 0
        norm_between_second_and_third = 0

        for i in range(10):
            for j in range(10):
                object1 = self.objects_list[i]
                object2 = self.objects_list[j]

                if (object1.first_nominal_feature == object2.first_nominal_feature
                    and object1.second_nominal_feature == object2.second_nominal_feature) or (object1.first_nominal_feature != object2.first_nominal_feature
                                                                                              and object1.second_nominal_feature != object2.second_nominal_feature):
                    norm_between_first_and_second += 0
                elif (object1.first_nominal_feature == object2.first_nominal_feature
                    and object1.second_nominal_feature != object2.second_nominal_feature) or (object1.first_nominal_feature != object2.first_nominal_feature
                                                                                              and object1.second_nominal_feature == object2.second_nominal_feature):
                    norm_between_first_and_second += 1
                else:
                    print("error")

                if (object1.first_nominal_feature == object2.first_nominal_feature
                    and object1.third_nominal_feature == object2.third_nominal_feature) or (object1.first_nominal_feature != object2.first_nominal_feature
                                                                                              and object1.third_nominal_feature != object2.third_nominal_feature):
                    norm_between_first_and_third += 0
                elif (object1.first_nominal_feature == object2.first_nominal_feature
                    and object1.third_nominal_feature != object2.third_nominal_feature) or (object1.first_nominal_feature != object2.first_nominal_feature
                                                                                              and object1.third_nominal_feature == object2.third_nominal_feature):
                    norm_between_first_and_third += 1
                else:
                    print("error")

                if (object1.second_nominal_feature == object2.second_nominal_feature
                    and object1.third_nominal_feature == object2.third_nominal_feature) or (object1.second_nominal_feature != object2.second_nominal_feature
                                                                                              and object1.third_nominal_feature != object2.third_nominal_feature):
                    norm_between_second_and_third += 0
                elif (object1.second_nominal_feature == object2.second_nominal_feature
                    and object1.third_nominal_feature != object2.third_nominal_feature) or (object1.second_nominal_feature != object2.second_nominal_feature
                                                                                              and object1.third_nominal_feature == object2.third_nominal_feature):
                    norm_between_second_and_third += 1
                else:
                    print("error")

        coefficient = 1/45
        norm_between_first_and_second = float("%.2f" % (norm_between_first_and_second * coefficient))
        norm_between_first_and_third = float("%.2f" % (norm_between_first_and_third * coefficient))
        norm_between_second_and_third = float("%.2f" % (norm_between_second_and_third * coefficient))
        list_of_features_distances = []
        list_of_features_distances.append(norm_between_first_and_second)
        list_of_features_distances.append(norm_between_first_and_third)
        list_of_features_distances.append(norm_between_second_and_third)

        print(" Distance between first nominal feature and second is: ", norm_between_first_and_second)
        print("\n Distance between first nominal feature and third is: ", norm_between_first_and_third)
        print("\n Distance between second nominal feature and third is: ", norm_between_second_and_third)

        min_distance = min(list_of_features_distances)
        second_min_distance = 0
        list_of_features_distances.remove(min(list_of_features_distances))
        for d in list_of_features_distances:
            if d == min_distance:
                second_min_distance = d

        if min_distance == norm_between_first_and_second:
            z = "first and second"
            if second_min_distance == norm_between_first_and_third:
                h = "first and third"
            else:
                h = "second and third"
        elif min_distance == norm_between_first_and_third:
            z = "first and third"
            if second_min_distance == norm_between_first_and_second:
                h = "first and second"
            else:
                h = "second and third"
        else:
            z = "second and third"
            if second_min_distance == norm_between_first_and_second:
                h = "first and second"
            else:
                h = "first and third"

        print("\n RESULT: The closest nominal features are", z, ". Distance between them =", min_distance)
        if second_min_distance != 0:
            print("\n AAAND also there are nominal features with identical distance!", h)