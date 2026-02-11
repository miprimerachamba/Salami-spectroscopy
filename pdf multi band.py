import helpFunctions as hf
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import scipy.stats as st

data_directory = './data/'

multiIm, annotationIm = hf.loadMulti('multispectral_day01.mat', 'annotation_day01.png', data_directory)

[fatPix, fatR, fatC] = hf.getPix(multiIm, annotationIm[:, :, 1])
[meatPix, meatR, meatC] = hf.getPix(multiIm, annotationIm[:, :, 2])
print(len(fatPix))
print(len(meatPix))

bands_fat = [[pixel[i] for pixel in fatPix] for i in range(19)]
means_fat = [np.mean(band) for band in bands_fat]

bands_meat = [[pixel[i] for pixel in meatPix] for i in range(19)]
means_meat = [np.mean(band) for band in bands_meat]

# equation (19)
co_fat = np.cov(bands_fat)
co_meat = np.cov(bands_meat)

# equation (20)
co_pooled = (co_fat*(len(fatPix)-1) + co_meat*(len(meatPix)-1)) / ((len(fatPix)-1) + (len(meatPix)-1))

def multi_pdf(x):
     if (st.multivariate_normal.pdf(x, mean=means_fat, cov=co_pooled)) > (st.multivariate_normal.pdf(x, mean=means_meat, cov=co_pooled)):
         return "fat"
     else:
         return "meat"

results_fat = [multi_pdf(pixel) for pixel in fatPix]
results_meat = [multi_pdf(pixel) for pixel in meatPix]

errors_fat = [f for f in results_fat if f == "meat"]
print(errors_fat)
print(len(errors_fat))

errors_meat = [f for f in results_meat if f == "fat"]
print(errors_meat)
print(len(errors_meat))