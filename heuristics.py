from sympy import *


def heuristic_1M(feasible_sequence, activities):
    activity_execution_list = define_execution_order(feasible_sequence)
    sequence_part_duration_list = []
    for ending_activity_number in activity_execution_list:
        ending_activity = activities[ending_activity_number]
        resource_allocation = Rational(1, len(feasible_sequence[activity_execution_list.index(ending_activity_number)]))
        processing_rate = Rational(resource_allocation ** Rational(1 / ending_activity.processing_rate_coeff))
        sequence_part_duration = Rational(ending_activity.processing_demand / processing_rate)
        for activity_number in feasible_sequence[activity_execution_list.index(ending_activity_number)]:
            activity = activities[activity_number]
            activity.processing_demand -= Rational(
                sequence_part_duration * Rational(resource_allocation ** Rational(1 / activity.processing_rate_coeff)))
        sequence_part_duration_list.append(sequence_part_duration)
    last_sequence_duration = 0
    for activity in feasible_sequence[-1]:
        last_activity = activities[activity]
        last_processing_rate = Rational(resource_allocation ** Rational(1 / last_activity.processing_rate_coeff))
        activity_duration = Rational(last_activity.processing_demand / last_processing_rate)
        last_sequence_duration = max(last_sequence_duration, activity_duration)
    sequence_part_duration_list.append(last_sequence_duration)
    return sum(sequence_part_duration_list)


def heuristic_1U(feasible_sequence, activities):
    activity_execution_list = define_execution_order(feasible_sequence)
    sequence_part_duration_list = []
    for ending_activites in activity_execution_list:
        sequence_part_duration = 0
        for ending_activity_number in ending_activites:
            ending_activity = activities[ending_activity_number]
            resource_allocation = Rational(1, len(feasible_sequence[activity_execution_list.index(ending_activites)]))
            processing_rate = N(resource_allocation ** Rational(1, ending_activity.processing_rate_coeff))
            sequence_part_duration = max(sequence_part_duration,
                                         Rational(ending_activity.processing_demand, processing_rate))
        for activity_number in feasible_sequence[activity_execution_list.index(ending_activites)]:
            activity = activities[activity_number]
            activity.processing_demand -= sequence_part_duration * N(
                resource_allocation ** Rational(1, activity.processing_rate_coeff))
        sequence_part_duration_list.append(sequence_part_duration)
    last_sequence_duration = 0
    for activity in feasible_sequence[-1]:
        last_activity = activities[activity]
        last_processing_rate = N(
            (Rational(1, len(feasible_sequence[-1]))) ** Rational(1, last_activity.processing_rate_coeff))
        activity_duration = Rational(last_activity.processing_demand / last_processing_rate)
        last_sequence_duration = max(last_sequence_duration, activity_duration)
    sequence_part_duration_list.append(last_sequence_duration)
    return Float(sum(sequence_part_duration_list))


def define_execution_order(feasible_sequence):
    activity_execution_list = []
    for feasible_sequence_part in feasible_sequence:
        previous_part_index = feasible_sequence.index(feasible_sequence_part) - 1
        if previous_part_index >= 0:
            activity_execution_list_part = []
            for activity_number in feasible_sequence[previous_part_index]:
                if activity_number not in feasible_sequence_part:
                    activity_execution_list_part.append(activity_number)
            activity_execution_list.append(activity_execution_list_part)
    return activity_execution_list


def heuristic_HUDD(feasible_sequence, activities):
    activities_counts_dict = {}
    for feasible_sequence_part in feasible_sequence:
        for activity_number in feasible_sequence_part:
            if activity_number in activities_counts_dict:
                activities_counts_dict[activity_number] += 1
            else:
                activities_counts_dict[activity_number] = 1
    activities_divided_dict = {}
    for key in activities_counts_dict:
        activities_divided_dict[key] = N(Float(activities[key].processing_demand) / activities_counts_dict[key])
    makespan = 0
    for feasible_sequence_part in feasible_sequence:
        makespan_equation = 0
        m = symbols("m", positive=True)
        for activity_number in feasible_sequence_part:
            makespan_equation += N(N(activities_divided_dict[activity_number] / m) ** activities[
                activity_number].processing_rate_coeff)
        makespan += solve(makespan_equation - 1, m)[0]
    return makespan


def ranking_heuristic(feasible_sequence, activities):
    activity_execution_list = define_execution_order(feasible_sequence)
    for feasible_sequence_part in feasible_sequence:
        # create ranking of activities and resource allocation in feasible sequence
        resource_allocation_dict = allocate_resource(feasible_sequence_part, activities)
        # find duration of m_k

        #deduct work from activities
    return Float(sum())


def allocate_resource(feasible_sequence_part, activities, percent):
    resource_allocation = {}

    for activity in feasible_sequence_part:
        resource_allocation[activity] = Float(1.00 / len(feasible_sequence_part) * (1 - percent))

    ranking_power = Float(len(feasible_sequence_part))
    ranking_all = Float(sum(range(0, len(feasible_sequence_part) + 1)))
    ranking = sorted(activities, key=lambda x: x.processing_rate_coeff)
    for activity in ranking:
        resource_allocation[activity.id] += N((ranking_power / ranking_all) * percent)
        ranking_power -= 1
    return resource_allocation


def get_sequence_part_duration(ending_activities_numbers, activities, resource_allocation):
    sequence_part_duration = 0
    for activity_number in ending_activities_numbers:
        processing_rate = N(resource_allocation ** Rational(1, activities[activity_number].processing_rate_coeff))
        sequence_part_duration = max(sequence_part_duration,
                                     Rational(activities[activity_number].processing_demand, processing_rate))