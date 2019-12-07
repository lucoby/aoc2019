print("Part 1")

def parse(input):
    return [orbit.split(')') for orbit in input.split('\n')]

def get_orbits(input):
    orbits = parse(input)
    bodies = {}
    for orbit in orbits:
        if orbit[0] not in bodies:
            bodies[orbit[0]] = set()
        if orbit[1] not in bodies:
            bodies[orbit[1]] = set()
        bodies[orbit[0]].add(orbit[1])
    return bodies

def orbit_checksum(input):
    orbits = get_orbits(input)

    checksum = 0
    bodies_to_count = [("COM", 0)]
    while len(bodies_to_count) > 0:
        body = bodies_to_count.pop()
        checksum += body[1]
        for orbiting in orbits[body[0]]:
            bodies_to_count.append((orbiting, body[1] + 1))
    return checksum

test = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""
assert orbit_checksum(test) == 42

input = ''.join(open("input.txt", "r").readlines())
print(orbit_checksum(input))


print("\nPart 2")

def get_parents(input):
    orbits = parse(input)
    parents = {orbit[1]: orbit[0] for orbit in orbits}
    return parents

def get_orbits_to_com(orbits, body):
    chain = [body]
    orbit = orbits[body]
    while orbit != 'COM':
        chain.append(orbit)
        orbit = orbits[orbit]
    chain.append('COM')
    return chain

def min_orbit_transfers(input):
    parents = get_parents(input)
    you_orbits = get_orbits_to_com(parents, 'YOU')
    san_orbits = get_orbits_to_com(parents, 'SAN')
    i = -1
    while you_orbits[i] == san_orbits[i]:
        i -= 1
    return len(you_orbits) + len(san_orbits) + 2 * i

test = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""
assert min_orbit_transfers(test) == 4

input = ''.join(open("input.txt", "r").readlines())
print(min_orbit_transfers(input))
