import math


def easeInOutSin(x):
    return -(math.cos(math.pi * x) - 1) / 2


def easeInOutQuad(x):
    return 2 * x * x if x < 0.5 else 1 - math.pow(-2 * x + 2, 2) / 2


def easeInOutCubic(x):
    return 4 * x * x * x if x < 0.5 else 1 - math.pow(-2 * x + 2, 3) / 2


def aaa(x):
    return (0.18) * math.cos((math.pi * (x - 62.5)) / 90) + 0.015


min = 12
max = 90

sin = []
quad = []
cubic = []
linear = []

variants = ["50", "100", "200", "300", "400", "500", "600", "700", "800", "900", "950"]

for i in range(len(variants)):
    x = i / (len(variants) - 1)
    sin.append(min + (max - min) * easeInOutSin(x))
    quad.append(min + (max - min) * easeInOutQuad(x))
    cubic.append(min + (max - min) * easeInOutCubic(x))
    linear.append(min + (max - min) * x)

# linear = [aaa(x) for x in linear]

decimals = 4

sin = [round(x, decimals) for x in sin]
quad = [round(x, decimals) for x in quad]
cubic = [round(x, decimals) for x in cubic]
linear = [round(x, decimals) for x in linear]

variable = "--base-l-"
postpend = "%"

print("Sin:")
for i, value in enumerate(sin):
    print(f"{variable}{variants[i]}: {value}{postpend};")
print("Quad:")
for i, value in enumerate(quad):
    print(f"{variable}{variants[i]}: {value}{postpend};")
print("Cubic:")
for i, value in enumerate(cubic):
    print(f"{variable}{variants[i]}: {value}{postpend};")
print("Linear:")
for i, value in enumerate(linear):
    print(f"{variable}{variants[i]}: {value}{postpend};")
