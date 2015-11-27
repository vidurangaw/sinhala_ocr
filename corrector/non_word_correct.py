# -*- coding: utf-8 -*-
__author__ = 'Amali Rathnapriya'

import codecs
from collections import Counter
import os

package_directory = os.path.dirname(os.path.abspath(__file__))

def correction(input_string, Correct_word_string,incorrect_word_string,suggestions,unidentified,output):

    # output=[]
    # unidentified=[]
    
    text = codecs.open('corrector/outfile.txt', encoding='utf-8')
    text2 = text.read()
    text2 = text2.replace(',',' ').replace('.',' ').replace('?',' ').split()

    # calculating probabilities

    counts = Counter(text2)
    states = counts.keys()
    sumv = sum(counts.values())
    initProbs = {c: counts[c] / float(sumv) for c in counts}
    probs={}

    dictionary = codecs.open('corrector/dictionary.txt', encoding='utf-8')
    dictionary = dictionary.read()
    file=open('corrector/permutations.txt','w')
    # print dictionary.encode('utf-8')

    # Correct_word_string = []
    # incorrect_word_string = []
    character_set = []
    # suggestions={}

    # if manual input for testing

    # input_string = u" සංවිටානවලිනුත් ඉල්ලා සිවින"
    input_string = input_string.split()


    # similar grapheme families defined

    character_list1 = ['ක', 'ත', 'න' , 'හ' , 'ග']
    character_list1 = [x.decode('UTF8') for x in character_list1]

    character_list2 = ['ය', 'ස', 'ඝ']
    character_list2 = [x.decode('UTF8') for x in character_list2]

    character_list3 = ['ම', 'ව', 'ච', 'ඹ' , 'ඩ' ,'ධ','ට']
    character_list3 = [x.decode('UTF8') for x in character_list3]

    character_list4 = ['අ', 'ද', 'ඳ']
    character_list4 = [x.decode('UTF8') for x in character_list4]

    character_list5 = ['ජ', 'ර' , 'ඡ','ප්' ]
    character_list5 = [x.decode('UTF8') for x in character_list5]

    character_list6 = ['මි','ටි','ම්','මී','ටී','වි','ච්','ව්', 'ථ']
    character_list6 = [x.decode('UTF8') for x in character_list6]

    character_list7= ['ල','ළ','උ','ලු','ලූ']
    character_list7 = [x.decode('UTF8') for x in character_list7]

    character_list8 = ['කූ','ගූ','ශු','කු','තු','ඥ','තූ','ගු','ඤ']
    character_list8 = [x.decode('UTF8') for x in character_list8]

    character_list9 = ['පු','සු','දු']
    character_list9 = [x.decode('UTF8') for x in character_list9]

    character_list10 = ['ඛ','ධ','බ','ඩ']
    character_list10 = [x.decode('UTF8') for x in character_list10]

    All_characters=[character_list1,character_list2,character_list3,character_list4,character_list5,character_list6,character_list6,character_list7,character_list8,character_list9,character_list10]

    for input_word in input_string:
        # if input_word.isdigit():
        #     Correct_word_string.append(input_word)
        if input_word in dictionary:
            correct_word = input_word

            Correct_word_string.append(correct_word)


        else:
            incorrect_word = input_word
            checkfamily(input_word,character_set,suggestions,initProbs,probs,All_characters)

            incorrect_word_string.append(incorrect_word)

    # return Correct_word_string




    correct_word_string_generate(Correct_word_string,incorrect_word_string,suggestions,input_string,output,unidentified)

    # print "Corrected : "
    # print '%s' % ''.join([' '.join('%s' % ''.join(e) for e in output)])

    print "to be corrected : "
    print '%s' % ''.join([' '.join('%s' % ''.join(e) for e in unidentified)])

    return output,unidentified


def correct_word_string_generate(Correct_word_string,incorrect_word_string,suggestions ,input_string,output,unidentified):
    Corrected_word_string = unicode(" ").join(Correct_word_string)

    # print "verified word string is : "
    # print Corrected_word_string.encode('utf-8')



    for input_word in input_string:
        # for incorrect , correct in suggestions.iteritems():
            if input_word not in Correct_word_string or input_word not in suggestions.iterkeys() and input_word.isalpha()==False  or input_word.isdigit()==False:
        #          output.append(input_word)
             # elif input_word in suggestions.iterkeys():
             #     output.append(suggestions[input_word])

                 unidentified.append(input_word)

    # return Correct_word_string

    # print output


def checkfamily(text,character_set,suggestions,initProbs,probs,All_characters):
    for tuple in All_characters:
        if any((c in tuple) for c in text):
            character_set.append(tuple)


    ff = open('permutations.txt', 'w')


    permutations = []


    for atuple in character_set:


        for c in text:
            if (c in atuple):
               for x in atuple:

                   text_rev = text.replace(c, x)

                   if text_rev!=None:
                        permutations.append(text_rev)
                        ff.write(text_rev.encode('utf-8'))
                        ff.write(" , ")
                        for name, prob in initProbs.iteritems():
                            if name == text_rev:
                                probs[text_rev]=prob
                                suggestions[text]=text_rev

    # for key in probs.iterkeys():
    #     print "corrected words" , key

    # for incorrect , correct in suggestions.iteritems():
    #     print incorrect ," : " , correct

    return suggestions

# def main():
#     input_string = u" සංවිටානවලිනුත් ඉල්ලා සිවින"
#     correction(input_string)
#
# main()