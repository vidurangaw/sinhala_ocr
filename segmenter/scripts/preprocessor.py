import cv2
import numpy as np
import math

def preprocess(image):
  gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
  clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8,8))
  gray_equalized = clahe.apply(gray)
    
  gray_smoothed = cv2.fastNlMeansDenoising(gray_equalized,None,5,7,13)
  #gray_smoothed = cv2.GaussianBlur(gray_equalized,(3,3),0)
  #gray_smoothed = cv2.medianBlur(gray_equalized,1)
  #gray_smoothed = gray_equalized

  bw = cv2.threshold(gray_smoothed, 127, 255, cv2.THRESH_BINARY_INV)[1]


  #bw = cv2.adaptiveThreshold(gray_smoothed,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,11,2)
  
  rows,cols = bw.shape

  #### ---Fix skew angle--- #####

  #edges = cv2.Canny(gray_smoothed, 50, 150, apertureSize = 3)
  lines = cv2.HoughLinesP(bw, 2, np.pi/180, 200, minLineLength = int(cols*0.2), maxLineGap = 200)[0]
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


  #Rotate the image  
  (h, w) = bw.shape[:2]
  center = (w / 2, h / 2)
  M = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
  rotated = cv2.warpAffine(bw, M, (w, h))
  rotated_gray = cv2.warpAffine(gray_smoothed, M, (w, h))

  return rotated, rotated_gray