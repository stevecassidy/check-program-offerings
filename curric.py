from pprint import pprint
import json

# A program is a dictionary of unit offerings:
# {
#     "COMP6010": {"offered": ["S1", "S2"], "prereq": []}, 
#     "COMP6F-DB":     {"offered": ["S1", "S2"], "prereq": []}, 
#     "COMP6F-PM":     {"offered": ["S1"], "prereq": []}, 
#     "COMP6F-Cloud":  {"offered": ["S2"], "prereq": []}, 
# within the program, units are ordered by sequence and unit code, 
# semester should alternate between S1 and S2 for successive sequence numbers



def satisfy_prereq(unit, sequence, program):
    """Have we satisfied all the pre-reqs for this unit?"""

    completed = [p['unit'] for p in program if p['sequence'] < sequence]
    return all([p in completed for p in unit['prereq']])

def available(program, semester, sequence, units):
    """Return a list of units that are available
    in the given semester given the list of units
    already completed in program"""

    result = [] 
    completed = [p['unit'] for p in program]
    for u in units.keys():
        ## if it's an option set, then add both of the units as long as neither one is in the program

        if semester in units[u]['offered'] and u not in completed and satisfy_prereq(units[u], sequence, program):
            result.append({"unit": u, "semester": semester, "sequence": sequence})
    
    #print("available", show(program), semester, sequence, "\n-->", result, "\n")
    return result

def cmp_offering(p):
    """Return a string that can be used to compare unit offerings"""
    return str(p['sequence']) + '-' + p['unit'] + '-' + p['semester']

def cmp_program(program):
    """Return a string that can be used to compare programs"""
    #return str(len(program)) + str(program)
    return str(len(program)) + '-' + '/'.join([cmp_offering(p) for p in program])

def already_present(program, programs):
    """Return True if program is already in the list of programs"""
    if programs == []:
        return False

    sh = cmp_program(program)
    for p in programs:
        if sh == cmp_program(p):
            return True
    return False

def extensions(program, semester, sequence, units):
    """Return a list of new programs that are possible 
    extensions of this program in the given semester"""

    result = [program]
    avail = available(program, semester, sequence, units)
    for ext in avail:
        pg = program.copy()
        pg.append(ext)
        pg.sort(key=cmp_offering) 
        result.append(pg)
    return result

def extend_programs(programs, semester, sequence, units):
    """Given a list of programs, extend them all"""

    result = []
    for program in programs:
        for ext in extensions(program, semester, sequence, units):
            if not already_present(ext, result):
                result.append(ext)
    return sorted(result, key=cmp_program)

def extend_sequence(progs, N, semester, sequence, units):
    """Choose N units"""

    for i in range(N):
        progs = extend_programs(progs, semester, sequence, units) 
    return progs

def prune_by_length(progs, length):
    """Remove any programs that aren't this length"""

    return [p for p in progs if len(p) >= length]

def show(program):
    """Print out a program in a csv format"""
    print(",Semester,Unit 1,Unit 2,Unit 3,Unit 4")
    for seq in range(4):
        units = [u for u in program if u['sequence'] == seq]
        print(seq, end=',')
        print(units[0]['semester'], end=',')
        for u in units:
            print(u['unit'], end=',')
        print('\n', end='')

def show_programs(programs):
    """Print out a list of programs"""
    if len(programs) == 0:
        print("No Study Plans Found")
    else:
        for program in programs:
            show(program)
            print(",,,,,,,,,")



def semester(start_semester, units):
    if (start_semester == "S1"):
        alt_semester = "S2"
    else:
        alt_semester = "S1"

    units_6000 = {u: units[u] for u in units if u[4] == '6'}

    progs = [[]]
    
    print(start_semester, 'Start')
    print(',,,')
    progs = extend_sequence(progs, 4, start_semester, 0, units_6000) 
    progs = prune_by_length(progs, 4)
    print(len(progs), "programs of length 4")
    progs = extend_sequence(progs, 4, alt_semester, 1, units_6000) 
    progs = prune_by_length(progs, 8)
    print(len(progs), "programs of length 8")
    progs = extend_sequence(progs, 4, start_semester, 2, units) 
    progs = prune_by_length(progs, 12)
    print(len(progs), "programs of length 12")
    progs = extend_sequence(progs, 2, alt_semester, 3, units) 
    progs = prune_by_length(progs, 14)
    print(len(progs), "programs of length 14")
    return progs

def show_units(units):
    """Output a csv table of the units"""
    print("Unit,S1,S2,Prereqs")
    for u in units.keys():
        print(u, end=',')
        print('Yes', end=',') if 'S1' in units[u]['offered'] else print('No', end=',')
        print('Yes', end=',') if 'S2' in units[u]['offered'] else print('No', end=',')
        print(','.join(units[u]['prereq']), end='\n')
    print(',,,,,,')


if __name__=='__main__':
    import sys
    with open(sys.argv[1]) as input:
        units = json.load(input)

    show_units(units)
    show_programs(semester("S1", units))
    show_programs(semester("S2", units))
