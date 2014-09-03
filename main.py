# load apm library
from apm import *
from sympy import *
from model import *



def main():
	activity_list=[Activity(0,4,2),Activity(1,2,2),Activity(2,2,1)]
	feasible_sequence=[[0],[0,1],[2]]
	part_list = []
	solution_list =[]
	for feasible_sequence_part in feasible_sequence:
		minimal_length_part_equation = 0 
		sequence_part_number = feasible_sequence.index(feasible_sequence_part)
		length_symbol = symbols("M{}".format(sequence_part_number), positive=True)
		for activity_number in feasible_sequence_part:
			demand_part = symbols("x{}{}".format(activity_number,sequence_part_number),positive=True)
			minimal_length_part_equation += (demand_part/length_symbol)**activity_list[activity_number].processing_function_root
		solution = solve(minimal_length_part_equation-1,length_symbol)
		solution_list.append(solution[0])
	string=""
	for solution_part in solution_list:
		string += str(solution_part)+" + "
	print  string[:-3]
		
		

	#x, y, z, t = symbols('x y z t')
	#k, m, n = symbols('k m n', integer=True)
	#f, g, h = symbols('f g h', cls=Function)
	# Integrate model and return solution
	#z = apm_solve('prob_p',6);
	#print z
	pass

main();

