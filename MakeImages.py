import subprocess
from PIL import Image, ImageDraw, ImageFont
import PIL
import os

MakeThresholdsAndDFTs = True
MakeDiagrams = True

fontSize = 20
font1 = ImageFont.truetype("arial.ttf", fontSize)
font2 = ImageFont.truetype("arialbi.ttf", fontSize)

os.makedirs("out", exist_ok=True)

# 6.2 is the max dft mag value, but stable fidussion is 64x64 instead of 128x128 and so has a different max value.
# Empty string makes them all normalize to their own values
DFTNormalization = "6.2"

ThresholdList = {
	"FAST_Sigma1_0/real_uniform_gauss1_0.png" : ["out/FAST_S", "FAST S"],
	"FAST_Sigma1_0/real_uniform_gauss1_0_Gauss10_separate05_0.png" : ["out/FAST_ST", "FAST ST"],
	"STBN_Sigma1_0/stbn_scalar_2Dx1Dx1D_128x128x1x1_0.png" : ["out/STBN10_S", "STBN 1.0 S"],
	"STBN_Sigma1_0/stbn_scalar_2Dx1Dx1D_128x128x32x1_0.png" : ["out/STBN10_ST", "STBN 1.0 ST"],
	"STBN_Sigma1_9/stbn_scalar_2Dx1Dx1D_128x128x1x1_0.png" : ["out/STBN19_S", "STBN 1.9 S"],
	"STBN_Sigma1_9/stbn_scalar_2Dx1Dx1D_128x128x32x1_0.png" : ["out/STBN19_ST", "STBN 1.9 ST"],
	"VNC/VNC10.png" : ["out/VNC10", "VNC 1.0 S"],
	"VNC/VNC15.png" : ["out/VNC15", "VNC 1.5 S"],
	"VNC/VNC19.png" : ["out/VNC19", "VNC 1.9 S"],
	#"VNC/fbnt_128x128_10.png" : ["out/FreeBNT_10", "FreeBNT 1.0 S"],
	#"VNC/fbnt_128x128_15.png" : ["out/FreeBNT_15", "FreeBNT 1.5 S"],
	#"VNC/fbnt_128x128_19.png" : ["out/FreeBNT_19", "FreeBNT 1.9 S"],
	#"tellusim/128x128_Crop.png" : ["out/Tellusim_8b", "Tell. 8b ST"],
	"tellusim/128x128_16b_Crop.png" : ["out/Tellusim_16b", "Tellusim ST"],
	"Stable_Fiddusion/64x64_Crop.png" : ["out/Stable_Fiddusion", "Fiddusion ST"],
}

ThresholdValues = [1 , 2, 10, 26, 51, 77, 102, 128, 153, 179, 204, 230, 245, 253, 254]

DFTList = {
	"FAST_Sigma1_0/real_uniform_gauss1_0.png" : ["out/FAST_S_Full.dft.png", "FAST S"],
	"FAST_Sigma1_0/real_uniform_gauss1_0_Gauss10_separate05_0.png" : ["out/FAST_ST_Full.dft.png", "FAST ST"],
	"STBN_Sigma1_0/stbn_scalar_2Dx1Dx1D_128x128x1x1_0.png" : ["out/STBN10_S_Full.dft.png", "STBN 1.0 S"],
	"STBN_Sigma1_0/stbn_scalar_2Dx1Dx1D_128x128x32x1_0.png" : ["out/STBN10_ST_Full.dft.png", "STBN 1.0 ST"],
	"STBN_Sigma1_9/stbn_scalar_2Dx1Dx1D_128x128x1x1_0.png" : ["out/STBN19_S_Full.dft.png", "STBN 1.9 S"],
	"STBN_Sigma1_9/stbn_scalar_2Dx1Dx1D_128x128x32x1_0.png" : ["out/STBN19_ST_Full.dft.png", "STBN 1.9 ST"],
	"VNC/VNC10.png" : ["out/VNC10_Full.dft.png", "VNC 1.0 S"],
	"VNC/VNC15.png" : ["out/VNC15_Full.dft.png", "VNC 1.5 S"],
	"VNC/VNC19.png" : ["out/VNC19_Full.dft.png", "VNC 1.9 S"],
	#"VNC/fbnt_128x128_10.png" : ["out/fbnt_128x128_10_Full.dft.png", "FreeBNT 1.0 S"],
	#"VNC/fbnt_128x128_15.png" : ["out/fbnt_128x128_15_Full.dft.png", "FreeBNT 1.5 S"],
	#"VNC/fbnt_128x128_19.png" : ["out/fbnt_128x128_19_Full.dft.png", "FreeBNT 1.9 S"],
	#"tellusim/128x128_Crop.png" : ["out/Tellusim_8b_Full.dft.png", "Tell. 8b ST"],
	"tellusim/128x128_16b_Crop.png" : ["out/Tellusim_16b_Full.dft.png", "Tellusim ST"],
	"Stable_Fiddusion/64x64_Crop.png" : ["out/Stable_Fiddusion_Full.dft.png", "Fiddusion ST"],
}

# Make thresholds and DFTs
if MakeThresholdsAndDFTs:

	# Thresholds
	for fileName, ThresholdInfo in ThresholdList.items():
		outFileNameBase = ThresholdInfo[0]
		for ThresholdValue in ThresholdValues:
			result = subprocess.run(["python", "Threshold.py", fileName, outFileNameBase + "_" + str(ThresholdValue) + ".png", str(ThresholdValue) ], capture_output=True, text=True)
			if result.stdout:
				print(result.stdout)
			result = subprocess.run(["python", "DFT.py", outFileNameBase + "_" + str(ThresholdValue) + ".png", outFileNameBase + "_" + str(ThresholdValue) + ".dft.png", DFTNormalization], capture_output=True, text=True)
			if result.stdout:
				print(result.stdout)

	# DFTs
	for fileName, DFTDetails in DFTList.items():
		outFileName = DFTDetails[0]
		result = subprocess.run(["python", "DFT.py", fileName, outFileName, DFTNormalization], capture_output=True, text=True)
		if result.stdout:
			print(result.stdout)

# Make the full noise texture / DFTs diagram
if MakeDiagrams:
	numRows = 2
	numCols = len(DFTList)
	tileWidth = 128
	tileHeight = 128
	margin = 5
	leftMargin = 0
	topMargin = 25

	imageWidth = numCols * tileWidth + (numCols + 1) * margin + leftMargin
	imageHeight = numRows * tileHeight + (numRows + 1) * margin + topMargin

	imOut = Image.new("L", (imageWidth, imageHeight), 255)
	im1 = ImageDraw.Draw(imOut) 

	col = 0
	for fileName, DFTDetails in DFTList.items():
		outFileName = DFTDetails[0]
		label = DFTDetails[1]

		im = Image.open(fileName)#.resize((tileWidth,tileHeight), PIL.Image.NEAREST)
		imOut.paste(im, (leftMargin + margin + col*(tileWidth + margin) , topMargin + margin))

		im = Image.open(outFileName)#.resize((tileWidth,tileHeight), PIL.Image.NEAREST)
		imOut.paste(im, (leftMargin + margin + col*(tileWidth + margin) , topMargin + margin + tileHeight + margin))

		im1.text((leftMargin + margin + col *(tileWidth + margin) , 0), label, font = font1, align ="left", fill=(0))

		col = col + 1

	imOut.save("out/_Full.png")

# Make the thresholded point set diagram:
if MakeDiagrams:
	numRows = len(ThresholdValues)
	numCols = len(DFTList)
	tileWidth = 128
	tileHeight = 128
	margin = 5
	leftMargin = 45
	topMargin = 25

	imageWidth = numCols * tileWidth + (numCols + 1) * margin + leftMargin
	imageHeight = numRows * tileHeight + (numRows + 1) * margin + topMargin

	imOut = Image.new("L", (imageWidth, imageHeight), 255)
	im1 = ImageDraw.Draw(imOut) 

	row = 0
	for ThresholdValue in ThresholdValues:
		col = 0
		for fileName, ThresholdInfo in ThresholdList.items():
			outFileNameBase = ThresholdInfo[0]
			im = Image.open(outFileNameBase + "_" + str(ThresholdValue) + ".png")#.resize((tileWidth,tileHeight), PIL.Image.NEAREST)
			x1 = leftMargin + col*(tileWidth + margin) + margin - 1
			y1 = topMargin + row*(tileHeight + margin) + margin - 1
			x2 = x1 + im.width + 1
			y2 = y1 + im.height + 1
			im1.rectangle([(x1, y1),(x2, y2)], fill=(128))
			imOut.paste(im, (leftMargin + col*(tileWidth + margin) + margin, topMargin + row*(tileHeight + margin) + margin))
			col = col + 1
		row = row + 1

	col = 0
	for fileName, ThresholdInfo in ThresholdList.items():
		label = ThresholdInfo[1]
		im1.text((leftMargin + margin + col *(tileWidth + margin), 0), label, font = font1, align ="left", fill=(0))
		col = col + 1

	row = 0
	for ThresholdValue in ThresholdValues:
		label = str(ThresholdValue)
		if label == "1":
			label = "<= 1"
		im1.text((margin, topMargin + margin + row * (tileHeight + margin)), label, font = font1, align ="left", fill=(0))
		row = row + 1

	imOut.save("out/_Threshold.png")

# Make the thresholded point set DFT diagrams:
if MakeDiagrams:
	numRows = len(ThresholdValues)
	numCols = len(DFTList)
	tileWidth = 128
	tileHeight = 128
	margin = 5
	leftMargin = 45
	topMargin = 25

	imageWidth = numCols * tileWidth + (numCols + 1) * margin + leftMargin
	imageHeight = numRows * tileHeight + (numRows + 1) * margin + topMargin

	imOut = Image.new("L", (imageWidth, imageHeight), 255)
	im1 = ImageDraw.Draw(imOut) 

	row = 0
	for ThresholdValue in ThresholdValues:
		col = 0
		for fileName, ThresholdInfo in ThresholdList.items():
			outFileNameBase = ThresholdInfo[0]
			label = ThresholdInfo[1]
			im = Image.open(outFileNameBase + "_" + str(ThresholdValue) + ".dft.png")#.resize((tileWidth,tileHeight), PIL.Image.NEAREST)
			imOut.paste(im, (leftMargin + col*(tileWidth + margin) + margin, topMargin + row*(tileHeight + margin) + margin))
			col = col + 1
		row = row + 1

	col = 0
	for fileName, ThresholdInfo in ThresholdList.items():
		label = ThresholdInfo[1]
		im1.text((leftMargin + margin + col *(tileWidth + margin), 0), label, font = font1, align ="left", fill=(0))
		col = col + 1

	row = 0
	for ThresholdValue in ThresholdValues:
		label = str(ThresholdValue)
		if label == "1":
			label = "<= 1"
		im1.text((margin, topMargin + margin + row * (tileHeight + margin)), label, font = font1, align ="left", fill=(0))
		row = row + 1

	imOut.save("out/_ThresholdDFT.png")

'''
NOTES:
? why does purely spatial STBN not look the same as void and cluster? they should be equivelant. review how STBN works?
 * i looked. should be the same but apparently isn't. implementation detail? unsure.
* Link to stochastic transparency, and tease spatiotemporal point sets or no?
 * Link as in say that this will happen directly
 * Also that fast doesnt affect points outside of filter footprint (is gauss truncated?)
* low sigma VNC has problems with sparsity. the algorithm seems like it shouldn't. my impl and "free blue noise textures" impl both show it.
* tellusim was 16 bit greyscale png. I opened in gimp, changed it to 8 bit. told it to use "linear", not sRGB.
 * pretty much same difference.
 * i did not do this, went with 16 bit greyscale! not apples to apples then but shrug.
* void and cluster paper says use sigma 1.5.  "free blue noise textures" uses 1.9. I'm including 1.0 as well.
* all DFTs normalized by same value: amplitude is divided by 6.2 to bring them all to be between 0 and 1.
* stable-fiddusion was 64x64, resized thresholded images and DFTs to 128x128, but worked in 64x64.
* Other blue noises came from:
 * https://tellusim.com/improved-blue-noise/
 * https://acko.net/blog/stable-fiddusion/
 * void and cluster  https://github.com/Atrix256/VoidAndCluster.git
  * and "free blue noise textures" https://momentsingraphics.de/BlueNoise.html
   * https://github.com/MomentsInGraphics/BlueNoise
  * and paper: https://cv.ulichney.com/papers/1993-void-cluster.pdf

Conclusions:
* good blue noise IMO has a darker center (no low frequencies left after filtering) and secondly, that center is as large as possible to push the noise to the highest frequencies only that it can.
 * no proof this is best perceptually, just from a filtering perspective, this is easier to filter, and leaves more of the scene data (lower frequencies) intact.
* mention this is one way to use scalar blue noise textures, so only one measure of quality of blue noise. "quality is as quality does"
* None seem to really do well at sparse counts like <= 1 which is 0.4% density. More do well at <= 10, which is 4% density.
* Fiddusion has a very dark center which is great for filtering, but it does poorly on thresholding.
 * Probably easier to optimize for a darker center if you don't consider thresholding.
* adding temporal constraints decreases spatial quality
 * FAST lets you give a weighting to space vs time. We gave each equal weighting.
'''