def get_2sat(filename):

    with open(filename, mode="r") as input_file:

        # Exctract raw lines from file
        raw_lines = input_file.readlines()

        # Get the number of variables from the first line
        n_variables = int(raw_lines[0][:-1])

        # Get the clauses of the 2-sat problem from all other lines
        string_lines = [x[:-1].split(" ") for x in raw_lines[1:]]
        clauses = [(int(x), int(y)) for x, y in string_lines]

    return n_variables, clauses