def recursive_mass_to_fuel(mass):
    total = 0
    fuel_mass = mass // 3 - 2
    while fuel_mass > 0:
        total += fuel_mass
        fuel_mass = fuel_mass // 3 - 2
    return total

# print(recursive_mass_to_fuel(12))
# print(recursive_mass_to_fuel(14))
# print(recursive_mass_to_fuel(1969))
# print(recursive_mass_to_fuel(100756))

total = 0
with open("input.txt", "r") as f:
    for l in f.readlines():
        total += recursive_mass_to_fuel(int(l))
print(f"part 1: {total}")
