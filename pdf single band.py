import helpFunctions as hf
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

data_directory = './data/'

multiIm, annotationIm = hf.loadMulti('multispectral_day01.mat', 'annotation_day01.png', data_directory)

[fatPix, fatR, fatC] = hf.getPix(multiIm, annotationIm[:, :, 1])
[meatPix, meatR, meatC] = hf.getPix(multiIm, annotationIm[:, :, 2])

bands_fat = [[pixel[i] for pixel in fatPix] for i in range(19)]
means_fat = [np.mean(band) for band in bands_fat]
stdevs_fat = [np.std(band) for band in bands_fat]

bands_meat = [[pixel[i] for pixel in meatPix] for i in range(19)]
means_meat = [np.mean(band) for band in bands_meat]
stdevs_meat = [np.std(band) for band in bands_meat]


# solve for threshold beween lower mean and upper mean + 4 stdevs
def threshold(i):
    if means_meat[i] < means_fat[i]:
        lower = "meat"
        xs = np.linspace(means_meat[i], means_fat[i] + stdevs_fat[i] * 4, 1000)
    else:
        lower = "fat"
        xs = np.linspace(means_fat[i], means_meat[i] + stdevs_meat[i] * 4, 1000)
    for x in xs:
        pdf_meat = norm.pdf(x, loc=means_meat[i], scale=stdevs_meat[i])
        pdf_fat = norm.pdf(x, loc=means_fat[i], scale=stdevs_fat[i])
        if (lower == "meat" and pdf_fat > pdf_meat) or (lower == "fat" and pdf_fat < pdf_meat):
            return x

# plot pdf curves and threshold
def plot(i):
    x_fat = np.linspace(means_fat[i] - stdevs_fat[i] * 4, means_fat[i] + stdevs_fat[i] * 4, 50)
    x_meat = np.linspace(means_meat[i] - stdevs_meat[i] * 4, means_meat[i] + stdevs_meat[i] * 4, 50)
    fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
    ax.plot(x_fat, [norm.pdf(x, loc=means_fat[i], scale=stdevs_fat[i]) for x in x_fat], label = "Fat")
    ax.plot(x_meat, [norm.pdf(x, loc=means_meat[i], scale=stdevs_meat[i]) for x in x_meat], label = "Meat")
    ax.scatter(threshold(i), norm.pdf(threshold(i), loc=means_meat[i], scale=stdevs_meat[i]))
    ax.legend()
    plt.title("Band number " + str(i))
    plt.show()

for i in range(19):
    print(i)
    print(threshold(i))
    plot(i)






