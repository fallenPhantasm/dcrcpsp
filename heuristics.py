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
	activities_divided_dict = {}
	for key in activities_counts_dict:
		activities_divided_dict[key] = Rational(activities[key].overall_processing_demand, activities_counts_dict[key])
	makespan=0
	for feasible_sequence_part in feasible_sequence:
		makespan_equation = 0
		m = symbols("m",positive=True)
		for activity_number in feasible_sequence_part:
			makespan_equation += (activities_divided_dict[activity_number]/m)**activities[activity_number].processing_function_root
		makespan += solve(makespan_equation -1, m)[0]
	return makespan


print heuristicHUDD([[0],[0,1],[2]],{0:Activity(0,20,2),1:Activity(1,30,2),2:Activity(2,40,1)})

