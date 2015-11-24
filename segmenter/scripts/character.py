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
import scipy.ndimage.morphology as m
from scipy import ndimage as ndimage
import numpy as np
import scipy as scipy
from matplotlib import pyplot as plt
import line as line_script
import time

package_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

fig4 = plt.figure()
sub_plots4 = {}

sub_plots4["0"] = fig4.add_subplot(211)
sub_plots4["1"] = fig4.add_subplot(212)
sub_plots4["1"].invert_yaxis()

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

  middle = resized[base_lines_r[0]:base_lines_r[1], 0:cols]

  top = resized[0:base_lines_r[0], 0:cols]
  top_rows, top_cols = top.shape 
  if top_rows < 21:
    top_added = np.zeros((21-top_rows, cols), dtype='uint8')
    top_added.fill(0)
    top = np.concatenate((top_added, top), axis=0)
  elif top_rows > 21:   
    dim = (top_cols, 21)
    top = cv2.resize(top, dim, interpolation = cv2.INTER_NEAREST)    
  #top_rows,top_cols = top.shape  

  bottom = resized[base_lines_r[1]:rows, 0:cols] 
  bottom_rows, bottom_cols = bottom.shape
  if bottom_rows < 21:
    bottom_added = np.zeros((21-bottom_rows, cols), dtype='uint8')
    bottom_added.fill(0)
    bottom = np.concatenate((bottom, bottom_added), axis=0)
  elif bottom_rows > 21:    
    dim = (bottom_cols, 21)
    bottom = cv2.resize(bottom, dim, interpolation = cv2.INTER_NEAREST)   
  #bottom_rows,bottom_cols = bottom.shape  

  # dim_top = (top_cols, top_height)
  # top_resized = cv2.resize(top, dim_top, interpolation = cv2.INTER_NEAREST)

  # dim_bottom = (bottom_cols, bottom_height)
  # bottom_resized = cv2.resize(bottom, dim_bottom, interpolation = cv2.INTER_NEAREST)

  #join 3 segments
  resized_1 = np.concatenate((top, middle), axis=0)
  resized_2 = np.concatenate((resized_1, bottom), axis=0)  
  
  # rows,cols = character.shape  
  # ver_hist = [0]*rows
  # hor_hist = [0]*cols
  return resized_2

def char_base_line_points(character, ver_hist, boundary_lines, l_boundary_lines, l_base_lines, category, code):
  base_lines = l_base_lines[:]
  
  character_base_height = l_base_lines[1] - l_base_lines[0]

  rows,cols = character.shape 
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
  
        
  # contours, hierarchy = cv2.findContours(top_,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
  # print len(contours)
  # if len(contours) > 1:          
  #   #resized_characters.extend(character_script.seg_overlapping_char(cropped_character_, l_base_lines, l_boundary_lines, str(line_no)+'_'+str(i)+'_'+str(j)))
  #   print "hori"
  # else:
  

  #top = character
  character_ = character.copy()
  character__ = character.copy()
  

  contours, hierarchy = cv2.findContours(character_,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
  no_of_contours = len(contours)
  contour_data = []
  
  if len(contours) > 1:
    for contour in contours:
      left,top,width,height = cv2.boundingRect(contour)      
      if width > 10 or height > 10:
        contour_data.append([top, top+height])
        no_of_contours += 1

  contour_data = sorted(contour_data, key=lambda x: x[0])     
  if len(contour_data) > 1:
    print "horizontal group"
    #if top
    if contour_data[0][0] < base_lines[0]:
      base_lines[0] = contour_data[1][0]
      if contour_data[1][0] < base_lines[1]:
        base_lines[1] = contour_data[1][1]
      else:
        if boundary_lines[1] < (base_lines[1] + character_base_height*0.5):
          base_lines[1] = boundary_lines[1] 
    elif contour_data[0][1] > base_lines[0]:
      base_lines[0] = contour_data[0][0]
      base_lines[1] = contour_data[0][1]      
  else:    
    if boundary_lines[0] > (base_lines[0] - character_base_height*0.5):    
      base_lines[0] = boundary_lines[0]
    if boundary_lines[1] < (base_lines[1] + character_base_height*0.5):
      base_lines[1] = boundary_lines[1] 

  

  # top = character__[0:base_lines[0], 0:cols]
  # lines = cv2.HoughLinesP(top, 2, np.pi/180, 50, minLineLength = int(character_base_height*0.5), maxLineGap = 0)
  # if lines is not None:
  #   angles = np.empty([0])
  #   for x1,y1,x2,y2 in lines[0]:        
  #     cv2.line(character__,(x1,y1),(x2,y2),(0,255,0),1)

  #     (dx, dy) = (x2-x1, y2-y1)
  #     # Compute the angle
  #     if dy != 0:
  #       angle_ = math.atan(float(dx)/float(dy))
  #     else:
  #       angle_ = 0
  #     # The_ angle is in radians (-pi/2 to +pi/2).  If you want degrees, you need the following line
  #     angle_ *= 180/math.pi
  #     # Now you have an angle from -90 to +90.  But if the player is below the turret,
  #     # you want to flip it
  #     if dy < 0:
  #        angle_ += 180
  #     if angle_ != 0:
  #       angle_ = 90 - angle_
  #     angles = np.append(angles, angle_)
  #     print angle_
  #   angle = np.mean(angles)
  # cv2.imwrite(package_directory+'/'+category+'/'+code+'_l.jpg',character__)


  return base_lines

def detect_verticle_regions(character, l_base_lines, l_boundary_lines, category, code):
  rows,cols = character.shape  
  ver_hist = [0]*rows
  hor_hist = [0]*cols

  for y in xrange(rows):
    for x in xrange(cols):
      if character[y,x] == 255:
          ver_hist[y] += 1

  #character = character[boundary_lines[0]:boundary_lines[1], 0:cols] 

  #del ver_hist[-(rows-boundary_lines[1]+1):]
  #del ver_hist[boundary_lines[0]:]

  # for x in xrange(cols):
  #     for y in xrange(rows):
  #       if character[y,x] == 255:
  #           hor_hist[x] += 1
  
  boundary_lines = line_script.get_boundary_line_points(ver_hist)
  boundary_lines_diff = boundary_lines[1] - boundary_lines[0]

  base_lines = char_base_line_points(character, ver_hist, boundary_lines, l_boundary_lines, l_base_lines, category, code)
  
  character = resize(character, base_lines)
  
  return character, base_lines
  #raise Exception('I know Python!') 

def seg_single_char(character, l_base_lines, l_boundary_lines, category, code):
   

  resized_character, region_coordinates = detect_verticle_regions(character, l_base_lines, l_boundary_lines, category, code)
  rows,cols = character.shape 

  character_ = character.copy()
  cv2.bitwise_not(character, character_)

  character_ = cv2.cvtColor(character_,cv2.COLOR_GRAY2RGB)     
  cv2.line(character_,(0, region_coordinates[0]),(rows, region_coordinates[0]),(255,0,0),1)
  cv2.line(character_,(0, region_coordinates[1]),(rows, region_coordinates[1]),(255,0,0),1)

  cv2.imwrite(package_directory+'/'+category+'/'+code+'.jpg',character_) 
  cv2.imwrite(package_directory+'/'+category+'/'+code+'_r.jpg',resized_character)        
  
  return resized_character

def seg_overlapping_char(character, l_base_lines, l_boundary_lines, code):
  print "overlapping_character"

  rows,cols = character.shape

  # character_ = character.copy()

  # cv2.bitwise_not(character, character_)

  contours, hierarchy = cv2.findContours(character,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)

  contours_hierarchy = []

  #print hierarchy

  for l in range(len(hierarchy[0])):
    left,top,width,height = cv2.boundingRect(contours[l])
    #hprint str(left)+"-"+str(top)+"-"+str(width)+"-"+str(height)
    if hierarchy[0][l][3] == -1:
      contours_hierarchy.append([l])
    elif hierarchy[0][l][3] != -1:
      index = len(contours_hierarchy) - 1
      contours_hierarchy[index].append(l)

  #contours_hierarchy_det = []
  contour_groups = []
  for k in range(len(contours_hierarchy)):   
    merged_points  = np.empty(shape=[0, 1, 2], dtype='uint8')    
    merged_points_list = []

    for p in range(len(contours_hierarchy[k])):
      merged_points = np.append(merged_points, contours[contours_hierarchy[k][p]], 0)
      merged_points_list.append(contours[contours_hierarchy[k][p]])
    
    left,top,width,height = cv2.boundingRect(merged_points)
    right = left + width
    bottom = top + height
    # remove small objects
    if width > 3:
      contour_groups.append([left,top,right,bottom, merged_points_list])
  

  #re-order contour groups according their starting point
  contour_groups = sorted(contour_groups, key=lambda x: x[0])

  horizontal_groups = []

  already_included = []
  for k in range(len(contour_groups)): 
    if k not in already_included:
      for l in range(len(contour_groups)):
        if l not in already_included :          
          if l == k:
            horizontal_groups.append([contour_groups[l]])
          #detect contour groups belongs to same horizontal character
          elif (horizontal_groups[-1][0][2])*0.8 > contour_groups[l][0]:
            horizontal_groups[-1].append(contour_groups[l])
          else:
            horizontal_groups.append([contour_groups[l]])
          already_included.append(l)  
 
  resized_characters = []    

  for k in range(len(horizontal_groups)):    
    empty_image = np.zeros((rows,cols,1), np.uint8)
    empty_image = cv2.threshold(empty_image, 127, 255, cv2.THRESH_BINARY)[1]
    
    merged_points_list = []

    for l in range(len(horizontal_groups[k])):
      merged_points_list.extend(horizontal_groups[k][l][4])
   
    left = min([int(l[0]) for l in horizontal_groups[k]])  
    right = max([int(l[2]) for l in horizontal_groups[k]])
    # top = min([int(l[1]) for l in horizontal_groups[k]])
    # bottom = min([int(l[3]) for l in horizontal_groups[k]])

    cv2.drawContours(empty_image ,merged_points_list, -1, 255, -1)

    empty_image = empty_image[0:rows, left:right]
    # empty_image_ = empty_image.copy()
    # cv2.bitwise_not(empty_image, empty_image_)
    
    character = seg_single_char(empty_image, l_base_lines, l_boundary_lines, "overlapping_characters", code+'_'+str(k))

    resized_characters.append(character)

  return resized_characters    

def seg_touching_char(character, l_base_lines, l_boundary_lines, code):  
  print "touching_character"  

  rows,cols = character.shape 
  
  print rows
  print cols

  from_top = np.zeros(cols)
  for x in range(cols):   
    for y in range(0, int(rows)):
      if character[y,x] == 255:
        from_top[x] = y
        break

  from_bottom = np.zeros(cols)
  for x in range(cols):   
    for y in list(reversed(range(int(0),rows))):
      #print y
      if character[y,x] == 255:
        from_bottom[x] = y
        break

  sub_plots4["0"].imshow(character, cmap='gray')
  

  sub_plots4["1"].plot(from_top)  
  sub_plots4["1"].plot(from_bottom)
  

  # idx = np.argwhere(np.isclose(f, g, atol=10)).reshape(-1)
  # plt.plot(x[idx], f[idx], 'ro')
  graph_intersections = np.isclose(from_top, from_bottom, atol=5)

  intersections = []
  intersection_marker = False
  for i, value in enumerate(graph_intersections):
    if i > cols*0.1 and i < cols*0.9:
      if value == True:
        if intersection_marker == False:
          intersections.append([i])
        else:
          intersections[-1].append(i)
      intersection_marker = value
  print intersections

  for intersection in intersections:
    
    if len(intersection) >= 3:
      from_bottom_ = from_bottom[intersection[0]-len(intersection):intersection[-1]+len(intersection)]

      local_maxima_indexes = argrelextrema(np.asarray(from_bottom_), np.greater_equal)[0]
      print local_maxima_indexes
  #intersections_ = sum(intersections, [])
  
  #sub_plots4["1"].plot(intersections_)
  #sub_plots4["2"].plot(from_bottom)
  #print combined
  #   
  # cv2.waitKey(0)

  fig4.savefig(package_directory+'/figures/touching'+code+'.jpg')
  
  sub_plots4["0"].clear()
  sub_plots4["1"].clear()
  #sub_plots4["2"].clear()
  #fig4.close()
  #seg_single_char(character, l_base_lines, l_boundary_lines, "touching_characters", code)
  #cv2.imwrite(package_directory+'/touching_characters/'+str(i)+'_'+str(j)+'_'+str(1)+'.jpg', character)
 

