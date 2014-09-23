from sympy import *
from random import *
from copy import *
import time
from scipy.optimize import minimize
from heuristics import *

class Activity:
    def __init__(self, id, processing_demand, processing_rate_coeff, resource_demands, predecessors, successors):
        self.id = id
        self.processing_demand = processing_demand
        self.processing_rate_coeff = processing_rate_coeff
        self.resource_demands = resource_demands
        self.predecessors  = predecessors
        self.successors = successors

def makeLambda(demand_part_tuple, constraint, processing_demand):
		constraint-=processing_demand
		l = lambdify(flatten(demand_part_tuple),constraint)
		return lambda x :l(*x)

def generate_activity_list(how_many):
	activity_list=[]
	for i in range(0,how_many):
		activity_list.append(Activity(i,randint(30,100),randint(1,2),None,None,None))
	return activity_list

def generate_feasible_sequence(activity_list,machines_number):
	feasible_sequence=[]
	feasible_sequence_part=[]
	activities_numbers=range(0,len(activity_list))

	for i in range(0,randint(1,machines_number)):
		feasible_sequence_part.append(activities_numbers.pop(0))
	feasible_sequence.append(feasible_sequence_part)
	

	while len(feasible_sequence_part) > 1 or len(activities_numbers)!=0:
		new_feasible_sequence_part= copy(feasible_sequence_part)
		if len(new_feasible_sequence_part) > 0 :
			new_feasible_sequence_part.pop(randint(0,len(new_feasible_sequence_part)-1))
			
			for i in range(randint(1,machines_number-len(new_feasible_sequence_part))):
				if len(activities_numbers) > 0:
					new_feasible_sequence_part.append(activities_numbers.pop(0))
		feasible_sequence.append(new_feasible_sequence_part)
		feasible_sequence_part=new_feasible_sequence_part
	return feasible_sequence

def main():
	activity_list = generate_activity_list(15)
	activity_numbers = range(0,len(activity_list))

	print activity_list
	feasible_sequence = generate_feasible_sequence(activity_list,2)
	print feasible_sequence
	
	solution_list = []
	demand_part_tuple = ()
	demand_part_list = []
	constraints_dict = { x:0 for x in range(0,len(activity_list))}
	demand_part_counter=0

	for feasible_sequence_part in feasible_sequence:
		minimal_length_part_equation = 0 
		sequence_part_number = feasible_sequence.index(feasible_sequence_part)
		length_symbol = symbols("M{}".format(sequence_part_number), positive=True)
		 #Creating equations for calculating minimal sequence part duration
		for activity_number in feasible_sequence_part:
			demand_part = symbols("x_{}_{}".format(activity_number,sequence_part_number),positive=True)
			demand_part_list.append(demand_part)
			demand_part_counter+=1
			constraints_dict[activity_number]+=demand_part
			if (len(demand_part_tuple) == 0):
				demand_part_tuple = demand_part,
			else:
				demand_part_tuple = demand_part_tuple, demand_part

			minimal_length_part_equation += (demand_part/length_symbol)**activity_list[activity_number].processing_rate_coeff
	
		solution = solve(minimal_length_part_equation-1,length_symbol)

		solution_list.append(solution[-1])
	
	#Creating objective function in its final form
	whole_solution = 0
	for solution_part in solution_list:
		whole_solution +=  solution_part
	f = lambdify(flatten(demand_part_tuple), whole_solution)

	obj_function = lambda x: f(*x)

	#creation of constraints and bounds for demand parts
	cons_list = []
	for activity_number in activity_numbers:
		cons_list.append(makeLambda(demand_part_tuple,constraints_dict[activity_number],activity_list[activity_number].processing_demand))
	
	cons_map_list = []
	for i in range(len(cons_list)):
		cons_map_list.append({'type': 'eq', 'fun': cons_list[i] })
	bnds=[]
	for demand_part in demand_part_list:
		cons_map_list.append({'type':'ineq', 'fun': makeLambda(demand_part_tuple,demand_part,0)})
		bnds.append((0,None))
	
	#initialization of all x with 1
	init_val=(1,)*demand_part_counter
	start = time.clock()
	res = minimize(obj_function,init_val,constraints=tuple(cons_map_list),bounds=tuple(bnds), method='SLSQP', options={"maxiter":100000})
	end = time.clock()
	print end-start
	# print(res.x)
	print(res.fun)
		
	pass

main();

