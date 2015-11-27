__author__ = 'Chin'

import dictionary

def map_graphemes(characters):
    
    new_list = []
    digit = ''

    for i in range(0, len(characters), 1):
        if (characters[i]==' ' or characters[i]=='.' or characters[i]==',' or characters[i]=='?' or characters[i]=='!'):
            if (digit != ''):
                new_list.append(digit)
                digit = ''
            new_list.append(characters[i])
        elif (characters[i].isdigit()):
            digit = digit + characters[i]
        else:
            if (digit != ''):
                new_list.append(digit)
                digit = ''
            new_list.append(dictionary.graphemes[characters[i]])

    return new_list