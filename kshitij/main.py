import csv

lstOflsts = []

with open('percentage-of-schools.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        lstOflsts.append(row)

for thatList in lstOflsts:
    thatList.append(69)

csv.register_dialect('myDialect', delimiter=',', quoting=csv.QUOTE_ALL)
with open('office.csv', 'w', newline='') as file:
    writer = csv.writer(file, dialect='myDialect')
    writer.writerows(lstOflsts)

