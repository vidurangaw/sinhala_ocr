__author__ = 'Naleen'
import cv2

# image : input image, cv2.imread()
def char_location(character):

    ret,thresh = cv2.threshold(character, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    xMax = 0
    yMax = 0
    xMin = 100
    yMin = 100
    for cnt in contours:
           x,y,w,h = cv2.boundingRect(cnt)
           if(x>xMax or x+w>xMax):
               xMax=x+w
           if(y>yMax or y+h>yMax):
               yMax=y+h
           if(x<xMin):
               xMin=x
           if(y<yMin):
               yMin=y

    # print "xmin:"+str(xMin) + "   " +"yMin" +str(yMin)
    # print "xmax:"+str(xMax) + "   " +"yMax" +str(yMax)
    # cv2.rectangle(character,(xMin,yMin),(xMax,yMax),(0,255,0),2)

    return xMin, xMax, yMin, yMax
#


