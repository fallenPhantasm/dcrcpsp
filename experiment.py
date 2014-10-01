from model import *
from solver import *
from heuristics import *
from copy import *

def main():
     activities_list = generate_activity_list(10)
     feasible_sequence =  generate_feasible_sequence(activities_list)
    # print feasible_sequence
    # print solve_SLSQP(feasible_sequence, deepcopy(activities_list))
     print ranking_heuristic(feasible_sequence, deepcopy(activities_list))
     print heuristic_1U(feasible_sequence, deepcopy(activities_list))
     print heuristic_HUDD(feasible_sequence, deepcopy(activities_list))

    #print allocate_resource([1,2,3],[Activity(1,20,1),Activity(2,20,2),Activity(3,20,1)],0.20)

main();