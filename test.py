# -*- coding: utf-8 -*-

import cv2
import os

import numpy as np
import segmenter
import classifier
import collections, itertools
import corrector
from classifier.src.mapper import character_position as char_pos
import pickle

# import synthesizer

from itertools import tee, islice, chain, izip

def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return izip(prevs, items)

# print corrector.correct(input_text)
# package_directory = os.path.dirname(os.path.abspath(__file__))

image = cv2.imread('ww - Copy.jpg')

# CharReco2.tester_char(image)





image_bw, image_gray = segmenter.preprocess(image)
lines = segmenter.segment_lines(image_bw)

classified_text = ""
ctp = ""
ctc = ""
ctn = ""

for line in lines[:]:
    character_images = segmenter.segment(line)

    # for character_image in character_images:
    #     character_image_ = character_image.copy()
    #     classified_text += str(classifier.classify(character_image,0)[0])
    #
    #     nxt=character_images[character_images.index(character_image.all())+1]

        # print str(classifier.classify(nxt,0)[0])


    # for current_char_img, next_char_img in zip(character_images, character_images[1:]):

    # for previous_char_img, current_char_img in zip([None]+character_images[:-1], character_images):
    i=0
    for previous_char_img, current_char_img in previous_and_next(character_images):


            # previous_char_img =previous_char_img_.copy()
            # current_char_img = current_char_img.copy()
            # next_char_img = next_char_img.copy()


#             classified_text += str(classifier.classify(current_char_img,0)[0])
# ###################################################################################
#
            index=0

            prv_char =classifier.classify(previous_char_img, 0)
            cnt_char =classifier.classify(current_char_img, 0)
            cv2.imwrite('T/'+str(i)+'pre.jpg',previous_char_img)
            cv2.imwrite('T/'+str(i)+'cur.jpg',current_char_img)
            i=i+1
            print str(prv_char)+" : "#+str(cnt_char)
            # ctp += prv_char
            # ctc += str(classifier.classify(current_char_img,0)[0])
            #
            # for index in range(0,99):
            #
            #     # if current is a left modifier
            #         # prev : space or none, base char, right mod, upper mod, lower mod
            #     if (char_pos.blank.__contains__(prv_char) or
            #         char_pos.right_mod.__contains__(prv_char) or
            #         char_pos.upper_mod_char.__contains__(prv_char) or
            #         char_pos.lower_mod_char.__contains__(prv_char) or
            #         char_pos.base_char.__contains__(prv_char)) and char_pos.left_mod.__contains__(cnt_char):
            #             classified_text += cnt_char
            #             print "char1:  "+ cnt_char
            #             print "1------"
            #             break
            #     else:
            #         index=index+1
            #         cnt_char=classifier.classify(current_char_img, index)
            #         print "1#########:  "+str(index)+": cnt "+cnt_char+"      prv"+prv_char
            #
            #     # if current is a right modifier
            #         # prev : base char,
            #     if char_pos.base_char.__contains__(prv_char) and char_pos.right_mod.__contains__(cnt_char):
            #         classified_text += cnt_char
            #         print "char2:  "+ cnt_char
            #         print "2------"
            #         break
            #     else:
            #         index=index+1
            #         cnt_char=classifier.classify(current_char_img, index)
            #         print "2#########"
            #
            #     # if current is a base char
            #         # prev : left mod, base char, upper mod, lower mod, none/space
            #     if (char_pos.base_char.__contains__(prv_char) or ) and char_pos.right_mod.__contains__(cnt_char):
            #         classified_text += cnt_char
            #         print "char2:  "+ cnt_char
            #         print "2------"
            #         break
            #     else:
            #         index=index+1
            #         cnt_char=classifier.classify(current_char_img, index)
            #         print "2#########"

print "classified text : " + classified_text

print ctp
print ctc
print ctn

# corrected_text = corrector.correct(classified_text)
# print "corrected text : " + corrected_text

# synthesized_voice = synthesizer.synthesize(corrected_text)
