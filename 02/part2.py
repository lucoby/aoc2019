def run_program_with_inputs(program_str, noun, verb):
    program = [int(x) for x in program_str.split(",")]
    program[1] = noun
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

program = None
with open("input.txt", "r") as f:
    for l in f.readlines():
        program = l
        
target = 19690720
for i in range(100):
    for j in range(100):
        output = run_program_with_inputs(program, i, j)
        if target == output[0]:
            print(f"i: {i}, j: {j}")