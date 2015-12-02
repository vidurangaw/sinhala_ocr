# -*- coding: utf-8 -*-

import cv2
import numpy as np
import segmenter
import classifier
import corrector
# import synthesizer

# input_text=u" සංවිටාතවලිනුක්, 123 ඉල්ලා සිවින? amali ග�තක් කො�ඹ ඡලයa ඉහළන්  "

image = cv2.imread('ww4.jpg')

image_bw = segmenter.preprocess(image)

lines = segmenter.segment_lines(image_bw)

classified_text = ""

for i, line in enumerate(lines[:1]):
	character_images = segmenter.segment_line(line, i)
	for character_image in character_images:			
		classified_text += classifier.classify(character_image)
		#classified_text += "2"				

# remove extra spaces
classified_text = classified_text.strip()
classified_text = " ".join(classified_text.split())

print "classified text : " + classified_text

# corrected_text = corrector.correct(classified_text)
#print "corrected text : " + corrected_text

# synthesized_voice = synthesizer.synthesize(corrected_text)
