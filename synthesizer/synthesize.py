__author__ = 'Chin'

import text_reader
import grapheme_mapper
import phoneme_mapper
import speech_generator

# file = open('input/input_text.txt', 'r')
# raw_text = file.read()
# text = raw_text[3:]
# print text

def synthesize(text):

    characters = text_reader.read_text(text)
    print characters

    grapheme_list = grapheme_mapper.map_graphemes(characters)
    print grapheme_list

    phoneme_list = phoneme_mapper.map_phonemes(grapheme_list)
    print phoneme_list

    return speech_generator.generate_audio(phoneme_list)

#synthesize(text)







