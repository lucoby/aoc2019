from itertools import permutations

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

def calculate_thrust(program, phase_settings):
    input = 0
    for phase_setting in phase_settings:
        outputs = run_program(program, inputs=[input, phase_setting])
        input = outputs[0]
    return input

def max_output(program):
    max_thrust = 0
    for permutation in permutations(range(5)):
        thrust = calculate_thrust(program, permutation)
        if thrust > max_thrust:
            max_thrust = thrust
    return max_thrust

test = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
assert max_output(test) == 43210

test = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
assert max_output(test) == 54321

test = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
assert max_output(test) == 65210

input = ''.join(open("input.txt", "r").readlines())
print(max_output(input))


print("\nPart 2")

class Intcomputer():
    def __init__(self, program_str, noun=None, verb=None, inputs=[]):
        self.inputs = inputs
        self.program = parse(program_str)
        if noun is not None:
            self.program[1] = noun
        if verb is not None:
            self.program[2] = verb
        self.position = 0

    def get_opcode(self):
        return self.program[self.position] % 100

    def get_param_mode(self):
        instruction = self.program[self.position]
        instruction //= 100
        param_mode = []
        while instruction > 0:
            param_mode.append(instruction % 10)
            instruction //= 10
        return param_mode

    def run_program(self):
        while self.program[self.position] != 99:
            opcode = self.get_opcode()
            # print(f"opcode {opcode}")
            params = self.get_param_mode()
            increment = 4
            if opcode in [3, 4]:
                increment = 2
            if opcode in [5, 6]:
                increment = 3
            while len(params) < increment - 1:
                params.append(0)
            # print(f"params: {params}")
            args = [self.program[self.program[self.position + i + 1]] if params[i] == 0 else self.program[self.position + i + 1] for i in range(len(params))]
            # print(f"args: {args}")
            if opcode == 1: # +
                self.program[self.program[self.position + 3]] = args[0] + args[1]
            elif opcode == 2: # *
                self.program[self.program[self.position + 3]] = args[0] * args[1]
            elif opcode == 3: # input
                increment = 2
                self.program[self.program[self.position + 1]] = self.inputs.pop()
            elif opcode == 4: # output
                increment = 2
                # outputs.append(args[0])
                self.position += increment
                return  args[0]
            elif opcode == 5: # jump if true
                increment = args[1] - self.position if args[0] != 0 else 3
            elif opcode == 6: # jump if false
                increment = args[1] - self.position if args[0] == 0 else 3
            elif opcode == 7: # <
                self.program[self.program[self.position + 3]] = 1 if args[0] < args[1] else 0
            elif opcode == 8: # ==
                self.program[self.program[self.position + 3]] = 1 if args[0] == args[1] else 0
            elif opcode == 99: # done
                return None
            else:
                print(f"Fuck {opcode}")
            self.position += increment
    
    def input(self, value):
        self.inputs.insert(0, value)
    
def calculate_thrust_p2(program, phase_settings):
    input = 0
    thruster = 0
    amp = []
    for i, phase_setting in enumerate(phase_settings):
        amp.append(Intcomputer(program, inputs=[input, phase_setting]))
        input = amp[i].run_program()
        if i == 4:
            thruster = input
    i = 0
    while input != None:
        amp[i].input(input)
        input = amp[i].run_program()
        if i == 4:
            thruster = input
            i = -1
        i += 1
    return thruster

def max_output_p2(program):
    max_thrust = 0
    for permutation in permutations(range(5, 10)):
        thrust = calculate_thrust_p2(program, permutation)
        if thrust > max_thrust:
            max_thrust = thrust
    return max_thrust

test = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
computer = Intcomputer(test, inputs=[7])
assert computer.run_program() == 999
computer = Intcomputer(test, inputs=[8])
assert computer.run_program() == 1000
computer = Intcomputer(test, inputs=[9])
assert computer.run_program() == 1001

test="3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
assert max_output_p2(test) == 139629729

test="3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"
assert max_output_p2(test) == 18216

input = ''.join(open("input.txt", "r").readlines())
print(max_output_p2(input))