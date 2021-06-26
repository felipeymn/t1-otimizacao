import sys

MAX_PERIOD = 540

PLUS_OPERATOR = ' + '


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
        raise IndexError(
            f'The number of declared demands is different from expected (declared: {len(input_data)} expected: {demands_count})')
    if machines_count <= 0:
        raise IndexError(
            f'The amount of machines should be greater than zero'
        )
    return input_data


def list_possibilities(limit, periods):
    current_combinations = [[period] for period in periods]
    possibilities = []
    aux = []
    shorter_period = min(periods)

    while current_combinations:
        for combination in current_combinations:
            combination_sum = sum(combination)
            if limit - combination_sum < shorter_period:
                # valid combination
                possibilities.append(combination)
            else:
                # filter function returns only values greater than the last element in combination
                for period in filter(lambda x: x >= combination[-1], periods):
                    if combination_sum + period <= limit:
                        aux.append(combination + [period])
        current_combinations = aux
        aux = []

    return possibilities


def create_model(demands, possibilities):
    constraints = []
    # create the objective function (min: x0 + x1 + ... + xn)
    objective_function = list(map(lambda x: f'x{x}', list(range(0, len(possibilities)))))

    # create the constraints by checking how many times a period appears in each possibility
    for amount, period in demands:
        current_expression = []
        for index, possibility in enumerate(possibilities):
            if period in possibility:
                count = possibility.count(period)
                current_expression.append(f'{str(count) + " " if count != 1 else ""}x{index}')
        current_expression.append(str(amount))
        constraints.append(current_expression)
    return objective_function, constraints


def output_lp_solve(objective_function, constraints):
    print(f'min: {PLUS_OPERATOR.join(objective_function)};')
    for constraint in constraints:
        amount = constraint.pop(-1)  # remove the last element (amount)
        print(f'{PLUS_OPERATOR.join(constraint)} >= {amount};')
    return 0


def print_log(demands, possibilities, objective_function, constraints):
    print('Demands: ', demands)
    print('Possibilities: ', possibilities)
    print('Expressions: ', objective_function, constraints)


def main():
    try:
        demands = read_input()
    except (FileNotFoundError, IndexError) as e:
        print('Error:', e)
        sys.exit(1)

    periods = [demand[-1] for demand in demands]
    possibilities = list_possibilities(MAX_PERIOD, periods)
    objective_function, constraints = create_model(demands, possibilities)
    output_lp_solve(objective_function, constraints)
    # print_log(demands, possibilities, objective_function, constraints)


if __name__ == '__main__':
    main()
