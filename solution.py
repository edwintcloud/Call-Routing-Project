# ==================================================================================
# File: solution.py
#
# Desc: Call Routing project solution file. This is the main solution as a longer
#       startup time is an acceptable tradeoff for near constant time lookups. In
#       a realistic scenario, the server would stay running anyways so this tradoff
#       would be negligible.
#
# Copyright © 2019 Edwin Cloud and Asim Zaidi. All rights reserved.
# ==================================================================================

# ----------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------
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

    # ------------------------------------------------------------------------------
    # CallRoutes - Intended Private Methods
    # ------------------------------------------------------------------------------
    def _read_routes(self, file_name):
        """Read route costs file into a dictionary and return the result.
        Runtime: Θ(n) Space: Θ(n)"""
        data = {}
        with open('data/' + file_name) as f:
            for line in f:
                row = line.strip().split(',')
                # if the route is already in dictionary
                # and the current route has a lower price,
                # or if the route is not in dictionary
                if (row[0] in data and data[row[0]] > row[1]) or (row[0] not in data):
                    if row[0] not in data:
                        self.route_costs += 1
                    # update/insert the route cost
                    data[row[0]] = row[1]
        return data

    def _read_numbers(self, file_name):
        """Read phone numbers into a list and return the result.
        Runtime: Θ(n) Space: Θ(n)"""
        with open('data/'+file_name) as f:
            return f.read().splitlines()

    # ------------------------------------------------------------------------------
    # CallRoutes - Public Methods
    # ------------------------------------------------------------------------------

    def get_costs(self, number):
        """Return costs from each carrier for a number.
        Runtime: Θ(nk) Space: Θ(n).
        Where n is the number of carriers, and k is the 
        iterations needed to find a match from trimming off 
        the end."""
        # create a result list
        result = []
        # iterate for each carrier, k is the carrier name
        # and v is the dictionary of route costs
        for k, v in self.routes.items():
            # trim numbers off the right side of the number until
            # we find a match for each carrier
            for index in range(len(number), 1, -1):
                # if the trimmed number is in current carrier's
                # route costs
                if number[:index] in v:
                    # append a tuple of carrier, cost to result
                    # list
                    result.append((k, v[number[:index]]))
                    # we found the longest matching prefix,
                    # break from the inner loop
                    break
        # if route was not found for any carriers, return 0
        if len(result) == 0:
            return 0
        # return the result list
        return result

    def yield_costs(self):
        """Return an iterator to get the costs of each number in self.numbers.
        Runtime: Θ(nk) Space: Θ(1)"""
        for number in self.numbers:
            yield "{} : {}".format(number, self.get_costs(number))

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
    # start the timer
    start = time.time()
    print("\nInitializing please wait...")
    # initialize the CallRoutes class with some data
    calls = CallRoutes("phone-numbers-10000.txt",
                       ("carrierA", "route-costs-3.txt"),
                       ("carrierB", "route-costs-10.txt"),
                       ("carrierC", "route-costs-100.txt"),
                       ("carrierD", "route-costs-600.txt"),
                       ("carrierE", "route-costs-35000.txt"),
                       ("carrierF", "route-costs-106000.txt"),
                       ("carrierG", "route-costs-1000000.txt"),
                       ("carrierH", "route-costs-10000000.txt"))
    # calculate and print load time and memory
    load_time = round(time.time()-start, 4)
    print("\nInitialized {:,} route costs in {} seconds.".format(calls.route_costs,
                                                                 load_time))
    get_mem()

    # Main Loop
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
        # ensure choice is a number, or break
        try:
            choice = int(choice)
        except Exception:
            break
        # Option 1
        if choice == 1:
            start = time.time()
            for _ in range(100):
                idx = randint(0, len(calls.numbers)-1)
                print("\n{} : {}".format(
                    calls.numbers[idx], calls.get_costs(calls.numbers[idx])))
            print("\nCompleted in {} seconds.".format(
                round(time.time()-start, 4)))
        # Option 2
        elif choice == 2:
            new_number = input("\nEnter full number with prefix: ")
            print("\n{} : {}".format(
                new_number, calls.get_costs(new_number)))
        # Option 3
        elif choice == 3:
            costs_gen = calls.yield_costs()
            while(True):
                opt = input(
                    "\nPress any key to get the next result or q to go back to main menu: ")
                if opt == "q":
                    break
                print("\n{}".format(next(costs_gen)))
        # Option 4
        elif choice == 4:
            print("\n{:,} route costs were loaded in {} seconds.".format(calls.route_costs,
                                                                         load_time))
            get_mem()
        # Option 5
        else:
            break
    # cheerio
    print("\nGoodbye!")
