import sys
from PIL import Image
import numpy as np

fileName = sys.argv[1]
outFileName = sys.argv[2]
threshold = float(sys.argv[3])

# load the image
im = np.array(Image.open(fileName), dtype=float) / 255.0

if len(im.shape) > 2:
    im = im[:,:,0]

# Threshold the image
im = np.where(im < threshold, 0, 1)

# Save the image
Image.fromarray((im*255.0).astype(np.uint8), mode="L").save(outFileName)