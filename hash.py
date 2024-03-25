import hashlib
from config import *
import random
import csv
import csv


#just a function for md5 hashing 
def hash_data(element):
    result = hashlib.md5(str(element).encode())
    #digest as hex and append as decimal
    return int(result.hexdigest(),16)%2**N


def read_csv_file(file_path):
    data_list = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data_list.append(row)
    return data_list

data = read_csv_file('merged_file.txt')


hashedData = []
for column in data:
    hashedData.append(hash_data(column["university"]))