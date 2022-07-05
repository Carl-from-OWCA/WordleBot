import csv

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

nested = [[(0, 0), (0, 1), (0, 2)],
          [(1, 0), (1, 1), (1, 2)],
          [(2, 0), (2, 1), (2, 2)]]

with open("test.csv", 'w', newline="") as file:
    writer = csv.writer(file)
    writer.writerows([RED, 
                      GREEN, 
                      BLUE])
    for row in nested:
        writer.writerows(row)

    
with open("test.csv", newline="") as file:
    reader = csv.reader(file)

    # Get the colors
    row = next(reader)
    RED = [int(elem) for elem in row]
    row = next(reader)
    GREEN = [int(elem) for elem in row]
    row = next(reader)
    YELLOW = [int(elem) for elem in row]

    for row in reader:
        coord = tuple([int(elem) for elem in row])
        print(coord)

print([RED, GREEN, YELLOW])
