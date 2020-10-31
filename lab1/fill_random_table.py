import csv
import random


def fill_table():
    with open('table.csv', 'w', newline='') as out_csv_file:
        csv_out = csv.writer(out_csv_file)
        for k in [1, 11, 111]:
            row = []
            for j in range(5000):
                row.append(random.randint(k - 1, 9 * k))
            csv_out.writerow(row)


def main():
    fill_table()


if __name__ == '__main__':
    main()
