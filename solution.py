# ==================================================================================
# File: solution.py
#
# Desc: Call Routing project solution file.
#
# Copyright © 2019 Edwin Cloud and Asim Zaidi. All rights reserved.
# ==================================================================================

# ----------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------
import csv
from random import randint
import time
import resource
import platform


# ----------------------------------------------------------------------------------
# CallRoutes (Class)
# ----------------------------------------------------------------------------------
class CallRoutes(object):

    # ------------------------------------------------------------------------------
    # CallRoutes - Constructor
    # ------------------------------------------------------------------------------
    def __init__(self, numbers_file_name, *carrier_route_costs):
        """Create a new CallRoutes instance. numbers_file_name should be 
        a fully qualified file name. carrier_route_costs is a variadic parameter,
        each of which should be a tuple of ('carrier name', 'file name')."""

        # for each carrier_route_costs argument(variadic), map the name
        # to the dictionary of route costs for the file
        self.routes = {route_costs[0]: self._read_routes(
            route_costs[1]) for route_costs in carrier_route_costs}

        # set numbers to list of numbers from specified file
        self.numbers = self._read_numbers(numbers_file_name)

        # costs will be a dictionary of dictionaries mapping the phone
        # number to a dictionary of matched carrier costs
        self.costs = self._get_costs_for_numbers()

    # ------------------------------------------------------------------------------
    # CallRoutes - Intended Private Methods
    # ------------------------------------------------------------------------------
    def _read_routes(self, file_name):
        """Read route costs file into a dictionary and return the result.
        Runtime: Θ(n) Space: Θ(n)"""
        data = {}
        with open('data/' + file_name) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                data[row[0]] = row[1]
        return data

    def _read_numbers(self, file_name):
        """Read phone numbers into a list and return the result.
        Runtime: Θ(n) Space: Θ(n)"""
        with open('data/'+file_name) as f:
            return f.read().splitlines()

    def _get_costs_for_numbers(self):
        """Get costs for all numbers for each carrier. 
        Return resulting dictionary of dictionaries.
        Runtime: Θ(nkl) Space: Θ(n)"""
        # create a result dictionary
        result = {}
        # iterate over phone numbers
        for number in self.numbers:
            # trim numbers off the right side of the number until
            # we find a match for each carrier
            for index in range(len(number), 1, -1):
                # iterate for each carrier, k is the carrier name
                # and v is the dictionary of route costs
                for k, v in self.routes.items():
                    # if the trimmed number is in current carrier's
                    # route costs
                    if number[:index] in v:
                        # and the full phone number is not in result
                        # dictionary
                        if number not in result:
                            # create new entry in result dictionary
                            # with full phone number as the key and
                            # a new dictionary with a single entry of
                            # carrier name: route cost for carrier
                            result[number] = {k: v[number[:index]]}
                        # else if the carrier name not in the dictionary
                        # at result[number]
                        elif k not in result[number]:
                            # create new entry in result[number] dictionary
                            # equal to carrier name: route cost for carrier
                            result[number][k] = v[number[:index]]
            # if route was not found for any carriers, set it's cost to 0
            if number not in result:
                result[number] = 0
        # return the result dictionary
        return result

    # ------------------------------------------------------------------------------
    # CallRoutes - Public Methods
    # ------------------------------------------------------------------------------
    def get_cost(self, phone_number):
        """Return the carrier costs dictionary for a specified phone number.
        Runtime: Θ(1) Space: Θ(1)"""
        return self.costs[phone_number]

    def yield_costs(self):
        """Return an iterator to iterate over each phone number in costs.
        Runtime: Θ(1) Space: Θ(1)"""
        for cost in self.costs.items():
            yield cost


# ------------------------------------------------------------------------------
# Main Entry Point
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    start = time.time()
    calls = CallRoutes("phone-numbers-10000.txt",
                       ("carrierA", "route-costs-3.txt"),
                       ("carrierB", "route-costs-10.txt"),
                       ("carrierC", "route-costs-100.txt"),
                       ("carrierD", "route-costs-600.txt"),
                       ("carrierE", "route-costs-35000.txt"),
                       ("carrierF", "route-costs-106000.txt"),
                       ("carrierG", "route-costs-1000000.txt"),
                       ("carrierH", "route-costs-10000000.txt"))

    for _ in range(100):
        idx = randint(0, len(calls.numbers)-1)
        print("{} : {}".format(
            calls.numbers[idx], calls.get_cost(calls.numbers[idx])))
    end = time.time()
    print("\nCross-compared 10,000 phone numbers with 8 different carriers \
        and a total of 11,141,713 different route costs.")
    print("\nFor the sake of an example, 100 random numbers from the 10,000 \
        in the data set were displayed above.")
    print("\nRuntime: {} seconds.".format(round(end-start, 4)))
    # print memory usage
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if platform.system() == 'Linux':
        usage = round(usage/float(1 << 10), 2)
    else:
        usage = round(usage/float(1 << 20), 2)
    print("Memory Usage: {} mb.".format(usage))

    print("\nBelow is an example of using a generator to get the results one by one.")
    costs_gen = calls.yield_costs()
    for _ in range(10):
        print(next(costs_gen))
