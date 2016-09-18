import random as rndm
import numpy as np

def two_sat_backtrack(n_vars, clauses):

    # build list with relative clauses for each variable. From of the entries:
    # req[i_var][var_value][req_var, req_value]

    # Build 4 lists of lists, one for combination of booleans that would violate a clause
    t_reqs_t = [[] for x in range(n_vars)]
    t_reqs_f = [[] for x in range(n_vars)]
    f_reqs_t = [[] for x in range(n_vars)]
    f_reqs_f = [[] for x in range(n_vars)]

    # Initialize list to keep track of how many clauses each variable is involved in
    var_n_clauses = [0 for x in range(n_vars)]

    for clause in clauses:
        var1, var2 = abs(clause)-1
        val1, val2 = (clause >= 0)

        var_n_clauses[var1] += 1
        var_n_clauses[var2] += 1

        if val1:
            if val2: # v1 or v2
                f_reqs_t[var1].append(var2)
                f_reqs_t[var2].append(var1)
            else: # v1 or not v2
                f_reqs_f[var1].append(var2)
                t_reqs_t[var2].append(var1)
        else:
            if val2: # not v1 or v2
                t_reqs_t[var1].append(var2)
                f_reqs_f[var2].append(var1)
            else: # not v1 or not v2
                t_reqs_f[var1].append(var2)
                t_reqs_f[var2].append(var1)

    conflict_found = False
    i_start = 0
    bool_start = True
    feasible = True
    local_conflict = [False, False]

    while i_start < n_vars and not conflict_found:

        reqs = np.zeros((n_vars, 2), dtype=bool)

        if var_n_clauses[i_start] > 1:
            local_conflict[bool_start] = propagate(reqs, i_start, bool_start, t_reqs_t, t_reqs_f, f_reqs_t, f_reqs_f)

        # update iterators
        if bool_start:
            bool_start = False
        else:
            bool_start = True
            if sum(local_conflict) ==2:
                feasible = False
            local_conflict = [False, False]
            i_start += 1

    return feasible

def propagate(reqs, i_start, bool_start, t_reqs_t, t_reqs_f, f_reqs_t, f_reqs_f):
    reqs[i_start, bool_start] = True

    if bool_start:
        for target in t_reqs_t[i_start]:
            if reqs[target, 0]:
                conflict_found = True
                return conflict_found
            elif not reqs[target, 1]:
                conflict_found = propagate(reqs, target, True, t_reqs_t, t_reqs_f, f_reqs_t, f_reqs_f)
                if conflict_found:
                    return conflict_found

        for target in t_reqs_f[i_start]:
            if reqs[target, 1]:
                conflict_found = True
                return conflict_found
            elif not reqs[target, 0]:
                conflict_found = propagate(reqs, target, False, t_reqs_t, t_reqs_f, f_reqs_t, f_reqs_f)
                if conflict_found:
                    return conflict_found

    else:
        for target in f_reqs_t[i_start]:
            if reqs[target, 0]:
                conflict_found = True
                return conflict_found
            elif not reqs[target, 1]:
                conflict_found = propagate(reqs, target, True, t_reqs_t, t_reqs_f, f_reqs_t, f_reqs_f)
                if conflict_found:
                    return conflict_found

        for target in f_reqs_f[i_start]:
            if reqs[target, 1]:
                conflict_found = True
                return conflict_found
            elif not reqs[target, 0]:
                conflict_found  = propagate(reqs, target, False, t_reqs_t, t_reqs_f, f_reqs_t, f_reqs_f)
                if conflict_found:
                    return conflict_found

    return False