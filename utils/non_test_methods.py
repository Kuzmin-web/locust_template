import csv, random
from itertools import cycle
from datetime import datetime, timedelta
from urllib.parse import quote_plus


def open_csv_file(filepath:str):
    with open(filepath, "r") as file:
        reader = csv.DictReader(file)
        return cycle(list(reader))

def open_random_csv_file(filepath:str):
    with open(filepath, "r") as file:
        reader = csv.DictReader(file)
        return list(reader)
    
def generateFlightDate():
    departDate = quote_plus((datetime.now() + timedelta(days=random.randint(2, 10))).strftime("%m/%d/%Y"))
    returnDate = quote_plus((datetime.now() + timedelta(days=random.randint(11, 20))).strftime("%m/%d/%Y"))
    return departDate, returnDate