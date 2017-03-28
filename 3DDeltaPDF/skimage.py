from mantid.simpleapi import LoadMD
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import reconstruction, ball, disk, erosion, closing, opening
from skimage.feature import peak_local_max
from skimage.restoration import inpaint
from scipy import ndimage as ndi

filename='/SNS/CORELLI/IPTS-16344/shared/symm_007K_long_all_ub_13feb.nxs'

ws=LoadMD(filename,LoadHistory=False)
signal=ws.getSignalArray().copy()

# Do something with nan's and inf's
signal[np.isnan(signal)]=0
signal[np.isinf(signal)]=0

image=signal[251]
seed = np.copy(image)
seed[1:-1, 1:-1] = image.min()
mask = image
dilated = reconstruction(seed, mask, method='dilation')

dilated2 = reconstruction(seed, mask, method='dilation', selem=disk(3))

plt.imshow(dilated,vmax=1e-4)
plt.show()


eros = erosion(image)

eros = erosion(image, selem=disk(2))

plt.imshow(eros,vmax=5e-5)
plt.show()

eros = erosion(signal)

eros = erosion(signal, selem=ball(2))

plt.imshow(eros[251],vmax=5e-5)
plt.show()

plt.imshow(np.log(eros[251]))
plt.show()



fft=np.fft.fftshift(np.fft.fftn(np.fft.fftshift(eros)))
out=(fft*np.conj(fft)).real

plt.imshow(np.log(out[251]))
plt.show()


eros = ndi.grey_erosion(signal, footprint=ball(3))
eros2 = ndi.grey_erosion(image, footprint=disk(3))


opened = opening(image)
closed = closing(image)


opened = opening(signal)
closed = closing(signal)

gf = ndi.gaussian_filter(image, 1)
opened = opening(gf)
closed = closing(gf)
eros = erosion(gf)


# Finding local maxima
# http://scikit-image.org/docs/dev/auto_examples/segmentation/plot_peak_local_max.html

coordinates = peak_local_max(image, min_distance=20)
plt.imshow(np.log(image),cmap=plt.cm.gray)
plt.plot(coordinates[:, 1], coordinates[:, 0], 'r.')
plt.show()


# Inpainting
# http://scikit-image.org/docs/dev/auto_examples/filters/plot_inpaint.html
s=signal[251]
result = inpaint.inpaint_biharmonic(s, np.isnan(s))
