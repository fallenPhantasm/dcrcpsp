from copy import *
import solver
from model import *
from heuristics import *
import csv
import time

def main():
    activities_number_list=[10,15,20]

    for activities_number in activities_number_list:

        firstrow=["solv","-coef","coef","demand","-demand","demand*coef","-demand*coef", "ranking_another_dem","ranking_another_coef"]
        percent_list =[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
        quality_writer = csv.writer(open("rank{}.csv".format(activities_number), "wb"))
        quality_writer.writerow(firstrow)
        for i in range(0, 10):
            print i
            activities_list = generate_activity_list(activities_number)
            for j in range(0, 10):

                feasible_sequence = generate_feasible_sequence(activities_list)
                experiment_data=[]
                #experiment_data.append(solver.solve_SLSQP(feasible_sequence,deepcopy(activities_list)))
                for percent in percent_list:
                    ranking_dem=heuristic_ranking_based(feasible_sequence, deepcopy(activities_list),lambda x: x.processing_demand,percent)
                    ranking_demneg=heuristic_ranking_based(feasible_sequence, deepcopy(activities_list),lambda x: -x.processing_demand,percent)
                    ranking_coef=heuristic_ranking_based(feasible_sequence, deepcopy(activities_list),lambda x: x.processing_rate_coeff,percent)
                    ranking_coefneg=heuristic_ranking_based(feasible_sequence, deepcopy(activities_list),lambda x: -x.processing_rate_coeff,percent)
                    ranking_demcoef=heuristic_ranking_based(feasible_sequence, deepcopy(activities_list),lambda x: x.processing_demand*x.processing_rate_coeff,percent)
                    ranking_demcoefneg=heuristic_ranking_based(feasible_sequence, deepcopy(activities_list),lambda x: -x.processing_demand*x.processing_rate_coeff,percent)

                    ranking_another=another_heuristic_ranking_based_demand(feasible_sequence,deepcopy(activities_list),percent)
                    ranking_another2=another_heuristic_ranking_based_coef(feasible_sequence,deepcopy(activities_list),percent)

                    experiment_data.append(ranking_dem)
                    experiment_data.append(ranking_demneg)
                    experiment_data.append(ranking_coef)
                    experiment_data.append(ranking_coefneg)
                    experiment_data.append(ranking_demcoef)
                    experiment_data.append(ranking_demcoefneg)
                    experiment_data.append(ranking_another)
                    experiment_data.append(ranking_another2)
                quality_writer.writerow(experiment_data)

main();