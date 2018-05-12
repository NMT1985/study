from argparse import ArgumentParser

from PIL import Image
import numpy as np

argparser = ArgumentParser()
argparser.add_argument('-i', '--input', type=str, default="in.png")
argparser.add_argument('-o', '--output', type=str, default="out.png")
argparser.add_argument('-f', '--function', type=str, default="test")
args = argparser.parse_args()

def solarize(src):
    return 2 * src if src < 128 else 2 * (255 - src)

def reverse(src):
    return 255 - src

def channel(img):
    return bytes(np.array([(r[0], r[2], r[1]) for r in img]).flatten().tolist())

def sepia(img):
    return bytes(np.array([(sum(r) // 3, int(sum(r) * 0.267), int(sum(r) * 0.183)) for r in img]).flatten().tolist())

def gray(img):
    return bytes(np.array([(sum(r) // 3, sum(r) // 3, sum(r) // 3) for r in img]).flatten().tolist())

def postarize(img, d=4):
    q = 255 // d
    return bytes(np.array([((r[0] // q) * q, (r[1] // q) * q, (r[2] // q) * q) for r in img]).flatten().tolist())

def distance(x, y):
    return np.sum(np.square(x-y))

def compute_nearest_center(img, N, center):
    return np.array([np.argmin([distance(i, center[n]) for n in range(N)]) for i in img])

def kmeans(img, N=16):
    center = np.random.randint(256, size=(N, 3))
    for i in range(15):
        nearest_center_label = compute_nearest_center(img, N, center)
        center = np.array([np.mean(np.array(img)[np.where(nearest_center_label == j)[0]], axis=0).astype(np.int64) for j in range(N)])
    return bytes(np.array([center[nearest_center_label[i]].tolist() for i in range(len(img))]).flatten().tolist())

np.random.seed(1)
funcs = {"solarize": solarize, "reverse": reverse, "channel": channel, "sepia": sepia, "gray": gray, "postarize": postarize, "kmeans": kmeans}
mod = 'RGB'
image = Image.open(args.input).convert(mod)
#Image.frombuffer(mod, image.size, funcs[args.function](image.getdata()), 'raw', mod, 0, 1).save(args.output)

image.point(solarize).save(args.output)
