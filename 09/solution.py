import time
print("Part 1")

def parse(program):
    program = [int(x) for x in program.split(",")]
    for _ in range(1000):
        program.append(0)
    return program

class Intcomputer():
    def __init__(self, program_str, noun=None, verb=None, inputs=[]):
        self.inputs = inputs
        self.program = parse(program_str)
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
                val = self.inputs.pop()
                self.program[args[0]] = val
                # print(f"mem[{args[0]}] updated to {val}")
            elif opcode == 4: # output
                increment = 2
                # outputs.append(args[0])
                self.position += increment
                # print(f"output from mem[{args[0]}]")
                return  args[0]
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
                return None
            else:
                print(f"Fuck {opcode}")
            self.position += increment

    def run_until_done(self):
        total_output = []
        output = self.run_program()
        while output != None:
            total_output.append(output)
            output = self.run_program()
        return total_output
    
    def input(self, value):
        self.inputs.insert(0, value)


test = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
computer = Intcomputer(test)
assert computer.run_until_done() == [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]

test = "1102,34915192,34915192,7,4,7,99,0"
computer = Intcomputer(test)
assert computer.run_until_done()[0] >= 1e15

test = "104,1125899906842624,99"
computer = Intcomputer(test)
assert computer.run_until_done()[0] == 1125899906842624

input = ''.join(open("input.txt", "r").readlines())
computer = Intcomputer(input, inputs=[1])
print(computer.run_until_done())

print("\nPart 2")

input = ''.join(open("input.txt", "r").readlines())
computer = Intcomputer(input, inputs=[2])
print(computer.run_until_done())

