from PIL import Image
import numpy as np

im = Image.open(r'E:\py-img\333.jpg')
print(im.format, im.size, im.mode)
im_cmyk = im.convert('CMYK')
img_array = np.array(im_cmyk) // 2.55
print('Convert to: ',im_cmyk.mode)

# Проблема в черном, при переводе раскладывает на все кроме черного

def sum_cmyk(): # подсчет по краскам, список CMYK [синий, красный, желтый, черный]
    CMYK = []
    for i in range(0,4):
        color_arr = np.rint(img_array[:, :, i])
        colors = round(color_arr.sum()/(im.size[0]*im.size[1]),0)
        CMYK.append(colors)
    print(CMYK)

    return CMYK

sum_cmyk()

