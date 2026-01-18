import csv
from itertools import cycle

def open_csv_file(filepath:str):
    with open(filepath, "r") as file:
        reader = csv.DictReader(file)
        return cycle(list(reader))

def open_random_csv_file(filepath:str):
    with open(filepath, "r") as file:
        reader = csv.DictReader(file)
        return list(reader)