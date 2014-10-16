from sympy import *


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
        sequence_part_duration_list.append(Float(sequence_part_duration))
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
    activity_execution_list.append(feasible_sequence[-1])
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


def heuristic_ranking_based(feasible_sequence, activities, ranking_lambda, percent):
    activity_execution_list = define_execution_order(feasible_sequence)
    sequence_duration_list = []
    for feasible_sequence_part in feasible_sequence:
        sorted_activities = sorted(activities, key=ranking_lambda)
        # create ranking of activities and resource allocation in feasible sequence
        resource_allocation_dict = allocate_resource(feasible_sequence_part, percent, sorted_activities)
        # find duration of m_k
        sequence_part_duration = get_sequence_part_duration(
            activity_execution_list[feasible_sequence.index(feasible_sequence_part)], activities,
            resource_allocation_dict)
        sequence_duration_list.append(Float(sequence_part_duration))
        # deduct work from activities
        for activity_number in feasible_sequence_part:
            process_activity(activities[activity_number], resource_allocation_dict[activity_number],
                             sequence_part_duration)
    return Float(sum(sequence_duration_list))


def allocate_resource(feasible_sequence_part, percent, sorted_activities):
    resource_allocation = {}

    for activity in feasible_sequence_part:
        resource_allocation[activity] = Float(1.00 / len(feasible_sequence_part) * (1 - percent))

    ranking_power = Float(len(feasible_sequence_part))
    ranking_all = Float(sum(range(0, len(feasible_sequence_part) + 1)))
    ranking = sorted_activities

    for activity in ranking:
        if activity.id in resource_allocation:
            resource_allocation[activity.id] += N((ranking_power / ranking_all) * percent)
            ranking_power -= 1
    return resource_allocation


def get_sequence_part_duration(ending_activities_numbers, activities, resource_allocation):
    sequence_part_duration = 0
    for activity_number in ending_activities_numbers:
        processing_rate = N(
            resource_allocation[activity_number] ** Rational(1, activities[activity_number].processing_rate_coeff))
        sequence_part_duration = max(sequence_part_duration,
                                     Rational(activities[activity_number].processing_demand, processing_rate))
    return sequence_part_duration


def process_activity(activity, resource_allocation, duration):
    activity.processing_demand -= duration * N(
        resource_allocation ** Rational(1, activity.processing_rate_coeff))
    pass


def heuristic_end_favoring(feasible_sequence, activities,percent):
    activity_execution_list = define_execution_order(feasible_sequence)
    sequence_duration_list = []
    for feasible_sequence_part in feasible_sequence:
        ending_activities = activity_execution_list[feasible_sequence.index(feasible_sequence_part)]
        resource_allocation_dict = allocate_resource_favoring_ending(feasible_sequence_part, ending_activities, percent)
        # find duration of m_k
        sequence_part_duration = get_sequence_part_duration(
            ending_activities, activities,
            resource_allocation_dict)
        sequence_duration_list.append(Float(sequence_part_duration))
        # deduct work from activities
        for activity_number in feasible_sequence_part:
            process_activity(activities[activity_number], resource_allocation_dict[activity_number],
                             sequence_part_duration)
    return Float(sum(sequence_duration_list))


def allocate_resource_favoring_ending(feasible_sequence_part, ending_activities, percent):
    resource_allocation = {}

    for activity in feasible_sequence_part:
        resource_allocation[activity] = Float(1.00 / len(feasible_sequence_part) * (1 - percent))

    additional_resource = N(percent / len(ending_activities))
    for ending_activity in ending_activities:
        if ending_activity in resource_allocation:
            resource_allocation[ending_activity] += additional_resource
    return resource_allocation


def allocate_resource_favoring_ending_ranking(feasible_sequence_part, ending_activities, activities, percent):
    resource_allocation = {}
    for activity in feasible_sequence_part:
        resource_allocation[activity] = Float(1.00 / len(feasible_sequence_part) * (1 - percent))
    filter_activities = filter(lambda x: x.id in ending_activities, activities)
    ranking = sorted(filter_activities, key=lambda x: x.processing_demand)
    ranking_all = Float(sum(range(0, len(ranking) + 1)))
    max_pow = len(ranking)
    ranking_power = {}
    for activity in ranking:
        ranking_power[activity.id] = max_pow
        max_pow -= 1

    for ending_activity in ending_activities:
        if ending_activity in resource_allocation:
            resource_allocation[ending_activity] += N((ranking_power[ending_activity] / ranking_all) * percent)

    return resource_allocation


def heuristic_ending_favoring_with_ranking(feasible_sequence, activities):
    activity_execution_list = define_execution_order(feasible_sequence)
    sequence_duration_list = []
    for feasible_sequence_part in feasible_sequence:
        ending_activities = activity_execution_list[feasible_sequence.index(feasible_sequence_part)]
        resource_allocation_dict = allocate_resource_favoring_ending_ranking(feasible_sequence_part,
                                                                             ending_activities, activities, 0.1)
        # find duration of m_k
        sequence_part_duration = get_sequence_part_duration(
            ending_activities, activities,
            resource_allocation_dict)
        sequence_duration_list.append(Float(sequence_part_duration))
        # deduct work from activities
        for activity_number in feasible_sequence_part:
            process_activity(activities[activity_number], resource_allocation_dict[activity_number],
                             sequence_part_duration)
    return Float(sum(sequence_duration_list))


def another_ranking_by_coef(feasible_sequence_part, activities, percent):
    resource_allocation = {}
    power_dict = {}
    activities_list = []
    values_set = set()
    for activity in feasible_sequence_part:
        resource_allocation[activity] = Float(1.00 / len(feasible_sequence_part) * (1 - percent))
        values_set.add(activities[activity].processing_rate_coeff)
        activities_list.append(activities[activity])
        power_dict[activities[activity].processing_rate_coeff] = 0

    for value in values_set:
        for activity in activities_list:
            if activity.processing_rate_coeff == value:
                power_dict[value] += 1

    ranking_sum = 0
    for key, value in power_dict.items():
        ranking_sum += value

    for activity in feasible_sequence_part:
        resource_allocation[activities[activity].id] += N(
            (power_dict[activities[activity].processing_rate_coeff] / ranking_sum) * percent)
    return resource_allocation


def another_heuristic_ranking_based_coef(feasible_sequence, activities, percent):
    activity_execution_list = define_execution_order(feasible_sequence)
    sequence_duration_list = []
    for feasible_sequence_part in feasible_sequence:
        # create ranking of activities and resource allocation in feasible sequence
        resource_allocation_dict = another_ranking_by_coef(feasible_sequence_part, activities, percent)
        # find duration of m_k
        sequence_part_duration = get_sequence_part_duration(
            activity_execution_list[feasible_sequence.index(feasible_sequence_part)], activities,
            resource_allocation_dict)
        sequence_duration_list.append(Float(sequence_part_duration))
        # deduct work from activities
        for activity_number in feasible_sequence_part:
            process_activity(activities[activity_number], resource_allocation_dict[activity_number],
                             sequence_part_duration)
    return Float(sum(sequence_duration_list))


def another_ranking_by_demand(feasible_sequence_part, activities, percent):
    resource_allocation = {}
    power_dict = {}
    activities_list = []
    values_set = set()
    for activity in feasible_sequence_part:
        resource_allocation[activity] = Float(1.00 / len(feasible_sequence_part) * (1 - percent))
        values_set.add(activities[activity].processing_demand)
        activities_list.append(activities[activity])
        power_dict[activities[activity].processing_demand] = 0

    for value in values_set:
        for activity in activities_list:
            if activity.processing_demand == value:
                power_dict[value] += 1

    ranking_sum = 0
    for key, value in power_dict.items():
        ranking_sum += value

    for activity in feasible_sequence_part:
        resource_allocation[activities[activity].id] += N(
            (power_dict[activities[activity].processing_demand] / ranking_sum) * percent)
    return resource_allocation


def another_heuristic_ranking_based_demand(feasible_sequence, activities):
    activity_execution_list = define_execution_order(feasible_sequence)
    sequence_duration_list = []
    for feasible_sequence_part in feasible_sequence:
        # create ranking of activities and resource allocation in feasible sequence
        resource_allocation_dict = another_ranking_by_demand(feasible_sequence_part, activities, 0.1)
        # find duration of m_k
        sequence_part_duration = get_sequence_part_duration(
            activity_execution_list[feasible_sequence.index(feasible_sequence_part)], activities,
            resource_allocation_dict)
        sequence_duration_list.append(Float(sequence_part_duration))
        # deduct work from activities
        for activity_number in feasible_sequence_part:
            process_activity(activities[activity_number], resource_allocation_dict[activity_number],
                             sequence_part_duration)
    return Float(sum(sequence_duration_list))


def create_resource_allocation_by_groups(feasible_sequence_part, activities, m):
    percent = 0.3
    resource_dict = {}
    score_dict = {}
    min_score = 0
    max_score = 0

    for activity_number in feasible_sequence_part:
        curr_score = score(activities[activity_number])
        score_dict[activity_number] = curr_score
        min_score = min(min_score, curr_score)
        max_score = max(max_score, curr_score)

    groups_range = Float((max_score - min_score) / m)
    grouped_activities = []
    groups = {}

    for i in range(0, m):
        groups[i] = []
        for activity_number in feasible_sequence_part:
            if i * groups_range <= score_dict[activity_number] <= (
                        i + 1) * groups_range and activity_number not in grouped_activities:
                groups[i].append(activity_number)
                grouped_activities.append(activity_number)

    for i in feasible_sequence_part:
        if i not in grouped_activities:
            groups[m - 1].append(i)
    groups_res_allocation = {}

    free_sum = 0
    for i in range(0, m):
        res_allocation = Float((1.00 / len(groups)) * (1 - percent))
        if len(groups[i]) == 0:
            free_sum += res_allocation
        else:
            groups_res_allocation[i] = res_allocation

    ranking_power = 1
    ranking_all = Float(sum(range(0, len(groups) + 1)))

    for i in range(0, m):
        res_allocation = N((ranking_power / ranking_all) * percent)
        if len(groups[i]) == 0:
            free_sum += res_allocation
        else:
            groups_res_allocation[i] += res_allocation
        ranking_power += 1

        for activity_num in groups[i]:
            resource_dict[activity_num] = N(groups_res_allocation[i] / len(groups[i]))

    for activity_num in feasible_sequence_part:
        resource_dict[activity_num] += N(free_sum / len(feasible_sequence_part))
    return resource_dict


def score(activity):
    return activity.processing_demand + 10 * activity.processing_rate_coeff


def heuristic_group(feasible_sequence, activities, m):
    activity_execution_list = define_execution_order(feasible_sequence)
    sequence_duration_list = []
    for feasible_sequence_part in feasible_sequence:
        ending_activities = activity_execution_list[feasible_sequence.index(feasible_sequence_part)]
        resource_allocation_dict = create_resource_allocation_by_groups(feasible_sequence_part, activities, m)
        # find duration of m_k
        sequence_part_duration = get_sequence_part_duration(
            ending_activities, activities,
            resource_allocation_dict)
        sequence_duration_list.append(Float(sequence_part_duration))
        # deduct work from activities
        for activity_number in feasible_sequence_part:
            process_activity(activities[activity_number], resource_allocation_dict[activity_number],
                             sequence_part_duration)
    return Float(sum(sequence_duration_list))
