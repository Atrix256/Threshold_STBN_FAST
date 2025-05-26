import subprocess
from PIL import Image, ImageDraw, ImageFont
import PIL
import os

MakeThresholdsAndDFTs = False
MakeDiagrams = True

fontSize = 20
font1 = ImageFont.truetype("arial.ttf", fontSize)
font2 = ImageFont.truetype("arialbi.ttf", fontSize)

os.makedirs("out", exist_ok=True)

# 6.2 is the max dft mag value, but stable fidussion is 64x64 instead of 128x128 and so has a different max value.
# Empty string makes them all normalize to their own values
DFTNormalization = "6.2"

ThresholdList = {
	"FAST_Sigma1_0/real_uniform_gauss1_0.png" : "out/FAST_S",
	"FAST_Sigma1_0/real_uniform_gauss1_0_Gauss10_separate05_0.png" : "out/FAST_ST",
	"STBN_Sigma1_0/stbn_scalar_2Dx1Dx1D_128x128x1x1_0.png" : "out/STBN10_S",
	"STBN_Sigma1_0/stbn_scalar_2Dx1Dx1D_128x128x32x1_0.png" : "out/STBN10_ST",
	"STBN_Sigma1_9/stbn_scalar_2Dx1Dx1D_128x128x1x1_0.png" : "out/STBN19_S",
	"STBN_Sigma1_9/stbn_scalar_2Dx1Dx1D_128x128x32x1_0.png" : "out/STBN19_ST",
	"Stable_Fiddusion/64x64_Crop.png" : "out/Stable_Fiddusion",
	"tellusim/128x128_Crop.png" : "out/Tellusim",
}

ThresholdValues = [1 , 2, 10, 26, 51, 77, 102, 128, 153, 179, 204, 230]

DFTList = {
	"FAST_Sigma1_0/real_uniform_gauss1_0.png" : ["out/FAST_S_Full.dft.png", "FAST S"],
	"FAST_Sigma1_0/real_uniform_gauss1_0_Gauss10_separate05_0.png" : ["out/FAST_ST_Full.dft.png", "FAST ST"],
	"STBN_Sigma1_0/stbn_scalar_2Dx1Dx1D_128x128x1x1_0.png" : ["out/STBN10_S_Full.dft.png", "STBN 1.0 S"],
	"STBN_Sigma1_0/stbn_scalar_2Dx1Dx1D_128x128x32x1_0.png" : ["out/STBN10_ST_Full.dft.png", "STBN 1.0 ST"],
	"STBN_Sigma1_9/stbn_scalar_2Dx1Dx1D_128x128x1x1_0.png" : ["out/STBN19_S_Full.dft.png", "STBN 1.9 S"],
	"STBN_Sigma1_9/stbn_scalar_2Dx1Dx1D_128x128x32x1_0.png" : ["out/STBN19_ST_Full.dft.png", "STBN 1.9 ST"],
	"Stable_Fiddusion/64x64_Crop.png" : ["out/Stable_Fiddusion_Full.dft.png", "Fiddusion"],
	"tellusim/128x128_Crop.png" : ["out/Tellusim_Full.dft.png", "Tellusim"],
}

# Make thresholds and DFTs
if MakeThresholdsAndDFTs:

	# Thresholds
	for fileName, outFileNameBase in ThresholdList.items():
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

		im = Image.open(fileName).resize((tileWidth,tileHeight), PIL.Image.NEAREST)
		imOut.paste(im, (leftMargin + margin + col*(tileWidth + margin) , topMargin + margin))

		im = Image.open(outFileName).resize((tileWidth,tileHeight), PIL.Image.NEAREST)
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
	leftMargin = 50
	topMargin = 50

	imageWidth = numCols * tileWidth + (numCols + 1) * margin + leftMargin
	imageHeight = numRows * tileHeight + (numRows + 1) * margin + topMargin

	imOut = Image.new("L", (imageWidth, imageHeight), 255)

	row = 0
	for ThresholdValue in ThresholdValues:
		col = 0
		for fileName, outFileNameBase in ThresholdList.items():
			im = Image.open(outFileNameBase + "_" + str(ThresholdValue) + ".png").resize((tileWidth,tileHeight), PIL.Image.NEAREST)
			imOut.paste(im, (leftMargin + col*(tileWidth + margin) + margin, topMargin + row*(tileHeight + margin) + margin))
			col = col + 1
		row = row + 1


	imOut.save("out/_Threshold.png")

# Make the thresholded point set DFT diagrams:
if MakeDiagrams:
	numRows = len(ThresholdValues)
	numCols = len(DFTList)
	tileWidth = 128
	tileHeight = 128
	margin = 5
	leftMargin = 50
	topMargin = 50

	imageWidth = numCols * tileWidth + (numCols + 1) * margin + leftMargin
	imageHeight = numRows * tileHeight + (numRows + 1) * margin + topMargin

	imOut = Image.new("L", (imageWidth, imageHeight), 255)

	row = 0
	for ThresholdValue in ThresholdValues:
		col = 0
		for fileName, outFileNameBase in ThresholdList.items():
			im = Image.open(outFileNameBase + "_" + str(ThresholdValue) + ".dft.png").resize((tileWidth,tileHeight), PIL.Image.NEAREST)
			imOut.paste(im, (leftMargin + col*(tileWidth + margin) + margin, topMargin + row*(tileHeight + margin) + margin))
			col = col + 1
		row = row + 1


	imOut.save("out/_ThresholdDFT.png")

# TODO: put labels on the diagrams.
# TODO: why does STBN10_S_1.png have all the points at the bottom? seems like a bug. maybe related to void and cluster implementation. first 10% points initial binary pattern thing. maybe should threshold someone else's void and cluster.

'''
NOTES:
* all DFTs normalized by same value: amplitude is divided by 6.2 to bring them all to be between 0 and 1.
* stable-fiddusion was 64x64, resized thresholded images and DFTs to 128x128, but worked in 64x64.
* Other blue noises came from:
 * https://tellusim.com/improved-blue-noise/
 * https://acko.net/blog/stable-fiddusion/
'''