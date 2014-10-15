from copy import *
import solver
from model import *
from heuristics import *
import csv
import time

def main():
    activities_number=10
    firstrow=["-coef","coef","demand","-demand","count","-count","demand*coef","-demand*coef", "ranking_another"]
    quality_writer = csv.writer(open("rank{}.csv".format(activities_number), "wb"))
    quality_writer.writerow(firstrow)
    for i in range(0, 10):
        print i
        activities_list = generate_activity_list(activities_number)
        for j in range(0, 2):

            feasible_sequence = generate_feasible_sequence(activities_list)

            ranking_dem=heuristic_ranking_based(feasible_sequence, deepcopy(activities_list),lambda x: x.processing_demand)
            ranking_demneg=heuristic_ranking_based(feasible_sequence, deepcopy(activities_list),lambda x: -x.processing_demand)
            ranking_coef=heuristic_ranking_based(feasible_sequence, deepcopy(activities_list),lambda x: x.processing_rate_coeff)
            ranking_coefneg=heuristic_ranking_based(feasible_sequence, deepcopy(activities_list),lambda x: -x.processing_rate_coeff)
            ranking_demcoef=heuristic_ranking_based(feasible_sequence, deepcopy(activities_list),lambda x: x.processing_demand*x.processing_rate_coeff)
            ranking_demcoefneg=heuristic_ranking_based(feasible_sequence, deepcopy(activities_list),lambda x: -x.processing_demand*x.processing_rate_coeff)



            ranking_another=another_heuristic_ranking_based(feasible_sequence,deepcopy(activities_list))
            experiment_data=[]
            experiment_data.append(ranking_dem)
            experiment_data.append(ranking_demneg)
            experiment_data.append(ranking_coef)
            experiment_data.append(ranking_coefneg)
            experiment_data.append(ranking_demcoef)
            experiment_data.append(ranking_demcoefneg)
            experiment_data.append(ranking_another)
            quality_writer.writerow(experiment_data)



main();