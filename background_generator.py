import numpy as np
import random
import cv2
from PIL import Image

SHAPE = (227, 227)
cutoff_threshold = 20

def image_rotation(image, rotation):
    h, w = image.shape[:2]
    M = cv2.getRotationMatrix2D((round(h/2), round(w/2)), rotation, 1)
    X = cv2.warpAffine(image, M, (h, w))
    return X

def phaseScrambledBg(image, avg, std, rotation=True):
    if rotation:
        # rot_angle = random.random() * 360 - 180
        rot_angle = random.choice([0])
        image = image_rotation(image, rot_angle)
    noise = np.random.normal(avg,std,SHAPE)
    noise_image = Image.fromarray(noise)
    noise_spectrum = np.fft.fftshift(np.fft.fft2(noise_image))

    image_spectrum = np.fft.fftshift(np.fft.fft2(image))

    imageAmp = np.abs(image_spectrum)
    outPhase = np.angle(noise_spectrum)
    product = np.multiply(imageAmp, np.exp(1j * outPhase))
    scrambled_image = np.fft.ifft2(product)

    return np.abs(scrambled_image)

def mergeBgFg(foreground, background):
    foreground = np.asarray(Image.fromarray(foreground).convert("L"))
    merged = np.zeros(SHAPE)

    for i in range(SHAPE[0]):
        for j in range(SHAPE[1]):
            if foreground[i][j] > cutoff_threshold:
                merged[i][j] = foreground[i][j]
            else:
                merged[i][j] = background[i][j]
    return merged