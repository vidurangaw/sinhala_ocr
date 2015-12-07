# -*- coding: utf-8 -*-


import numpy as np
# import segmenter
# import classifier
import corrector
# import synthesizer


file = open('corrector/input.txt', 'r')
input_text = file.read()
# input_text = raw_text[3:]
print input_text
# input_text=" රජගහා විහාරෆ හඤූතර තරඔක් කදූභැටියරී වර පසින් ඇහ් අ "
# input_text="මම රජගහා විහාරෆ හඤූතර තරඔක් කදූභැටිය වර පසින් ඇහ් අ මිනාගය සංමිටානය නඳුවැටිය ගියෙමි සමවන්ධ කෙෂ්ත්‍රඵලය තොරකුරු තාක්ෂණ කඨය  "
# input_text="රට පුරා මේ වන විට උග්‍ර ‍පොහොර හිඟයක් පවතින බවත්, මේ හේතුවෙන් ගොවි  ජනතව දැඩි දුෂ්කරතාවකට පත්ව සිටින බවත් ප්‍රධායා"

corrected_text = corrector.correct(input_text)
# corrected_text=corrected_text.split(" ")
# print( corrected_text)

#print corrected_text


print '%s' % ''.join([' , '.join('%s' % ' '.join(e) for e in corrected_text)])

# corrected_text = corrector.correct(classified_text)
#print "corrected text : " + corrected_text

# synthesized_voice = synthesizer.synthesize(corrected_text)
