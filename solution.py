# ==================================================================================
# File: solution.py
#
# Desc: Call Routing Project solution file. This is the main solution as a longer
#       load time is an acceptable tradeoff for near constant time lookups. In
#       a realistic scenario, the server would stay running with the route costs
#       in memory so this tradoff would be unnoticed by the end-user.
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
import os


# ----------------------------------------------------------------------------------
# CallRoutes (Class)
# ----------------------------------------------------------------------------------
class CallRoutes(object):

    # ------------------------------------------------------------------------------
    # CallRoutes - Constructor
    # ------------------------------------------------------------------------------

    def __init__(self):
        """Create a new CallRoutes instance.
        Runtime: Θ(1) Space: Θ(1)."""

        # total number of route costs
        self.route_costs = 0

        # routes is a dictionary of dictionaries mapping carrier names
        # to a costs dictionary for that carrier
        self.routes = {}

    # ------------------------------------------------------------------------------
    # CallRoutes - Intended Private Methods
    # ------------------------------------------------------------------------------

    def _read_route_costs(self, file_name):
        """Read route costs file into a dictionary and return the result.
        Runtime: Θ(n) Space: Θ(n)"""

        # create a results dictionary
        results = {}

        # open the specified file
        with open('data/' + file_name) as route_costs_file:

            # iterate over each line in the open file
            for line in route_costs_file:
                # strip the line of \n characters and split
                # the line by commas into a list
                row = line.strip().split(',')
                # if the route is already in dictionary
                # and the current route has a lower price,
                # or if the route is not in dictionary
                if (row[0] in results and results[row[0]] > row[1]) \
                        or (row[0] not in results):
                    # only increment route_costs for new entries
                    if row[0] not in results:
                        self.route_costs += 1
                    # update/insert the route cost
                    results[row[0]] = row[1]

        # return the results dictionary
        return results

    def _read_phone_numbers(self, file_name):
        """Read phone numbers into a list and return the result.
        Runtime: Θ(n) Space: Θ(1)"""

        # open the specified file
        with open('data/'+file_name) as phone_numbers_file:
            # return a list of lines in the file,
            # excluding the \n character
            return phone_numbers_file.read().splitlines()

    def _list_files(self, filter):
        """Lists files in data directory that match filter. Returns 
        selected file or None if invalid input.
        Runtime: Θ(n) Space: Θ(n)."""

        # get list of files in data dir that match filter
        files = [fileName for fileName in os.listdir(
            "data/") if filter in fileName]

        print("\n\x1b[0;32m{:=^50}".format("="))
        print("|\x1b[0;36m{:^48}\x1b[0;32m|".format("Load a File"))
        print("{:=^50}\n".format("="))

        # print choices to stdout
        for i in range(len(files)):
            print("\x1b[1;37m{}.) \x1b[1;35m{}".format(i+1, files[i]))

        print("\x1b[1;37mq.) \x1b[1;33mMain Menu\n")
        print("\x1b[1;37mPlease make a selection:")

        # wait for input
        choice = input("\x1b[1;32m> \x1b[0;36m")

        # ensure input was valid and return fileName, otherwise
        # return None
        try:
            index = int(choice)
            fileName = files[index-1]
            return fileName
        except:
            return None

    # ------------------------------------------------------------------------------
    # CallRoutes - Public Methods
    # ------------------------------------------------------------------------------

    def get_costs(self, number):
        """Return costs from each carrier for a number.
        Runtime: Θ(nk) Space: Θ(n).
        Where n is the number of carriers, and k is the 
        iterations needed to find a match from trimming off 
        the end."""

        # create a results list
        results = []

        # iterate for each carrier in routes dictionary
        for carrierName, costsDict in self.routes.items():
            # trim numbers off the right side of the prefix until
            # we find a match
            for index in range(len(number), 1, -1):
                # if the trimmed number is in current carrier's
                # costs dictionary
                if number[:index] in costsDict:
                    # append a tuple of (carrier, cost) to result
                    # list
                    results.append((carrierName, costsDict[number[:index]]))
                    # we found the longest matching prefix,
                    # break from inner loop and restart the
                    # process for the next carrier
                    break

        # if prefix was not found for any carriers, return 0
        if len(results) == 0:
            return 0

        # return the results list
        return results

    def load_route_costs(self):
        """Loads route costs from selected file into memory.
        Runtime: Θ(n) Space: Θ(1)."""

        # list available route-costs files, wait for a selection,
        # ensure selection is valid, and get file name
        fileName = self._list_files("route")
        if fileName is None:
            return

        # prompt for carrier name
        carrier = input("\n\x1b[1;37mPlease enter carrier name: \x1b[0;36m")

        # start timer
        start = time.time()

        # load selected route-costs file into self.routes
        self.routes[carrier] = self._read_route_costs(fileName)

        # print function run time
        print("\n\x1b[0;33mCompleted in {} seconds.".format(
            round(time.time()-start, 4)))

    def lookup_costs_from_file(self):
        """Prints costs for all numbers in a file to stdout.
        Runtime: Θ(n) Space: Θ(1)."""

        # list available phone-numbers files, wait for a selection,
        # ensure selection is valid, and get file name
        fileName = self._list_files("phone")
        if fileName is None:
            return

        # start timer
        start = time.time()

        # print costs for selected phone-numbers file
        for phone_number in self._read_phone_numbers(fileName):
            print("\n\x1b[1;35m{} \x1b[0;37m: \x1b[1;34m{}".format(
                phone_number, calls.get_costs(phone_number)))

        # print function run time
        print("\n\x1b[0;33mCompleted in {} seconds.".format(
            round(time.time()-start, 4)))

    # ------------------------------------------------------------------------------
    # CallRoutes - Public Properties
    # ------------------------------------------------------------------------------

    @property
    def carriers(self):
        """Returns the number of carriers in self.routes.
        Runtime: Θ(n) Space: Θ(1)."""
        return len(self.routes.keys())


# ----------------------------------------------------------------------------------
# Memory Usage Function
# ----------------------------------------------------------------------------------
def get_mem():
    """Get current memory usage in mb.
    Runtime: Θ(1) Space: Θ(1)."""
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if platform.system() == 'Linux':
        return round(usage/float(1 << 10), 2)
    return round(usage/float(1 << 20), 2)


# ----------------------------------------------------------------------------------
# Main Entry Point
# ----------------------------------------------------------------------------------
if __name__ == '__main__':

    # create new class instance
    calls = CallRoutes()

    # Main Menu Loop
    while(True):

        print("\n\x1b[0;32m{:=^50}".format("="))
        print("|\x1b[0;36m{:^48}\x1b[0;32m|".format("Main Menu"))
        print("{:=^50}".format("="))
        print("\n\x1b[0;33m{:^50}"
              .format("{} carriers and {:,} route costs currently loaded.".format(
                  calls.carriers, calls.route_costs)))
        print("{:^50}\x1b[1;37m".format(
            "Current Memory Usage: {} mb.".format(get_mem())))
        print(
            "\n1.) \x1b[1;34mLoad carrier route costs from a file.\x1b[1;37m")
        print("2.) \x1b[1;34mLookup costs for a number.\x1b[1;37m")
        print(
            "3.) \x1b[1;34mLookup costs for all numbers in a file.\x1b[1;37m")
        print("4.) \x1b[1;31mExit the program.\x1b[1;37m")
        print("\nPlease make a selection:")

        # wait for input
        choice = input("\x1b[1;32m> \x1b[0;36m")

        # ensure input is a number, or continue
        try:
            choice = int(choice)
        except:
            continue

        # Option 1
        if choice == 1:
            calls.load_route_costs()

        # Option 2
        elif choice == 2:
            number = input(
                "\n\x1b[1;37mEnter full number with prefix: \x1b[0;36m")
            print("\n\x1b[1;35m{} \x1b[0;37m: \x1b[1;34m{}".format(
                number, calls.get_costs(number)))

        # Option 3
        elif choice == 3:
            calls.lookup_costs_from_file()

        # Option 4
        elif choice == 4:
            break

        # Any other number (invalid input)
        else:
            continue

    # cheerio
    print("\n\x1b[1;32mGoodbye!")
