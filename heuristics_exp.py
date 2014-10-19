from copy import *
import csv
import time

import solver
from model import *
from heuristics import *


def main():
    activities_list = [60,80,100,120,140,200,300,500]
    for activities_number in activities_list:
        firstrow = ["HUDD", "EA", "1U", "EA-rank", "rank", "group"]
        quality_writer = csv.writer(open("final{}.csv".format(activities_number), "wb"))
        quality_writer.writerow(firstrow)
        for i in range(0, 10):
            print i
            activities_list = generate_activity_list(activities_number)
            for j in range(0, 50):
                feasible_sequence = generate_feasible_sequence(activities_list)

                hudd_result = heuristic_HUDD(feasible_sequence, deepcopy(activities_list))
                end_favoring = heuristic_end_favoring(feasible_sequence, deepcopy(activities_list), 0.8)
                equal_u = heuristic_1U(feasible_sequence, deepcopy(activities_list))
                end_favoring_ranking = heuristic_ending_favoring_with_ranking(feasible_sequence,
                                                                              deepcopy(activities_list))
                ranking = heuristic_ranking_based(feasible_sequence, deepcopy(activities_list),
                                                  lambda x: x.processing_rate_coeff,0.5)
                group_heu = heuristic_group(feasible_sequence, deepcopy(activities_list), 8,
                                            lambda x: x.processing_demand - 10 * x.processing_rate_coeff)
                experiment_data = []
                experiment_data.append(end_favoring)
                experiment_data.append(equal_u)
                experiment_data.append(hudd_result)
                experiment_data.append(end_favoring_ranking)
                experiment_data.append(ranking)
                experiment_data.append(group_heu)
                quality_writer.writerow(experiment_data)




main();