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


for line in lines[:]:
    character_images = segmenter.segment(line)

    for character_image in character_images:
        character_image_ = character_image.copy()

        char=classifier.classify(character_image,0)
        classified_text += char
        #
        #
        #
        #
        # char_pos.test_position(character_images, classified_text)

print "corrected text : " + classified_text

