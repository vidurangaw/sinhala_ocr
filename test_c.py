# # -*- coding: utf-8 -*-

#import cv2
#import numpy as np
#import segmenter
#import classifier
#import corrector
#import synthesizer

join_dictionary = {u'\u0dd9'u'\u0dd9' : u'\u0ddb',  u'\u0dd9'u'\u0dca' : u'\u0dda', u'\u0dd9'u'\u0dcf' : u'\u0ddc', u'\u0dd9'u'\u0dca'u'\u0dcf' : u'\u0ddd',    u'\u0dd9'u'\u0dcf'u'\u0dca' : u'\u0ddd',
                   u'\u0dd9'u'\u0ddf' : u'\u0dde',  u'\u0dd9'u'\u0df3' : u'\u0dde', u'\u0dd8'u'\u0dd8' : u'\u0df2', }

modifier_list = [u'\u0dca', u'\u0dcf', u'\u0df2', u'\u0df3', u'\u0dd0', u'\u0dd1', u'\u0dd2', u'\u0dd3', u'\u0dd4', u'\u0dd5', u'\u0dd6', u'\u0dd7', u'\u0dd8', u'\u0dd9', u'\u0dda', u'\u0ddb', u'\u0ddc', u'\u0ddd',
                 u'\u0dde', u'\u0ddf', u'\u0d82', u'\u0d83']

left_modifiers = []
right_modifiers = []

punctuation_list = [u'.', u' ', u'?', u',', u'!']
#පරීගණත ඟූෂපිෙක්රීඹ්්‍ය ය්ද්‍යාඛ ප්‍රෑස්‍රරීඛ් රයෑයූන ෙතාරකූඬප කායීඝණ ෂ්ඨය
#මම ගෙදර යනවා

raw_text = "පරීගණත ඟූෂපිෙක්රීඹ්්‍ය ය්ද්‍යාඛ ප්‍රෑස්‍රරීඛ් රයෑයූන ෙතාරකූඬප කායීඝණ ෂ්ඨය"
print raw_text
input_text = list(raw_text.decode("utf-8"))
print input_text

def join_modifiers(edit_text):
    new_list = []
    temp = ''
    print len(edit_text)
    for i in range(len(edit_text)):
        if (edit_text[i] == " ") or (edit_text[i] == ".") or (edit_text[i] == ",") or (edit_text[i] == "?") or (edit_text[i] == "!"):
            if (temp != ''):
                try:
                    new_list.append(join_dictionary[temp])
                except KeyError:
                    new_list.append(temp)
                temp = ''
            new_list.append(edit_text[i])
        elif (i==0):
            if (edit_text[i] in modifier_list):
                temp = edit_text[i]
            else:
                new_list.append(edit_text[i])
        elif (i==len(edit_text)-1):
            if (edit_text[i] not in modifier_list):
                new_list.append(edit_text[i])
                if (temp != ''):
                    try:
                        new_list.append(join_dictionary[temp])
                    except KeyError:
                        new_list.append(temp)
                    temp = ''
            else:
                if (temp != ''):
                    temp = temp + edit_text[i]
                    try:
                        new_list.append(join_dictionary[temp])
                    except KeyError:
                        new_list.append(temp)
                    temp = ''
                else:
                    new_list.append(edit_text[i])
        elif (edit_text[i] == u'\u0dca') and (i>1) and (edit_text[i-1] not in modifier_list) and (edit_text[i-1] not in punctuation_list) and (edit_text[i-2] in punctuation_list):
            new_list.append(u'\u0dd3')
        elif (edit_text[i] == u'\u0dd9'):
            if (temp != ''):
                try:
                    new_list.append(join_dictionary[temp])
                except KeyError:
                    new_list.append(temp)
            temp = edit_text[i]
        elif (edit_text[i] in modifier_list):
            if (edit_text[i-1] in modifier_list) or (edit_text[i-1]  in punctuation_list):
                temp = temp + edit_text[i]
            else:
                if (temp!=''):
                    temp = temp + edit_text[i]
                    try:
                        new_list.append(join_dictionary[temp])
                    except KeyError:
                        new_list.append(temp)
                    temp = ''
                else:
                    new_list.append(edit_text[i])
        else:
            new_list.append(edit_text[i])
            if (edit_text[i+1] not in modifier_list) or (edit_text[i+1]== u'\u0dd9'):
                if (temp != ''):
                    try:
                        new_list.append(join_dictionary[temp])
                    except KeyError:
                        new_list.append(temp)
                    temp = ''

    print new_list
    output_string = '%s' % ''.join([''.join('%s' % ' '.join(e) for e in new_list)])
    return output_string

print join_modifiers(input_text)

#print u'aあä'.encode('ascii')

#listA = read_text(raw_text)

#corrector.correct(raw_text)

# input_text=u" සංවිටාතවලිනුක්, 123 ඉල්ලා සිවින? amali ග�තක් කො�ඹ ඡලයa ඉහළන්  "
#
# image = cv2.imread('test.jpg')
#
# image_bw, image_gray = segmenter.preprocess(image)
#
# lines = segmenter.segment_lines(image_bw)
#
# classified_text = ""
#
# for i, line in enumerate(lines[:1]):
# 	character_images = segmenter.segment_line(line, i)
# 	for character_image in character_images:
# 		classified_text += classifier.classify(character_image)
# 		#classified_text += "2"
#
# remove extra spaces
# classified_text = classified_text.strip()
# classified_text = " ".join(classified_text.split())
#
# print "classified text : " + classified_text
#
# corrected_text = corrector.correct(classified_text)
# print "corrected text : " + corrected_text
#
# synthesized_voice = synthesizer.synthesize(corrected_text)
