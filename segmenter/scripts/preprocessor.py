import cv2
import numpy as np
import math
import os
import time
import glob

package_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def delete_images(folder):
  files_jpg = glob.glob(package_directory + "/" + folder + '/*.jpg')
  files_png = glob.glob(package_directory + "/" + folder + '/*.png')
  files_jpg.extend(files_png)

  for filename in files_jpg:
      os.unlink(filename)

def preprocess(image):
  print "start"

  delete_images('lines')
  delete_images('figures')
  delete_images('overlapping_characters')
  delete_images('single_characters')
  delete_images('touching_characters')
  delete_images('touching_characters/segmented')
  delete_images('final_characters')

  

  gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 

  #cv2.imwrite(package_directory+'/figures/grey.jpg',gray)
  #clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(2,2))
  #gray_equalized = clahe.apply(gray)
    
  gray_smoothed = cv2.fastNlMeansDenoising(gray,None,5,7,11)

  #cv2.imwrite(package_directory+'/figures/smooth.jpg',gray_smoothed)
  #gray_smoothed = cv2.GaussianBlur(gray_equalized,(3,3),0)
  #gray_smoothed = cv2.medianBlur(gray_smoothed,3)
  #gray_smoothed = gray_equalized
  #ret3,bw = cv2.threshold(gray_smoothed,170,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

  #print ret3
  bw = cv2.threshold(gray_smoothed, 150, 255, cv2.THRESH_BINARY_INV)[1]


  #bw = cv2.adaptiveThreshold(gray_smoothed,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,55,2)


  cv2.imwrite(package_directory+'/figures/pre-thesh.jpg',bw)

  bw_clr = cv2.cvtColor(bw,cv2.COLOR_GRAY2RGB)


  rows,cols = bw.shape

  print cols
  #print 
  #### ---Fix skew angle--- #####

  #edges = cv2.Canny(gray_smoothed, 50, 150, apertureSize = 3)
  lines = cv2.HoughLinesP(bw, 2, np.pi/180, 200, minLineLength = int(cols*0.2), maxLineGap = 120)[0]
  no_of_lines = len(lines)

  angles = np.empty([0])
  for x1,y1,x2,y2 in lines:        
    cv2.line(bw_clr,(x1,y1),(x2,y2),(0,255,0),1)

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

  #remove outliers from a angle list
  angles = angles[abs(angles - np.mean(angles)) < 2 * np.std(angles)]
  if angles.size > 0:
    #get mean of angle list
    rotation_angle = np.mean(angles)
  else:
    rotation_angle = 0
     

  cv2.imwrite(package_directory+'/figures/pre-angles.jpg',bw_clr)

  print "doc rotation angle : "+ str(rotation_angle)


  #Rotate the image  
  (h, w) = bw.shape[:2]
  center = (w / 2, h / 2)
  M = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
  rotated = cv2.warpAffine(bw, M, (w, h))
  # rotated_gray = cv2.warpAffine(gray_smoothed, M, (w, h))

  cv2.imwrite(package_directory+'/figures/rotated.jpg',rotated)
 
  return rotated