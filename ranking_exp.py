from copy import *
import solver
from model import *
from heuristics import *
import csv
import time

def main():
    activities_number=10
    firstrow=["SLSQP","EA","1U","HUDD","EA-rank","rank","another_rank"]
    quality_writer = csv.writer(open("rank{}.csv".format(activities_number), "wb"))
    quality_writer.writerow(firstrow)
    for i in range(0, 10):
        print i
        activities_list = generate_activity_list(activities_number)
        for j in range(0, 10):
            feasible_sequence = generate_feasible_sequence(activities_list)

            ranking_demand=heuristic_ranking_based(feasible_sequence, deepcopy(activities_list),allocate_resource_by_demand)

            ranking_another=another_heuristic_ranking_based(feasible_sequence,deepcopy(activities_list))
            experiment_data=[]
            experiment_data.append(ranking_demand)
            experiment_data.append(ranking_another)
            quality_writer.writerow(experiment_data)



main();