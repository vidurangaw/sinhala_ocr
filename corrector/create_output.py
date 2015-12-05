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
   for key, value in final_output.iteritems():
        temp = [value, key]
        #temp="".join(temp)
        dictlist.append(temp)

   # for item in dictlist:
   #     print(" , ".join(item))
   #
   # print dictlist


   # fp.write(s.encode('utf-8'))

   return dictlist



# def main():
#
#     inputp=u"තන්විධනය දෙඉශක"
#     outputp=[u"සංවිධානය",[u"දේශන ,දේශය"]]
#     output_function(inputp,outputp)
#
# main()