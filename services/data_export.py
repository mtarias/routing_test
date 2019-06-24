import os

# Method te write result to txt file
# Input: String exp, Integer solution_cost, Array<String> final_solution
def export_results(exp, solution_cost, final_solution):
    with open('results/results_'+exp+'.txt', 'w') as the_file:
        the_file.writelines('COSTE DE LA SOLUCIÓN: '+str(solution_cost)+ os.linesep)

        for solution in final_solution:
            the_file.writelines(solution+ os.linesep)