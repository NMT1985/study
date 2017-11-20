from PIL import Image
from itertools import zip_longest


buf = bytearray([0 for i in range(256*256)])
nodes = [0j, 1.0 + 0j]

N = 14
w = 0.5 + 0.5j
for l in range(N):
    #_nodes = [(b - a)*w + a for a, b in zip(nodes[:-1], nodes[1:])]
    _nodes = [(b - a)*(w - 1j*(i % 2)) + a for i, (a, b) in enumerate(zip(nodes[:-1], nodes[1:]))]
    nodes = sum(zip_longest(nodes, _nodes, fillvalue=0j), ())[:-1]

for z in nodes:
    x = int(z.real*120) + 68
    y = int(z.imag*120) + 100
    buf[y*256 + x] = 255

Image.frombytes("L", (256, 256), bytes(buf)).show()
