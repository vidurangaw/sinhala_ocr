__author__ = 'Naleen'


__author__ = 'Naleen'

import pickle

import numpy as np

import cv2
import Orange
import os
from src.mapper import feature_mapper
from src.scripts import normalize, fileIO, locate_character, prob_match


package_directory = os.path.dirname(os.path.abspath(__file__))

np.set_printoptions(threshold='nan')

classifier_lower = pickle.load(open(os.path.join(package_directory,'learner/ANN_lower')))
classifier_middle = pickle.load(open(os.path.join(package_directory,'learner/ANN_middle')))
classifier_upper = pickle.load(open(os.path.join(package_directory,'learner/ANN_upper')))
# lowerZoneLabels = fileIO.read_label_file('learner/lowerZoneLabels')
# middleZoneLabels = fileIO.read_label_file('learner/middleZoneLabels')
# upperZoneLabels = fileIO.read_label_file('learner/upperZoneLabels')


def classify(img):
    lowerZoneLabels = fileIO.read_label_file('learner/lowerZoneLabels')
    middleZoneLabels = fileIO.read_label_file('learner/middleZoneLabels')
    upperZoneLabels = fileIO.read_label_file('learner/upperZoneLabels')

    index = 0
    #print img
    # for i in range(1, 3)
    if img is None:
        # print "None"
        return ""

    if img.any() == np.array([0]).all():
        # print "space"
        return " "

    else:        
        #im = np.array(img * 255, dtype = np.uint8)
        #gray = np.array(img * 255, dtype = np.uint8)

        dataString_middle=""
        dataString_lower=""
        dataString_upper=""

        character = img
        # print character

        character = normalize.get_mask(character, 5)
        xMin, xMax, yMin, yMax= locate_character.char_location(character)
        # print xMin, xMax, yMin, yMax

        dataArray_middle = feature_mapper.middle(character, 21, 43, xMin, xMax)
        dataArray_middle.append('m1')
        # print dataArray_middle

        dataArray_lower = feature_mapper.lower(character, 42, 64, xMin, xMax)
        dataArray_lower.append('l0')
        # print dataArray_lower

        dataArray_upper = feature_mapper.upper(character, 0, 22, xMin, xMax)
        dataArray_upper.append('u0')

        # for i in range(1, 3):
        # char1=""
        # char2=""
        # char3=""
        MiddleZoneProb = classifier_middle(dataArray_middle, Orange.classification.Classifier.GetProbabilities)
        UpperZoneProb = classifier_upper(dataArray_upper, Orange.classification.Classifier.GetProbabilities)
        LowerZoneProb = classifier_lower(dataArray_lower, Orange.classification.Classifier.GetProbabilities)

        # MiddleZoneClass=(classifier_middle(dataArray_middle, Orange.classification.Classifier.GetBoth))
        # UpperZoneClass=(classifier_upper(dataArray_upper, Orange.classification.Classifier.GetBoth))
        # LowerZoneClass=(classifier_lower(dataArray_lower, Orange.classification.Classifier.GetBoth))

        ###############################################
        if classifier_lower(dataArray_lower, Orange.classification.Classifier.GetValue) == 'l0':
        
            for i in range(0, len(lowerZoneLabels)):
               lowerZoneLabels[i] = 'l0'
        
            for i in xrange(0, len(LowerZoneProb)):
               LowerZoneProb[i] = 1
        
        
        if classifier_upper(dataArray_upper, Orange.classification.Classifier.GetValue) == 'u0':
        
            for i in range(0, len(upperZoneLabels)):
               upperZoneLabels[i] = 'u0'
        
            for i in xrange(0, len(UpperZoneProb)):
               UpperZoneProb[i] = 1

        predicted_char, lower, middle, upper = prob_match.probability_match(lower=[LowerZoneProb,lowerZoneLabels],
                                                middle=[MiddleZoneProb, middleZoneLabels],
                                                upper=[UpperZoneProb,upperZoneLabels])
        # char_mapper.char_map()

        # print char+"   "+lower+"  "+middle+"  "+upper
        return predicted_char

def join_modifiers(edit_text_):
    #edit_text = edit_text.decode("utf-8")
    edit_text = list(edit_text_.decode("utf-8"))
    join_dictionary = {u'\u0dd9'u'\u0dd9' : u'\u0ddb',  u'\u0dd9'u'\u0dca' : u'\u0dda', u'\u0dd9'u'\u0dcf' : u'\u0ddc', u'\u0dd9'u'\u0dca'u'\u0dcf' : u'\u0ddd',    u'\u0dd9'u'\u0dcf'u'\u0dca' : u'\u0ddd',
                   u'\u0dd9'u'\u0ddf' : u'\u0dde',  u'\u0dd9'u'\u0df3' : u'\u0dde', u'\u0dd8'u'\u0dd8' : u'\u0df2', }

    modifier_list = [u'\u0dca', u'\u0dcf', u'\u0df2', u'\u0df3', u'\u0dd0', u'\u0dd1', u'\u0dd2', u'\u0dd3', u'\u0dd4', u'\u0dd5', u'\u0dd6', u'\u0dd7', u'\u0dd8', u'\u0dd9', u'\u0dda', u'\u0ddb', u'\u0ddc', u'\u0ddd',
                     u'\u0dde', u'\u0ddf', u'\u0d82', u'\u0d83']

    left_modifiers = []
    right_modifiers = []

    punctuation_list = [u'.', u' ', u'?', u',', u'!']

    new_list = []
    temp = ''
    print len(edit_text)
    for i in range(len(edit_text)):
        if (edit_text[i] == " ") or (edit_text[i] == ".") or (edit_text[i] == ",") or (edit_text[i] == "?") or (edit_text[i] == "!"):
            if (temp != ''):
                try:
                    new_list.append(join_dictionary[temp])
                except KeyError:
                    new_list.append(temp)
                temp = ''
            new_list.append(edit_text[i])
        elif (i==0):
            if (edit_text[i] in modifier_list):
                temp = edit_text[i]
            else:
                new_list.append(edit_text[i])
        elif (i==len(edit_text)-1):
            if (edit_text[i] not in modifier_list):
                new_list.append(edit_text[i])
                if (temp != ''):
                    try:
                        new_list.append(join_dictionary[temp])
                    except KeyError:
                        new_list.append(temp)
                    temp = ''
            else:
                if (temp != ''):
                    temp = temp + edit_text[i]
                    try:
                        new_list.append(join_dictionary[temp])
                    except KeyError:
                        new_list.append(temp)
                    temp = ''
                else:
                    new_list.append(edit_text[i])
        elif (edit_text[i] == u'\u0dca') and (i>1) and (edit_text[i-1] not in modifier_list) and (edit_text[i-1] not in punctuation_list) and (edit_text[i-2] in punctuation_list):
            new_list.append(u'\u0dd3')
        elif (edit_text[i] == u'\u0dd9'):
            if (temp != ''):
                try:
                    new_list.append(join_dictionary[temp])
                except KeyError:
                    new_list.append(temp)
            temp = edit_text[i]
        elif (edit_text[i] in modifier_list):
            if (edit_text[i-1] in modifier_list) or (edit_text[i-1]  in punctuation_list):
                temp = temp + edit_text[i]
            else:
                if (temp!=''):
                    temp = temp + edit_text[i]
                    try:
                        new_list.append(join_dictionary[temp])
                    except KeyError:
                        new_list.append(temp)
                    temp = ''
                else:
                    new_list.append(edit_text[i])
        else:
            new_list.append(edit_text[i])
            if (edit_text[i+1] not in modifier_list) or (edit_text[i+1]== u'\u0dd9'):
                if (temp != ''):
                    try:
                        new_list.append(join_dictionary[temp])
                    except KeyError:
                        new_list.append(temp)
                    temp = ''

    #print new_list
    output_string = '%s' % ''.join([''.join('%s' % ' '.join(e) for e in new_list)])
    return output_string

def classify_image(url):
    img = cv2.imread(url)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    char = classify(img)
    print char

#classify_image("/home/viduranga/Desktop/project/segmenter/single_characters/2_1_r.jpg")
# classify_image("C:/Users/Naleen/PycharmProjects/sinhala_ocr/segmenter/final_characters/14.jpg")
