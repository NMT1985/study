from PIL import Image

class ImageRGB(object):
    def __init__(self, width, height, img=None):
        self.width = width
        self.height = height
        if img is None:
            self.buffer = [0 for i in range(width * height * 3)]
        else:
            self.buffer = list(Image.open(img).convert('RGB').tostring())

    def setPixel(self, x, y, color):
        if x >= self.width or y >= self.height or y < 0 or x < 0:
            return
        for i in range(3):
            self.buffer[x * 3 + y * self.width * 3 + i] = color[i]

    def getPILImage(self):
        return Image.frombuffer('RGB', (self.width, self.height), bytes(self.buffer), "raw", 'RGB', 0, 1)

def main():
    pass

if __name__ == '__main__':
    main()