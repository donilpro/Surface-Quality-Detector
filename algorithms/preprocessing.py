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


def change_sharpness(image, value):
    """
    Алгоритм преобразования резкости
    :param image:
    :param value:
    :return:
    """
    kernel = np.array([[0, -1, 0], [-1, 5 + value, -1], [0, -1, 0]])
    if value == 0:
        return image
    if value < 0:
        kernel = np.array([[0, -1 - value, 0], [-1 - value, 5 + value, -1 - value], [0, -1 - value, 0]])
    sharpened = cv.filter2D(image, -1, kernel)
    return sharpened.astype('uint8')


def explore(image, area, area_std):
    """
    Входной параметр:
    image - исследуемое изображение
    Выход:
    image - изображение с контурами пор
    area_c - отношение площади всех пор ко всей площади
    изображения (пористость)
    len(bad_conrours) - количество 'плохих' пор
    """
    image = np.copy(image)
    blured = cv.GaussianBlur(image, (5, 5), 0)
    hsv = cv.cvtColor(blured, cv.COLOR_RGB2HSV)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([120, 120, 120])
    mask = cv.inRange(hsv, lower_black, upper_black)
    # получаем массив конутров
    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    good_contours = []
    bad_contours = []
    area_c = 0
    # находим поры, не превышающие нормативную площадь
    for contour in contours:
    # также подсчитываем общую площадь пор
        area_c += cv.contourArea(contour)
        if area - area_std <= cv.contourArea(contour) <= area + area_std:
            good_contours.append(contour)
        else:
            bad_contours.append(contour)
    area_c = area_c / (image.shape[0] * image.shape[1])
    # выделяем 'хорошие' поры зеленым цветом
    cv.drawContours(image, good_contours, -1, (0, 255, 0), 3)
    # выделяем 'плохие' поры красным цветом
    cv.drawContours(image, bad_contours, -1, (0, 0, 255), 3)
    return image, area_c, len(bad_contours)
