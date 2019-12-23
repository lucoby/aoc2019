print("Part 1")

def parse(input):
    return [int(i) for i in list(input)]

def generate_pattern(phase, length):
    i = 0
    j = phase + 1
    subpattern = [0] * j + [1] * j + [0] * j + [-1] * j
    subpattern_len = 4 * j
    pattern = []
    while i < length + 1:
        pattern += subpattern
        i += subpattern_len
    pattern.pop(0)
    return pattern

def generte_next_signal(signal, patterns):
    next_signal = []
    for i in range(len(signal)):
        total = 0
        for j, element in enumerate(signal):
            # print(f"{patterns[i][j]} * {element}")
            total += patterns[i][j] * element
        # print(f"total: {abs(total) % 10}")
        next_signal.append(abs(total) % 10)
    return next_signal

def fft(input, phases=100):
    signal = parse(input)
    signal_len = len(signal)
    print(signal_len)
    patterns = []
    for i in range(signal_len):
        patterns.append(generate_pattern(i, signal_len))
    for i in range(phases):
        print(i)
        # print(f"sig: {signal}")
        signal = generte_next_signal(signal, patterns)
    final_signal = "".join([str(s) for s in signal])
    return final_signal


test = "12345678"
assert fft(test, phases=1) == "48226158"
assert fft(test, phases=2) == "34040438"
assert fft(test, phases=3) == "03415518"
assert fft(test, phases=4) == "01029498"

test="80871224585914546619083218645595"
assert fft(test)[:8] == "24176176"

test="19617804207202209144916044189917"
assert fft(test)[:8] == "73745418"

test="69317163492948606335995924319873"
assert fft(test)[:8] == "52432133"

input = ''.join(open("input.txt", "r").readlines())
print(fft(input)[:8])


print("\nPart 2")

def actual_fft(input):
    return fft(input * 650)

input = ''.join(open("input.txt", "r").readlines())
final_sig = actual_fft(input)
start = int(final_sig[:7])
print(final_sig[start:start+8])

