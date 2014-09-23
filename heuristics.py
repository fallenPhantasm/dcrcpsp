from model import *
from sympy import *

def heuristic_1M(feasible_sequence, activities):
	activity_execution_list = define_execution_order(feasible_sequence)
	activities_completion = [0 for activity in activities]
	sequence_part_duration_list = []
	for ending_activity_number in activity_execution_list:
		ending_activity=activities[ending_activity_number]
		resource_allocation=Rational(1,len(feasible_sequence[activity_execution_list.index(ending_activity_number)]))
		processing_rate=Rational(resource_allocation**Rational(1/ending_activity.processing_rate_coeff))
		sequence_part_duration=Rational(ending_activity.processing_demand/processing_rate)
		for activity_number in feasible_sequence[activity_execution_list.index(ending_activity_number)]:
			activity=activities[activity_number]
			activity.processing_demand-=Rational(sequence_part_duration*Rational(resource_allocation**Rational(1/activity.processing_rate_coeff)))
		sequence_part_duration_list.append(sequence_part_duration)
	last_sequence_duration=0
	for activity in feasible_sequence[-1]:
		last_activity=activities[activity]
		last_processing_rate=Rational(resource_allocation**Rational(1/last_activity.processing_rate_coeff))
		activity_duration=Rational(last_activity.processing_demand/processing_rate)
		last_sequence_duration= max(last_sequence_duration,activity_duration)	
	sequence_part_duration_list.append(last_sequence_duration)
	return sum(sequence_part_duration_list)

def heuristic_1U(feasible_sequence, activities):
	activity_execution_list = define_execution_order(feasible_sequence)
	activities_completion = [0 for activity in activities]
	sequence_part_duration_list = []
	for ending_activites in activity_execution_list:
		sequence_part_duration=0
		for ending_activity_number in ending_activites:
			ending_activity=activities[ending_activity_number]
			resource_allocation=Rational(1,len(feasible_sequence[activity_execution_list.index(ending_activites)]))
			processing_rate=Rational(resource_allocation**Rational(1,ending_activity.processing_rate_coeff))
			sequence_part_duration=max(sequence_part_duration, Rational(ending_activity.processing_demand,processing_rate))
		for activity_number in feasible_sequence[activity_execution_list.index(ending_activites)]:
			activity=activities[activity_number]
			activity.processing_demand-=Rational(sequence_part_duration*Rational(resource_allocation**Rational(1,activity.processing_rate_coeff)))
		sequence_part_duration_list.append(sequence_part_duration)
	last_sequence_duration=0
	for activity in feasible_sequence[-1]:
		last_activity=activities[activity]
		last_processing_rate=Rational((Rational(1,len(feasible_sequence[-1])))**Rational(1,last_activity.processing_rate_coeff))
		print activity,last_activity.processing_demand,last_processing_rate,Rational(1,len(feasible_sequence[-1]))
		activity_duration=Rational(last_activity.processing_demand/last_processing_rate)
		last_sequence_duration= max(last_sequence_duration,activity_duration)	
	sequence_part_duration_list.append(last_sequence_duration)
	print sequence_part_duration_list
	return sum(sequence_part_duration_list)
	


def define_execution_order(feasible_sequence):
	activity_execution_list=[]
	for feasible_sequence_part in feasible_sequence:
		previous_part_index = feasible_sequence.index(feasible_sequence_part) - 1
		if previous_part_index>=0:
			activity_execution_list_part=[]
			for activity_number in feasible_sequence[previous_part_index]:
				if  activity_number not in feasible_sequence_part:
					activity_execution_list_part.append(activity_number)
			activity_execution_list.append(activity_execution_list_part)
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
		activities_divided_dict[key] = Rational(activities[key].processing_demand, activities_counts_dict[key])
	makespan=0
	for feasible_sequence_part in feasible_sequence:
		makespan_equation = 0
		m = symbols("m",positive=True)
		for activity_number in feasible_sequence_part:
			makespan_equation += (activities_divided_dict[activity_number]/m)**activities[activity_number].processing_rate_coeff
		makespan += solve(makespan_equation -1, m)[0]
	return makespan


def ranking_heuristic(feasible_sequence,activities, ranking_list):
	for feasible_sequence_part in feasible_sequence:
		pass
	

	
print heuristic_1U([[1,0],[2,4,3],[2,3]],[Activity(0,20,1),Activity(1,20,1),Activity(2,40,1),Activity(3,40,1),Activity(4,10,1)])
