# -*- coding: utf-8 -*-
__author__ = 'Amali rathnapriya'

import codecs
import json
import io



def output_function(inputp,outputp):

   # fp= io.open('result.json', 'w',encoding='utf-8')

   final_output=dict(zip(inputp,outputp))


   # for incorrect , correct in final_output.iteritems():
   #    print incorrect ," : " , correct

   dictlist=[]
   for input in inputp:
        for key, value in final_output.iteritems():
            if key==input:

                print key.encode("utf-8")
                print "correctedd"
                print value

                words = []

                if not value:
                    print "G"
                    words.append(key)
                elif isinstance(value, basestring):
                    words.append(value)
                    words.append(key)
                else:
                    value=value[::-1]
                    words.extend(value)
                    words.append(key)

                # temp=",".join(temp)

                print words
                dictlist.append(words)


   return dictlist



