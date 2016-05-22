# -*- coding: utf-8 -*-
import cv2
import numpy as np
import wave
import segmenter
import classifier
import corrector
import synthesizer

# input_text=u" සංවිටාතවලිනුක්, 123 ඉල්ලා සිවින? amali ග�තක් කො�ඹ ඡලයa ඉහළන්  "
def run(image_path):
	image_path_ = image_path.rsplit('.', 1)[0]
	preprocess_image_path = image_path_+'_bw.jpg'
	audio_path = image_path_+'.wav'

	image = cv2.imread(image_path)

	image_bw = segmenter.preprocess(image)

	cv2.imwrite(preprocess_image_path, image_bw) 

	lines = segmenter.segment_lines(image_bw)

	#classified_text = "රජගහා විහාරෆ හඤූතර තරඔක් කදූභැටියරී වර පසින් ඇහ් අ"
	classified_text = ""

	for i, line in enumerate(lines):
		character_images = segmenter.segment_line(line, i)
		for character_image in character_images:			
			classified_text += classifier.classify(character_image)
			#classified_text += "2"				

	#classified_text = "රජගහා විහාරෆ හඤූතර තරඔක් කදූභැටියරී වර පසින් ඇහ්"

	# remove extra spaces
	


	#classified_text = ""
	classified_text = classified_text.strip()
	classified_text = " ".join(classified_text.split())

	#join modifiers
	classified_text = classifier.join_modifiers(classified_text)

	print classified_text
	
	corrected_words = corrector.correct(classified_text)

	corrected_text = ""

	for words in corrected_words:			
			corrected_text += words[0].encode("utf-8") + " " 

	print corrected_text
	
	synthesized_data = synthesizer.synthesize(corrected_text)

	audio_outfile = wave.open(audio_path, 'wb')

	audio_outfile.setparams(synthesized_data[0][0])

	for i in range(0, len(synthesized_data), 1):
			audio_outfile.writeframes(synthesized_data[i][1])

	# classified_text = "රජගහා විහාරෆ හඤූතර තරඔක් කදූභැටියරී වර පසින් ඇහ් අ"
	# corrected_words = [[1111111,2,"old1"],[3233333,4,"old2"]]


	return classified_text, corrected_words, image_path_, audio_path
