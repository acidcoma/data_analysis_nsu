import pandas as pd

from Analyser import Analyser

if __name__ == '__main__':
    dataframe = pd.read_csv('data.csv')
    analyser = Analyser(dataframe)
    #analyser.form_ordinal_list()
    Analyser.calculate_distance_between_objects(analyser)
    analyser.print_triples()
    analyser.make_and_print_distances_matrix()
    analyser.calculate_sum_distances()
    analyser.calculate_distance_between_nominal_features()
