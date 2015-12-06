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
                print "correctedd"
                print value
                if value != "":
                    temp = [value, key]
                else:
                    temp=[key]
                # temp=",".join(temp)
                dictlist.append(temp)


   return dictlist



