from model import *
from sympy import *

def heuristic_1M(feasible_sequence, activities):
	activity_execution_list = define_execution_order(feasible_sequence)
	activities_completion = [0 for activity in activities]
	sequence_part_duration_list = []
	for ending_activity_number in activity_execution_list:
		ending_activity=activities[ending_activity_number]
		resource_allocation=Rational(1,len(feasible_sequence[activity_execution_list.index(ending_activity_number)]))
		processing_rate=Rational(resource_allocation**Rational(1/ending_activity.processing_function_root))
		sequence_part_duration=Rational(ending_activity.overall_processing_demand/processing_rate)
		for activity_number in feasible_sequence[activity_execution_list.index(ending_activity_number)]:
			activity=activities[activity_number]
			activity.overall_processing_demand-=Rational(sequence_part_duration*Rational(resource_allocation**Rational(1/activity.processing_function_root)))
		sequence_part_duration_list.append(sequence_part_duration)
	last_sequence_duration=0
	for activity in feasible_sequence[-1]:
		last_activity=activities[activity]
		last_processing_rate=Rational(resource_allocation**Rational(1/last_activity.processing_function_root))
		activity_duration=Rational(last_activity.overall_processing_demand/processing_rate)
		last_sequence_duration= max(last_sequence_duration,activity_duration)	
	sequence_part_duration_list.append(last_sequence_duration)
	return sum(sequence_part_duration_list)
	


def define_execution_order(feasible_sequence):
	activity_execution_list=[]
	for feasible_sequence_part in feasible_sequence:
		previous_part_index = feasible_sequence.index(feasible_sequence_part) - 1
		if previous_part_index>=0:
			
			for activity_number in feasible_sequence[previous_part_index]:
				# print activity_number , feasible_sequence[previous_part_index], feasible_sequence_part
				if  activity_number not in feasible_sequence_part:
					activity_execution_list.append(activity_number)
	return activity_execution_list

def heuristic_HUDD(feasible_sequence,activities):
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

print heuristic_1M([[0,1],[1,2],[2]],[Activity(0,40,1),Activity(1,50,1),Activity(2,20,1)])
