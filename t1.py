import sys

def read_input():
    if sys.stdin.isatty():
        raise FileNotFoundError('Input file not found')
    
    input_data = []
    # read all lines from input file
    for line in sys.stdin:
        input_data.append((list(map(int, line.split(" ")))))
    # split the first line (number of machines and demands)
    machines_count, demands_count = input_data.pop(0)
    if demands_count != len(input_data):
        raise IndexError('The number of declared demands is different from expected (declared: {current} expected: {expected})'.format(current=len(input_data), expected=demands_count))
    return [machines_count, demands_count, input_data]

def list_possibilities(demands):
    # TODO
    return 0

def output_lp_solve():
    # TODO
    return 0

def main():
    try:
        machines_count, demands_count, demands = read_input()
    except (FileNotFoundError, IndexError) as e:
        print('Error:', e)
        sys.exit(1)
    print('Number of Machines: ', machines_count)
    print('Number of Demands: ', demands_count)
    print('Demands: ', demands)

main()
