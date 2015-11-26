import cv2
import numpy as np
import itertools
import math

np.set_printoptions(threshold=np.inf)

img = cv2.imread('star2.jpg')
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

kernel = np.ones((4,4),np.uint8)
# img = cv2.dilate(img,kernel,iterations = 1)
rows, cols = img_gray.shape

# new_width = rows*3
# r = float(new_width) / cols
# dim = (new_width, int(rows*r)) 
# img = cv2.resize(img, dim, interpolation = cv2.INTER_NEAREST)


img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

rows, cols = img_gray.shape

ret, thresh = cv2.threshold(img_gray, 127, 255,cv2.THRESH_BINARY)



thresh = cv2.dilate(thresh,kernel,iterations = 1)
img = cv2.dilate(img,kernel,iterations = 1)
#print thresh[0,0]
for x in range(cols):   
	for y in range(0, int(rows)):
		if thresh[y,x] == 255:
			if x % 5 == 0:        
				thresh[y-1:y,x] = 255
			if x % 10 == 0:        
				thresh[y-2:y,x] = 255
			if x % 15 == 0:        
				thresh[y-3:y,x] = 255
			if x % 20 == 0:        
				thresh[y-4:y,x] = 255        
			break

thresh_ = thresh.copy()

#print thresh_
contours,hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

cnt  = np.empty(shape=[0, 1, 2], dtype='uint8')  


for contour in contours:
	left,top,width,height = cv2.boundingRect(contour)
	if width > 5 or height > 5:    
		cnt = np.append(cnt, contour, 0)
#cnt = contours[0]
hull = cv2.convexHull(cnt,returnPoints = False)

#print hull
defects = cv2.convexityDefects(cnt,hull)

points = []
if defects is not None:
	for i in range(defects.shape[0]):
		s,e,f,d = defects[i,0]
		start = tuple(cnt[s][0])
		end = tuple(cnt[e][0])
		far = tuple(cnt[f][0])      
		cv2.line(img,start,end,[255,0,0],2)
		if d > 1500:
			points.append(far)
			#print far
			cv2.circle(img,far,3,[0,0,255],-1)

points_three = []
points_close = []
points_horizontal = []
points_vertical = []

character_base_height = 50

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
	
	#consider horizontally aligned points
	if len(points) > 1:			
		remove_indices = []	    
		for p1, p2 in itertools.combinations(enumerate(points), 2): 
			if p1[0] not in remove_indices and p2[0] not in remove_indices:
				
				if abs(p1[1][1] - p2[1][1]) < 20 and abs(p1[1][0] - p2[1][0]) < 20:
					h_points = [list(p1[1]), list(p2[1])]
					h_points = list(reversed(sorted(h_points, key=lambda x: float(x[1]), reverse=True)))
					points_horizontal.append(h_points)			

					remove_indices.extend([p1[0], p2[0]])
					
		points = [i for j, i in enumerate(points) if j not in remove_indices]
	

print "-------"

print('points_three : '), points_three
print('points_close : '), points_close
print('points_vertical : '), points_vertical
print('points_horizontal : '), points_horizontal

segment_points = []


for p in points_three: 	
	
	cv2.line(img,(p[0],0),(p[0],rows),[0,0,255],2)
	cv2.imwrite('1.jpg', img)

	white_pixels = []	 
	p[1] = p[1] + character_base_height/2
	
	for x in range(p[0]-10,p[0]+10):
		if thresh_[p[1]][x] == 255:
			white_pixels.append(x)
		
	segment_points.append(white_pixels[-1])

	cv2.line(img,(white_pixels[-1],0),(white_pixels[-1],rows),[0,0,255],2)
	cv2.imwrite('1_.jpg', img)
	#print p
end

for p1, p2 in points_horizontal: 
	p_row = (p1[1]+p2[1])/2
	p_col = (p1[0]+p2[0])/2

	if thresh_[p1[1]-1][p1[0]] == 0:
		break
	
	cv2.line(img,(p_col,0),(p_col,rows),[0,0,255],2)
	cv2.imwrite('1.jpg', img)

	segment_points.append(p_col)

end

for p1, p2 in points_vertical: 	
	p_row = (p1[1]+p2[1])/2
	p_col = (p1[0]+p2[0])/2

	cv2.line(img,(p_col,0),(p_col,rows),[0,0,255],2)
	cv2.imwrite('1.jpg', img)

	white_pixels = []	 
	
	for x in range(p1[0]-10,p2[0]+10):				
		if thresh_[p_row][x] == 255:
			white_pixels.append(x)
		
	segment_points.append(white_pixels[-1])

	cv2.line(img_,(white_pixels[-1],0),(white_pixels[-1],rows),[0,0,255],2)
	cv2.imwrite('1_.jpg', img)
	#print p
end

for p1, p2 in points_close:

	p_row = (p1[1]+p2[1])/2
	p_col = (p1[0]+p2[0])/2

	cv2.line(img,(p_col,0),(p_col,rows),[0,0,255],2)
	cv2.imwrite('1.jpg', img)

	segment_points.append(p_col)

	#print p
end

for segment_point in segment_points:
	print segment_point


cv2.imshow('img2',img)

cv2.waitKey(0)
cv2.destroyAllWindows()