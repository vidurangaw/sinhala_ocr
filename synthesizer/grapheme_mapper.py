__author__ = 'Chin'

import dictionary

def map_graphemes(characters):

    grapheme_list = []
    digit = ''

    for i in range(0, len(characters), 1):
        try:
            if (characters[i]==' ' or characters[i]=='.' or characters[i]==',' or characters[i]=='?' or characters[i]=='!'):
                if (digit != ''):
                    grapheme_list.append(digit)
                    digit = ''
                grapheme_list.append(characters[i])
            elif (characters[i].isdigit()):
                digit = digit + characters[i]
            else:
                if (digit != ''):
                    grapheme_list.append(digit)
                    digit = ''
                grapheme_list.append(dictionary.graphemes[characters[i]])
        except KeyError:
            continue

    return grapheme_list

