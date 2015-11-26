from __future__ import division
__author__ = 'Naleen'

import cv2
import numpy as np

__author__ = 'Naleen'
import cv2
import numpy as np



def features(character, y1, y2, x1, x2):
    # dataArray = []


    character_resized = cv2.resize(character[y1:y2, x1:x2], (16, 16), fx=0, fy=0, interpolation=cv2.INTER_NEAREST)

    # print character_resized.shape


    ret, character_resized = cv2.threshold(character_resized, 127, 255, 0)


    char_array_ver_left = np.divide(np.array(character_resized[:, :8]).sum(axis=1), 255)
    # dataArray.extend(char_array_ver_left)
    char_array_ver_right = np.divide(np.array(character_resized[:, 8:]).sum(axis=1), 255)
    # dataArray.extend(char_array_ver_right)
    char_array_ver = np.divide(np.array(character_resized[:, :]).sum(axis=1), 255)
    # dataArray.extend(char_array_ver)

    char_array_hor_top = np.divide(np.array(character_resized[:8, :]).sum(axis=0), 255)
    # dataArray.extend(char_array_hor_top)
    char_array_hor_bottom = np.divide(np.array(character_resized[8:, :]).sum(axis=0), 255)
    # dataArray.extend(char_array_hor_bottom)
    char_array_hor = np.divide(np.array(character_resized[:, :]).sum(axis=0), 255)
    # dataArray.extend(char_array_hor)

    matrix_info = np.reshape(np.array(character_resized), 16*16)
    # matrix_info =0
    # dataArray.extend(np.divide(matrix_info, 255))

    # # print char_array_ver
    # # print character
    # cv2.imshow("char", character)
    # cv2.imwrite("C:/Users/Naleen/Desktop/New folder (2)/lower.jpg", character)
    # cv2.waitKey(0)


    return char_array_ver_left, char_array_ver_right, char_array_ver, char_array_hor_top, char_array_hor_bottom, char_array_hor, matrix_info

def char_info(character):


    # character_copy = cv2.cvtColor(character, cv2.COLOR_GRAY2BGR)
    ret,thresh = cv2.threshold(character, 127, 255, 0)
    # print character.shape

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    arc_length=0
    contour_area=0
    for i in range(0, len(contours)):
        arc_length=arc_length+cv2.arcLength(contours[i], False)
        contour_area=contour_area+cv2.contourArea(contours[i])



    return int(arc_length), int(contour_area)
#



