# ==================================================================================
# File: mm_solution.py
#
# Desc: Call Routing project memory map solution file. This solution is ideal
#       for fast startup with relatively fast lookup for a single number.
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
import mmap


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

        # for each carrier_route_costs argument(variadic), allocate
        # the file in memory as a mmap
        self.routes = {route_costs[0]: self._read_routes(
            route_costs[1]) for route_costs in carrier_route_costs}

        # set numbers to list of numbers from specified file
        # **this is an expensive operation** but it's the best we can do
        self.numbers = self._read_numbers(numbers_file_name)

    # ------------------------------------------------------------------------------
    # CallRoutes - Destructor
    # ------------------------------------------------------------------------------
    def __del__(self):
        """Frees allocated mmap's from memory and closes opened files
        before instance destruction."""
        for route in self.routes.values():
            route[0].close()
            route[1].close()

    # ------------------------------------------------------------------------------
    # CallRoutes - Intended Private Methods
    # ------------------------------------------------------------------------------
    def _read_routes(self, file_name):
        """Read route costs file into memory. Return a tuple of mmap
        and open file reference.
        Runtime: Θ(1) Space: Θ(n)"""
        f = open('data/' + file_name)
        mm = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
        return (mm, f)

    def _read_numbers(self, file_name):
        """Read phone numbers into a list and return the result.
        Runtime: Θ(n) Space: Θ(n)"""
        with open('data/'+file_name) as f:
            return f.read().splitlines()

    # ------------------------------------------------------------------------------
    # CallRoutes - Public Methods
    # ------------------------------------------------------------------------------
    def get_costs(self, phone_number):
        """Return the carrier costs for a specified phone number.
        Runtime: Θ(1) Space: Θ(1)"""
        results = {}
        for carrier in self.routes.items():
            for i in range(len(phone_number), 1, -1):
                mm = carrier[1][0]
                cost_idx = mm.find((phone_number[:i]+",").encode())
                if cost_idx != -1:
                    mm.seek(cost_idx)
                    line = mm.readline().decode().strip().split(',')
                    results[carrier[0]] = line[1]
                    mm.seek(0)
                    break
        return results

    def yield_costs(self):
        """Return an iterator to iterate over each phone number in costs.
        Runtime: Θ(1) Space: Θ(1)"""
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
    print("\nInitialized 11,141,712 route costs in {} seconds.".format(load_time))
    get_mem()
    while(True):
        print("\n==========================================")
        print("|              Main Menu                 |")
        print("==========================================")
        print("\nPlease select an option below:")
        print("1. Print results for 5 random numbers.")
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
            for _ in range(5):
                idx = randint(0, len(calls.numbers)-1)
                print("\n{} : {}".format(
                    calls.numbers[idx], calls.get_costs(calls.numbers[idx])))
            complete_time = round(time.time()-start, 4)
            print("\nCompleted in {} seconds.".format(
                complete_time))
            print("Average lookup time per entry: {} seconds.".format(
                round(complete_time/5, 4)))

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
