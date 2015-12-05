# -*- coding: utf-8 -*-


import numpy as np
# import segmenter
# import classifier
import corrector
# import synthesizer

input_text=" සංවිටාතවලිනුක්, 123 ඉල්ලා සිවින? amali ග�තක් කො�ඹ ඡලය ඉහළන්  "

corrected_text = corrector.correct(input_text)

print corrected_text

# print '%s' % ''.join([' , '.join('%s' % ''.join(e) for e in corrected_text)])

# corrected_text = corrector.correct(classified_text)
#print "corrected text : " + corrected_text

# synthesized_voice = synthesizer.synthesize(corrected_text)
