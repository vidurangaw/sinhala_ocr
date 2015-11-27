__author__ = 'Chin'

import dictionary

def map_phonemes(grapheme_list):

    new_list = []

    for i in range(0, len(grapheme_list), 1):
        if (grapheme_list[i]==' ' or grapheme_list[i]=='.' or grapheme_list[i]==',' or grapheme_list[i]=='?' or grapheme_list[i]=='!'):
            new_list.append(grapheme_list[i])
        elif (grapheme_list[i].isdigit()):
            new_list.append(map_digits(grapheme_list[i]))
        elif (grapheme_list[i].find('M')== -1):
            if (i==0):
                new_list.append(dictionary.phonemes[grapheme_list[i]])
            elif (grapheme_list[i-1]==' ' or grapheme_list[i-1]=='.' or grapheme_list[i-1]==',' or grapheme_list[i-1]=='?' or grapheme_list[i-1]=='!'):
                new_list.append(dictionary.phonemes[grapheme_list[i]])
            else:
                new_list.append(dictionary.phonemes[grapheme_list[i] + '_'])
        elif (grapheme_list[i].find('M')!= -1):
            last = new_list.pop()
            if (last.find('_')!= -1):
                new_list.append(dictionary.phonemes[last[:-1] + grapheme_list[i]])
            else:
                new_list.append(dictionary.phonemes[last + grapheme_list[i]])

    return new_list

def map_digits(digit):
    new_list = []
    return digit