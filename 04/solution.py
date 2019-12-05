print("Part 1")

def parse(range):
    return [int(x) for x in range.split('-')]

def valid(password, additonal_criteria=False):
    if not len(password) == 6:
        return False
    
    adjacent_duplicate = False
    rising = True
    has_pair = False
    for i in range(5):
        if password[i] == password[i + 1]:
            adjacent_duplicate = True
        if password[i] > password[i + 1]:
            rising = False
        if additonal_criteria and password[i] == password[i + 1] and (i == 0 or password[i - 1] != password[i]) and (i == 4 or password[i + 1] != password[i + 2]):
            has_pair = True

    if not adjacent_duplicate:
        return False

    if not rising:
        return False 

    if additonal_criteria and not has_pair:
       return False 

    return True

def num_passwords(input, additional_criteria=False):
    pw_range = parse(input)
    num_passwords = 0
    for password in range(pw_range[0], pw_range[1]):
        if valid(str(password), additonal_criteria=additional_criteria):
            num_passwords += 1
    return num_passwords

assert valid("111111")
assert not valid("223450")
assert not valid("123789")

input = ''.join(open("input.txt", "r").readlines())
print(num_passwords(input))


print("\nPart 2")

assert valid("112233", additonal_criteria=True)
assert not valid("123444", additonal_criteria=True)
assert valid("111122", additonal_criteria=True)

print(num_passwords(input, additional_criteria=True))
