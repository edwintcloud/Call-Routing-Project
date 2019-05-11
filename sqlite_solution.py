# ==================================================================================
# File: sqlite_solution.py
#
# Desc: Call Routing project sqlite solution file. This method is terribly slow
#       and should not be used.
#
# Copyright © 2019 Edwin Cloud and Asim Zaidi. All rights reserved.
# ==================================================================================

# ----------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------
import csv
from random import randint
import time
import os
import resource
import platform
import sqlite3


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

        self.db, self.db_conn = self._init_db(carrier_route_costs)

        # set numbers to list of numbers from specified file
        # **this is an expensive operation** but it's the best we can do
        self.numbers = self._read_numbers(numbers_file_name)

    # ------------------------------------------------------------------------------
    # CallRoutes - Destructor
    # ------------------------------------------------------------------------------
    def __del__(self):
        """Close sqlite3 db file."""
        self.db_conn.close()

    # ------------------------------------------------------------------------------
    # CallRoutes - Intended Private Methods
    # ------------------------------------------------------------------------------
    def _init_db(self, carrier_route_costs):
        exists = os.path.isfile('data/' + 'costs_data.db')
        conn = sqlite3.connect('data/' + 'costs_data.db')
        cur = conn.cursor()
        if not exists:
            # create table
            cur.execute(
                "CREATE TABLE costs (carrier, prefix, cost);")
            conn.commit()
            # create table for each carrier
            for carrier in carrier_route_costs:
                records = []
                with open('data/' + carrier[1]) as f:
                    for line in f:
                        line = line.strip().split(',')
                        records.append((carrier[0], line[0], line[1]))
                cur.executemany("INSERT INTO costs VALUES (?, ?, ?)", records)
                conn.commit()

        return cur, conn

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
        for i in range(len(phone_number), 1, -1):
            t = (phone_number[:i],)
            self.db.execute('SELECT * FROM costs WHERE prefix=?', t)
            result = self.db.fetchall()
            if len(result) > 0:
                return result

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
