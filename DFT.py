import sys
from PIL import Image
import numpy as np

fileName = sys.argv[1]
outFileName = sys.argv[2]

normalization = 0
if len(sys.argv) > 4:
    normalization = float(sys.argv[3])

# load the image
im = np.array(Image.open(fileName), dtype=float) / 255.0

if len(im.shape) > 2:
    im = im[:,:,0]

# get the magnitude, zero out DC and shift it so DC is in the middle
dft = abs(np.fft.fft2(im))
dft[0,0] = 0.0
dft = np.fft.fftshift(dft)

# log and normalize
imOut = np.log(1+dft)
if normalization == 0:
    normalization = np.max(imOut)

imOut = imOut / normalization
print("normalization = " + str(normalization))

Image.fromarray((imOut*255.0).astype(np.uint8), mode="L").save(outFileName)
