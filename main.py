from FileReadLib import get_2sat
from TwoSatLib import two_sat_kosaraju
from TwoSatLib import two_sat_papadimitriou

# method = "kosaraju"
method = "papadimitriou"
test_mode = False

# Parameter to set maximum number of independent searches in papadimitriou's algorithm.
max_searches = 1

if test_mode:
    n_cases = 2
    filename_root = "2sat_test"
else:
    n_cases = 6
    filename_root = "2sat"

# Initialize list that will hold results
satisfiable = [False for k in range(n_cases)]

for i_case in range(n_cases):

    # Read input file
    filename = filename_root + str(i_case+1) + ".txt"
    n_variables, clauses = get_2sat(filename)

    print("Working on file: " + filename)

    # Run 2-sat algorithm
    if method == "kosaraju":
        satisfiable[i_case] = two_sat_kosaraju(n_variables, clauses)
    elif method == "papadimitriou":
        satisfiable[i_case] = two_sat_papadimitriou(n_variables, clauses, max_searches)
    else:
        raise(NameError, "Invalid method specified.")

    # Print result
    print("Solution found for case #" + str(i_case+1) + ": " + str(satisfiable[i_case]))

print("done.")