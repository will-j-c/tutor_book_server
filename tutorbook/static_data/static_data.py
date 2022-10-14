import csv
from pathlib import Path

import sys
print(sys.path)

def create_choices(filename):
    filepath = Path(__file__).parent/f'{filename}'
    choices = []
    with open(filepath, 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            choices.append((row[0], row[0]))
    return choices

def values_for_db(filename):
    filepath = Path(__file__).parent/f'{filename}'
    values = []
    with open(filepath, 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            values.append(row[0])
    return values