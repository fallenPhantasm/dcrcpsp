
from scipy.optimize import minimize

from heuristics import *

def makeLambda(demand_part_tuple, constraint, processing_demand):
    constraint -= processing_demand
    l = lambdify(flatten(demand_part_tuple), constraint)
    return lambda x: l(*x)




def solve_SLSQP(feasible_sequence, activity_list):
    activity_numbers = range(0, len(activity_list))
    solution_list = []
    demand_part_tuple = ()
    demand_part_list = []
    constraints_dict = {x: 0 for x in range(0, len(activity_list))}
    demand_part_counter = 0

    for feasible_sequence_part in feasible_sequence:
        minimal_length_part_equation = 0
        sequence_part_number = feasible_sequence.index(feasible_sequence_part)
        length_symbol = symbols("M{}".format(sequence_part_number), positive=True)
        # Creating equations for calculating minimal sequence part duration
        for activity_number in feasible_sequence_part:
            demand_part = symbols("x_{}i_{}k".format(activity_number, sequence_part_number), positive=True)
            demand_part_list.append(demand_part)
            demand_part_counter += 1
            constraints_dict[activity_number] += demand_part
            if (len(demand_part_tuple) == 0):
                demand_part_tuple = demand_part,
            else:
                demand_part_tuple = demand_part_tuple, demand_part

            minimal_length_part_equation += (demand_part / length_symbol) ** activity_list[
                activity_number].processing_rate_coeff

        solution = solve(minimal_length_part_equation - 1, length_symbol)
        solution_list.append(solution[-1])

        # Creating objective function in its final form
    whole_solution = 0
    for solution_part in solution_list:
        whole_solution += solution_part
    f = lambdify(flatten(demand_part_tuple), whole_solution)

    obj_function = lambda x: f(*x)

    #creation of constraints and bounds for demand parts
    cons_list = []
    for activity_number in activity_numbers:
        cons_list.append(makeLambda(demand_part_tuple, constraints_dict[activity_number],
                                    activity_list[activity_number].processing_demand))

    cons_map_list = []
    for i in range(len(cons_list)):
        cons_map_list.append({'type': 'eq', 'fun': cons_list[i]})
    bnds = []
    for demand_part in demand_part_list:
        cons_map_list.append({'type': 'ineq', 'fun': makeLambda(demand_part_tuple, demand_part, 0)})
        bnds.append((0, None))

    #initialization of all x with 0
    init_val = (0,) * demand_part_counter
    res = minimize(obj_function, init_val, constraints=tuple(cons_map_list), bounds=tuple(bnds), method='SLSQP',
                   options={"maxiter": 100000})
    return res.fun


