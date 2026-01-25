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


def processCancelRequestBody(flight_ids, flights_nums):
    
    random_index = random.randrange(len(flights_nums))

    delete_num = f'{flights_nums[random_index]}=on'
    flights_ids = 'flightID=' + '&flightID='.join(flight_ids)
    flights_nums = '.cgifields=' + '&.cgifields='.join(flights_nums)  
    static = 'removeFlights.x=47&removeFlights.y=12'

    return f'{flights_ids}&{delete_num}&{flights_nums}{static}'