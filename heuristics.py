from model import *
from sympy import *

def heuristic1M(feasible_sequence, activities):
	resource_allocation = []
	for feasible_sequence_part in feasible_sequence:
		resource_allocation_part = []
		for activity_number in feasible_sequence_part:
			resource_allocation_part.append(Rational(1,len(feasible_sequence_part)))
		resource_allocation.append(resource_allocation_part)
	return resource_allocation

def heuristicHUDD(feasible_sequence,activities):
	resource_allocation = []
	activities_counts_dict = {}
	for feasible_sequence_part in feasible_sequence:
		for activity_number in feasible_sequence_part:
			if activity_number in activities_counts_dict:
				activities_counts_dict[activity_number] += 1
			else:
				activities_counts_dict[activity_number] = 1
	print activities_counts_dict

print heuristic1M([[0],[0,1],[2]],[Activity(0,4,2),Activity(1,2,2),Activity(2,2,1)])

