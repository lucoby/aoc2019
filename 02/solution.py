print("Part 1")

def parse(program):
    return [int(x) for x in program.split(",")]

def run_program(program_str, noun=None, verb=None):
    program = parse(program_str)
    if noun is not None:
        program[1] = noun
    if verb is not None:
        program[2] = verb
    position = 0
    while program[position] != 99:
        if program[position] == 1:
            program[program[position + 3]] = program[program[position + 1]] + program[program[position + 2]]
        elif program[position] == 2:
            program[program[position + 3]] = program[program[position + 1]] * program[program[position + 2]]
        else:
            print("fuck")
        position += 4
    return program

input = "1,0,0,0,99"
assert run_program(input) == parse("2,0,0,0,99")

input = "2,3,0,3,99"
assert run_program(input) == parse("2,3,0,6,99")

input = "2,4,4,5,99,0"
assert run_program(input) == parse("2,4,4,5,99,9801")

input = "1,1,1,4,99,5,6,0,99"
assert run_program(input) == parse("30,1,1,4,2,5,6,0,99")

input = ''.join(open("input.txt", "r").readlines())
print(run_program(input, noun=12, verb=2)[0])


print("\nPart 2")
target = 19690720
for i in range(100):
    for j in range(100):
        output = run_program(input, noun=i, verb=j)
        if target == output[0]:
            print(f"{i * 100 + j}")

