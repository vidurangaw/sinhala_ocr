#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Naleen'

import numpy as np
import classifier
import cv2

base_char = np.array(["අ", "උ", "ඏ", "ඔ", "එ", "ළු", "ඉ", "ක", "ඛ", "ග", "ඝ", "ඟ", "ච", "ඡ", "ජ", "ඣ", "ඤ", "ඦ",
                      "ට", "ථ", "ඨ", "ධ", "ඩ", "ඪ", "ණ", "ඬ", "ත", "ද", "න", "ඳ", "ප", "ඵ", "බ", "භ", "ම",
                      "ඹ", "හ", "ය", "ර", "ල", "ව", "ශ", "ෂ", "ස", "ළ","ළු", "ෆ", "ඥ"])


base_hal =np.array(["ඒ", "ක්", "ඛ්", "ග්", "ඝ්", "ඟ්", "ඡ්", "ච්", "ඣ්", "ජ්", "ඤ්", "ඦ්", "ට්", "ථ්", "ඨ්", "ධ්", "ඩ්", "ඪ්", "ණ්", "ඬ්", "ත්", "ද්", "න්",
                    "ඳ්", "ප්", "ඵ්", "බ්", "භ්",  "ම්", "ඹ්", "හ්", "ළ්",  "ය්", "ර්", "ල්",  "ව්", "ශ්", "ෂ්", "ස්", "ෆ්",  "ඥ්"])

upper_mod_char = np.array(["ඕ", "ඒ", "කි", "කී", "ක්", "ඛි", "ඛී", "ඛ්", "ගි", "ගී", "ග්", "ඝි", "ඝී", "ඝ්", "ඟි", "ඟී", "ඟ්",
                           "ඡ්", "චි", "චී", "ච්", "ඡි", "ඡී", "ඣි", "ඣී", "ඣ්", "ජි", "ජී", "ජ්", "ඤි", "ඤී", "ඤ්", "ඦි", "ඦී",
                           "ඦ්", "ටි", "ටී", "ට්", "ථි", "ථී", "ථ්", "ඨි", "ඨී", "ඨ්", "ධි", "ධී", "ධ්", "ඩි", "ඩී", "ඩ්", "ඪි",
                           "ඪී", "ඪ්", "ණි", "ණී", "ණ්", "ඬි", "ඬී", "ඬ්", "ති", "තී", "ත්", "දි", "දී", "ද්", "නි", "නී", "න්",
                           "ඳි", "ඳී", "ඳ්", "පි", "පී", "ප්", "ඵි", "ඵී", "ඵ්", "බි", "බී", "බ්", "භි", "භී", "භ්", "මි", "මී",
                           "ම්", "ඹි", "ඹී", "ඹ්", "හි", "හී", "හ්", "ළ්", "යි", "යී", "ය්", "රි", "රී", "ර්", "ඊ", "ලි", "ලී",
                           "ල්", "වි", "වී", "ව්", "ශි", "ශී", "ශ්", "ෂි", "ෂී", "ෂ්", "සි", "සී", "ස්", "ළි", "ළී", "ෆි", "ෆී",
                           "ෆ්", "ඥි", "ඥී", "ඥ්"])

lower_mod_char = np.array(["කු", "කූ", "ක්‍ර", "ඛු", "ඛූ", "ගු", "ගූ", "ග්‍ර", "ඝු", "ඝූ", "ඝ්‍ර", "ඟු", "ඟූ", "ඡ්‍ර", "චු", "චූ",
                           "ච්‍ර", "ඡු", "ඡූ", "ඣු", "ඣූ", "ඣ්‍ර", "ජු", "ජූ", "ජ්‍ර", "ඤු", "ඤූ", "ඤ්‍ර", "ඦු", "ඦූ", "ඦ්‍ර",
                           "ටු", "ටූ", "ට්‍ර", "ථු", "ථූ", "ථ්‍ර", "ඨු", "ඨූ", "ඨ්‍ර", "ධු", "ධූ", "ධ්‍ර", "ඩු", "ඩූ", "ඩ්‍ර",
                           "ඪු", "ඪූ", "ඪ්‍ර", "ණු", "ණූ", "ණ්‍ර", "ඬු", "ඬූ", "ඬ්‍ර", "තු", "තූ", "ත්‍ර", "දු", "දූ", "ද්‍ර",
                           "නු", "නූ", "න්‍ර", "ඳු", "ඳූ", "ඳ්‍ර", "පු", "පූ", "ප්‍ර", "ඵු", "ඵූ", "ඵ්‍ර", "බු", "බූ", "බ්‍ර",
                           "භු", "භූ", "භ්‍ර", "මු", "මූ", "ම්‍ර", "ඹු", "ඹූ", "ඹ්‍ර", "හු", "හූ", "හ්‍ර", "යු", "යූ", "ය්‍ර",
                           "ලු", "ලූ", "ල්‍ර", "වු", "වූ", "ව්‍ර", "ශු", "ශූ", "ශ්‍ර", "ෂු", "ෂූ", "ෂ්‍ර", "සු", "සූ", "ස්‍ර",
                           "ෆු", "ෆූ", "ෆ්‍ර", "ඥු", "ඥූ", "ඥ්‍ර"])
right_mod = np.array(["ා", "ක්‍ය", "ෘ", "ෳ", "ැ", "ෑ", "ඃ", "ං"])
left_mod = np.array(["ෙ"])
blank = np.array(["", " ", ""])


from itertools import tee, islice, chain, izip

def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return izip(prevs, items)


def test_position(character_images, classified_text):
    i=0
    for previous_char_img, current_char_img in previous_and_next(character_images):


            # previous_char_img =previous_char_img_.copy()
            # current_char_img = current_char_img.copy()
            # next_char_img = next_char_img.copy()


#             classified_text += str(classifier.classify(current_char_img,0)[0])
# ###################################################################################
#
            index=0

            prv_char =classifier.classify(previous_char_img, 0)
            cnt_char =classifier.classify(current_char_img, 0)
            cv2.imwrite('T/'+str(i)+'pre.jpg',previous_char_img)
            cv2.imwrite('T/'+str(i)+'cur.jpg',current_char_img)

            # print str(prv_char)+" : "+str(cnt_char)
            # ctp += prv_char
            # ctc += str(classifier.classify(current_char_img,0)[0])
            #
            for i in range(0,99):

                # prv_char =classifier.classify(previous_char_img, index)
                # cnt_char =classifier.classify(current_char_img, index)

                # if current is blank
                # prev : right mod, base char, upper mod, lower mod, base-hal, blank
                if blank.__contains__(cnt_char):
                    if (right_mod.__contains__(prv_char) or
                        base_char.__contains__(prv_char) or
                        upper_mod_char.__contains__(prv_char) or
                        lower_mod_char.__contains__(prv_char) or
                        base_hal.__contains__(prv_char) or
                        blank.__contains__(prv_char)):
                        classified_text += cnt_char
                        print "char1:  "+ cnt_char
                        print "1------"
                        break
                    else:
                        index=index+1
                        cnt_char=classifier.classify(current_char_img, index)
                        print "1#########:  "+str(index)+": prv "+prv_char+"      crnt"+cnt_char



                # if current is a base-hal
                # prev : left mod, right mod, base char, upper mod, lower mod, blank
                if base_char.__contains__(cnt_char):
                    if (left_mod.__contains__(prv_char) or
                        right_mod.__contains__(prv_char) or
                        base_char.__contains__(prv_char) or
                        upper_mod_char.__contains__(prv_char) or
                        lower_mod_char.__contains__(prv_char) or
                        blank.__contains__(prv_char)):
                        classified_text += cnt_char
                        print "char1:  "+ cnt_char
                        print "1------"
                        break
                    else:
                        index=index+1
                        cnt_char=classifier.classify(current_char_img, index)
                        print "1#########:  "+str(index)+": prv "+prv_char+"      crnt"+cnt_char

                # if current is a right modifier
                # prev : base char,
                if right_mod.__contains__(cnt_char):
                    if (base_char.__contains__(prv_char)):
                        classified_text += cnt_char
                        print "char2:  "+ cnt_char
                        print "2------"
                        break
                    else:
                        index=index+1
                        cnt_char=classifier.classify(current_char_img, index)
                        print "2#########:  "+str(index)+": prv "+prv_char+"      crnt"+cnt_char

                # if current is a base char
                # prev : left mod, right mod, upper mod, lower mod, blank
                if base_char.__contains__(cnt_char):
                    if (left_mod.__contains__(prv_char) or
                            right_mod.__contains__(prv_char) or
                            upper_mod_char.__contains__(prv_char) or
                            lower_mod_char.__contains__(prv_char) or
                            blank.__contains__(prv_char)):
                        classified_text += cnt_char
                        print "char3:  "+ cnt_char
                        print "3------"
                        break
                    else:
                        index=index+1
                        cnt_char=classifier.classify(current_char_img, index)
                        print "3#########:  "+str(index)+": prv "+prv_char+"      crnt"+cnt_char


                # if current is a left mod
                # prev : right mod, base char, upper mod, lower mod, blank
                if left_mod.__contains__(cnt_char):
                    if (right_mod.__contains__(prv_char) or
                            base_char.__contains__(prv_char) or
                            upper_mod_char.__contains__(prv_char) or
                            lower_mod_char.__contains__(prv_char) or
                            blank.__contains__(prv_char)):
                        classified_text += cnt_char
                        print "char4:  "+ cnt_char
                        print "4------"
                        break
                    else:
                        index=index+1
                        cnt_char=classifier.classify(current_char_img, index)
                        print "4#########:  "+str(index)+": prv "+prv_char+"      crnt"+cnt_char

                # if current is a base
                # prev : right mod, left mod, base char, upper mod, lower mod, blank
                if base_char.__contains__(cnt_char):
                    if (right_mod.__contains__(prv_char) or
                            left_mod.__contains__(prv_char) or
                            base_char.__contains__(prv_char) or
                            upper_mod_char.__contains__(prv_char) or
                            lower_mod_char.__contains__(prv_char) or
                            blank.__contains__(prv_char)):
                        classified_text += cnt_char
                        print "char5:  "+ cnt_char
                        print "5------"
                        break
                    else:
                        index=index+1
                        cnt_char=classifier.classify(current_char_img, index)
                        print "5#########:  "+str(index)+": prv "+prv_char+"      crnt"+cnt_char

                # if current is a upper mod
                # prev : right mod, base char, upper mod, lower mod, blank
                if left_mod.__contains__(cnt_char):
                    if (right_mod.__contains__(prv_char) or
                            base_char.__contains__(prv_char) or
                            upper_mod_char.__contains__(prv_char) or
                            lower_mod_char.__contains__(prv_char) or
                            blank.__contains__(prv_char)):
                        classified_text += cnt_char
                        print "char6:  "+ cnt_char
                        print "6------"
                        break
                    else:
                        index=index+1
                        cnt_char=classifier.classify(current_char_img, index)
                        print "6#########:  "+str(index)+": prv "+prv_char+"      crnt"+cnt_char

                # if current is a lower mod
                # prev : right mod, base char, upper mod, lower mod, blank
                if left_mod.__contains__(cnt_char):
                    if (right_mod.__contains__(prv_char) or
                            base_char.__contains__(prv_char) or
                            upper_mod_char.__contains__(prv_char) or
                            lower_mod_char.__contains__(prv_char) or
                            blank.__contains__(prv_char)):
                        classified_text += cnt_char
                        print "char7:  "+ cnt_char
                        print "7------"
                        break
                    else:
                        index=index+1
                        cnt_char=classifier.classify(current_char_img, index)
                        print "7#########:  "+str(index)+": prv "+prv_char+"      crnt"+cnt_char

                # if (char_pos.blank.__contains__(prv_char) or char_pos.right_mod.__contains__(prv_char))and char_pos.right_mod.__contains__(cnt_char):


                # if current is a left modifier
                    # prev : space or none, base char, right mod, upper mod, lower mod
                # if (char_pos.blank.__contains__(prv_char) or
                #         char_pos.right_mod.__contains__(prv_char) or
                #         char_pos.upper_mod_char.__contains__(prv_char) or
                #         char_pos.lower_mod_char.__contains__(prv_char) or
                #         char_pos.base_char.__contains__(prv_char)) and char_pos.left_mod.__contains__(cnt_char):
                #     print "111111111111111111111"
                #     classified_text += cnt_char
                #     print "char1:  "+ cnt_char
                #     print "1------"
                #     index=0
                #     break
                # else:
                #     index=index+1
                #     cnt_char=classifier.classify(current_char_img, index)
                #     print "1#########:  "+str(index)+": prv "+prv_char+"      crnt"+cnt_char
                #
                #
                # if (char_pos.base_char.__contains__(prv_char)) and char_pos.right_mod.__contains__(cnt_char):
                #     classified_text += cnt_char
                #     print "char2:  "+ cnt_char
                #     print "2------"
                #     index=0
                #     break
                # else:
                #     index=index+1
                #     cnt_char=classifier.classify(current_char_img, index)
                #     print "2#########:  "+str(index)+": prv "+prv_char+"      crnt"+cnt_char
                #
                # # if current is a base char
                #     # prev : left mod, base char, upper mod, lower mod, none/space
                #
                # if prv_char == "None" or cnt_char == "None":
                #     print "break1"
                #     index=0
                #     break
                # if prv_char == "None" or cnt_char == "Space":
                #     print "break2"
                #     index=0
                #     break
                # if prv_char == "Space" or cnt_char == "None":
                #     print "break3"
                #     index=0
                #     break
                # if prv_char == "Space"  or cnt_char == "Space":
                #     print "break4"
                #     index=0
                #     break

    print "classified text : " + classified_text
