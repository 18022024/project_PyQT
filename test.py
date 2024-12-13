from PIL import Image, ImageFilter


def black_white(name):
    im = Image.open(name)
    pixels = im.load()
    x, y = im.size
    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            c = (r + g + b) // 3
            pixels[i, j] = c, c, c
    im.save(name)


def brighter(name):
    im = Image.open(name)
    pixels = im.load()
    x, y = im.size
    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            if r < 200:
                r += 30
            if g < 200:
                g += 30
            if r < 200:
                b += 30
            pixels[i, j] = r, g, b
    im.save(name)


def sepia(name):
    im = Image.open(name)
    im = im.quantize(16)
    im.save(name)


def negative(name):
    im = Image.open(name)
    pixels = im.load()
    x, y = im.size
    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            r1, g1, b1 = 255 - r, 255 - g, 255 - b
            pixels[i, j] = r1, g1, b1
    im.save(name)


def red_only(name):
    im = Image.open(name)
    pixels = im.load()
    x, y = im.size
    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            pixels[i, j] = r, 0, 0
    im.save(name)


def green_only(name):
    im = Image.open(name)
    pixels = im.load()
    x, y = im.size
    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            pixels[i, j] = 0, g, 0
    im.save(name)


def blue_only(name):
    im = Image.open(name)
    pixels = im.load()
    x, y = im.size
    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            pixels[i, j] = 0, 0, b
    im.save(name)


def blur(name):
    im = Image.open(name)
    im = im.filter(ImageFilter.GaussianBlur(5))
    im.save(name)


