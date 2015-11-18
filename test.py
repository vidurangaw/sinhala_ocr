# -*- coding: utf-8 -*-

import cv2
import numpy as np
import segmenter
import classifier
import corrector
# import synthesizer

# input_text=u" සංවිටාතවලිනුක්, 123 ඉල්ලා සිවින? amali ග�තක් කො�ඹ ඡලයa ඉහළන්  "

# print corrector.correct(input_text)


image = cv2.imread('ww.jpg')

# CharReco2.tester_char(image)

image_bw, image_gray = segmenter.preprocess(image)
lines = segmenter.segment_lines(image_bw)

classified_text = ""
for line in lines[:1]: 
	character_images = segmenter.segment(line)

	for character_image in character_images:
		if (character_image == np.array([0])).all():
			classified_text += " "
		else:
			character_image_ = character_image.copy()
  		
			cv2.bitwise_not(character_image, character_image_)

			classified_text += classifier.classify(character_image_)

			#classified_text += "2"	
			#print classified_text

print "classified text : " + classified_text

# corrected_text = corrector.correct(classified_text)
# print "corrected text : " + corrected_text

# synthesized_voice = synthesizer.synthesize(corrected_text)
