import subprocess

MakeThresholdsAndDFTs = True

DFTNormalization = "" # 6.2 is the max dft mag value, but stable fidussion is 64x64 instead of 128x128 and so has a different max value.

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
	"FAST_Sigma1_0/real_uniform_gauss1_0.png" : "out/FAST_S_Full.dft.png",
	"FAST_Sigma1_0/real_uniform_gauss1_0_Gauss10_separate05_0.png" : "out/FAST_ST_Full.dft.png",
	"STBN_Sigma1_0/stbn_scalar_2Dx1Dx1D_128x128x1x1_0.png" : "out/STBN10_S_Full.dft.png",
	"STBN_Sigma1_0/stbn_scalar_2Dx1Dx1D_128x128x32x1_0.png" : "out/STBN10_ST_Full.dft.png",
	"STBN_Sigma1_9/stbn_scalar_2Dx1Dx1D_128x128x1x1_0.png" : "out/STBN19_S_Full.dft.png",
	"STBN_Sigma1_9/stbn_scalar_2Dx1Dx1D_128x128x32x1_0.png" : "out/STBN19_ST_Full.dft.png",
	"Stable_Fiddusion/64x64_Crop.png" : "out/Stable_Fiddusion_Full.dft.png",
	"tellusim/128x128_Crop.png" : "out/Tellusim_Full.dft.png",
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
	for fileName, outFileName in DFTList.items():
		result = subprocess.run(["python", "DFT.py", fileName, outFileName, DFTNormalization], capture_output=True, text=True)
		if result.stdout:
			print(result.stdout)

# Make the diagrams

# TODO: why does STBN10_S_1.png have all the points at the bottom? seems like a bug. maybe related to void and cluster implementation. first 10% points initial binary pattern thing. maybe should threshold someone else's void and cluster.
# TODO: use python to put all the images together into diagrams. using the logic from make rows / columns. maybe have a makegrid python script.
# TODO: resize stable fiddusion when making the diagrams, not before, since it changes the DFT!