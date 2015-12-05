__author__ = 'Chin'

import dictionary

def map_phonemes(grapheme_list):

    phoneme_list = []

    for i in range(0, len(grapheme_list), 1):
        if (grapheme_list[i]==' ' or grapheme_list[i]=='.' or grapheme_list[i]==',' or grapheme_list[i]=='?' or grapheme_list[i]=='!'):
            phoneme_list.append(grapheme_list[i])
        elif (grapheme_list[i].isdigit()):
            phoneme_list.append(map_digits(grapheme_list[i]))
        elif (grapheme_list[i].find('M')== -1):
            if (i==0):
                phoneme_list.append(dictionary.phonemes[grapheme_list[i]])
            elif (grapheme_list[i-1]==' ' or grapheme_list[i-1]=='.' or grapheme_list[i-1]==',' or grapheme_list[i-1]=='?' or grapheme_list[i-1]=='!'):
                phoneme_list.append(dictionary.phonemes[grapheme_list[i]])
            else:
                phoneme_list.append(dictionary.phonemes[grapheme_list[i] + '_'])
        elif (grapheme_list[i].find('M')!= -1):
            last = phoneme_list.pop()
            if (last.find('_')!= -1):
                phoneme_list.append(dictionary.phonemes[last[:-1] + grapheme_list[i]])
            else:
                phoneme_list.append(dictionary.phonemes[last + grapheme_list[i]])

    for i in range(0, len(phoneme_list), 1):
        if (phoneme_list[i]=='k') or (phoneme_list[i]=='th') or (phoneme_list[i]=='n'):
            store = phoneme_list.pop()
            previous = phoneme_list.pop()
            if (previous.find('i')!= -1) \
                    or (previous.find('o')!= -1) \
                    or (previous.find('u')!= -1) \
                    or(previous.find('e')!= -1) \
                    or(previous.find('ang')!= -1)   \
                    or(previous.find('ru')!= -1)\
                    or(previous.find('aa')!= -1):
                phoneme_list.append(previous)
                phoneme_list.append(store)
            else:
                phoneme_list.append(previous[:-1])
                phoneme_list.append(store)

    return phoneme_list

def map_digits(digit):
    new_list = []
    return digit