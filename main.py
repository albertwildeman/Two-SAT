from FileReadLib import get_2sat
from TwoSatLib import two_sat

n_cases = 1

satisfiable = [False for k in range(n_cases)]

for i_case in range(n_cases):

    # Read input file
    filename = "2sat" + str(i_case+1) + ".txt"
    n_variables, clauses = get_2sat(filename)

    # Run 2-sat algorithm
    satisfiable[i_case] = two_sat(n_variables, clauses)

    # Print result
    print("Solution found for case #" + str(i_case+1) + ": " + str(satisfiable[i_case]))

print("done.")