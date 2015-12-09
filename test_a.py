# -*- coding: utf-8 -*-


import numpy as np
# import segmenter
# import classifier
import corrector
import codecs
# import synthesizer


file = open('corrector/input.txt', 'r')
input_text = file.read()
# input_text = raw_text[3:]
print input_text

corrected_text = corrector.correct(input_text)



print '%s' % ''.join([' , '.join('%s' % ' '.join(e) for e in corrected_text)])

# corrected_text = corrector.correct(classified_text)
#print "corrected text : " + corrected_text

# synthesized_voice = synthesizer.synthesize(corrected_text)
