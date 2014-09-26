from model import *
from solver import *
from heuristics import *


def main():
    activities_list = generate_activity_list(10)
    feasible_sequence = generate_feasible_sequence(activities_list)
#    solve_SLSQP(feasible_sequence, activities_list)
    ranking = create_ranking_by_processingrate(activities_list)
    print ranking_heuristic(feasible_sequence, activities_list, ranking)


main();