import random
import numpy as np
import cv2
import os
import pickle
import matplotlib.pyplot as plt
from scipy.stats import truncnorm
from scipy.ndimage import zoom

SHAPE = (227, 227)
cutoff_threshold = 1

def get_truncated_normal(mean=0, std=1, low=0, upp=5):
    return truncnorm(
        (low - mean) / std, (upp - mean) / std, loc=mean, scale=std)

def get_standard_dist(mean, std):
    filename = os.path.join("standard_dist", str(mean) + "_" + str(std) + ".pickle")
    if os.path.exists(filename):
        # load standard distribution
        with open(filename, 'rb') as handle:
            basic_norm_data = pickle.load(handle)
    else:
        # save new standard distribution
        trunc_norm = get_truncated_normal(mean=255./2, std=255./5, low=0, upp=255)
        basic_norm_data = trunc_norm.rvs(227*227).astype(int)
        basic_norm_data.sort()
        with open(filename, 'wb') as handle:
            pickle.dump(basic_norm_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return basic_norm_data

def image_normalizing(image, mean, std, norm_all = False):
    if norm_all:
        linear_image = image.reshape(image.size)
        background_index = []
        image_index = list(range(1,len(linear_image)))
        norm_data = get_standard_dist(mean, std)
    else:
        linear_image = image.reshape(image.size)
        background_index = np.where(linear_image < cutoff_threshold)[0]
        image_index = np.where(linear_image > cutoff_threshold)[0]
        trunc_norm = get_truncated_normal(mean=mean, std=std, low=0, upp=255)
        norm_data = trunc_norm.rvs(len(image_index)).astype(int)
        norm_data.sort()

    sort_index = linear_image[image_index].argsort()

    for i in range(len(sort_index)):
        linear_image[image_index[sort_index[i]]] = norm_data[i]
    linear_image[background_index] = 0

    reconstructed_image = linear_image.reshape(SHAPE)

    return reconstructed_image

def scramble_image_generator(image):
    # zero-padding to make 228x228 image (228 = 2^2 * 3 * 19)
    scrambled_image = np.zeros((SHAPE[0] + 1, SHAPE[1] + 1))
    scrambled_image[0:227, 0:227] = image

    piece = 6
    space = int(228 / piece)

    pieces = []
    pieces_info = []
    for i in range(piece):
        for j in range(piece):
            single_piece = scrambled_image[i*space : (i+1)*space, j*space : (j+1)*space]
            pieces.append(single_piece)
            pieces_info.append((single_piece>1).sum()/ single_piece.size > 0.3)

    # shuffle piece with constraint of freeze
    freeze_ratio = 0.5
    shuffle_mode = 3

    if shuffle_mode == 1:
        # shuffle all
        shuffle_idx = list(range(len(pieces)))
        random.shuffle(shuffle_idx)
        shuffle_idx = shuffle_idx[0:round(len(pieces) * (1 - freeze_ratio))]
    elif shuffle_mode == 2:
        # shuffle inside object
        shuffle_idx = [index for (index, item) in enumerate(pieces_info) if item == True]
        random.shuffle(shuffle_idx)
        shuffle_idx = shuffle_idx[0:round(len(pieces) * (1 - freeze_ratio))]
    elif shuffle_mode == 3:
        object_idx = [index for (index, item) in enumerate(pieces_info) if item == True]
        background_idx = [index for (index, item) in enumerate(pieces_info) if item == False]
        random.shuffle(object_idx)
        shuffle_idx = object_idx[0:round(len(object_idx) * (1 - freeze_ratio))] + background_idx
        random.shuffle(shuffle_idx)
    elif shuffle_mode == 4:
        object_idx = [index for (index, item) in enumerate(pieces_info) if item == True]
        background_idx = [index for (index, item) in enumerate(pieces_info) if item == False]
        random.shuffle(object_idx)
        random.shuffle(background_idx)
        shuffle_idx = object_idx[0:round(len(object_idx) * (1 - freeze_ratio))]
        bg_shuffle_idx = background_idx[0:len(shuffle_idx)]
        shuffle_idx = shuffle_idx + bg_shuffle_idx

    shuffle_piece = []
    for idx in shuffle_idx:
        shuffle_piece.append(pieces[idx])
    shuffle_idx.reverse()
    for ii, idx in enumerate(shuffle_idx):
        pieces[idx] = np.array(shuffle_piece[ii])

    # reconstruct image
    for i in range(piece):
        for j in range(piece):
            scrambled_image[i*space : (i+1)*space, j*space : (j+1)*space] = pieces[i*piece + j]

    scrambled_image = scrambled_image[:227, :227]

    return scrambled_image

def show_image(image, save=False, savetype="Image",filename="filename.png"):
    plt.imshow(image, cmap='gray', vmin=0, vmax=255)
    plt.colorbar()

    if save:
        if savetype == "Image":
            plt.imsave(filename, image)
        elif savetype == "Total":
            plt.savefig(filename)
    else:
        plt.show()

def image_translation(image, translation):
    RF_radius = 195/2
    translation = int(translation * RF_radius)
    X = np.roll(image, translation, axis=1)
    if translation>0:
        X[:, :translation] = 0
    elif translation<0:
        X[:, translation:] = 0
    return X

def image_rotation(image, rotation):
    h, w = image.shape[:2]
    M = cv2.getRotationMatrix2D((round(h/2), round(w/2)), rotation, 1)
    X = cv2.warpAffine(image, M, (h, w))
    return X

def image_scaling(image, scaling):
    h, w = image.shape[:2]
    if scaling < 1:
        zh = int(np.round(h*scaling))
        zw = int(np.round(w*scaling))
        top = (h-zh)//2
        left = (w-zw)//2

        X = np.zeros_like(image)
        X[top:top+zh, left:left+zw] = zoom(image, scaling)

    elif scaling > 1:
        zh = int(np.ceil(h / scaling))
        zw = int(np.ceil(w / scaling))
        top = (h - zh) // 2
        left = (w - zw) // 2

        X = zoom(image[top:top+zh, left:left+zw], scaling)

        trim_top = ((X.shape[0] - h) // 2)
        trim_left = ((X.shape[1] - w) // 2)
        X = X[trim_top:trim_top+h, trim_left:trim_left+w]

    else:
        X = image
    return X

