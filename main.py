import csv
import sys
import numpy as np

from models import vehicle as vehicle_model
from models import package as package_model

vehicles = []
packages = []
matrix_costs = {}
incompatibles = {}

solution_cost = 0
final_solution = []

if __name__ == "__main__":
    _, arg1 = sys.argv
    # Read vehicles list
    with open('data/'+arg1+'/vehicles.txt','r') as f:
        data = csv.reader(f)
        for row in data:
            vehicle = vehicle_model.Vehicle(row[0], int(row[1]))
            vehicles.append(vehicle)

    # Read incompatible
    with open('data/'+arg1+'/incompatible.txt','r') as f:
        data = csv.reader(f)
        for row in data:
            incompatibles[row[0]] = row[1]
            incompatibles[row[1]] = row[0]

    # Read Packages list
    with open('data/'+arg1+'/packages.txt','r') as f:
        data = csv.reader(f)
        for row in data:
            incompatibles_for_package = incompatibles[row[0]] if row[0] in incompatibles else []
            package = package_model.Package(row[0], int(row[1]), incompatibles_for_package)
            packages.append(package)

    # Read weights
    with open('data/'+arg1+'/costs.txt','r') as f:
        data = csv.reader(f)
        for row in data:
            package = row[0]
            cost = row[2]

            if package in matrix_costs:
                matrix_costs[package].append(int(cost))
            else:
                matrix_costs[package] = []
                matrix_costs[package].append(int(cost))

    print([package.weight for package in packages])
    # Check data
    for vehicle in vehicles:
        print('Name: ', vehicle.name + ', Capacity: '+ str(vehicle.capacity))

    for package in packages:
        print('Name: ', package.name + ', Weight: '+ str(package.weight))

    for key in list(matrix_costs.keys()):
        print('Key: ', str(key) + ', Costs: '+ str(matrix_costs[key]))
