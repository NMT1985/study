from PIL import Image
from itertools import zip_longest
import math


buf = bytearray([0] * (256*256))
nodes = [0j, 1.0 + 0j]

N = 14


def get_rotation(i=0, mode="c", angle=math.pi/4):
    w = complex(math.cos(angle), math.sin(angle))
    if mode == "c":
        return w
    else:
        return complex(math.cos(angle), math.sin(angle)) / 2 / math.cos(angle)


for l in range(N):
    #_nodes = [(b - a) * get_rotation(mode="c") + a for a, b in zip(nodes[:-1], nodes[1:])]
    _nodes = [(b - a) * get_rotation(i, mode="dragon", angle=math.pi/10) + a for i, (a, b) in enumerate(zip(nodes[:-1], nodes[1:]))]
    nodes = sum(zip_longest(nodes, _nodes, fillvalue=0j), ())[:-1]

for z in nodes:
    x = int(z.real*80) + 68
    y = int(z.imag*80) + 100
    buf[y*256 + x] = 255

Image.frombytes("L", (256, 256), bytes(buf)).show()
