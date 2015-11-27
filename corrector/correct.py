# -*- coding: utf-8 -*-
__author__ = 'Asus'

# import preprocess
import non_word_correct
import codecs
import missing_correct
import operator

# input_text=u" සංවිටාතවලිනුක්, 123 ඉල්ලා සිවින? amali ග�තක් කො�ඹ ඡලය ඉහළන්  "

def correct(input_text):

    Correct_word_string = []
    incorrect_word_string = []
    suggestions={}
    unidentified=[]
    output=[]
    edit_distances={}


    input_text = input_text.decode("utf-8")


    input_text=input_text.replace(',',' ').replace('.',' ').replace('?',' ').replace('!',' ')
    # for test in text:
    #     test=test.encode('utf-8')


    # preprocess.preprocess()
    non_word_correct.correction(input_text,Correct_word_string,incorrect_word_string,suggestions,unidentified,output)

    for item in unidentified:

        # print "unidentified: ",item

        corrected=missing_correct.correct(item.encode('utf-8'))

        suggestions[item]=corrected

    # for item in suggestions.itervalues():
    #     print '%s' % ' '.join([' '.join('%s' % ''.join(e) for e in item)])
        # for item in corrected:
        #     print "s: "+item

        # print '%s' % ''.join([' '.join('%s' % ''.join(e) for e in corrected)])

        # get the chosen word to be added
        # if len(corrected)==1:
        #     suggestions[item]=corrected

    # print "\nsuggested"
    # for item in suggestions.iterkeys():
    #     print '%s' % ''.join([''.join('%s' % ''.join(e) for e in item)])

    input_text=input_text.split()


    for input_word in input_text:
             # print input_word
        # for incorrect , correct in suggestions.iteritems():
             if input_word.isdigit():
                 output.append(input_word)
             elif input_word.isalpha():
                 output.append(input_word)
             elif input_word in Correct_word_string:
                 output.append(input_word)
             elif input_word in suggestions.iterkeys():
                 output.append('%s' % ''.join([' , '.join('%s' % ''.join(e) for e in suggestions[input_word])]))
                 # output.append(suggestions[input_word])
             else:
                 output.append(input_word)





    print "Final : "

    for item in output:
        print item

    # output = '%s' % ''.join([' '.join('%s' % ''.join(e) for e in output)])
    # print '%s' % ''.join([' '.join('%s' % ''.join(e) for e in output)])
    return output


# main(input_text)