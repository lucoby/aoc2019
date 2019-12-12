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

def robot_sim(input, start_color = 0):
    hull = {}
    position = (0, 0)
    orientation = "up"
    directions = {"left": (-1, 0), "right": (1, 0), "up": (0, 1), "down": (0, -1)}
    relative_pos ={"up": ("left", "right"), "left": ("down", "up"), "down": ("right", "left"), "right": ("up", "down")}
    computer = Intcomputer(input, inputs=[start_color])
    i = 0
    while True:
        # print(f"i: {i}")
        color = computer.run_program()
        # print(f"color: {color}")
        if color == None:
            break
        direction = computer.run_program()
        # print(f"dir: {direction}")
        hull[position] = color
        # print(f"hull: {hull}")
        orientation = relative_pos[orientation][direction]
        position = (position[0] + directions[orientation][0], position[1] + directions[orientation][1])
        # print(f"new pos: {position}")
        # print(f"new ori: {orientation}")
        computer.input(hull[position] if position in hull else 0)
        i += 1
        # if i > 20:
        #     break
    return hull


input = ''.join(open("input.txt", "r").readlines())
print(len(robot_sim(input)))


print("\nPart 2")

input = "".join(open("input.txt", "r").readlines())
hull = robot_sim(input, start_color=1)
hull_arr = [["#" for i in range(50)] for j in range(10)]
for coord in hull:
    hull_arr[coord[1] + 6][coord[0]+1] = "#" if hull[coord] == 0 else " "
print("\n".join(["".join(l) for l in hull_arr]))