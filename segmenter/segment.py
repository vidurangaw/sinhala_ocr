#__all__ = ['segment', 'preprocess']
import cv2
import bisect
from scipy.interpolate import interpolate
from scipy.interpolate import spline
from sklearn.cluster import MeanShift, estimate_bandwidth
import Image
import sys
from scipy import signal
from scipy.signal import argrelextrema
from scipy.signal import savgol_filter
# from skimage import morphology
import math
import itertools
from PIL import Image, ImageDraw
import glob
import os
from collections import OrderedDict

import scipy.ndimage.morphology as m
from scipy import ndimage as ndimage
import numpy as np
import scipy as scipy
from matplotlib import pyplot as plt

def delete_images(folder):     
  files = glob.glob(os.getcwd() + "/segmenter/" + folder + '/*')
  for filename in files:
      os.unlink(filename)

def l_get_base_line_points(ver_hist):
  max_value_index = ver_hist.index(max(ver_hist))

  #FIXME consider 
  local_maxima_indexes = argrelextrema(np.asarray(ver_hist), np.greater_equal)[0]

  
  #print local_maxima_indexes
 
  maximas_remove_count = len(local_maxima_indexes)*20/100
  local_maxima_indexes = local_maxima_indexes[maximas_remove_count:]  

  if maximas_remove_count > 0:
    local_maxima_indexes = local_maxima_indexes[:-maximas_remove_count]


  #print local_maxima_indexes
 
  local_maxima_indexes_ = []
  for local_maxima_index in local_maxima_indexes: 
    if ver_hist[local_maxima_index] > ver_hist[max_value_index]*0.5:    
      local_maxima_indexes_.append(local_maxima_index)
      
  
  #print local_maxima_indexes_

  max_distance = []
  max_distance.append(math.fabs(local_maxima_indexes_[0] - local_maxima_indexes_[1]))
  max_distance.append(local_maxima_indexes_[0])
  max_distance.append(local_maxima_indexes_[1])  

  for p1, p2 in itertools.combinations(local_maxima_indexes_, 2):        
    if abs(p1 - p2) > max_distance[0]:
      max_distance[0] = abs(p1 - p2)
      max_distance[1] = p1
      max_distance[2] = p2
  
  
  max_distance.pop(0)
  max_distance.sort()

  return max_distance

def c_get_base_line_points(ver_hist, boundary_lines, l_boundary_lines, l_base_lines):
  base_lines = l_base_lines[:]
  
  character_base_height = l_base_lines[1] - l_base_lines[0]
  # max_value_index = ver_hist.index(max(ver_hist))


  # local_maxima_indexes = argrelextrema(np.asarray(ver_hist), np.greater_equal)[0]

  

  # maximas_remove_count = len(local_maxima_indexes)*25/100
  # local_maxima_indexes = local_maxima_indexes[maximas_remove_count:]
  # local_maxima_indexes = local_maxima_indexes[:-maximas_remove_count]


  # #for i, v in enumerate(local_maximas): 
  # local_maxima_indexes_ = []
  # for local_maxima_index in local_maxima_indexes: 
  #   if ver_hist[local_maxima_index] > ver_hist[max_value_index]*0.5:    
  #     local_maxima_indexes_.append(local_maxima_index)     
       

  # max_distance = [0, 0, l_base_line_diff/2] 
  
  # # compare pairs for the optimum pair
  # for p1, p2 in itertools.combinations(local_maxima_indexes_, 2):        
  #   if abs(p1 - p2) > max_distance[2] and abs(p1 - p2) < l_base_line_diff*1.75:
  #     max_distance[0] = p1
  #     max_distance[1] = p2
  #     max_distance[2] = abs(p1 - p2)      

  #print boundary_lines
  #print max_distance

  # if boundary_lines[0] > 0.8*max_distance[0]:
  #   max_distance[0] = boundary_lines[0]   

  #19 36
  #print boundary_lines[0]
  #print "----"
  
  if boundary_lines[1] < (base_lines[1] + character_base_height*0.5):
    base_lines[1] = boundary_lines[1]   

  if boundary_lines[0] > (base_lines[0] - character_base_height*0.5):    
    base_lines[0] = boundary_lines[0]

  #print base_lines[0]

  return base_lines

def get_boundary_line_points(ver_hist):  
  top_line = np.nonzero(ver_hist)[0][0]
  bottom_line = len(ver_hist) - np.nonzero(ver_hist[::-1])[0][0]  
  return top_line, bottom_line

def calc_avg_char_width(character_widths):
  #http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans
  X = np.array(zip(character_widths,np.zeros(len(character_widths))), dtype=np.int)
  bandwidth = estimate_bandwidth(X, quantile=0.5)
  ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
  ms.fit(X)
  cluster_centers = ms.cluster_centers_
  # labels = ms.labels_
  # labels_unique = np.unique(labels)
  # n_clusters_ = len(labels_unique)

  # for k in range(n_clusters_):
  #     my_members = labels == k
  #     print "cluster {0}: {1}".format(k, X[my_members, 0])

  return cluster_centers[0][0]  

def resize(character, base_lines):
  rows,cols = character.shape 
  base_line_height = base_lines[1] - base_lines[0]
  top_height = 21
  bottom_height = 21

  #print base_line_height

  height_resize_ratio = 22 /float(base_line_height)    
  new_height = rows*height_resize_ratio  

  r = float(new_height) / rows
  dim = (int(cols * r), int(new_height))
  resized = cv2.resize(character, dim, interpolation = cv2.INTER_NEAREST)
  rows,cols = resized.shape

  #update baseline margins
  base_lines_r = [0,0]
  base_lines_r[0] = int(math.floor(base_lines[0]*height_resize_ratio)) 
  base_lines_r[1] = int(math.ceil(base_lines[1]*height_resize_ratio))

  top = resized[0:base_lines_r[0], 0:cols]
  top_rows,top_cols = top.shape

  middle = resized[base_lines_r[0]:base_lines_r[1], 0:cols]

  bottom = resized[base_lines_r[1]:rows, 0:cols] 
  bottom_rows,bottom_cols = bottom.shape

  dim_top = (top_cols, top_height)
  top_resized = cv2.resize(top, dim_top, interpolation = cv2.INTER_NEAREST)

  dim_bottom = (bottom_cols, bottom_height)
  bottom_resized = cv2.resize(bottom, dim_bottom, interpolation = cv2.INTER_NEAREST)

  #join 3 segments
  resized_1 = np.concatenate((top_resized, middle), axis=0)
  resized_2 = np.concatenate((resized_1, bottom_resized), axis=0)  
  
  # rows,cols = character.shape  
  # ver_hist = [0]*rows
  # hor_hist = [0]*cols
  return resized_2

def detect_verticle_regions(character, l_base_lines, l_boundary_lines):
  rows,cols = character.shape  
  ver_hist = [0]*rows
  hor_hist = [0]*cols

  for y in xrange(rows):
      for x in xrange(cols):
        if character[y,x] == 0:
            ver_hist[y] += 1

  for x in xrange(cols):
      for y in xrange(rows):
        if character[y,x] == 0:
            hor_hist[x] += 1
  
  boundary_lines = get_boundary_line_points(ver_hist)
  boundary_lines_diff = boundary_lines[1] - boundary_lines[0]

  base_lines = c_get_base_line_points(ver_hist, boundary_lines, l_boundary_lines, l_base_lines)
  base_line_diff = base_lines[1] - base_lines[0]

  #character = character
  character = resize(character, base_lines)
  
  return character, base_lines
  #raise Exception('I know Python!') 

def seg_touching_char(character, i, j):
  cv2.imwrite('segmenter/touching_characters/'+str(i)+'_'+str(j)+'_'+str(1)+'.jpg', character)
  print "touching_character"

def seg_single_char(character, i, j):
  return character

def seg_overlapping_char(character, i, j):
  print "overlapping_character"

  rows,cols = character.shape

  character_ = character.copy()

  cv2.bitwise_not(character, character_)

  contours, hierarchy = cv2.findContours(character_,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)

  contours_hierarchy = []

  #print hierarchy

  for l in range(len(hierarchy[0])):
    if hierarchy[0][l][3] == -1:
      contours_hierarchy.append([l])
    if hierarchy[0][l][3] != -1:
      index = len(contours_hierarchy) - 1
      contours_hierarchy[index].append(l)

  contours_hierarchy_det = []

  for k in range(len(contours_hierarchy)):
    left,top,width,height = cv2.boundingRect(contours[contours_hierarchy[k][0]])
    
    # remove small objects
    #if width > cols*0.2:
    contours_hierarchy_det.append([left,width, contours_hierarchy[k]])
  

  #re-order contour groups according their starting point
  contours_hierarchy_det = sorted(contours_hierarchy_det, key=lambda x: x[0])

  #merge contour groups
  contours_hierarchy_merged = []
  for m in range(len(contours_hierarchy_det)):
    if len(contours_hierarchy_merged) > 0 and contours_hierarchy_merged[-1][0]+contours_hierarchy_merged[-1][1]*0.5 > contours_hierarchy_det[m][0]:
      left,top,width,height = cv2.boundingRect(contours[contours_hierarchy_det[m][2][0]])
      contours_hierarchy_merged.append([min(contours_hierarchy_det[m][0],contours_hierarchy_merged[-1][0]),max(contours_hierarchy_det[m][1],contours_hierarchy_merged[-1][1]),contours_hierarchy_det[m][2]+contours_hierarchy_merged[-1][2],contours_hierarchy_merged[-1][3]+[top]])
      del contours_hierarchy_merged[-2]            
    else:
      left,top,width,height = cv2.boundingRect(contours[contours_hierarchy_det[m][2][0]])
      contours_hierarchy_merged.append(contours_hierarchy_det[m]+[[top]])
      
      #print contours_hierarchy_merged[-1]
  
  

  for k in range(len(contours_hierarchy_merged)):    
    empty_image = np.zeros((rows,cols,1), np.uint8)
    empty_image = cv2.threshold(empty_image, 127, 255, cv2.THRESH_BINARY)[1]
    
    # merge multiple contours in a group
    character_contours = list(contours[m] for m in contours_hierarchy_merged[k][2])
  
    left = contours_hierarchy_merged[k][0]
    width = contours_hierarchy_merged[k][1]

    #print "left" + str(left)

    cv2.drawContours(empty_image ,character_contours, -1, 255, -1)

    #rows,cols = empty_image.shape  
    # hor_hist = [0]*cols

    # for x in xrange(cols):
    #     for y in xrange(rows):
    #       if empty_image[y,x] == 255:
    #           hor_hist[x] += 1
    # left_boundary = np.nonzero(hor_hist)[0][0]
    # right_boundary = len(hor_hist) - np.nonzero(hor_hist[::-1])[0][0]  
    # character_width = right_boundary - left_boundary 
    
    #if width  > cols*0.2:    

    cv2.bitwise_not(empty_image, empty_image)

    cropped_character = empty_image[0:rows, left:left+width]

    cv2.imwrite('overlapping_characters/'+str(i)+'_'+str(j)+'_'+str(k)+'.jpg', cropped_character)

# fig0 = plt.figure()
# sub_plots0 = {}

# sub_plots0["0"] = fig0.add_subplot(511)
# sub_plots0["1"] = fig0.add_subplot(512)
# sub_plots0["2"] = fig0.add_subplot(513)
# sub_plots0["3"] = fig0.add_subplot(514)
# sub_plots0["4"] = fig0.add_subplot(515)

# fig1 = plt.figure()
# sub_plots1 = {}

# sub_plots1["0"] = fig1.add_subplot(511)
# sub_plots1["1"] = fig1.add_subplot(512)
# sub_plots1["2"] = fig1.add_subplot(513)
# sub_plots1["3"] = fig1.add_subplot(514)
# sub_plots1["4"] = fig1.add_subplot(515)

# fig2 = plt.figure()
# sub_plots2 = {}

# sub_plots2["0"] = fig2.add_subplot(211)
# sub_plots2["1"] = fig2.add_subplot(212)


# fig3 = plt.figure()
# sub_plots3 = {}

# sub_plots3["0"] = fig3.add_subplot(311)
# sub_plots3["1"] = fig3.add_subplot(312)
# sub_plots3["2"] = fig3.add_subplot(313)
# def reject_outliers(data, m=2):
#     return data[abs(data - np.mean(data)) < m * np.std(data)]
def preprocess(image):
  gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
  clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8,8))
  gray_equalized = clahe.apply(gray)

  gray_smoothed = cv2.fastNlMeansDenoising(gray_equalized,None,15,7,21)

  #gray_smoothed = cv2.medianBlur(gray_smoothed,2)
  #ret3,bw = cv2.threshold(gray_smoothed,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
  bw = cv2.threshold(gray_smoothed, 127, 255, cv2.THRESH_BINARY)[1]
  

  #bw__ = cv2.adaptiveThreshold(bw,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
  

  bw_ = bw.copy()
  cv2.bitwise_not(bw, bw_) 

  rows,cols = bw_.shape

  #### ---Fix skew angle--- #####

  #edges = cv2.Canny(gray_smoothed, 50, 150, apertureSize = 3)
  lines = cv2.HoughLinesP(bw_, 2, np.pi/180, 200, minLineLength = int(cols*0.2), maxLineGap = 200)[0]
  no_of_lines = len(lines)

  angles = np.empty([0])
  for x1,y1,x2,y2 in lines:        
    cv2.line(image,(x1,y1),(x2,y2),(0,255,0),1)

    (dx, dy) = (x2-x1, y2-y1)
    # Compute the angle
    if dy != 0:
      angle_ = math.atan(float(dx)/float(dy))
    else:
      angle_ = 0
    # The_ angle is in radians (-pi/2 to +pi/2).  If you want degrees, you need the following line
    angle_ *= 180/math.pi
    # Now you have an angle from -90 to +90.  But if the player is below the turret,
    # you want to flip it
    if dy < 0:
       angle_ += 180
    if angle_ != 0:
      angle_ = 90 - angle_
    angles = np.append(angles, angle_)

  #print angles
  #remove outliers from a angle list
  angles = angles[abs(angles - np.mean(angles)) < 2 * np.std(angles)]
  if angles.size > 0:
    rotation_angle = np.mean(angles)
  else:
    rotation_angle = 0
  #print angles 
  #get mean of angle list
  
  print "doc rotation angle : "+ str(rotation_angle)

  #### ------ #####


  # points = np.empty([0])
  # for contour in contours:
  #   if cv2.contourArea(contour) > 25:
  #     points = np.append(points, contour.flatten())


  
  # points = np.reshape(points, (len(points)/2, 2)).astype('float32')

  # rect = cv2.minAreaRect(points)

  # print rect[2] 
  # box_coords = cv2.cv.BoxPoints(rect)
  
  # box_coords = np.int0(box_coords)
  # cv2.drawContours(image,[box_coords],0,(0,255,0),1)

  # box_coords_ = []

  # x_coords = OrderedDict()
  # y_coords = OrderedDict()



  # for i, point in enumerate(box_coords):
  #   x_coords[point[0]] = i;
  #   y_coords[point[1]] = i;

  # x_coords = OrderedDict(sorted(x_coords.iteritems(), key=lambda t: t[0]))
  # y_coords = OrderedDict(sorted(y_coords.iteritems(), key=lambda t: t[0]))


  # lowest_x = box_coords[x_coords.items()[0][1]]
  # second_lowest_x = box_coords[x_coords.items()[1][1]]

  # highest_x = box_coords[x_coords.items()[3][1]]
  # second_highest_x = box_coords[x_coords.items()[2][1]]
  

  # if lowest_x[1] < second_lowest_x[1]:
  #   box_coords_.append(lowest_x[0])
  #   box_coords_.append(lowest_x[1])
  # else:
  #   box_coords_.append(second_lowest_x[0])
  #   box_coords_.append(second_lowest_x[1])

  # if highest_x[1] > second_highest_x[1]:
  #   box_coords_.append(highest_x[0])
  #   box_coords_.append(highest_x[1])
  # else:
  #   box_coords_.append(second_highest_x[0])
  #   box_coords_.append(second_highest_x[1])

  # print box_coords_
  


  #Rotate the image  
  (h, w) = bw.shape[:2]
  center = (w / 2, h / 2)
  M = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
  rotated = cv2.warpAffine(bw_, M, (w, h))
  rotated_gray = cv2.warpAffine(gray_smoothed, M, (w, h))





  # fig1 = plt.figure()
  # sub_plots1 = {}

  # sub_plots1["0"] = fig1.add_subplot(311)
  # sub_plots1["1"] = fig1.add_subplot(312)
  # sub_plots1["2"] = fig1.add_subplot(313)
  
  # sub_plots1["0"].imshow(gray_smoothed, cmap='gray',vmin=0,vmax=255)
  # sub_plots1["1"].imshow(image, cmap='gray',vmin=0,vmax=255)
  # sub_plots1["2"].imshow(rotated, cmap='gray',vmin=0,vmax=255)
  

  # plt.show()
  # cv2.waitKey(0)

  return rotated, rotated_gray

def segment(bw_):

  bw = bw_.copy()
  cv2.bitwise_not(bw_, bw) 

  fig4 = plt.figure()
  sub_plots4 = {}

  sub_plots4["0"] = fig4.add_subplot(411)
  sub_plots4["1"] = fig4.add_subplot(412)
  sub_plots4["2"] = fig4.add_subplot(413)
  sub_plots4["3"] = fig4.add_subplot(414)

  # fig5 = plt.figure()
  # sub_plots5 = {}

  # sub_plots5["0"] = fig5.add_subplot(511)
  # sub_plots5["1"] = fig5.add_subplot(512)
  # sub_plots5["2"] = fig5.add_subplot(513)
  # sub_plots5["3"] = fig5.add_subplot(514)
  # sub_plots5["4"] = fig5.add_subplot(515)
  delete_images('overlapping_characters')
  delete_images('single_characters')
  delete_images('touching_characters')

  rows, cols = bw.shape

  # th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
  #             cv2.THRESH_BINARY,11,25)
  #thresh = cv2.dilate(thresh,None,iterations = 3)
  #thresh = cv2.erode(thresh,None,iterations = 2)

  #edges = cv2.Canny(im_bw,50,150,apertureSize = 3)
  sub_plots4["0"].imshow(bw, cmap='gray',vmin=0,vmax=255)


  ver_hist = [0]*rows

  for y in xrange(rows):
      for x in xrange(cols):
      	if bw[y,x] == 0:
          	ver_hist[y] += 1


  #print ver_hist
  
  l_base_lines = l_get_base_line_points(ver_hist)
  l_base_line_diff = l_base_lines[1] - l_base_lines[0]

  l_boundary_lines = get_boundary_line_points(ver_hist)
  l_boundary_lines_diff = l_boundary_lines[1] - l_boundary_lines[0]


  sub_plots4["0"].hlines(y=l_base_lines[0], xmin=0, xmax=cols, linewidth=2, color = 'b')
  sub_plots4["0"].hlines(y=l_base_lines[1], xmin=0, xmax=cols, linewidth=2, color = 'b')



  hor_hist = [0]*cols

  for x in xrange(cols):
      for y in xrange(rows):
        if bw[y,x] == 0:
            hor_hist[x] += 1

  # sub_plots4["1"].plot(ver_hist)

  sub_plots4["1"].plot(hor_hist)
  sub_plots4["1"].set_xlim([0,cols-1])



  words = []
  characters = np.zeros(shape=(0,2))
  character_widths = []
  touching_characters = np.zeros(shape=(0,3))
  current_segment_start = 0;
  current_segment_end = 0;


  for i in range(len(hor_hist)):
    if hor_hist[i] != 0:
      if current_segment_start == 0:     
        current_segment_start = i
      if hor_hist[i-1] == 0:      
        current_segment_start = i
        if len(characters) > 1 :
          if (i - current_segment_end) > l_base_line_diff*2:         
            words.append(characters)
            characters = np.zeros(shape=(0,2))
    else:    
      if current_segment_start != 0:
        if hor_hist[i-1] != 0:
          current_segment_end = i;
          characters = np.append(characters,[[current_segment_start, i]], axis=0)
          character_widths.append(i-current_segment_start)


  words.append(characters)

  average_char_width = calc_avg_char_width(character_widths)
  #print average_char_width


  resized_characters = []
    

  for i in range(len(words)):
    resized_characters.append(np.array([0]))
    for j in range(len(words[i])):
      character_width = words[i][j][1] - words[i][j][0]
      cropped_character = bw[0:int(rows), int(words[i][j][0]):int(words[i][j][1])]
      if average_char_width*170/100 > character_width and average_char_width*10/100 < character_width:      
        print "single"


        
        cropped_character = seg_single_char(cropped_character, i, j)


        resized_character, region_coordinates = detect_verticle_regions(cropped_character, l_base_lines, l_boundary_lines)
        rows,cols = cropped_character.shape 

        cropped_character = cv2.cvtColor(cropped_character,cv2.COLOR_GRAY2RGB)

           
        cv2.line(cropped_character,(0, region_coordinates[0]),(rows, region_coordinates[0]),(255,0,0),1)
        cv2.line(cropped_character,(0, region_coordinates[1]),(rows, region_coordinates[1]),(255,0,0),1)

        # perform resizing of the image 
        # r = 200.0 / rows
        # dim = (int(cols * r), 200)             
        # cropped_character = cv2.resize(cropped_character, dim, interpolation = cv2.INTER_AREA)
        
        resized_characters.append(resized_character)
        cv2.imwrite('segmenter/single_characters/'+str(i)+'_'+str(j)+'.jpg',cropped_character) 
        cv2.imwrite('segmenter/single_characters/'+str(i)+'_'+str(j)+'_r.jpg',resized_character)        
        
      else:       
        rows,cols = cropped_character.shape
        
        cropped_character_ = cropped_character.copy()
        cv2.bitwise_not(cropped_character, cropped_character_)     
        cropped_character__ = cropped_character_.copy()
        contours, hierarchy = cv2.findContours(cropped_character_,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

        if len(contours) > 1:
          seg_overlapping_char(cropped_character, i, j)
        else:
          seg_touching_char(cropped_character, i, j)
        


        

        #sub_plots4["3"].imshow(cropped_character__, cmap='gray',vmin=0,vmax=255)
        

  return resized_characters      

  #sub_plots4["3"].imshow(crop_img, cmap='gray',vmin=0,vmax=255)
  plt.show()
  cv2.waitKey(0)