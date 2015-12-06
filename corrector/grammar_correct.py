# -*- coding: utf-8 -*-
import shutil
__author__ = 'Amali Rathanpriya'


import codecs
import re


def sinhala_grammar_rules(input_string):

    # input_string = '%s' % ''.join([' '.join('%s' % ''.join(e) for e in input_string)])
    # for item in input_string:unicode(item)

    input_word=input_string[0]


    if input_word==u"මම":
            last_character = input_string[-2:]
            if last_character== u"මි":
                print ('ok')
            else:
                print('not ok')

    elif input_word ==u"අපි":
            last_character = input_string[-2:]
            if last_character ==u"මු":
                print ('ok')
            else:
                print('not ok')
    elif input_word==u"ඔහු":
            last_character=input_string[-3:]
            if last_character in (u"යේය",u"යෙය",u"යයි"):
                print ('ok')
            else:
                print('not ok')
    elif input_word==u"ඇය":
            last_character=input_string[-3:]
            if last_character in (u"යාය",u"යයි"):
                print ('ok')
            else:
                print('not ok')
    elif input_word==u"ඔවුහු":
            last_character=input_string[-3:]
            if last_character in (u"යෝය", u"යයි"):
                print ('ok')
            else:
                print('not ok')

    return input_string