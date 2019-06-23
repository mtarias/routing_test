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

    # Sort vehicles
    packages = sorted(packages, key=lambda x: x.weight, reverse=True)

    print([package.weight for package in packages])
    # Check data
    #for vehicle in vehicles:
    #    print('Name: ', vehicle.name + ', Capacity: '+ str(vehicle.capacity))

    #for package in packages:
    #    print('Name: ', package.name + ', Weight: '+ str(package.weight))

    #for key in list(matrix_costs.keys()):
    #    print('Key: ', str(key) + ', Costs: '+ str(matrix_costs[key]))

    # Init algorithm
    for package in packages:
        package_name = package.name
        package_costs = matrix_costs[package_name]

        # Sort costs
        sorted_costs = sorted(package_costs)
        sorted_indexes_costs = list(np.argsort(package_costs))
        i = len(package_costs)
        a = 0
        print(sorted_costs)

        while i > 0:
            # Get max cost of costs hash for package
            max_cost = sorted_costs[a]
            index_max_cost = sorted_indexes_costs[a]

            # Get vehicle capacity
            vehicle_name = 'v' + str(index_max_cost+1)
            vehicle = next((vehicle for vehicle in vehicles if vehicle.name == vehicle_name), None)
            free_space = vehicle.capacity - vehicle.occupied_space

            # Check vehicle capacity
            # if is lower, then add to solution and change vehicle capacity
            if package.weight <= free_space and package.incompatibles not in vehicle.packages:
                # Add to solution
                final_solution.append('Package: '+ package.name + ', Vehicle: '+ vehicle_name + ', Cost: '+str(max_cost))
                vehicle.packages.append(package.name)
                vehicle.occupied_space += package.weight
                solution_cost += max_cost
                i = 0
            else:
                print('PACKAGES: '+str(sorted_costs))
                print('EL PAQUETE '+str(package.name)+' NO PUEDE SER ASIGNADO A '+str(vehicle.name)+', COSTO: ')
                i -= 1
                a += 1

    # Check results
    print('Optimal solution: '+str(solution_cost))

    for solution in final_solution:
        print(solution)

    for vehicle in vehicles:
        print('Vehicle '+vehicle.name+': Occupied: '+str(vehicle.occupied_space)+', Free: '+str(vehicle.capacity - vehicle.occupied_space))