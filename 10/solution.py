from math import gcd, atan2, pi

print("Part 1")

def parse(input):
    return [list(l) for l in input.split('\n')]

def count_viewable(asteroids, x, y):
    # print(f"{x}, {y}")
    asteroids = [list(l) for l in asteroids]
    viewable = 0
    frontier = [(x, y)]
    steps = ((-1, 0), (1, 0), (0, -1), (0, 1))
    while len(frontier) > 0:
        node = frontier.pop(0)
        # print(node)
        if asteroids[node[1]][node[0]] == "!":
            continue
        if asteroids[node[1]][node[0]] == "#" and (node[0] != x or node[1] != y):
            # print(f"view {node[0]}, {node[1]}")
            viewable += 1
            step_x, step_y = node[0] - x, node[1] - y
            step_divisor = gcd(step_x, step_y)
            step_x, step_y = step_x // step_divisor, step_y // step_divisor
            unviewable_x, unviewable_y = node[0], node[1]
            while 0 <= unviewable_x < len(asteroids[0]) and 0 <= unviewable_y < len(asteroids):
                # print(f"dab {unviewable_x}, {unviewable_y}")
                asteroids[unviewable_y][unviewable_x] = "."
                unviewable_x, unviewable_y = unviewable_x + step_x, unviewable_y + step_y
        asteroids[node[1]][node[0]] = "!"
        for s in steps:
            if 0 <= node[0] + s[0] < len(asteroids[0]) and 0 <= node[1] + s[1] < len(asteroids) :
                frontier.append((node[0] + s[0], node[1] + s[1]))
    return viewable


def max_viewable(input):
    asteroids = parse(input)
    max_viewable = 0
    max_viewable_coords = (0,0)
    for y in range(len(asteroids)):
        for x in range(len(asteroids[y])):
            if asteroids[y][x] == "#":
                viewable = count_viewable(asteroids, x, y)
                if viewable > max_viewable:
                    max_viewable = viewable
                    max_viewable_coords = (x, y)
    return max_viewable, max_viewable_coords

# test = """.#..#
# .....
# #####
# ....#
# ...##"""
# assert max_viewable(test)[0] == 8

# test = """......#.#.
# #..#.#....
# ..#######.
# .#.#.###..
# .#..#.....
# ..#....#.#
# #..#....#.
# .##.#..###
# ##...#..#.
# .#....####"""
# assert max_viewable(test)[0] == 33

# test = """#.#...#.#.
# .###....#.
# .#....#...
# ##.#.#.#.#
# ....#.#.#.
# .##..###.#
# ..#...##..
# ..##....##
# ......#...
# .####.###."""
# assert max_viewable(test)[0] == 35

# test = """.#..#..###
# ####.###.#
# ....###.#.
# ..###.##.#
# ##.##.#.#.
# ....###..#
# ..#.#..#.#
# #..#.#.###
# .##...##.#
# .....#.#.."""
# assert max_viewable(test)[0] == 41

# test = """.#..##.###...#######
# ##.############..##.
# .#.######.########.#
# .###.#######.####.#.
# #####.##.#.##.###.##
# ..#####..#.#########
# ####################
# #.####....###.#.#.##
# ##.#################
# #####.##.###..####..
# ..######..##.#######
# ####.##.####...##..#
# .#####..#.######.###
# ##...#.##########...
# #.##########.#######
# .####.#.###.###.#.##
# ....##.##.###..#####
# .#.#.###########.###
# #.#.#.#####.####.###
# ###.##.####.##.#..##"""
# assert max_viewable(test)[0] == 210

# input = ''.join(open("input.txt", "r").readlines())
# print(max_viewable(input))



print("\nPart 2")

def get_viewable(asteroids, x, y):
    # print(f"{x}, {y}")
    asteroids = [list(l) for l in asteroids]
    viewable = []
    frontier = [(x, y)]
    steps = ((-1, 0), (1, 0), (0, -1), (0, 1))
    while len(frontier) > 0:
        node = frontier.pop(0)
        # print(node)
        if asteroids[node[1]][node[0]] == "!":
            continue
        if asteroids[node[1]][node[0]] == "#" and (node[0] != x or node[1] != y):
            # print(f"view {node[0]}, {node[1]}")
            viewable.append((node[0], node[1]))
            step_x, step_y = node[0] - x, node[1] - y
            step_divisor = gcd(step_x, step_y)
            step_x, step_y = step_x // step_divisor, step_y // step_divisor
            unviewable_x, unviewable_y = node[0], node[1]
            while 0 <= unviewable_x < len(asteroids[0]) and 0 <= unviewable_y < len(asteroids):
                # print(f"dab {unviewable_x}, {unviewable_y}")
                asteroids[unviewable_y][unviewable_x] = "."
                unviewable_x, unviewable_y = unviewable_x + step_x, unviewable_y + step_y
        asteroids[node[1]][node[0]] = "!"
        for s in steps:
            if 0 <= node[0] + s[0] < len(asteroids[0]) and 0 <= node[1] + s[1] < len(asteroids) :
                frontier.append((node[0] + s[0], node[1] + s[1]))
    return viewable

def get_200(asteroids):
    asteroids = parse(input)
    viewable = get_viewable(asteroids, 26, 28)
    print(viewable)
    xy_coords = [(v[0] - 26, v[1] - 28) for v in viewable]
    polar_coords = [(atan2(xy[1], xy[0]), xy[0] + 26, xy[1] + 28) for xy in xy_coords]
    polar_coords.sort()
    i = 0
    while polar_coords[i][0] < - pi / 2:
        i += 1
    print(f"{i}: {polar_coords[i]}")
    for j in range(199):
        i = (i + 1) % len(polar_coords)
    print(f"{i}: {polar_coords[i]}")


input = ''.join(open("input.txt", "r").readlines())
print(get_200(input))