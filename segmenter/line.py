import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interpolate
from scipy import ndimage as ndimage
from scipy import signal
import matplotlib.ticker as ticker
import matplotlib.ticker as plticker
from scipy.signal import argrelextrema

def smooth(x,window_len=11,window='hanning'):
    """smooth the ver_hist using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also:

    np.hanning, np.hamming, np.bartlett, np.blackman, np.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


    s=np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y


def smoothList(list,strippedXs=False,degree=10):  

     if strippedXs==True: return Xs[0:-(len(list)-(len(list)-degree+1))]  

     smoothed=[0]*(len(list)-degree+1)  

     for i in range(len(smoothed)):  

         smoothed[i]=sum(list[i:i+degree])/float(degree)  

     return smoothed  

   

def smoothListTriangle(list,strippedXs=False,degree=5):  

 weight=[]  

 window=degree*2-1  

 smoothed=[0.0]*(len(list)-window)  

 for x in range(1,2*degree):weight.append(degree-abs(degree-x))  

 w=np.array(weight)  

 for i in range(len(smoothed)):  

     smoothed[i]=sum(np.array(list[i:i+window])*w)/float(sum(w))  

 return smoothed  



def smoothListGaussian(list,strippedXs=False,degree=5):  

 window=degree*2-1  

 weight=np.array([1.0]*window)  

 weightGauss=[]  

 for i in range(window):  

     i=i-degree+1  

     frac=i/float(window)  

     gauss=1/(np.exp((4*(frac))**2))  

     weightGauss.append(gauss)  

 weight=np.array(weightGauss)*weight  

 smoothed=[0.0]*(len(list)-window)  

 for i in range(len(smoothed)):  

     smoothed[i]=sum(np.array(list[i:i+window])*weight)/sum(weight)  

 return smoothed  

def segment_lines(im):
    #print ("start")


    fig3 = plt.figure()
    sub_plots3 = {}
    sub_plots3["a"] = fig3.add_subplot(211)
    sub_plots3["a"] = fig3.add_subplot(212)


    rows,cols = im.shape 
      
    ver_hist = np.zeros(rows)
    for x in xrange(rows):
        for y in xrange(cols):
            if im[x,y] == 255:
                ver_hist[x] += 1



    # #ver_hist = smooth(np.array(array_hist),window_len=21,window='flat')
    # #print ver_hist
    # #ver_hist = np.r_[True, ver_hist[1:] < ver_hist[:-1]] & np.r_[ver_hist[:-1] < ver_hist[1:], True]

    # #ver_hist = map(lambda x: 1 if x else 0, ver_hist)
    # #print ver_hist

    # #print type(ver_hist)
    # #print type(ver_hist[1])
    # #print ver_hist[100]
    # # for x in xrange(len(ver_hist)):
    # #   if ver_hist[x] == 1:
    # #       print x


    # #hist = cv2.calcHist([im],[0],None,[256],[0,256])
    # #cv2.imshow('morphologyEx',im)

    # # plt.show()

    # # cv2.waitKey(0)

    # sub_plots2["c"].plot(ver_hist)

    # l = 0
    # for l in xrange(len(ver_hist)):
    #     if ver_hist[l] < 10:
    #         ver_hist[l] = 0



    # #ver_hist = smoothList(ver_hist,degree=2)


    # sub_plots2["d"].plot(ver_hist)

    # print len(ver_hist)

    # #change parameter
    # #ver_hist = ndimage.gaussian_filter(ver_hist, 2)


    # #ver_hist = smooth( ver_hist,window_len=5,window='flat')

    # ver_hist_max = max(ver_hist)


    # #sub_plots["cx"].plot(ver_hist)


    # # for i in range(ver_hist_len):
    # #     if ver_hist[i]/ver_hist_max*100 <= 5:
    # #         ver_hist[i] = 0

    # #change parameter
    # #box = np.ones(4)/4
    # #ver_hist  = np.convolve(ver_hist, box, mode='same')






    #print ver_hist

    # #sub_plots["dx"].plot(ver_hist)

    # #ver_space_data = np.zeros(shape=(0,2))
    ver_line_data = np.zeros(shape=(0,2))
    ver_line_data_copy = np.zeros(shape=(0,2))
    # count number of non-zeros
    def recur_lines(n, hist, count=0):
        hist_len = len(hist)
        if hist[n] < 2:
           hist[n] = 0
        if n == hist_len or hist[n] == 0:
            return count
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
            #print count
            ver_line_data = np.append(ver_line_data,[[i, count]], axis=0)
            i = i + count
        i += 1

    no_of_lines = len(ver_line_data)

    print "no of lines : " + str(no_of_lines)

    for i in xrange(no_of_lines):
        print ver_line_data[i][1]
        if ver_line_data[i][1] > 10:
            ver_line_data_copy = np.append(ver_line_data_copy,[[ver_line_data[i][0], ver_line_data[i][1]]], axis=0)

    hor_hist = np.zeros([no_of_lines,cols])

    hor_line_data = np.zeros(shape=(0,3))

    #print ver_line_data_copy


   
    no_of_lines = len(ver_line_data_copy)
    line_images = []

    print "no of lines : " + str(no_of_lines)

    for i in xrange(no_of_lines):

        y_min = ver_line_data_copy[i][0]
        y_max = y_min + ver_line_data_copy[i][1]
        
        print "line : "+str(i)
        #horizontal lines
        sub_plots3["a"].hlines(y=y_min, xmin=0, xmax=cols, linewidth=2, color = 'b')
        sub_plots3["a"].hlines(y=y_max, xmin=0, xmax=cols, linewidth=2, color = 'b')

        #vertical lines
        sub_plots3["a"].vlines(x=0, ymin=y_min, ymax=y_max, linewidth=2, color = 'b')
        sub_plots3["a"].vlines(x=cols, ymin=y_min, ymax=y_max, linewidth=2, color = 'b')
        #print 
        line_image = im[int(y_min):int(y_max), 0:int(cols)]

        #print len(line_image)

        line_images.append(line_image)




    # sub_plots3["a"].imshow(im, cmap='gray',vmin=0,vmax=255)     
    # plt.show()
    # cv2.waitKey(0)
    return line_images


