import csv
import sys
import numpy as np

from services import data_export
from services import data_extractor
from algorithm import vehicle_assign_calculator

if __name__ == "__main__":
    _, exp = sys.argv
    
    # Get data from txt files
    vehicles, packages, matrix_costs = data_extractor.get_data_from_txt(exp)

    # Call algorithm: Calculate vehicle for each package
    solution_cost, final_solution = vehicle_assign_calculator.calculate(vehicles, packages, matrix_costs)

    # Show results in console
    print('COSTO DE LA SOLUCIÓN: '+str(solution_cost))

    for solution in final_solution:
        print(solution)

    # Save results in txt
    data_export.export_results(exp, solution_cost, final_solution)