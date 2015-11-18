__author__ = 'Naleen'

import numpy as np

from ..mapper import character_mapper as char_map

# import mapper.feature_mapper

# def sort_probs(zone_list):
#         prob_list = zone_list[0]
#         label_list = zone_list[1]
#
#         prob_array = []
#         for i in range(0, len(prob_list)):
#             prob_array.append(round(float(prob_list[i]),4))
#             # print i
#
#         joint_array = np.dstack((np.array(label_list), np.array(prob_array)))
#
#         # take the first 10 value of the sorted [label, probability] list
#         return joint_array[0][joint_array[0][:, 1].argsort()[::-1]][:]
#
#
# def probability_match(lower, middle, upper):
#
#
#     lower_arr = sort_probs(lower)
#     middle_arr = sort_probs(middle)
#     upper_arr = sort_probs(upper)
#     print "middle"+str(middle_arr)
#     print "upper"+str(upper_arr)
#     print "lower"+str(lower_arr)
#     # vhj = np.delete(lower_arr, 0, axis=0)
#     # print vhj
#     # for i in range(len(middle_arr)):
#     char=''
#     for i in range(10):
#         if char_mapper1.char_map(lower_arr[i][0], middle_arr[i][0],upper_arr[i][0]) is not None:
#             char = char_mapper1.char_map(lower_arr[i][0], middle_arr[i][0],upper_arr[i][0])
#
#             # print "lower  "+str(lower_arr[i][0])
#             # print "upper  "+str(upper_arr[i][0])
#             # print "middl  "+str(middle_arr[i][0])
#             print char
#             return char
#         else:
#             if lower_arr[i][1]<middle_arr[i][1] and lower_arr[i][1]<upper_arr[i][1]:
#                 lower_arr[i][1]
#                 np.delete(lower_arr, 0, axis=0)
#             elif  middle_arr[i][1]<upper_arr[i][1] and middle_arr[i][1]<lower_arr[i][1]:
#                 middle_arr[i][1]
#                 np.delete(middle_arr, 0, axis=0)
#             else:
#                 upper_arr[i][1]
#                 np.delete(upper_arr, 0, axis=0)
#
#
#
#         # np.delete(lower_arr, 0, axis=0)
#
#
#




#############################################################
def sort_probs(zone_list):
        prob_list = zone_list[0]
        label_list = zone_list[1]

        prob_array = []
        for i in range(0, len(prob_list)):
            prob_array.append(round(float(prob_list[i]),4))
            # print i

        joint_array = np.dstack((np.array(label_list), np.array(prob_array)))
        # print joint_array
        # take the first 10 value of the sorted [label, probability] list
        return joint_array[0][joint_array[0][:, 1].argsort()[::-1]][:]

def probability_match(lower, middle, upper):

    lower_arr = sort_probs(lower)
    middle_arr = sort_probs(middle)
    upper_arr = sort_probs(upper)
    # print middle_arr
    # for i in range(1, len(lower_arr)):
    arr=[]
    i=0
    j=0
    k=0
    for i in range(0, len(lower_arr)):
        for j in range(0, len(middle_arr)):
            for k in range(0, len(upper_arr)):
                list_arr=[]
                # print np.float64(lower_arr[:,1][i])
                cumulative_prob = float(lower_arr[:,1][i])*float(middle_arr[:,1][j])*float(upper_arr[:,1][k])
                list_arr.append(round(float(cumulative_prob),4))

                list_arr.append(lower_arr[:, 0][i])
                list_arr.append(middle_arr[:, 0][j])
                list_arr.append(upper_arr[:, 0][k])

                arr.append(list_arr)
                # arr.append(cumulative_prob)

    numpy_arr=np.array(arr)
    # print numpy_arr

    sorted_numpy= numpy_arr[numpy_arr[:,0].argsort()[::-1]]
    # print sorted_numpy
    m=0
    for m in range(0, len(sorted_numpy)):
        # print sorted_numpy[1][1]
        char =char_map.char_map(sorted_numpy[m][1], sorted_numpy[m][2],sorted_numpy[m][3])

        # print sorted_numpy[1][1], sorted_numpy[1][2],sorted_numpy[1][3]
        if char != None:
             return char, sorted_numpy[m][1], sorted_numpy[m][2],sorted_numpy[m][3]

        # else:
        #     break
        # break

    #
    # char = 0
    # return char
