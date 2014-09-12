from sympy import *
import re
from model import *
from scipy.optimize import minimize




def main():
	activity_list=[Activity(0,4,2),Activity(1,2,2),Activity(2,2,2)]
	feasible_sequence=[[0,1],[1,2]]
	part_list = []
	solution_list =[]
	demand_part_tuple = ()
	for feasible_sequence_part in feasible_sequence:
		minimal_length_part_equation = 0 
		sequence_part_number = feasible_sequence.index(feasible_sequence_part)
		length_symbol = symbols("M{}".format(sequence_part_number), positive=True)
		for activity_number in feasible_sequence_part:
			demand_part = symbols("x_{}_{}".format(activity_number,sequence_part_number),positive=True)
			if (len(demand_part_tuple) == 0):
				demand_part_tuple = demand_part,
			else:
				demand_part_tuple = demand_part_tuple, demand_part

			minimal_length_part_equation += (demand_part/length_symbol)**activity_list[activity_number].processing_function_root
		solution = solve(minimal_length_part_equation-1,length_symbol)
		solution_list.append(solution[0])
		#print solution
		whole_solution = 0
	for solution_part in solution_list:
		whole_solution +=  solution_part

	f = lambdify(demand_part_tuple, whole_solution)
	print demand_part_tuple
	print whole_solution
	# print(f(1,2,3,4))

	obj_function = lambda x: f(*x)
	cons = ({'type': 'ineq', 'fun': lambda x:  x[0] },
			{'type': 'ineq', 'fun': lambda x:  x[1] },
			{'type': 'ineq', 'fun': lambda x:  x[2] },
			{'type': 'ineq', 'fun': lambda x:  x[3] })

	# x0 in [0, 10], x1 in [0, 20]
	bnds = ((0, 50000), (0, 50000),(0,50000),(0,50000))

	# initial (1, 1)
	res = minimize(obj_function, (40000, 6,2,3),bounds=bnds, method='SLSQP', options={"maxiter":100000})
	print(res)
		
	pass

main();

