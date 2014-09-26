from random import randint
from copy import copy


class Activity:
    def __init__(self, id, processing_demand, processing_rate_coeff):
        self.id = id
        self.processing_demand = processing_demand
        self.processing_rate_coeff = processing_rate_coeff

        def __repr__(self):
            return "Activity {} demand={} root={}".format(self.id, self.processing_demand, self.processing_rate_coeff)

        def __str__(self):
            return "Activity {} demand={} root={}".format(self.id, self.processing_demand, self.processing_rate_coeff)


def generate_activity_list(how_many):
    """
    Generates activities for DCRCPSP problem
    :param how_many: how many activities should be generated
    :return: list of Activity objects
    """
    activity_list = []
    for i in range(0, how_many):
        activity_list.append(Activity(i, randint(30, 100), randint(1, 2)))
    return activity_list


def generate_feasible_sequence(activities_list):
    """
    Generates feasible sequence for given activity list
    :param activities_list: list of activities to make feasible sequence of
    :return: feasible sequence in a form of list of lists
    """
    feasible_sequence = []
    feasible_sequence_part = []
    activities_numbers = range(0, len(activities_list))

    for i in range(0, randint(1, len(activities_list) - 1)):
        feasible_sequence_part.append(activities_numbers.pop(0))
    feasible_sequence.append(feasible_sequence_part)

    while len(feasible_sequence_part) > 1 or len(activities_numbers) != 0:
        new_feasible_sequence_part = copy(feasible_sequence_part)
        if len(new_feasible_sequence_part) > 0:
            maxind = randint(1, len(new_feasible_sequence_part))
            for x in range(1, maxind):
                new_feasible_sequence_part.pop(randint(0, len(new_feasible_sequence_part) - 1))
        if len(activities_numbers) > 0:
            for i in range(randint(1, len(activities_numbers))):
                new_feasible_sequence_part.append(activities_numbers.pop(0))
        feasible_sequence.append(new_feasible_sequence_part)
        feasible_sequence_part = new_feasible_sequence_part
    return feasible_sequence
