import csv
from random import randint
import time
import resource
import platform


class CallRoutes(object):

    def __init__(self, numbers_file_name, *carrier_route_costs):
        self.routes = {route_costs[0]: self._read_routes(
            route_costs[1]) for route_costs in carrier_route_costs}
        self.numbers = self._read_numbers(numbers_file_name)
        self.costs = self._get_costs_for_numbers()

    def _read_routes(self, file_name):
        data = {}
        with open('data/' + file_name) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                data[row[0]] = row[1]
        return data

    def _read_numbers(self, file_name):
        with open('data/'+file_name) as f:
            return f.read().splitlines()

    def _get_costs_for_numbers(self):
        result = {}
        for number in self.numbers:
            # trim numbers off the right side of the number until
            # we find a match in routes, once match is found return the cost
            for index in range(len(number), 1, -1):
                for k, v in self.routes.items():
                    if number[:index] in v:
                        if number not in result:
                            result[number] = {k: v[number[:index]]}
                        elif k not in result[number]:
                            result[number][k] = v[number[:index]]

            if number not in result:
                result[number] = 0
        return result

    def get_cost(self, phone_number):
        return self.costs[phone_number]


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
    print("\nCross-compared 10,000 phone numbers with 8 different carriers and a total of 11,141,713 different route costs.")
    print("\nFor the sake of an example, 100 random numbers from the 10,000 in the data set were displayed above.")
    print("\nRuntime: {} seconds.".format(round(end-start, 4)))
    # print memory usage
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if platform.system() == 'Linux':
        usage = round(usage/float(1 << 10), 2)
    else:
        usage = round(usage/float(1 << 20), 2)
    print("Memory Usage: {} mb.".format(usage))
