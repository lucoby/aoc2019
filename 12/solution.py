from functools import reduce

print("Part 1")

def parse(input):
    return [[int(pos) for pos in l.split(",")] for l in input.split("\n")]

def update_velocity(position, velocity):
    for i in range(len(position)):
        for j in range(len(position[0])):
            axis = [position[x][j] for x in range(len(position))]
            gravity_down = len(list(filter(lambda x: x < position[i][j], axis)))
            gravity_up = len(list(filter(lambda x: x > position[i][j], axis)))
            velocity[i][j] += gravity_up - gravity_down
    return position, velocity

def update_position(position, velocity):
    position = [[position[i][j] + velocity[i][j] for j in range(len(position[0]))] for i in range(len(position))]
    return position, velocity

def calculate_energy(position, velocity):
    pot_energy = [reduce(lambda x, y: x + y, map(lambda x: abs(x), position[i])) for i in range(len(position))]
    kin_energy = [reduce(lambda x, y: x + y, map(lambda x: abs(x), velocity[i])) for i in range(len(velocity))]
    return sum([pot_energy[i] * kin_energy[i] for i in range(len(pot_energy))])


def calculate_final_energy(input, iterations):
    position = parse(input)
    velocity = [[0 for i in range(3)] for j in range(4)]
    for i in range(iterations):
        position, velocity = update_velocity(position, velocity)
        position, velocity = update_position(position, velocity)
        # print(f"position: {position}")
        # print(f"velocity: {velocity}")
    return calculate_energy(position, velocity)

test = """-1,0,2
2,-10,-7
4,-8,8
3,5,-1"""
assert calculate_final_energy(test, 10) == 179
test = """-8,-10,0
5,5,10
2,-7,3
9,-8,-3"""
assert calculate_final_energy(test, 100) == 1940

input = ''.join(open("input.txt", "r").readlines())
print(calculate_final_energy(input, 1000))


print("\nPart 2")

def get_state(position, velocity, axis):
    return tuple([position[i][axis] for i in range(len(position))] + [velocity[i][axis] for i in range(len(velocity))])

def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b / gcd(a, b)

def repeat_state(input):
    repeat = []
    position = parse(input)
    velocity = [[0 for i in range(3)] for j in range(4)]
    original_states = set()
    for axis in range(3):
        original_states.add(get_state(position, velocity, axis=axis))
    found_states = set()
    i = 0
    while len(repeat) < 3:
        position, velocity = update_velocity(position, velocity)
        position, velocity = update_position(position, velocity)
        i += 1
        for axis in range(3):
            state = get_state(position, velocity, axis=axis)
            if state in original_states:
                repeat.append(i)
                found_states.add(state)
                original_states = original_states - found_states
                print(i)
    return reduce(lambda x, y: lcm(x, y), repeat)

test = """-1,0,2
2,-10,-7
4,-8,8
3,5,-1"""
assert repeat_state(test) == 2772

test = """-8,-10,0
5,5,10
2,-7,3
9,-8,-3"""
assert repeat_state(test) == 4686774924

print(repeat_state(input))