from copy import *
import solver
from model import *
from heuristics import *
import csv
import time

def main():
    activities_number=10
    firstrow=["ea10,ea20,ea30,ea40,ea50,ea60,ea70,ea80,ea90"]
    percent_list =[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    quality_writer = csv.writer(open("ea-tuning{}.csv".format(activities_number), "wb"))
    quality_writer.writerow(firstrow)
    for i in range(0, 10):
        print i
        activities_list = generate_activity_list(activities_number)
        for j in range(0, 10):

            experiment_data=[]
            feasible_sequence = generate_feasible_sequence(activities_list)
            for percent in percent_list:
                experiment_data.append(heuristic_end_favoring(feasible_sequence,deepcopy(activities_list),percent))
            quality_writer.writerow(experiment_data)

main();