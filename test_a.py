# -*- coding: utf-8 -*-


import numpy as np
# import segmenter
# import classifier
import corrector
# import synthesizer

# input_text=" රජගහා විහාරෆ හඤූතර තරඔක් කදූභැටියරී වර පසින් ඇහ් අ "
input_text="රජගහා විහාරෆ හඤූතර තරඔක් කදූභැටියරී වර පසින් ඇහ් අ"

corrected_text = corrector.correct(input_text)
# corrected_text=corrected_text.split(" ")
# print( corrected_text)

#print corrected_text


print '%s' % ''.join([' , '.join('%s' % ' '.join(e) for e in corrected_text)])

# corrected_text = corrector.correct(classified_text)
#print "corrected text : " + corrected_text

# synthesized_voice = synthesizer.synthesize(corrected_text)
