#__all__ = ['segment', 'preprocess']
import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interpolate
from scipy import ndimage as ndimage
from scipy import signal
import matplotlib.ticker as ticker
import matplotlib.ticker as plticker
from scipy.signal import argrelextrema
import glob
import os
import math
import itertools
from sklearn.cluster import MeanShift, estimate_bandwidth
import character as character_script

package_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def delete_images(folder):
  files = glob.glob(package_directory + "/" + folder + '/*.jpg')
  for filename in files:
      os.unlink(filename)

def l_get_base_line_points(ver_hist):
  max_value_index = ver_hist.index(max(ver_hist))
 
  local_maxima_indexes = argrelextrema(np.asarray(ver_hist), np.greater_equal)[0]
  
  #print local_maxima_indexes
 
  # maximas_remove_count = len(local_maxima_indexes)*20/100
  # local_maxima_indexes = local_maxima_indexes[maximas_remove_count:]  

  # if maximas_remove_count > 0:
  #   local_maxima_indexes = local_maxima_indexes[:-maximas_remove_count]


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

def segment_lines(im):
  delete_images('lines')
  delete_images('figures')
  delete_images('overlapping_characters')
  delete_images('single_characters')
  delete_images('touching_characters')
  delete_images('touching_characters/segmented')
  delete_images('final_characters')
  

  fig2 = plt.figure()
  sub_plots2 = {}
  sub_plots2["0"] = fig2.add_subplot(211)
  sub_plots2["1"] = fig2.add_subplot(212)


  rows,cols = im.shape 
    
  ver_hist = np.zeros(rows)
  for y in xrange(rows):
      for x in xrange(cols):
          if im[y,x] == 255:
              ver_hist[y] += 1

  sub_plots2["1"].plot(ver_hist, range(rows))  
  sub_plots2["1"].invert_yaxis()

  ver_line_data = np.zeros(shape=(0,2))
  ver_line_data_copy = np.zeros(shape=(0,2))
 
  # count number of non-zeros
  def recur_lines(n, hist, count=0):
      hist_len = len(hist)      
      if n == hist_len or hist[n] == 0:        
        return count
      elif hist[n] < 2:
        hist[n] = 0
      return recur_lines(n+1, hist, count+1)

  # def recur(i, n, hist, count=0):
  #     hist_len = len(hist[i, :])
  #     if n == hist_len or hist[i, n] == 0:
  #         return count
  #     return recur(i, n+1, hist, count+1)

  i = 0
  while i < len(ver_hist):
      if ver_hist[i] < 2:
         ver_hist[i] = 0
      if ver_hist[i] != 0:
          count = recur_lines(i, ver_hist, count=0)         
          ver_line_data = np.append(ver_line_data,[[i, count]], axis=0)
          i = i + count
      i += 1

  no_of_lines = len(ver_line_data)

  #print "no of lines : " + str(no_of_lines)

  for i in xrange(no_of_lines):      
      if ver_line_data[i][1] > 20:
          ver_line_data_copy = np.append(ver_line_data_copy,[[ver_line_data[i][0], ver_line_data[i][1]]], axis=0)

  hor_hist = np.zeros([no_of_lines,cols])
  hor_line_data = np.zeros(shape=(0,3))

 
  no_of_lines = len(ver_line_data_copy)
  line_images = []

  print "no of lines : " + str(no_of_lines)

  for i in xrange(no_of_lines):

    y_min = ver_line_data_copy[i][0]
    y_max = y_min + ver_line_data_copy[i][1]
    
    #print "line : "+str(i)
    #horizontal lines
    sub_plots2["0"].hlines(y=y_min, xmin=0, xmax=cols, linewidth=2, color = 'b')
    sub_plots2["0"].hlines(y=y_max, xmin=0, xmax=cols, linewidth=2, color = 'b')

    #vertical lines
    sub_plots2["0"].vlines(x=0, ymin=y_min, ymax=y_max, linewidth=2, color = 'b')
    sub_plots2["0"].vlines(x=cols, ymin=y_min, ymax=y_max, linewidth=2, color = 'b')
  
    line_image = im[int(y_min):int(y_max), 0:int(cols)]
    rows,cols = line_image.shape
    
    new_height = 128
    r = float(new_height) / rows
    dim = (int(cols * r), int(new_height))
    line_image = cv2.resize(line_image, dim, interpolation = cv2.INTER_NEAREST)
    


    cv2.imwrite(package_directory+'/lines/'+str(i)+'.jpg',line_image)

    line_images.append(line_image)


  sub_plots2["0"].imshow(im, cmap='gray',vmin=0,vmax=255)     
  fig2.savefig(package_directory+'/figures/lines.jpg')

  return line_images


def segment_line(bw, line_no):    
  bw_ = bw.copy()

  fig3 = plt.figure()
  sub_plots3 = {}

  sub_plots3["0"] = fig3.add_subplot(411)
  sub_plots3["1"] = fig3.add_subplot(412)
  sub_plots3["2"] = fig3.add_subplot(413)
  sub_plots3["3"] = fig3.add_subplot(414)

  rows, cols = bw.shape

  sub_plots3["0"].imshow(bw_, cmap='gray',vmin=0,vmax=255)


  ver_hist = [0]*rows

  for y in xrange(rows):
      for x in xrange(cols):
        if bw[y,x] == 255:
            ver_hist[y] += 1

 
  l_base_lines = l_get_base_line_points(ver_hist)
  l_base_line_diff = l_base_lines[1] - l_base_lines[0]

  l_boundary_lines = get_boundary_line_points(ver_hist)
  l_boundary_lines_diff = l_boundary_lines[1] - l_boundary_lines[0]


  sub_plots3["0"].hlines(y=l_base_lines[0], xmin=0, xmax=cols, linewidth=2, color = 'b')
  sub_plots3["0"].hlines(y=l_base_lines[1], xmin=0, xmax=cols, linewidth=2, color = 'b')



  hor_hist = [0]*cols

  for x in xrange(cols):
      for y in xrange(rows):
        if bw[y,x] == 255:
            hor_hist[x] += 1

  # sub_plots3["1"].plot(ver_hist)

  sub_plots3["1"].plot(hor_hist)
  sub_plots3["1"].set_xlim([0,cols-1])


  words = []
  characters = np.zeros(shape=(0,2))
  character_widths = []  
  current_segment_start = 0;
  current_segment_end = 0;


  for i in range(len(hor_hist)):
    if hor_hist[i] != 0:
      if current_segment_start == 0:     
        current_segment_start = i
      if hor_hist[i-1] == 0:      
        current_segment_start = i
        if len(characters) > 1 :
          if (i - current_segment_end) > l_base_line_diff*1.2:         
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

  new_character_widths = []
 
  resized_characters = []

  for i in range(len(words)):
    resized_characters.append(np.array([0]))
    for j in range(len(words[i])):
      character_width = words[i][j][1] - words[i][j][0]
      #ignore smaller character(commas, fullstops)
      if character_width < average_char_width*0.2:
        continue    
      cropped_character = bw[0:int(rows), int(words[i][j][0]):int(words[i][j][1])]
      cropped_character_ = cropped_character.copy()
      
      if average_char_width*80/100 > character_width and average_char_width*10/100 < character_width:      
        contours, hierarchy = cv2.findContours(cropped_character,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        
        #remove small contours
        no_of_contours = 0
        for contour in contours:
          left,top,width,height = cv2.boundingRect(contour) 
          if width > 10 or height > 10:            
            no_of_contours += 1

        if no_of_contours > 1:              
          resized_characters.extend(character_script.seg_overlapping_char(cropped_character_, l_base_lines, l_boundary_lines, str(line_no)+'_'+str(i)+'_'+str(j)))
        else:
          print "single" 
          character = character_script.seg_single_char(cropped_character_, l_base_lines, l_boundary_lines, "single_characters", str(line_no)+'_'+str(i)+'_'+str(j))
          resized_characters.append(character)
        
      else:       
        rows,cols = cropped_character.shape        
        
        
        contours, hierarchy = cv2.findContours(cropped_character,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        
        #remove small contours
        no_of_contours = 0
        for contour in contours:
          left,top,width,height = cv2.boundingRect(contour) 
          if width > 10 or height > 10:            
            no_of_contours += 1

        if no_of_contours > 1:              
          resized_characters.extend(character_script.seg_overlapping_char(cropped_character_, l_base_lines, l_boundary_lines, str(line_no)+'_'+str(i)+'_'+str(j)))
        else:
          resized_characters.extend(character_script.seg_touching_char(cropped_character_, l_base_lines, l_boundary_lines, str(line_no)+'_'+str(i)+'_'+str(j)))
  for char_no, resized_character in enumerate(resized_characters):
    cv2.imwrite(package_directory+'/final_characters/'+str(char_no)+'.jpg',resized_character) 
  # plt.show()
  # cv2.waitKey(0)  
  fig3.savefig(package_directory+'/figures/line_'+str(line_no)+'.jpg')

  return resized_characters      
