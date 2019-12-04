def run_1202_program(program_str):
    program = [int(x) for x in program_str.split(",")]
    program[1] = 12
    program[2] = 2
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

# program = "1,0,0,0,99"
# print(run_program(program))

# program = "2,3,0,3,99"
# print(run_program(program))

# program = "2,4,4,5,99,0"
# print(run_program(program))

# program = "1,1,1,4,99,5,6,0,99"
# print(run_program(program))

print(run_1202_program(program))

