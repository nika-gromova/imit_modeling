from solve import calculate_time
import random
from prettytable import PrettyTable


def generate_matrix(size):
    return [
        [round(random.random(), 4) if i != j else 0.00 for j in range(size)]
        for i in range(size)
    ]


def print_matrix(matrix):
    table = PrettyTable()
    names = ["Состояния"]
    names.extend([str(i + 1) for i in range(len(matrix))])
    table.field_names = names
    for i in range(len(matrix)):
        tmp = [item for item in matrix[i]]
        tmp.insert(0, i + 1)
        table.add_row(tmp)
    print(table)


def print_results(results_p, results_t):
    table = PrettyTable()
    table.add_column("Состояния", [i + 1 for i in range(len(results_p))])
    table.add_column("Предельные вероятности", results_p)
    table.add_column("Время", results_t)
    print(table)


def main():
    random.seed()
    input_size = int(input("Введите размерность системы: "))

    '''
    matrix = [
        [0.0, 0.7525, 0.2761],
        [0.1805, 0.0, 0.3038],
        [0.536, 0.906, 0.0]
    ]
    '''

    matrix = generate_matrix(input_size)

    print_matrix(matrix)
    results_p, results_t = calculate_time(matrix)
    print_results(results_p, results_t)


if __name__ == '__main__':
    main()
