import csv
import sys
import numpy as np

from models import vehicle as vehicle_model
from models import package as package_model
from models import cost as cost_model

vehicles = {}
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
            vehicle_name = row[0]
            vehicle = vehicle_model.Vehicle(vehicle_name, int(row[1]))
            vehicles[vehicle_name] = vehicle

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
            package_name = row[0]
            vehicle_name = row[1]
            cost = row[2]

            package = next((package for package in packages if package.name == package_name), None)
            vehicle = vehicles[vehicle_name]

            cost = cost_model.Cost(package, vehicle, int(cost))

            if package_name in matrix_costs:
                matrix_costs[package_name].append(cost)
            else:
                matrix_costs[package_name] = []
                matrix_costs[package_name].append(cost)

    # Sort packages
    packages = sorted(packages, key=lambda x: x.weight, reverse=True)

    print([package.weight for package in packages])
    # Check data
    #for vehicle_key in list(vehicles.keys()):
    #    print('Name: ', str(vehicle_key) + ', Capacity: '+ str(vehicles[vehicle_key].capacity))

    #for package in packages:
    #    print('Name: ', package.name + ', Weight: '+ str(package.weight))

    #for key in list(matrix_costs.keys()):
    #    print('Key: ', str(key) + ', Costs: '+ str(matrix_costs[key]))

    # Init algorithm
    for package in packages:
        package_name = package.name
        package_costs = matrix_costs[package_name]

        # Sort costs
        sorted_costs = sorted(package_costs, key=lambda x: (x.cost, -(x.vehicle.capacity-x.vehicle.occupied_space)))
        i = len(package_costs)
        a = 0
        print([(sorted_cost.vehicle.name, sorted_cost.cost, (sorted_cost.vehicle.capacity-sorted_cost.vehicle.occupied_space)) for sorted_cost in sorted_costs])
        #print([(sorted_cost.cost, sorted_cost.vehicle.occupied_space) for sorted_cost in sorted_costs])

        while i > 0:
            # Get min cost of costs hash for package
            min_cost = sorted_costs[a].cost
            vehicle_name = sorted_costs[a].vehicle.name

            # Get vehicle capacity
            vehicle = vehicles[vehicle_name]
            free_space = vehicle.capacity - vehicle.occupied_space

            # Check vehicle capacity
            # if is lower, then add to solution and change vehicle capacity
            if package.weight <= free_space and package.incompatibles not in vehicle.packages:
                # Add to solution
                final_solution.append('Package: '+ package.name + ', Vehicle: '+ vehicle_name + ', Cost: '+str(min_cost))
                vehicle.packages.append(package.name)
                vehicle.occupied_space += package.weight
                solution_cost += min_cost
                i = 0
                print('EL PAQUETE '+str(package.name)+' SE ASIGNO A '+str(vehicle.name)+', COSTO: '+str(min_cost)+' , ESPACIO LIBRE: '+str(vehicle.capacity-vehicle.occupied_space))
            else:
                print('EL PAQUETE '+str(package.name)+' NO PUEDE SER ASIGNADO A '+str(vehicle.name)+', CARGA: '+str(package.weight)+' , ESPACIO LIBRE: '+str(vehicle.capacity-vehicle.occupied_space))
                i -= 1
                a += 1

    # Check results
    print('Optimal solution: '+str(solution_cost))

    for solution in final_solution:
        print(solution)

    for vehicle_key in list(vehicles.keys()):
        print('Vehicle '+vehicle_key+': Occupied: '+str(vehicles[vehicle_key].occupied_space)+', Free: '+str(vehicles[vehicle_key].capacity - vehicles[vehicle_key].occupied_space))