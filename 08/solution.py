print("Part 1")

def parse(foo):
    pass


input = ''.join(open("input.txt", "r").readlines())
img = list(map(int, input))
layers_cnt = []
i = 0
while i < len(img):
    layer = img[i:i + 6 * 25]
    # print(layer)
    layers_cnt.append((layer.count(0), layer.count(1), layer.count(2)))
    i += 6*25
layers_cnt.sort(key=lambda x: x[0])
print(layers_cnt[0][1] * layers_cnt[0][2])

print("\nPart 2")

final_img = [2] * (25 * 6)
# print(img)

i = 0
while i < len(img):
    layer = img[i:i + 6 * 25]
    # print(layer)
    final_img = [final_img[j] if final_img[j] != 2 else layer[j] for j in range(6 * 25)]
    # print(final_img)
    i += 6*25

for i in range(6):
    print("".join(["#" if i == 0 else " " for i in final_img[i * 25:i * 25 + 25]]))