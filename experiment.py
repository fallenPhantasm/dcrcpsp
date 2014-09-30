from model import *
from solver import *
from heuristics import *
from copy import *

def main():
    activities_list = generate_activity_list(10)
    feasible_sequence =  generate_feasible_sequence(activities_list)
    print feasible_sequence
    print solve_SLSQP(feasible_sequence, deepcopy(activities_list))
    ranking = create_ranking_by_processingrate(activities_list)
    print ranking_heuristic(feasible_sequence, deepcopy(activities_list), ranking)
    print heuristic_1U(feasible_sequence, deepcopy(activities_list))
    print heuristic_HUDD(feasible_sequence, deepcopy(activities_list))


main();