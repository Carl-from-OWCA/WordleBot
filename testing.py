import csv

with open("word_bank.csv", newline="") as file:
    reader = csv.reader(file)

    for row in reader:
        print(row[0])

