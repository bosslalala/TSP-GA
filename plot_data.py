import matplotlib.pyplot as plt
import numpy as np
import csv

GApath = "bestPath.csv"
cityPath = "city.csv"
x = []
y = []
plt.figure(figsize=(9,6))
plt.ion()
with open(cityPath.encode('utf8')) as cityfile:

    citycsv = csv.reader(cityfile)
    for row in citycsv:
        x.append(row[1])
        y.append(row[2])
    plt.scatter(x,y)
    plt.pause(1)

with open(GApath.encode('utf8')) as gafile:
    GAcsv = csv.reader(gafile)
    for row in GAcsv:
        plt.cla()
        m = []
        n = []
        for i in row[:-1]:
            loc = int(i)
            m.append(x[loc])
            n.append(y[loc])
        plt.scatter(x, y)
        plt.plot(m,n,'ro-', label=str(i))
        plt.pause(0.01)

plt.ioff()
plt.show()