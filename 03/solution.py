print("Part 1")

def parse(wires):
    return [wire.split(",") for wire in wires.split("\n")]

def traverse_wire(wire, foo, measure_delay=False):
    position = [0,0]
    delay = 1
    direction = {'R':(1,0), 'L':(-1,0), 'U':(0,1), 'D':(0,-1)}
    for segment in wire:
        subseg = direction[segment[0]]
        for _ in range(int(segment[1:])):
            position[0] = position[0] + subseg[0]
            position[1] = position[1] + subseg[1]
            if measure_delay:
                foo(tuple(position), delay)
                delay += 1
            else:
                foo(tuple(position))

def nearest_intersect(input):
    wires = parse(input)
    wire0 = set()
    traverse_wire(wires[0], lambda x: wire0.add(x))
    intersections = []
    traverse_wire(wires[1], lambda x: intersections.append(x) if x in wire0 else False)
    dist = [abs(x[0]) + abs(x[1]) for x in intersections]
    return min(dist)

test = """R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83"""
assert nearest_intersect(test) == 159
test = """R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"""
assert nearest_intersect(test) == 135

input = ''.join(open("input.txt", "r").readlines())
print(nearest_intersect(input))

print("\nPart 2")

def min_signal_delay(input):
    wires = parse(input)
    wire0 = {}
    traverse_wire(wires[0], lambda pos, delay: wire0.update({pos: delay}) if pos not in wire0 else False, measure_delay=True)
    delays = []
    traverse_wire(wires[1], lambda pos, delay: delays.append(delay + wire0[pos]) if pos in wire0 else False, measure_delay=True)
    return min(delays)

test = """R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83"""
assert min_signal_delay(test) == 610
test = """R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"""
assert min_signal_delay(test) == 410

print(min_signal_delay(input))