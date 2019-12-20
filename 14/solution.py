from math import ceil

print("Part 1")

def parse_chemicals(chemicals):
    return {c.split(" ")[1]: int(c.split(" ")[0]) for c in chemicals}
    # return [c for c in chemicals.split(" ")]

def parse_reaction(reaction):
    input, output = reaction.split("=>")
    # return {"input": parse_chemicals(input.strip().split(", ")), "output": parse_chemicals(output.strip().split(", "))}
    output_of_equation = parse_chemicals(output.strip().split(", "))
    assert len(output_of_equation) == 1
    output_chemical = list(output_of_equation.keys())[0]
    output_quantity = output_of_equation[output_chemical]
    input_of_equation = parse_chemicals(input.strip().split(", "))
    return output_chemical, {"quantity": output_quantity, "input": input_of_equation}

def parse(input):
    return {parse_reaction(l)[0]: parse_reaction(l)[1] for l in input.split("\n")}

def get_ore(equations, quantity, chemical, inventory):
    ore = 0
    for child in equations[chemical]["input"]:
        # print(f"chem: {chemical}, quant: {quantity}, child: {child}")
        if child == "ORE":
            factor = ceil(quantity / equations[chemical]["quantity"])
            ore += equations[chemical]["input"]["ORE"] * factor
        else:
            factor = ceil(quantity / equations[chemical]["quantity"])
            if child in inventory:
                if inventory[child] > factor * equations[chemical]["input"][child]:
                    inventory[child] -= factor * equations[chemical]["input"][child]
                    # print(f"inv after: {inventory}")
                else:
                    child_quantity = factor * equations[chemical]["input"][child] - inventory.pop(child)
                    # print(f"inv before: {inventory}, child quant: {child_quantity}")
                    additional_ore, inventory = get_ore(equations, equations[child]["quantity"] * ceil(child_quantity / equations[child]["quantity"]), child, inventory)
                    inventory[child] -= child_quantity
                    # print(f"inv after: {inventory}")
                    ore += additional_ore
            else:
                # print(f"inv before: {inventory} factor = {factor}")
                child_quantity = factor * equations[chemical]["input"][child]
                additional_ore, inventory = get_ore(equations, equations[child]["quantity"] * ceil(child_quantity / equations[child]["quantity"]), child, inventory)
                inventory[child] -= factor * equations[chemical]["input"][child]
                # print(f"inv after: {inventory}")
                ore += additional_ore
    inventory[chemical] = quantity
    return ore, inventory

def ore_to_fuel(input):
    equations = parse(input)
    ore, inventory = get_ore(equations, 1, "FUEL", {})
    # print(f"ore: {ore}, final inv: {inventory}")
    return ore


    


test = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""
assert ore_to_fuel(test) == 31

test = """9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL"""
assert ore_to_fuel(test) == 165

test = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""
assert ore_to_fuel(test) == 13312

test = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF"""
assert ore_to_fuel(test) == 180697

test = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""
assert ore_to_fuel(test) == 2210736

input = ''.join(open("input.txt", "r").readlines())
print(ore_to_fuel(input))


print("\nPart 2")

def fuel_for_ore_search(equations, fuel, lower=0, upper=None, total_ore=1_000_000_000_000):
    ore, _ = get_ore(equations, fuel, "FUEL", {})
    # print(f"ore: {ore:.2E}, fuel: {fuel}, lower: {lower}, upper: {upper}")
    if lower == fuel:
        return lower
    elif ore < total_ore and upper == None:
        return fuel_for_ore_search(equations, fuel * 2, lower=fuel, upper=None)
    elif ore < total_ore:
        return fuel_for_ore_search(equations, (fuel + upper) // 2, lower=fuel, upper=upper)
    else:
        return fuel_for_ore_search(equations, (lower + fuel) // 2, lower=lower, upper=fuel)
    
def fuel_for_ore(input, total_ore=1_000_000_000_000):
    equations = parse(input)
    ore, _ = get_ore(equations, 1, "FUEL", {})
    fuel = total_ore // ore
    # while ore < total_ore:
    #     print(fuel)
    #     fuel += 1
    #     ore, _ = get_ore(equations, fuel, "FUEL", {})
    # return fuel - 1
    return fuel_for_ore_search(equations, fuel * 2, lower=fuel)

test = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""
assert fuel_for_ore(test) == 82892753

test = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF"""
assert fuel_for_ore(test) == 5586022

test = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""
assert fuel_for_ore(test) == 460664

print(fuel_for_ore(input))