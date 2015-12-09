# -*- coding: utf-8 -*-
__author__ = 'Amali Rathnapriya'

import codecs
from collections import Counter
import os


package_directory = os.path.dirname(os.path.abspath(__file__))


def correction(input_list, Correct_word_string,incorrect_word_string,suggestions,unidentified):



    text = codecs.open('corrector/outfile.txt', encoding='utf-8')
    text2 = text.read()
    text2 = text2.replace(',',' ').replace('.',' ').replace('?',' ').split()

    # calculating probabilities

    counts = Counter(text2)
    states = counts.keys()
    sumv = sum(counts.values())
    initProbs = {c: counts[c] / float(sumv) for c in counts}
    probs={}

    print "probabilities calculated"
    dictionary = codecs.open('corrector/dictionary.txt', encoding='utf-8')
    dictionary = dictionary.read()
    file=open('corrector/permutations.txt','w')

    character_set = []



#    input_string = input_string.split()


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

    character_list9 = ['පු','සු','දු','යු']
    character_list9 = [x.decode('UTF8') for x in character_list9]

    character_list10 = ['ඛ','ධ','බ','ඩ']
    character_list10 = [x.decode('UTF8') for x in character_list10]

    All_characters=[character_list1,character_list2,character_list3,character_list4,character_list5,character_list6,character_list6,character_list7,character_list8,character_list9,character_list10]

    for input_word in input_list:
        # if input_word.isdigit():
        #     Correct_word_string.append(input_word)
        if input_word in dictionary:
            correct_word = input_word
            print "correct",correct_word
            Correct_word_string.append(correct_word)
        elif input_word.isdigit()==True:
            correct_word=input_word
            print "correct",correct_word
            Correct_word_string.append(correct_word)
        elif input_word.isalpha()==True:
            correct_word=input_word
            print "correct",correct_word
            Correct_word_string.append(correct_word)


        else:
            incorrect_word = input_word

            checkfamily(incorrect_word,character_set,suggestions,initProbs,probs,All_characters)

            incorrect_word_string.append(incorrect_word)

    # return Correct_word_string

    correct_word_string_generate(Correct_word_string,incorrect_word_string,suggestions,input_list,unidentified)

    # print "Corrected : "
    # print '%s' % ''.join([' '.join('%s' % ''.join(e) for e in output)])



    return unidentified


def correct_word_string_generate(Correct_word_string,incorrect_word_string,suggestions ,input_string,unidentified):
    # Corrected_word_string = unicode(" ").join(Correct_word_string)


    for input_word in input_string:
        # for incorrect , correct in suggestions.iteritems():
            if input_word not in Correct_word_string:
                unidentified.append(input_word)


    # for item in unidentified:
    #     print "unidentified" , item


    print "to be corrected : "
    print '%s' % ''.join([' '.join('%s' % ''.join(e) for e in unidentified)])
    return unidentified

    # print output


def checkfamily(text,character_set,suggestions,initProbs,probs,All_characters):
    for tuple in All_characters:
        if any((c in tuple) for c in text):
            character_set.append(tuple)





    permutations = []

    for atuple in character_set:


        for c in text:
            if (c in atuple):
               for x in atuple:
                # if x in text:
                   text_rev = text.replace(c, x)
                   permutations.append(text_rev)
                   # for atuple2 in character_set:
                   for c2 in text_rev:
                       if (c2 in atuple):
                           for x2 in atuple:

                            text_rev2=text_rev.replace(c2,x2)
                            permutations.append(text_rev2)
                   # text_rev=text_rev.replace(c,x)
                   # permutations.append(text_rev)
                   # text_rev=text_rev.replace(c,x)
                   # permutations.append(text_rev)

    for name, prob in initProbs.iteritems():
        for item in permutations:
            if name == item:
                # print item
                probs[item]=prob
                correction=item
                suggestions[text].append(correction)
                break




    # for item in permutations:
    #     ff.write(item.encode('utf-8'))


    return suggestions

# def main():
#     input_string = u" සංවිටානවලිනුත් ඉල්ලා සිවින"
#     correction(input_string)
#
# main()

# ff.close()