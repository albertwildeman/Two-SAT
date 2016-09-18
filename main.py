from FileReadLib import get_2sat
from TwoSatLib import two_sat_backtrack

test_mode = True

# Parameter to set maximum number of independent searches in papadimitriou's algorithm.
max_searches = 1

if test_mode:
    n_cases = 6
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
    satisfiable[i_case] = two_sat_backtrack(n_variables, clauses)

    # Print result
    print("Solution possible for case #" + str(i_case+1) + ": " + str(satisfiable[i_case]))

print("done.")