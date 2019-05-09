import csv
from random import randint


class CallRoutes(object):

    def __init__(self, routes_file_name, numbers_file_name):
        self.routes = self._read_routes(routes_file_name)
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
                if number[:index] in self.routes:
                    result[number] = self.routes[number[:index]]
            if number not in result:
                result[number] = 0
        return result

    def get_cost(self, phone_number):
        return self.costs[phone_number]


if __name__ == '__main__':
    calls = CallRoutes("route-costs-35000.txt", "phone-numbers-10000.txt")

    for _ in range(100):
        idx = randint(0, len(calls.numbers))
        print("{} : {}".format(
            calls.numbers[idx], calls.get_cost(calls.numbers[idx])))
