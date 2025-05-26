import sys
from PIL import Image
import PIL
import numpy as np

fileName = sys.argv[1]
outFileName = sys.argv[2]
threshold = float(sys.argv[3])

# load the image
im = np.array(Image.open(fileName), dtype=np.uint8)

if len(im.shape) > 2:
    im = im[:,:,0]

# Threshold the image
im = np.where(im <= threshold, 0, 255)

# Save the image, making sure it's 128x128, since Stable_Fiddusion is 64x64
Image.fromarray(im.astype(np.uint8), mode="L").resize((128,128), PIL.Image.NEAREST).save(outFileName)