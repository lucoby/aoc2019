print("Part 1")

def parse(program):
    program = [int(x) for x in program.split(",")]
    for _ in range(1000):
        program.append(0)
    return program

class Intcomputer():
    def __init__(self, program_str, zero=None, noun=None, verb=None, inputs=[]):
        self.inputs = inputs
        self.program = parse(program_str)
        if zero is not None:
            self.program[0] = zero
        if noun is not None:
            self.program[1] = noun
        if verb is not None:
            self.program[2] = verb
        self.position = 0
        self.relative_position = 0

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
            # print(f"opcode {self.program[self.position]}")
            params = self.get_param_mode()
            increment = 4
            if opcode in [3, 4, 9]:
                increment = 2
            if opcode in [5, 6]:
                increment = 3
            while len(params) < increment - 1:
                params.append(0)
            # print(f"params: {params}")
            args = []
            for i in range(len(params)):
                if params[i] == 0:
                    if i == increment - 2 and opcode not in [4, 5, 6, 9]:
                        args.append(self.program[self.position + i + 1])
                    else:
                        args.append(self.program[self.program[self.position + i + 1]])
                elif params[i] == 1:
                    args.append(self.program[self.position + i + 1])
                elif params[i] == 2:
                    if i == increment - 2 and opcode not in [4, 5, 6, 9]:
                        args.append(self.relative_position + self.program[self.position + i + 1])
                    else:
                        args.append(self.program[self.relative_position + self.program[self.position + i + 1]])
            # print(f"args: {args}")
            if opcode == 1: # +
                self.program[args[2]] = args[0] + args[1]
                # print(f"mem[{args[2]}] = {args[0]} + {args[1]}")
            elif opcode == 2: # *
                self.program[args[2]] = args[0] * args[1]
                # print(f"mem[{args[2]}] = {args[0]} * {args[1]}")
            elif opcode == 3: # input
                increment = 2
                if len(self.inputs) < 1:
                    return None
                val = self.inputs.pop()
                self.program[args[0]] = val
                # print(f"mem[{args[0]}] updated to {val}")
            elif opcode == 4: # output
                increment = 2
                # outputs.append(args[0])
                self.position += increment
                # print(f"output from mem[{args[0]}]")
                return args[0]
            elif opcode == 5: # jump if true
                increment = args[1] - self.position if args[0] != 0 else 3
                # print(f"jumping to {args[1]} if {args[0]} isn't 0")
            elif opcode == 6: # jump if false
                increment = args[1] - self.position if args[0] == 0 else 3
                # print(f"jumping to {args[1]} if {args[0]} is 0")
            elif opcode == 7: # <
                self.program[args[2]] = 1 if args[0] < args[1] else 0
                # print(f"loc[{args[2]}] = 1 if {args[0]} < {args[1]} else 0")
            elif opcode == 8: # ==
                self.program[args[2]] = 1 if args[0] == args[1] else 0
                # print(f"loc[{args[2]}] = 1 if {args[0]} == {args[1]} else 0")
            elif opcode == 9: # update relative position
                self.relative_position += args[0]
                # print(f"relative position += {args[0]} to {self.relative_position}")
                increment = 2
            elif opcode == 99: # done
                # print("hello")
                return None
            else:
                print(f"Fuck {opcode}")
            self.position += increment

    def run_until_done_or_input(self):
        total_output = []
        output = self.run_program()
        while output != None:
            total_output.append(output)
            output = self.run_program()
        return total_output

    def run_until_done(self, handle_input=lambda x: x):
        output = self.run_until_done_or_input()
        while self.program[self.position] != 99:
            handled_inputs = handle_input(output)
            self.inputs.append(handled_inputs)
            output = self.run_until_done_or_input()
        return output
    
    def input_value(self, value):
        self.inputs.insert(0, value)


p_input = ''.join(open("input.txt", "r").readlines())
intcomputer = Intcomputer(p_input)
print(len(list(filter(lambda x: x == 2, intcomputer.run_until_done()[2::3]))))


print("\nPart 2")

display = [[0 for x in range(41)] for y in range(25)]
def handle_input(output):
    i = 0
    while i < len(output):
        if output[i] != -1:
            display_map = {0: " ", 1: "#", 2: "=", 3: "_", 4: "o"}
            display[output[i+1]][output[i]] = display_map[output[i+2]]
            i += 3
        else:
            i += 3
    # print("\n".join(["".join(l) for l in display]))

    ball_x = 0
    paddle_x = 0
    for y in range(len(display)):
        for x in range(len(display[0])):
            if display[y][x] == "o":
                ball_x = x
            if display[y][x] == "_":
                paddle_x = x
    return -1 if ball_x < paddle_x else 1 if ball_x > paddle_x else 0

p_input = ''.join(open("input.txt", "r").readlines())
intcomputer = Intcomputer(p_input, zero=2)
print(intcomputer.run_until_done(handle_input=handle_input)[-1])