from copy import *
import csv
import time

import solver
from model import *
from heuristics import *


def main():
    activities_list = [10,15,20]
    for activities_number in activities_list:
        firstrow = ["SLSQP", "EA", "1U", "HUDD", "EA-rank", "rank", "group"]
        quality_writer = csv.writer(open("quality{}.csv".format(activities_number), "wb"))
        quality_writer.writerow(firstrow)
        time_writer = csv.writer(open("time{}.csv".format(activities_number), "wb"))
        time_writer.writerow(firstrow)
        for i in range(0, 10):
            print i
            activities_list = generate_activity_list(activities_number)
            for j in range(0, 50):
                feasible_sequence = generate_feasible_sequence(activities_list)

                t1 = time.time()
                solver_result = solver.solve_SLSQP(feasible_sequence, deepcopy(activities_list))
                t2 = time.time()
                end_favoring = heuristic_end_favoring(feasible_sequence, deepcopy(activities_list), 0.8)
                t3 = time.time()
                equal_u = heuristic_1U(feasible_sequence, deepcopy(activities_list))
                t4 = time.time()
                hudd_result = heuristic_HUDD(feasible_sequence, deepcopy(activities_list))
                t5 = time.time()
                end_favoring_ranking = heuristic_ending_favoring_with_ranking(feasible_sequence,
                                                                              deepcopy(activities_list))
                t6 = time.time()
                ranking = heuristic_ranking_based(feasible_sequence, deepcopy(activities_list),
                                                  lambda x: x.processing_rate_coeff,0.5)
                t7 = time.time()
                group_heu = heuristic_group(feasible_sequence, deepcopy(activities_list), 8,
                                            lambda x: x.processing_demand - 10 * x.processing_rate_coeff)
                t8 = time.time()
                experiment_data = []
                experiment_data.append(solver_result)
                experiment_data.append(end_favoring)
                experiment_data.append(equal_u)
                experiment_data.append(hudd_result)
                experiment_data.append(end_favoring_ranking)
                experiment_data.append(ranking)
                experiment_data.append(group_heu)
                quality_writer.writerow(experiment_data)

                time_data = []
                time_data.append(t2 - t1)
                time_data.append(t3 - t2)
                time_data.append(t4 - t3)
                time_data.append(t5 - t4)
                time_data.append(t6 - t5)
                time_data.append(t7 - t6)
                time_data.append(t8 - t7)
                time_writer.writerow(time_data)


main();