from copy import *
import solver
from model import *
from heuristics import *
import csv


def main():
    writer = csv.writer(open("experiment.csv", "wb"))
    #for i in range(0, 2):
     #   print i
    activities_list = generate_activity_list(10)
      #  for j in range(0, 3):
    feasible_sequence = generate_feasible_sequence(activities_list)
    solver_result=solver.solve_SLSQP(feasible_sequence,deepcopy(activities_list))
    end_favoring=heuristic_end_favoring(feasible_sequence, deepcopy(activities_list))
    ranking=heuristic_ranking_based(feasible_sequence, deepcopy(activities_list),allocate_resource_by_demand)
    equal_u=heuristic_1U(feasible_sequence, deepcopy(activities_list))
    hudd_result=heuristic_HUDD(feasible_sequence, deepcopy(activities_list))

            # experiment_data=[]
            # experiment_data.append(solver_result)
            # experiment_data.append(end_favoring)
            # experiment_data.append(ranking)
            # experiment_data.append(equal_u)
            # experiment_data.append(hudd_result)
            # writer.writerow(experiment_data)


main();