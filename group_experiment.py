from copy import *
import solver
from model import *
from heuristics import *
import csv
import time

def main():
    activities_numbers=[10,15,20]
    m_list =[3,4,5,6,7,8]
    for activities_number in activities_numbers:
        firstrow=["solv","group+10c","group-10c","group+20c","group-20c"]
        quality_writer = csv.writer(open("group{}.csv".format(activities_number), "wb"))
        quality_writer.writerow(firstrow)
        for i in range(0, 10):
            print i
            activities_list = generate_activity_list(activities_number)
            for j in range(0, 10):
                experiment_data=[]
                feasible_sequence = generate_feasible_sequence(activities_list)
                experiment_data.append(solver.solve_SLSQP(feasible_sequence,deepcopy(activities_list)))
                for m in m_list:
                    experiment_data.append(heuristic_group(feasible_sequence,deepcopy(activities_list),m, lambda x: x.processing_demand + 10*x.processing_rate_coeff))
                    experiment_data.append(heuristic_group(feasible_sequence,deepcopy(activities_list),m, lambda x: x.processing_demand - 10*x.processing_rate_coeff))
                    experiment_data.append(heuristic_group(feasible_sequence,deepcopy(activities_list),m, lambda x: x.processing_demand + 20*x.processing_rate_coeff))
                    experiment_data.append(heuristic_group(feasible_sequence,deepcopy(activities_list),m, lambda x: x.processing_demand - 20*x.processing_rate_coeff))
                quality_writer.writerow(experiment_data)

main();