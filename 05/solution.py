print("Part 1")

def parse(program):
    return [int(x) for x in program.split(",")]

def get_opcode(instruction):
    return instruction % 100

def get_param_mode(instruction):
    instruction //= 100
    param_mode = []
    while instruction > 0:
        param_mode.append(instruction % 10)
        instruction //= 10
    return param_mode

def run_program(program_str, noun=None, verb=None, inputs=[]):
    program = parse(program_str)
    outputs = []
    if noun is not None:
        program[1] = noun
    if verb is not None:
        program[2] = verb
    position = 0
    while program[position] != 99:
        opcode = get_opcode(program[position])
        # print(f"opcode {opcode}")
        params = get_param_mode(program[position])
        increment = 4
        if opcode in [3, 4]:
            increment = 2
        while len(params) < increment - 1:
            params.append(0)
        # print(params)
        args = [program[program[position + i + 1]] if params[i] == 0 else program[position + i + 1] for i in range(len(params))]
        if opcode == 1:
            program[program[position + 3]] = args[0] + args[1]
        elif opcode == 2:
            program[program[position + 3]] = args[0] * args[1]
        elif opcode == 3:
            increment = 2
            program[program[position + 1]] = inputs.pop()
        elif opcode == 4:
            increment = 2
            outputs.append(args[0])
        else:
            print(f"Fuck {opcode}")
        position += increment
    return outputs

input = ''.join(open("input.txt", "r").readlines())
print(run_program(input, inputs=[1])[-1])


print("\nPart 2")
def run_program_p2(program_str, noun=None, verb=None, inputs=[]):
    program = parse(program_str)
    outputs = []
    if noun is not None:
        program[1] = noun
    if verb is not None:
        program[2] = verb
    position = 0
    while program[position] != 99:
        opcode = get_opcode(program[position])
        # print(f"opcode {opcode}")
        params = get_param_mode(program[position])
        increment = 4
        if opcode in [3, 4]:
            increment = 2
        if opcode in [5, 6]:
            increment = 3
        while len(params) < increment - 1:
            params.append(0)
        # print(f"params: {params}")
        args = [program[program[position + i + 1]] if params[i] == 0 else program[position + i + 1] for i in range(len(params))]
        # print(f"args: {args}")
        if opcode == 1: # +
            program[program[position + 3]] = args[0] + args[1]
        elif opcode == 2: # *
            program[program[position + 3]] = args[0] * args[1]
        elif opcode == 3: # input
            increment = 2
            program[program[position + 1]] = inputs.pop()
        elif opcode == 4: # output
            increment = 2
            outputs.append(args[0])
        elif opcode == 5: # jump if true
            increment = args[1] - position if args[0] != 0 else 3
        elif opcode == 6: # jump if false
            increment = args[1] - position if args[0] == 0 else 3
        elif opcode == 7: # <
            program[program[position + 3]] = 1 if args[0] < args[1] else 0
        elif opcode == 8: # ==
            program[program[position + 3]] = 1 if args[0] == args[1] else 0
        else:
            print(f"Fuck {opcode}")
        position += increment
    return outputs


assert run_program_p2("3,9,8,9,10,9,4,9,99,-1,8", inputs=[8]) == [1]
assert run_program_p2("3,9,8,9,10,9,4,9,99,-1,8", inputs=[7]) == [0]

assert run_program_p2("3,9,7,9,10,9,4,9,99,-1,8", inputs=[7]) == [1]
assert run_program_p2("3,9,7,9,10,9,4,9,99,-1,8", inputs=[8]) == [0]

assert run_program_p2("3,3,1108,-1,8,3,4,3,99", inputs=[8]) == [1]
assert run_program_p2("3,3,1108,-1,8,3,4,3,99", inputs=[7]) == [0]

assert run_program_p2("3,3,1107,-1,8,3,4,3,99", inputs=[7]) == [1]
assert run_program_p2("3,3,1107,-1,8,3,4,3,99", inputs=[8]) == [0]

assert run_program_p2("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", inputs=[0]) == [0]
assert run_program_p2("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", inputs=[1]) == [1]

assert run_program_p2("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", inputs=[0]) == [0]
assert run_program_p2("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", inputs=[1]) == [1]

test = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
assert run_program_p2(test, inputs=[7]) == [999]
assert run_program_p2(test, inputs=[8]) == [1000]
assert run_program_p2(test, inputs=[9]) == [1001]



input = ''.join(open("input.txt", "r").readlines())
print(run_program_p2(input, inputs=[5])[0])
