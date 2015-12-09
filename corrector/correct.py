# -*- coding: utf-8 -*-
__author__ = 'Asus'

# import preprocess
import non_word_correct
import codecs
import missing_correct
import operator
import edit_distance
import create_output
import grammar_correct
from collections import  defaultdict
# input_text=" සංවිටාතවලිනුක්, 123 ඉල්ලා සිවින? amali ග�තක් කො�ඹ ඡලය ඉහළන්  "

def correct(input_text):

    Correct_word_string = []
    incorrect_word_string = []
    # suggestions=[]
    unidentified=[]
    output=[]
    edit_distances={}
    suggestions=defaultdict(list)

    print input_text

    input_text = input_text.decode("utf-8")

    input_text=input_text.replace(',',' ').replace('.',' ').replace('?',' ').replace('!',' ')
    # for test in text:
    #     test=test.encode('utf-8')
    input_words=input_text.split()

    non_word_correct.correction(input_words,Correct_word_string,incorrect_word_string,suggestions,unidentified)
    print "permutations done"

    for item in unidentified:
        # print item
        #
            #
        if item not in suggestions:
            # corrected=missing_correct.correct(item.encode('utf-8'))
            # dic=defaultdict(corrected)
            corrected=edit_distance.correct(item)


            suggestions[item]=corrected
            # print item , "not here"

    print "edit distances done"

    for input_word in input_words:
             # print input_word
        # for incorrect , correct in suggestions.iteritems():
             if input_word.isdigit():
                 output.append(input_word)
             elif input_word.isalpha():
                 output.append(input_word)
             elif input_word in Correct_word_string:
                 output.append(input_word)
             elif input_word in suggestions.iterkeys():
                 # list(suggestions.itervalues())
                 if suggestions[input_word] is not None and len([item for item in suggestions if item])!=1 :
                    output.append(",".join(suggestions[input_word]))


             else:
                 output.append(input_word)

    print "Final : "

    final_output=create_output.output_function(input_words,output)
    # grammar_correction.sinhala_grammar_rules(output)


    # final_output=grammar_correct.sinhala_grammar_rules(output)
    return '%s' % ''.join(['\n'.join('%s' % ''.join(e) for e in final_output)])

# correct(input_text)