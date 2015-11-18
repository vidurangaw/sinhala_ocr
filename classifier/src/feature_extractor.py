__author__ = 'Naleen'

import numpy as np
import cv2
import Orange



from mapper import mapper_lower, mapper_upper, mapper_middle, feature_mapper
# from src.mapper import mapper_upper
# from src.mapper import mapper_middle
# from src.mapper import feature_mapper
from scripts import normalize, fileIO, locate_character
import os

np.set_printoptions(threshold='nan')
package_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def extractor(zone, start, end, phase):

    

    img = cv2.imread(os.path.join(package_directory, 'data/chars - Copy.jpg'))
    iMax = 109
    jMax = 41
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    dataString_middle=""
    dataString_lower=""
    dataString_upper=""
    for j in range (start, end):
    # for j in range (1,jMax):
        for i in range (1, iMax):
            ####tab file####
            character = gray[64*(j-1):64*j, 128*(i-1):128*i]
            character = normalize.get_mask(character, 5)
            xMin, xMax, yMin, yMax= locate_character.char_location(character)

            if zone=='middle':
                imapper, ilabel = mapper_middle.middlezone_mapper(i)
                if imapper is True:
                    dataArray_middle = feature_mapper.middle(character, 21, 43, xMin, xMax)
                    dataString_middle = dataString_middle+(ilabel+"\t")+('\t'.join(map(str,dataArray_middle)))+('\n')
                else:
                    continue

            if zone=='lower':
                imapper, ilabel= mapper_lower.lowerzone_mapper(i)
                if imapper is True:
                    # print i
                    dataArray_lower = feature_mapper.lower(character, 42, 64, xMin, xMax)
                    dataString_lower = dataString_lower+(ilabel+"\t")+('\t'.join(map(str,dataArray_lower)))+('\n')
                else:
                    continue

            if zone=='upper':
                imapper, ilabel= mapper_upper.upperzone_mapper(i)
                if imapper is True:
                    dataArray_upper = feature_mapper.upper(character, 0, 22, xMin, xMax)
                    dataString_upper = dataString_upper+(ilabel+"\t")+('\t'.join(map(str,dataArray_upper)))+('\n')
                else:
                    continue


    # write the features to tab file

    if zone == 'middle':
        fileIO.write_tl_file(dataArray_middle, dataString_middle, "learner/data_middle.tab")
        tl_data = Orange.data.Table(os.path.join(package_directory,'learner/data_middle'))
        if phase == 'validate':
            fileIO.write_tl_file(dataArray_middle, dataString_middle, "learner/data_middle_validate.tab")
            tl_data = Orange.data.Table(os.path.join(package_directory,'learner/data_middle_validate'))
    if zone == 'lower':
        fileIO.write_tl_file(dataArray_lower, dataString_lower, "learner/data_lower.tab")
        tl_data = Orange.data.Table(os.path.join(package_directory,'learner/data_lower'))
        if phase == 'validate':
            fileIO.write_tl_file(dataArray_lower, dataString_lower, "learner/data_lower_validate.tab")
            tl_data = Orange.data.Table(os.path.join(package_directory,'learner/data_lower_validate'))
    if zone == 'upper':
        fileIO.write_tl_file(dataArray_upper, dataString_upper, "learner/data_upper.tab")
        tl_data = Orange.data.Table(os.path.join(package_directory,'learner/data_upper'))
        if phase == 'validate':
            fileIO.write_tl_file(dataArray_upper, dataString_upper, "learner/data_upper_validate.tab")
            tl_data = Orange.data.Table(os.path.join(package_directory,'learner/data_upper_validate'))

    return tl_data





