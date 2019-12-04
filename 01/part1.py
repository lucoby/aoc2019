def mass_to_fuel(mass):
    return mass // 3 - 2

# print(mass_to_fuel(12))
# print(mass_to_fuel(14))
# print(mass_to_fuel(1969))
# print(mass_to_fuel(100756))

total = 0
with open("input.txt", "r") as f:
    for l in f.readlines():
        total += mass_to_fuel(int(l))
print(f"part 1: {total}")
