__author__ = 'Naleen'

from ..scripts import locate_character
from ..scripts import zone_info

def middle(character, y_low, y_high, x_low, x_high):

    # dataString=""
    dataArray=[]
    xMin, xMax, yMin, yMax= locate_character.char_location(character)
    dataArray.append(xMin)
    dataArray.append(xMax)
    dataArray.append(xMax-xMin)


    char_array_ver_left, char_array_ver_right, char_array_ver, char_array_hor_top, char_array_hor_bottom, char_array_hor, matrix_info= zone_info.features(character, y_low, y_high, x_low, x_high)
    dataArray.extend(char_array_ver_left)
    dataArray.extend(char_array_ver_right)
    # dataArray.extend(char_array_ver)
    dataArray.extend(char_array_hor_top)
    dataArray.extend(char_array_hor_bottom)
    # dataArray.extend(char_array_hor)
    dataArray.extend(matrix_info)

    arc_length, contour_area= zone_info.char_info(character[21:43, 0:128])
    dataArray.append(arc_length)
    # print "arch lenght:" + str(arc_length)
    # print "contour area:" +str(contour_area)



    return dataArray



def lower(character, y_low, y_high, x_low, x_high):

    # dataString=""
    dataArray=[]
    xMin, xMax, yMin, yMax= locate_character.char_location(character)

    #dataArray=y.tolist()
    dataArray.append(xMin)
    dataArray.append(xMax)
    dataArray.append(yMin)
    dataArray.append(yMax)
    # dataArray.append
    dataArray.append(xMax-xMin)  #?
    dataArray.append(yMax-yMin)  #?

    char_array_ver_left, char_array_ver_right, char_array_ver, char_array_hor_top, char_array_hor_bottom, char_array_hor, matrix_info= zone_info.features(character, y_low, y_high, x_low, x_high)
    dataArray.extend(char_array_ver_left)
    dataArray.extend(char_array_ver_right)
    # dataArray.extend(char_array_ver)
    dataArray.extend(char_array_hor_top)
    dataArray.extend(char_array_hor_bottom)
    # dataArray.extend(char_array_hor)
    # dataArray.extend(matrix_info)


    return dataArray


def upper(character, y_low, y_high, x_low, x_high):

    xMin, xMax, yMin, yMax= locate_character.char_location(character)

    dataArray=[]

    dataArray.append(xMin)
    dataArray.append(xMax)

    dataArray.append(xMax-xMin)

    char_array_ver_left, char_array_ver_right, char_array_ver, char_array_hor_top, char_array_hor_bottom, char_array_hor, matrix_info= zone_info.features(character, y_low, y_high, x_low, x_high)
    dataArray.extend(char_array_ver_left)
    dataArray.extend(char_array_ver_right)
    # dataArray.extend(char_array_ver)
    dataArray.extend(char_array_hor_top)
    dataArray.extend(char_array_hor_bottom)
    # dataArray.extend(char_array_hor)
    # dataArray.extend(matrix_info)

    return dataArray

