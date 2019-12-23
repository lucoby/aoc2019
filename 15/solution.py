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

current_pos = (0, 0)
directions = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}
inverse_d = {1: 2, 2: 1, 3: 4, 4: 3}
droid_command = None
frontier = [(0, 0)]
next_pos = None
route = []
backtrack = False
room_map = {current_pos: "D"}
goal = None

def pretty_map(origin=True):
    explored = list(room_map.keys())
    explored_x = [p[0] for p in explored]
    explored_y = [p[1] for p in explored]
    min_x, max_x = min(explored_x), max(explored_x)
    min_y, max_y = min(explored_y), max(explored_y)
    pretty_room = [[" " for x in range(min_x, max_x + 1)] for y in range(min_y, max_y + 1)]
    for p, status in room_map.items():
        pretty_room[p[1] + abs(min_y)][p[0] + abs(min_x)] = status
        if status == "!":
            print(f"oxygen system loc: {p}")
    if origin:
        pretty_room[abs(min_y)][abs(min_x)] = "O"
    print(f"min x: {min_x}, min_y: {min_y}")
    print("\n".join(["".join(l) for l in pretty_room]))

def handle_input(output):
    global droid_command
    global current_pos
    global next_pos
    global route
    global backtrack
    global goal

    if droid_command != None:
        droid_status = output[0]
        if droid_status == 0:
            wall_pos = (current_pos[0] + directions[droid_command][0], current_pos[1] + directions[droid_command][1])
            room_map[wall_pos] = "#"
            if wall_pos == next_pos:
                next_pos = None
        elif droid_status == 1:
            room_map[current_pos] = "!" if room_map[current_pos] == "!" else "."
            current_pos = (current_pos[0] + directions[droid_command][0], current_pos[1] + directions[droid_command][1])
            room_map[current_pos] = "D"
            if current_pos == next_pos:
                for _, d in directions.items():
                    new_pos = (next_pos[0] + d[0], next_pos[1] + d[1])
                    if new_pos not in room_map:
                        frontier.append(new_pos)
        elif droid_status == 2:
            room_map[current_pos] = "!" if room_map[current_pos] == "!" else "."
            current_pos = (current_pos[0] + directions[droid_command][0], current_pos[1] + directions[droid_command][1])
            room_map[current_pos] = "!"
            if goal != None and goal != current_pos:
                print("wtf")
            if goal != None:
                goal = current_pos
            if current_pos == next_pos:
                for _, d in directions.items():
                    new_pos = (next_pos[0] + d[0], next_pos[1] + d[1])
                    if new_pos not in room_map:
                        frontier.append(new_pos)
        else:
            pass
        # print(pretty_map())
    
    if backtrack:
        if len(route) == 1:
            backtrack = False
        droid_command = route.pop(0)
        return droid_command

    else:
        if len(frontier) > 0:
            next_pos = frontier.pop()
            if current_pos == next_pos:
                for _, d in directions.items():
                    new_pos = (next_pos[0] + d[0], next_pos[1] + d[1])
                    if new_pos not in room_map:
                        frontier.append(new_pos)
                next_pos = frontier.pop()

            route = bfs_frontier(next_pos)
            if len(route) > 1:
                backtrack = True
            droid_command = route.pop(0)
            return droid_command
        else:
            pretty_map()
            final_path = bfs((0, 0), (-12, 12))
            print(f"shortest route: {final_path}")
            print(f"shortest route length: {len(final_path)}")

def bfs_frontier(goal):
    pre_goal_step = None
    # print(f"goal: {goal}")
    for d, m in directions.items():
        pre_goal_pos = (goal[0] + m[0], goal[1] + m[1])
        if pre_goal_pos in room_map and room_map[pre_goal_pos] in (".", "!", "D"):
            pre_goal_step = inverse_d[d]
            break
    route = bfs(current_pos, pre_goal_pos)
    route.append(pre_goal_step)
    # print(f"route: {route}")
    return route

def bfs(current_pos, goal):
    explored = set()
    frontier = [[(0, current_pos)]]
    while frontier:
        path = frontier.pop(0)
        node = path[-1][1]
        if node == goal:
            return [m[0] for m in path[1:]]
        if node not in explored:
            for m, d in directions.items():
                next_node = (node[0] + d[0], node[1] + d[1])
                if next_node in room_map and room_map[next_node] in (".", "!", "D"):
                    new_path = list(path)
                    new_path.append((m, next_node))
                    frontier.append(new_path)
            explored.add(node)

def get_user_input():
    valid = False
    while not valid:
        user_input = input("Next move: ")
        try:
            droid_command = int(user_input)
            if 0 < droid_command < 5:
                valid = True
        except ValueError as _:
            print("Invalid input")
    return user_input

p_input = ''.join(open("input.txt", "r").readlines())
intcomputer = Intcomputer(p_input)
intcomputer.run_until_done(handle_input=handle_input)

print("\nPart 2")

room_map[current_pos] = "."
i = -1
frontier = [(-12, 12)]
while len(frontier) > 0:
    # print(f"frontier: {frontier}")
    new_frontier = []
    for node in frontier:
        room_map[node] = "O"
        for _, d in directions.items():
            new_pos = (node[0] + d[0], node[1] + d[1])
            if new_pos in room_map and room_map[new_pos] in ("."):
                new_frontier.append(new_pos)
    frontier = new_frontier
    i += 1
print(i)


