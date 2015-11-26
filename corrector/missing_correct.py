# -*- coding: utf-8 -*-
__author__ = 'Amali Rathnapriya'

import codecs
import operator
import os

package_directory = os.path.dirname(os.path.abspath(__file__))

def levenshteinDistance(s1,s2):
    if len(s1) > len(s2):
        s1,s2 = s2,s1
    distances = range(len(s1) + 1)
    for index2,char2 in enumerate(s2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1+1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]

def correct(s1):
    edit_distances={}
    # print package_directory
    dictionary_file = os.path.join(package_directory, 'dictionary.txt')
    f1=codecs.open(dictionary_file, encoding='utf-8')
    text2 = f1.read()
    text = text2.replace('-',' ').split()

    # print("input permuted list")
    # text=raw_input()
    for item in text:
            item=item.encode('utf-8')
        # if item.__len__()==s1.__len__():
            s2=item
    # for item in text.split(' '):
            # s2 = item
            # print (s2)
            distance=levenshteinDistance(s1,s2)
        # print(levenshteinDistance(s1.decode('utf-8'),s2.decode('utf-8')))

            edit_distances[s2]=distance


    sorted_edit_distances = sorted(edit_distances.items(), key=operator.itemgetter(1))




    # print ("Suggested words :" + s1)
# if min(edit_distances.values())!=None:
    min_val = min(edit_distances.values())
    min_keys = filter(lambda k: edit_distances[k] == min_val, edit_distances)

# word=min(edit_distances, key=lambda k: edit_distances[k])

    # print '%s' % '\n'.join(['\n'.join('%s' % ''.join(e) for e in min_keys)])

    return min_keys




# def main():
#     print("input the incorrect string")
#     s1=raw_input()
#     correct(s1)
#
# main()
