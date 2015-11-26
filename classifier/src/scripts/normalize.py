__author__ = 'Naleen'

import cv2
import numpy as np


def get_mask(character, border_limit):

    mask = np.zeros(character.shape, np.uint8)

    upper = character[0:22, 0:128]
    # upper_rgb = character_rgb[0:22, 0:128]
    lower = character[42:64, 0:128]
    # lower_rgb = character_rgb[42:64, 0:128]

    ret, thresh_upper = cv2.threshold(upper, 127, 255, 0)
    contours_upper, hierarchy = cv2.findContours(thresh_upper,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    ret, thresh_lower = cv2.threshold(lower, 127, 255, 0)
    contours_lower, hierarchy = cv2.findContours(thresh_lower,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours_upper:
        # Height coordinates of the contour
        val = 128
        for cn in cnt:
            if cn[:, 1][0] < val:
                val = cn[:, 1][0]

        if val> (22-border_limit):
            if cv2.contourArea(cnt) < 20 or 0 < cv2.arcLength(cnt, False) < 15:
                        # cv2.drawContours(upper_rgb, [cnt], 0, (0, 255, 0), -1)
                        cv2.drawContours(mask, [cnt], 0, 255, -1)

    for cnt in contours_lower:
       # Height coordinates of the contour
        val1 = 0
        for cn in cnt:

            if cn[:, 1][0] > val1:
                val1 = cn[:, 1][0]

        if val1 < border_limit:
            if cv2.contourArea(cnt)<20 or 0<cv2.arcLength(cnt, False)<15:
                        # cv2.drawContours(lower_rgb,[cnt],0,(0,255,0),-1)
                        cv2.drawContours(mask[42:64, 0:128],[cnt],0,255,-1)



    character = cv2.bitwise_xor(character, mask)


    # cv2.imshow("char", character)
    # # cv2.imshow("upper", lower)
    # # # cv2.imshow("mask", mask1)
    # cv2.imwrite("C:/Users/Naleen/Desktop/New folder (2)/character.jpg", character)
    # # cv2.imwrite("C:/Users/Naleen/Desktop/New folder (2)/lower.jpg", lower)
    # # cv2.imwrite("C:/Users/Naleen/Desktop/New folder (2)/mask.jpg", mask)
    # #
    # cv2.waitKey(0)
    return character
