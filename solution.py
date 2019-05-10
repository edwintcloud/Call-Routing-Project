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

        # number of route costs
        self.route_costs = 0

        # for each carrier_route_costs argument(variadic), map the name
        # to the dictionary of route costs for the file
        # **this is an expensive operation** but it's the best we can do
        self.routes = {route_costs[0]: self._read_routes(
            route_costs[1]) for route_costs in carrier_route_costs}

        # set numbers to list of numbers from specified file
        # **this is an expensive operation** but it's the best we can do
        self.numbers = self._read_numbers(numbers_file_name)

        # costs will be a dictionary of dictionaries mapping the phone
        # number to a dictionary of matched carrier costs
        # **this is a decently fast operation**
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
                self.route_costs += 1
                # if the route is already in dictionary
                # and the current route has a lower price,
                # or if the route is not in dictionary
                if (row[0] in data and data[row[0]] < row[1]) or (row[0] not in data):
                    # update/insert the route cost
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
        Runtime: Θ(nkl) Space: Θ(n).
        Where n is the number of numbers, k is the 
        number of carriers, and l is the iterations
        needed to find a match from trimming off the end."""
        # create a result dictionary
        result = {}
        # iterate over phone numbers
        for number in self.numbers:
            # iterate for each carrier, k is the carrier name
            # and v is the dictionary of route costs
            for k, v in self.routes.items():
                # trim numbers off the right side of the number until
                # we find a match for each carrier
                for index in range(len(number), 1, -1):
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
                        # we found the longest matching prefix,
                        # break from the inner loop
                        break
            # if route was not found for any carriers, set it's cost to 0
            if number not in result:
                result[number] = 0
        # return the result dictionary
        return result

    # ------------------------------------------------------------------------------
    # CallRoutes - Public Methods
    # ------------------------------------------------------------------------------
    def get_costs(self, phone_number):
        """Return the carrier costs dictionary for a specified phone number.
        Runtime: Θ(1) Space: Θ(1)"""
        try:
            return self.costs[phone_number]
        except KeyError:
            return "Key not found!"

    def yield_costs(self):
        """Return an iterator to iterate over each phone number in costs.
        Runtime: Θ(1) Space: Θ(1)"""
        for cost in self.costs.items():
            yield cost

# ------------------------------------------------------------------------------
# Memory Usage Function
# ------------------------------------------------------------------------------


def get_mem():
    """Print memory usage to stdout."""
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if platform.system() == 'Linux':
        usage = round(usage/float(1 << 10), 2)
    else:
        usage = round(usage/float(1 << 20), 2)
    print("Current Memory Usage: {} mb.".format(usage))


# ------------------------------------------------------------------------------
# Main Entry Point
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    start = time.time()
    print("\nInitializing please wait...")
    calls = CallRoutes("phone-numbers-10000.txt",
                       ("carrierA", "route-costs-3.txt"),
                       ("carrierB", "route-costs-10.txt"),
                       ("carrierC", "route-costs-100.txt"),
                       ("carrierD", "route-costs-600.txt"),
                       ("carrierE", "route-costs-35000.txt"),
                       ("carrierF", "route-costs-106000.txt"),
                       ("carrierG", "route-costs-1000000.txt"),
                       ("carrierH", "route-costs-10000000.txt"))
    load_time = round(time.time()-start, 4)
    print("\nInitialized {:,} route costs in {} seconds.".format(calls.route_costs,
                                                                 load_time))
    get_mem()
    while(True):
        print("\n==========================================")
        print("|              Main Menu                 |")
        print("==========================================")
        print("\nPlease select an option below:")
        print("1. Print results for 100 random numbers.")
        print("2. Get results for a new number.")
        print("3. Iterate over results one-by-one.")
        print("4. Display load time and memory statistics.")
        print("5. Exit the program.")
        choice = input("\nPlease enter a number: ")
        try:
            choice = int(choice)
        except Exception:
            break
        if choice == 1:
            start = time.time()
            for _ in range(100):
                idx = randint(0, len(calls.numbers)-1)
                print("\n{} : {}".format(
                    calls.numbers[idx], calls.get_costs(calls.numbers[idx])))
            print("\nCompleted in {} seconds.".format(
                round(time.time()-start, 4)))
        elif choice == 2:
            new_number = input("\nEnter full number with prefix: ")
            print("\n{} : {}".format(
                new_number, calls.get_costs(new_number)))
        elif choice == 3:
            costs_gen = calls.yield_costs()
            while(True):
                opt = input(
                    "\nPress any key to get the next result or q to go back to main menu: ")
                if opt == "q":
                    break
                print("\n{}".format(next(costs_gen)))
        elif choice == 4:
            print("\n11,141,712 route costs were loaded in {} seconds.".format(
                load_time))
            get_mem()
        else:
            break
    print("\nGoodbye!")
