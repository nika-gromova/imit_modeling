from prettytable import PrettyTable
import csv
from random import randint
from scipy.stats import chi2


class MyRandom:
    def __init__(self):
        self.current = 1
        self.m = 2.**31
        self.k = 1664525
        self.b = 1013904223

    def get_number(self, low=0, high=100):
        self.current = (self.k * self.current + self.b) % self.m
        result = int(low + self.current % (high - low))
        return result


def calc_proc(sequence):
    k = 10
    sum_all = 0
    all_digits = []

    for number in sequence:
        all_digits.extend(map(int, list(str(number))))

    for i in range(k):
        count = 0
        for digit in all_digits:
            if digit == i:
                count += 1
        sum_all += count * count * k
    number_of_digits = len(all_digits)
    chi2_value = sum_all / number_of_digits - number_of_digits
    return chi2.cdf(chi2_value, k - 1)


def table_random(size):
    one_digit = []
    two_digit = []
    three_digit = []
    data = []
    with open('table.csv', newline='') as csvfile:
        tmp = csv.reader(csvfile, delimiter=',')
        for row in tmp:
            data.append(row)

    data_len = len(data[0])
    for i in range(size):
        one_digit.append(int(data[0][randint(0, data_len)]))
        two_digit.append(int(data[1][randint(0, data_len)]))
        three_digit.append(int(data[2][randint(0, data_len)]))

    return one_digit, two_digit, three_digit


def main():
    numbers = [i for i in range(1, 11)]

    one_digit_tbl, two_digit_tbl, three_digit_tbl = table_random(len(numbers))
    table_tbl = PrettyTable()
    table_tbl.add_column('№', numbers)
    table_tbl.add_column('1 разряд', one_digit_tbl)
    table_tbl.add_column('2 разряда', two_digit_tbl)
    table_tbl.add_column('3 разряда', three_digit_tbl)
    table_tbl.add_row(['коэффициент', calc_proc(one_digit_tbl), calc_proc(three_digit_tbl), calc_proc(three_digit_tbl)])
    print("Табличный метод")
    print(table_tbl)

    my_random_class = MyRandom()
    one_digit_alg = [my_random_class.get_number(0, 9) for i in range(len(numbers))]
    two_digit_alg = [my_random_class.get_number(10, 99) for i in range(len(numbers))]
    three_digit_alg = [my_random_class.get_number(100, 999) for i in range(len(numbers))]
    table_alg = PrettyTable()
    table_alg.add_column('№', numbers)
    table_alg.add_column('1 разряд', one_digit_alg)
    table_alg.add_column('2 разряда', two_digit_alg)
    table_alg.add_column('3 разряда', three_digit_alg)
    table_alg.add_row(['коэффициент', calc_proc(one_digit_alg), calc_proc(two_digit_alg), calc_proc(three_digit_alg)])
    print("Алгоритмический метод")
    print(table_alg)

    # print(calc_proc([63, 62, 23, 98, 48, 26, 18, 74, 33, 17]))

if __name__ == '__main__':
    main()
