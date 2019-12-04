print("Part 1")

def parse(modules):
    return [int(x) for x in input.split("\n")]

def mass_to_fuel(mass):
    return mass // 3 - 2

assert mass_to_fuel(12) == 2
assert mass_to_fuel(14) == 2
assert mass_to_fuel(1969) == 654
assert mass_to_fuel(100756) == 33583

input = ''.join(open("input.txt", "r").readlines())
modules = parse(input)
print(sum([mass_to_fuel(m) for m in modules]))

print("\nPart 2")

def recursive_mass_to_fuel(mass):
    total = 0
    fuel_mass = mass_to_fuel(mass)
    while fuel_mass > 0:
        total += fuel_mass
        fuel_mass = mass_to_fuel(fuel_mass)
    return total

assert recursive_mass_to_fuel(12) == 2
assert recursive_mass_to_fuel(1969) == 966
assert recursive_mass_to_fuel(100756) == 50346

print(sum([recursive_mass_to_fuel(m) for m in modules]))
