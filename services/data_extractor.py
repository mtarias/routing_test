from models import vehicle as vehicle_model
from models import package as package_model
from models import cost as cost_model

import csv

# Method to get data from txt files to use in algorithm
# Input: String exp_name, Dict<Vehicle> vehicles, Dict<Cost> matrix_costs
# Output: Dict<Vehicle> vehicles, Array<Package> packages, Dict<Cost> matrix_costs
def get_data_from_txt(exp_name):
    vehicles = get_vehicles(exp_name)
    packages = get_packages(exp_name)
    matrix_costs = get_costs(exp_name, vehicles, packages)

    # Check data
    #for vehicle_key in list(vehicles.keys()):
    #    print('Name: ', str(vehicle_key) + ', Capacity: '+ str(vehicles[vehicle_key].capacity))

    #for package in packages:
    #    print('Name: ', package.name + ', Weight: '+ str(package.weight))

    #for key in list(matrix_costs.keys()):
    #    print('Key: ', str(key) + ', Costs: '+ str(matrix_costs[key]))

    return vehicles, packages, matrix_costs

def get_vehicles(exp_name):
    vehicles = {}

    # Read vehicles list
    with open('data/'+exp_name+'/vehicles.txt','r') as f:
        data = csv.reader(f)
        for row in data:
            vehicle_name = row[0]
            vehicle = vehicle_model.Vehicle(vehicle_name, int(row[1]))
            vehicles[vehicle_name] = vehicle
    return vehicles

def get_packages(exp_name):
    packages = []
    incompatibles = {}

    # Read incompatible
    with open('data/'+exp_name+'/incompatible.txt','r') as f:
        data = csv.reader(f)
        for row in data:
            incompatibles[row[0]] = row[1]
            incompatibles[row[1]] = row[0]

    # Read Packages list
    with open('data/'+exp_name+'/packages.txt','r') as f:
        data = csv.reader(f)
        for row in data:
            incompatibles_for_package = incompatibles[row[0]] if row[0] in incompatibles else []
            package = package_model.Package(row[0], int(row[1]), incompatibles_for_package)
            packages.append(package)

    return packages

def get_costs(exp_name, vehicles, packages):
    matrix_costs = {}
    # Read weights
    with open('data/'+exp_name+'/costs.txt','r') as f:
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

    return matrix_costs