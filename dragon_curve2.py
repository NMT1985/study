from PIL import Image
from itertools import zip_longest
import math


N = 14
angles = [4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4]

def get_rotation(i=0, mode="c", angle=math.pi/4):
    w = complex(math.cos(angle), math.sin(angle)) / 2 / math.cos(angle)
    if mode == "c":
        return w
    else:
        if i%2 == 1:
            w = complex(w.real, -w.imag)
        return w

imgs = []
for angle in angles:
    buf = bytearray([0] * (256*256))
    nodes = [0j, 1.0 + 0j]

    for l in range(N):
        #_nodes = [(b - a) * get_rotation(mode="c") + a for a, b in zip(nodes[:-1], nodes[1:])]
        _nodes = [(b - a) * get_rotation(i, mode="dragon", angle=math.pi/angle) + a for i, (a, b) in enumerate(zip(nodes[:-1], nodes[1:]))]
        nodes = sum(zip_longest(nodes, _nodes, fillvalue=0j), ())[:-1]

    for z in nodes:
        x = int(z.real*120) + 68
        y = int(z.imag*120) + 100
        buf[y*256 + x] = 255

    imgs.append(Image.frombytes("L", (256, 256), bytes(buf)))

imgs[0].save('out.gif', save_all=True, append_images=imgs[1:], loop=0, duration=10)
