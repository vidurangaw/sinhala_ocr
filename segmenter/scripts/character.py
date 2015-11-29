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

	#join 3 segments
	resized_1 = np.concatenate((top, middle), axis=0)
	resized_2 = np.concatenate((resized_1, bottom), axis=0)  
	

	return resized_2

def char_base_line_points(character, ver_hist, boundary_lines, l_boundary_lines, l_base_lines, category, code):
	base_lines = l_base_lines[:]
	
	character_base_height = l_base_lines[1] - l_base_lines[0]

	rows,cols = character.shape 

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
	print contour_data
	if len(contour_data) > 1:
		print "horizontal group"
		#if top
		if contour_data[0][1] < base_lines[0] + character_base_height*0.3:
			print "1"
			base_lines[0] = contour_data[1][0]
			if contour_data[1][0] < base_lines[1]:
				print "2"
				base_lines[1] = contour_data[1][1]
			else:
				print "3"
				if boundary_lines[1] < (base_lines[1] + character_base_height*0.2):
					base_lines[1] = boundary_lines[1] 
		elif contour_data[0][1] > base_lines[0]:
			print "4"
			base_lines[0] = contour_data[0][0]
			base_lines[1] = contour_data[0][1]      
	else:    
		if boundary_lines[0] > (base_lines[0] - character_base_height*0.5):    
			base_lines[0] = boundary_lines[0]
		if boundary_lines[1] < (base_lines[1] + character_base_height*0.2):
			base_lines[1] = boundary_lines[1] 

	print base_lines

	return base_lines

def detect_verticle_regions(character, l_base_lines, l_boundary_lines, category, code):
	rows,cols = character.shape  
	ver_hist = [0]*rows
	hor_hist = [0]*cols

	for y in xrange(rows):
		for x in xrange(cols):
			if character[y,x] == 255:
					ver_hist[y] += 1
	
	boundary_lines = line_script.get_boundary_line_points(ver_hist)
	boundary_lines_diff = boundary_lines[1] - boundary_lines[0]

	base_lines = char_base_line_points(character, ver_hist, boundary_lines, l_boundary_lines, l_base_lines, category, code)
	
	#print base_lines

	character = resize(character, base_lines)
	
	return character, base_lines	

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
		if len(horizontal_groups) > 1:
			character = seg_single_char(empty_image, l_base_lines, l_boundary_lines, "overlapping_characters", code+'_'+str(k))
		else:
			character = seg_single_char(empty_image, l_base_lines, l_boundary_lines, "single_characters", code)
		resized_characters.append(character)

	return resized_characters    

def seg_touching_char(character, l_base_lines, l_boundary_lines, code):  
	np.set_printoptions(threshold=np.inf)
	print "touching_character"  
	rows,cols = character.shape 

	t_path = package_directory+'/touching_characters/segmented/'+code

	ver_hist = [0]*rows
	base_lines = [0]*2

	for y in xrange(rows):
		for x in xrange(cols):
			if character[y,x] == 255:
					ver_hist[y] += 1
	# new_width = rows*3
	# r = float(new_width) / cols
	# dim = (new_width, int(rows*r)) 
	# resized = character

	boundary_lines = line_script.get_boundary_line_points(ver_hist)
	character_base_height = l_base_lines[1] - l_base_lines[0]
	 
	# base_lines[0] = l_base_lines[0] - 15
	# base_lines[1] = l_base_lines[1] + 15


	# character = character[base_lines[0]:base_lines[1],0:cols]

	rows,cols = character.shape 


	character_ = character.copy()   
	character_clr = cv2.cvtColor(character_,cv2.COLOR_GRAY2RGB)
	

	for x in range(cols):   
		for y in range(0, int(rows)):
			if character_[y,x] == 255:
				if x % 4 == 0:        
					character_[y-1:y,x] = 255
					character_clr[y-1:y,x] = 255
				if x % 8 == 0:        
					character_[y-2:y,x] = 255
					character_clr[y-2:y,x] = 255
				if x % 12 == 0:        
					character_[y-3:y,x] = 255
					character_clr[y-3:y,x] = 255
				if x % 16 == 0:        
					character_[y-4:y,x] = 255   
					character_clr[y-4:y,x] = 255       
				break
	
	kernel = np.ones((4,4),np.uint8)
	character_ = cv2.dilate(character_,kernel,iterations = 1)
	character_clr = cv2.dilate(character_clr,kernel,iterations = 1)

	character__ = character_.copy()

	contours,hierarchy = cv2.findContours(character__, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnt  = np.empty(shape=[0, 1, 2], dtype='uint8')  
	for contour in contours:
		left,top,width,height = cv2.boundingRect(contour)   
		if width > 5 or height > 5:    
			cnt = np.append(cnt, contour, 0)    
	
	hull = cv2.convexHull(cnt,returnPoints = False)
	defects = cv2.convexityDefects(cnt,hull)
	

	print code

	points = []
	if defects is not None:
		for i in range(defects.shape[0]):
			s,e,f,d = defects[i,0]
			start = tuple(cnt[s][0])
			end = tuple(cnt[e][0])
			far = tuple(cnt[f][0])      
			cv2.line(character_clr,start,end,[255,0,0],2)
			if d > 1000:
				points.append(far)      
				cv2.circle(character_clr,far,3,[0,0,255],-1)

	#cv2.imwrite(t_path+'__.jpg', character_clr)

	segment_points = []

	points_three = []
	points_close = []
	points_l_shape = []
	points_vertical = []

	#character_base_height = 50

	points = list(reversed(sorted(points, key=lambda x: float(x[0]), reverse=True)))


	if len(points) > 1:

		#consider 3 points
		for p1, p2, p3 in itertools.combinations(enumerate(points), 3): 
			if abs(p1[1][1] - p2[1][1]) < 12:
				if abs(p2[1][1] - p3[1][1]) < 12:
					if abs(p1[1][0] - p2[1][0]) < 20:
						if abs(p2[1][0] - p3[1][0]) < 20:
							points_three.append(list(p2[1]))
							remove_indices = [p1[0], p2[0], p3[0]]
							points = [i for j, i in enumerate(points) if j not in remove_indices]

		

		#consider 2 points

		#consider closely aligned points
		if len(points) > 1:
			remove_indices = []   
			for p1, p2 in itertools.combinations(enumerate(points), 2): 
				if p1[0] not in remove_indices and p2[0] not in remove_indices:
					distance = math.hypot(p2[1][0]-p1[1][0], p2[1][1]-p1[1][1])
								
					if distance < 12:
						h_points = [list(p1[1]), list(p2[1])]
						h_points = list(reversed(sorted(h_points, key=lambda x: float(x[1]), reverse=True)))
						points_close.append(h_points) 

						remove_indices.extend([p1[0], p2[0]])
			points = [i for j, i in enumerate(points) if j not in remove_indices]

			
		#consider vertically aligned points
		if len(points) > 1:
			remove_indices = []
			for p1, p2 in itertools.combinations(enumerate(points), 2): 
				if p1[0] not in remove_indices and p2[0] not in remove_indices:
												
					if abs(p1[1][1] - p2[1][1]) > character_base_height*0.5 and abs(p1[1][1] - p2[1][1]) < character_base_height and abs(p1[1][0] - p2[1][0]) < 10:
						h_points = [list(p1[1]), list(p2[1])]
						h_points = list(reversed(sorted(h_points, key=lambda x: float(x[1]), reverse=True)))
						points_vertical.append(h_points)  

						remove_indices.extend([p1[0], p2[0]])
			points = [i for j, i in enumerate(points) if j not in remove_indices]
		
		#consider L shape aligned points
		if len(points) > 1:     
			remove_indices = []     
			for p1, p2 in itertools.combinations(enumerate(points), 2): 
				if p1[0] not in remove_indices and p2[0] not in remove_indices:
					
					if abs(p1[1][1] - p2[1][1]) < 20 and abs(p1[1][0] - p2[1][0]) < 20:
						h_points = [list(p1[1]), list(p2[1])]
						h_points = list(reversed(sorted(h_points, key=lambda x: float(x[1]), reverse=True)))
						points_l_shape.append(h_points)      

						remove_indices.extend([p1[0], p2[0]])
						
			points = [i for j, i in enumerate(points) if j not in remove_indices]
	

	# print "-------"

	# print('points_three : '), points_three
	# print('points_close : '), points_close
	# print('points_vertical : '), points_vertical
	# print('points_l_shape : '), points_l_shape

	segment_points = []

	character_clr_ = character_clr.copy()

	#consider 3 points
	for p in points_three:  
		if character_[p[1]-1][p[0]] != 0:			
			continue

		print "points_three"
		cv2.line(character_clr,(p[0],0),(p[0],rows),[0,0,255],2)
		cv2.imwrite(t_path+'.jpg', character_clr)	

		white_pixels = []  
		p[1] = p[1] + character_base_height/2		
 
		for x in range(p[0]-10,p[0]+10):
			if character_[p[1]][x] > 0:        
				white_pixels.append(x)

		segment_points.append(white_pixels[-1])

		cv2.line(character_clr_,(white_pixels[-1],0),(white_pixels[-1],rows),[0,0,255],2)
		cv2.imwrite(t_path+'_.jpg', character_clr_)
	
	
	#consider closely aligned points
	for p1, p2 in points_close:
		

		p_row = (p1[1]+p2[1])/2
		p_col = (p1[0]+p2[0])/2

		if character_[p1[1]-2][p1[0]] > 0:			
			continue
		if character_[p2[1]+2][p1[0]] > 0:			
			continue

		print "points_close"
		cv2.line(character_clr_,(p_col,0),(p_col,rows),[0,0,255],2)
		cv2.imwrite(t_path+'.jpg', character_clr_)

		segment_points.append(p_col)
 
	#consider vertically aligned points	
	for p1, p2 in points_vertical:  
		

		p_row = (p1[1]+p2[1])/2
		p_col = (p1[0]+p2[0])/2

		if p1[1] < l_base_lines[0]*0.8 or p2[1] > l_base_lines[1]*1.2:			
			continue

		for point_ in points:
			if point_[0] > p1[0]*1.2:
				break
			else:
				continue
		continue

		print "points_vertical"
		cv2.line(character_clr,(p_col,0),(p_col,rows),[0,0,255],2)
		cv2.imwrite(t_path+'.jpg', character_clr)

		white_pixels = []  
		
		for x in range(p1[0]-10,p2[0]+10):        
			if character__[p_row][x] > 0:
				white_pixels.append(x)
		
		segment_points.append(white_pixels[-1])

		cv2.line(character_clr_,(white_pixels[-1],0),(white_pixels[-1],rows),[0,0,255],2)
		cv2.imwrite(t_path+'_.jpg', character_clr_)
		#print p
	
	#consider L shape points
	for p1, p2 in points_l_shape: 
		p_row = (p1[1]+p2[1])/2
		p_col = (p1[0]+p2[0])/2

		if character_[p1[1]-1][p1[0]] == 0:
			continue
		if character_[p2[1]-4][p2[0]] == 0:
			continue
		if character_[p2[1]][p2[0]+2] > 0:
			continue	
		if character_[p2[1]][p2[0]-2] == 0:
			continue

		print "points_l_shape"
		cv2.line(character_clr_,(p_col,0),(p_col,rows),[0,0,255],2)
		cv2.imwrite(t_path+'.jpg', character_clr_)

		segment_points.append(p_col)

	print segment_points

	resized_characters = []

	segment_points.append(cols)
	segment_points.sort();
	left_margin = 0
	for char_no, segment_point in enumerate(segment_points):		
		if segment_point - left_margin < 5:
			continue
		seg_character = character[0:rows, left_margin:segment_point]
		left_margin = segment_point

		seg_character = seg_single_char(seg_character, l_base_lines, l_boundary_lines, "touching_characters", code+'_'+str(char_no))

		resized_characters.append(seg_character)

	

	sub_plots4["0"].imshow(character_clr_)

	#cv2.imwrite(package_directory+'/touching_characters/'+code+'.jpg', character_clr_)
	#fig4.savefig(package_directory+'/figures/touching'+code+'.png')
	
	sub_plots4["0"].clear()
	sub_plots4["1"].clear()

	return resized_characters  
	#sub_plots4["2"].clear()
	#fig4.close()
	#seg_single_char(character, l_base_lines, l_boundary_lines, "touching_characters", code)
	#cv2.imwrite(package_directory+'/touching_characters/'+str(i)+'_'+str(j)+'_'+str(1)+'.jpg', character)
 

