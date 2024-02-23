from PIL import Image, ImageEnhance
import cv2 as cv
import numpy as np


def linear_change(image, contrast, brightness) -> np.ndarray:
    '''
    Алгоритм преобразования контрастности
    :param brightness:
    :param image:
    :param contrast:
    :return: np.ndarray
    '''
    new_image = np.clip(image * contrast + brightness, 0, 255)
    return new_image.astype('uint8')


def change_sharpness(img):
    pass
