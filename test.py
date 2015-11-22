# -*- coding: utf-8 -*-

import cv2
import os

import numpy as np
import segmenter
import classifier
import corrector
from classifier.src.mapper import character_position as char_pos
import pickle

# import synthesizer

# input_text=u" සංවිටාතවලිනුක්, 123 ඉල්ලා සිවින? amali ග�තක් කො�ඹ ඡලයa ඉහළන්  "

# print corrector.correct(input_text)
# package_directory = os.path.dirname(os.path.abspath(__file__))


image = cv2.imread('WW.jpg')

# CharReco2.tester_char(image)





image_bw, image_gray = segmenter.preprocess(image)
lines = segmenter.segment_lines(image_bw)

classified_text = ""
for line in lines[:]:
    character_images = segmenter.segment(line)

    # for current, next in zip(the_list, the_list[1:]):
    char1=" "
    char2 = " "
    char3=" "
    for current_char_image, next_char_image in zip(character_images,character_images[1:]):

###################################################################################
        if (current_char_image == np.array([0])).all():
            classified_text += " "
        else:
            index=0
            current_char_image = current_char_image.copy()
            next_char_image = next_char_image.copy()
            cv2.bitwise_not(current_char_image, current_char_image)
            cv2.bitwise_not(next_char_image,next_char_image)
            # classified_text += classifier.classify(character_image_, index)
###################################################################################

        # character_image_ = character_image.copy()
        # cv2.bitwise_not(character_image, character_image_)
        # #
        # index=0


            ##char 2 changes always

            index_max=99
            char2, index_max = classifier.classify(current_char_image, index)
            for index in range(index, index_max):

#if char2 is a right modifier  #1) char1 should be a character  #2) char3 is a not a right modifier(left modifier or a character)
                if char_pos.right_mod.__contains__(char2):
                    if char_pos.base_char.__contains__(char1):
                        if char_pos.left_mod.__contains__(char3) or char_pos.left_mod.__contains__(char3):
                            classified_text = classified_text+char2

                            index = 0
                            print "!!!!!!!!!!"
                            char1=char2
                            char2=char3
                            char3, index_max=classifier.classify(next_char_image, index)
                            print char3+"------"
                            break
                else:
                    index=index+1
                    char2, index_max=classifier.classify(current_char_image, index)
                    print "#########"

##if char2 is a left modifier  #1) char1 is a right modifier or a character #2) char2 is a character
                if char_pos.right_mod.__contains__(char2):
                    if char_pos.base_char.__contains__(char1):
                        if char_pos.left_mod.__contains__(char3) or char_pos.left_mod.__contains__(char3):
                            classified_text = classified_text+char2

                            index = 0
                            print "!!!!!!!!!!"
                            char1=char2
                            char2=char3
                            char3, index_max=classifier.classify(next_char_image, index)
                            print char3+"------"
                            break
                else:
                    index=index+1
                    char2, index_max=classifier.classify(current_char_image, index)
                    print "#########"

##if char2 is a character #1) left/right modifier or a characte
                if char_pos.right_mod.__contains__(char2):
                    if char_pos.base_char.__contains__(char1):
                        if char_pos.left_mod.__contains__(char3) or char_pos.left_mod.__contains__(char3):
                            classified_text = classified_text+char2

                            index = 0
                            print "!!!!!!!!!!"
                            char1=char2
                            char2=char3
                            char3, index_max=classifier.classify(next_char_image, index)
                            print char3+"------"
                            break
                else:
                    index=index+1
                    char2, index_max=classifier.classify(current_char_image, index)
                    print "#########"

##if char2 has lower modifiers
                if char_pos.right_mod.__contains__(char2):
                    if char_pos.base_char.__contains__(char1):
                        if char_pos.left_mod.__contains__(char3) or char_pos.left_mod.__contains__(char3):
                            classified_text = classified_text+char2

                            index = 0
                            print "!!!!!!!!!!"
                            char1=char2
                            char2=char3
                            char3, index_max=classifier.classify(next_char_image, index)
                            print char3+"------"
                            break
                else:
                    index=index+1
                    char2, index_max=classifier.classify(current_char_image, index)
                    print "#########"

##if char 2 has upper modifiers
                if char_pos.right_mod.__contains__(char2):
                    if char_pos.base_char.__contains__(char1):
                        if char_pos.left_mod.__contains__(char3) or char_pos.left_mod.__contains__(char3):
                            classified_text = classified_text+char2

                            index = 0
                            print "!!!!!!!!!!"
                            char1=char2
                            char2=char3
                            char3, index_max=classifier.classify(next_char_image, index)
                            print char3+"------"
                            break
                else:
                    index=index+1
                    char2, index_max=classifier.classify(current_char_image, index)
                    print "#########"



print "classified text : " + classified_text

# corrected_text = corrector.correct(classified_text)
# print "corrected text : " + corrected_text

# synthesized_voice = synthesizer.synthesize(corrected_text)
