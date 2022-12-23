## Arya Kulkarni
## ak9354
## Project 1: Extended Otsu's Method

import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt
import skimage
import math
from PIL import Image


# get histogram of test image
def hist_plot(img):
    # stores count of each intensity values
    count = []

    # stores intensity values
    r = []

    # loop through each intensity value
    for k in range(0, 256):
        # loops through each pixel in the image 
        count1 = np.count_nonzero(img == k)
        count.append(count1)
        r.append(k)
          
    return (r, count)
  

# otsu thresholding for 2 regions only
def otsu(img):
    # Get the image histogram
    print("Calculating Histogram...")
    # intensity = r1, count per intensity = count1
    histogram, intensity = hist_plot(img)
    
    # plotting the histogram
    plt.stem(histogram, intensity)
    plt.xlabel('intensity value')
    plt.ylabel('number of pixels')
    plt.title('Histogram of the Grayscale Image')
    plt.show()

    # otsu variables need to be initialized
    thres = 0
    minVariance = np.Inf
    totalPixels = (img.shape[0] * img.shape[1])

    # DEBUG: check variance values
    #var_arr = []
    #var_arr3 = []
    
    # calculate between class vaiance by looping through intensities
    for t in range(0, 255):
        # intensities that belong in the background vs foreground (2 regions)
        background = intensity[0:t]
        foregroud = intensity[t:256]
        histogram_left = histogram[0:t]
        histogram_right = histogram[t:256]
        histogram_left_sum = np.sum(intensity[0:t])
        histogram_right_sum = np.sum(intensity[t:256])


        # calculate mean gray values for both [with library]
        #print(np.sum(histogram[0:t]), flush=True)
        m1 = 1 if histogram_left_sum == 0 else np.dot(histogram_left, background) / histogram_left_sum
        m2 = 1 if histogram_right_sum == 0 else np.dot(histogram_right, foregroud) / histogram_right_sum

        # calculate weights
        w1 = (histogram_left_sum / totalPixels)
        w2 = (histogram_right_sum / totalPixels)

        # calc varience ((intensity[i] - mean)**2) * hist[i]
        # find first variance
        v1_diff = []
        i = 0
        for i in range(len(background)):
            v1_diff.append(((histogram[i] - m1)**2)*intensity[i])
        v1_sum = 0
        i = 0
        for i in range(len(v1_diff)):
            v1_sum += v1_diff[i]
        v1 = 1 if histogram_left_sum == 0 else v1_sum / histogram_left_sum

        # find second variance
        v2_diff = []
        i=0
        for i in range(len(foregroud)):
            v2_diff.append(((histogram[i+t] - m2)**2)*intensity[i+t])
        v2_sum = 0
        i=0
        for i in range(len(v2_diff)):
            v2_sum += v2_diff[i]
        v2 = 1 if histogram_right_sum == 0 else v2_sum / histogram_right_sum

        # find class variance  
        wcv = w1*v1 + w2*v2
        
        #DEBUG
        #var_arr.append(wcv)
        #var_arr3.append((histogram_left, histogram_right, histogram_left_sum, histogram_right_sum, w1, w2, m1, m2, v1, v2))
        #var_arr3.append((m1, m2, v1, v2))
        #var_arr3.append((histogram_left_sum, histogram_right_sum))

        # compare variences to minimize it
        if wcv < minVariance:
            #print("Threshold Found: ", t, " @ var: ", wcv)
            minVariance = wcv
            thres = t
            
    print("Otsu's Threshold Computed: ", thres)
    print("Otsu's Variance: ", minVariance)
            
    #DEBUG
    #print("Varience Vector length: ", len(var_arr))
    #print("Comparing Otsu and CV: ", var_arr[thres], var_arr[108])

    # apply threshold
    image_size = (img.shape[0],img.shape[1])
    final_image = np.zeros(image_size)
    print("Applying Threshold...")

    # loop over image
    for r in range(0, img.shape[0]):
        for c in range(0, img.shape[1]):
            # apply threshold
            if img[r, c] < thres:
                final_image[r, c] = 0
            else:
                final_image[r,c] = 252
        
    return final_image, thres, minVariance


# otsu thresholding for 3 regions only
def multi_otsu_3regions(img):
    # Get the image histogram
    print("Calculating Histogram...")
    histogram, intensity = hist_plot(img)
    
    # plotting the histogram
    plt.stem(histogram, intensity)
    plt.xlabel('intensity value')
    plt.ylabel('number of pixels')
    plt.title('Histogram of the Grayscale Image')
    plt.show()

    # otsu variables
    thres = 0
    minVariance = np.Inf
    totalPixels = (img.shape[0] * img.shape[1])

    # DEBUG: check variance values
    #var_arr = []
    #var_arr3 = []
        
    # calculate between class vaiance by looping through intensities
    for t in range(0, 255):
        import time
        #print("Threshold lvl: ", t)
        total_time = 0
        total_time2 = 0
        total_time3 = 0
        start_func_time = time.time()
        
        for u in range(t+1, 255): # loop through remaining intensities to find 2nd intensity
                start_mid_time = time.time()
                start_mid2_time = time.time()
                # intensities that belong in the background, between, and foreground (3 regions)
                background = np.array(intensity[0:t])
                intermediate = np.array(intensity[t:u])
                foregroud = np.array(intensity[u:256])
                histogram_left = np.array(histogram[0:t])
                histogram_middle = np.array(histogram[t:u])
                histogram_right = np.array(histogram[u:256])
                histogram_left_sum = np.sum(intensity[0:t])
                histogram_mid_sum = np.sum(intensity[t:u])
                histogram_right_sum = np.sum(intensity[u:256])

                start_mid2_time = time.time()
                # calculate mean gray values for both [with library]
                #print(np.sum(histogram[0:t]), flush=True)
                m1 = 1 if histogram_left_sum == 0 else np.dot(histogram_left, background) / histogram_left_sum
                m_mid = 1 if histogram_mid_sum == 0 else np.dot(histogram_middle, intermediate) / histogram_mid_sum
                m2 = 1 if histogram_right_sum == 0 else np.dot(histogram_right, foregroud) / histogram_right_sum
                end_mid2_time = time.time()

                # calculate weights
                w1 = (histogram_left_sum / totalPixels)
                w_mid = (histogram_mid_sum / totalPixels)
                w2 = (histogram_right_sum / totalPixels)

                #end_mid2_time = time.time()

                # calc varience ((intensity[i] - mean)**2) * hist[i]
                # find first variance
                v1_diff = []
                i = 0
                v1_start_time = time.time()
                v1_diff = np.multiply((histogram_left - m1)**2,background)
                
                v1_sum = np.sum(v1_diff)
                v1 = 1 if histogram_left_sum == 0 else v1_sum / histogram_left_sum

                # find second variance
                v2_diff = []
                v2_start_time = time.time()
                v2_diff = np.multiply((histogram_right - m2)**2,foregroud)

                v2_end_time = time.time()
                v2_sum = np.sum(v2_diff)
                v2 = 1 if histogram_right_sum == 0 else v2_sum / histogram_right_sum

                # find middle region variance
                v3_diff = []
                i=0
                v3_start_time = time.time()
                v3_diff = np.multiply((histogram_middle - m_mid)**2,intermediate)
                v3_end_time = time.time()
                v3_sum = np.sum(v3_diff)
                i=0
                v3 = 1 if histogram_mid_sum == 0 else v3_sum / histogram_mid_sum


                v1_end_time = time.time()

                # find class variance  
                wcv = w1*v1 + w2*v2 + w_mid*v3
                
                #DEBUG
                #var_arr.append(wcv)
                #var_arr3.append((histogram_left, histogram_right, histogram_left_sum, histogram_right_sum, w1, w2, m1, m2, v1, v2))
                #var_arr3.append((m1, m2, v1, v2))
                #var_arr3.append((histogram_left_sum, histogram_right_sum))

                # compare variences to minimize it
                if wcv < minVariance:
                    #print("Threshold Found: ", t, " @ var: ", wcv)
                    minVariance = wcv
                    thres = (t, u)
                end_mid_time = time.time()
                
                #total_time += (v1_end_time - v1_start_time + v2_end_time - v2_start_time + v3_end_time - v3_start_time)
                total_time2 += (v1_end_time - v1_start_time)
                total_time += end_mid2_time - start_mid2_time
                total_time3 += end_mid_time - start_mid_time

        end_func_time = time.time()
        #print(end_func_time - start_func_time)
        #print(total_time)
        #print(total_time2)
        #print(total_time3)

    print("Otsu's Threshold Computed: ", thres)
    print("Otsu's Variance: ", minVariance)
            
    #DEBUG
    #print("Varience Vector length: ", len(var_arr))
    #print("Comparing Otsu and CV: ", var_arr[thres], var_arr[108])
 
    # apply threshold
    image_size = (img.shape[0],img.shape[1])
    final_image = np.zeros(image_size)
    print("Applying Threshold...")

    # loop over image
    for r in range(0, img.shape[0]):
        for c in range(0, img.shape[1]):
            # apply threshold
            if 0 <= img[r, c] < thres[0]:
                final_image[r, c] = 0
            elif thres[0] <= img[r,c] < thres[1]:
                final_image[r,c] = 150
            else:
                final_image[r,c] = 255

    # return values
    return final_image, thres, minVariance


# otsu thresholding for 4 regions only
def multi_otsu_4regions(img):
    # Get the image histogram
    print("Calculating Histogram...")
    histogram, intensity = hist_plot(img)
    
    # plotting the histogram
    plt.stem(histogram, intensity)
    plt.xlabel('intensity value')
    plt.ylabel('number of pixels')
    plt.title('Histogram of the Grayscale Image')
    plt.show()

    # otsu variables
    thres = 0
    minVariance = np.Inf
    totalPixels = (img.shape[0] * img.shape[1])

    # DEBUG: check variance values
    #var_arr = []
    #var_arr3 = []
        
    # calculate between class vaiance by looping through intensities
    for t in range(0, 255):
        import time # check time it takes for operations to run
        print("MultiOtsu Progress: ", str(round((t/255)*100, 2)), "%")
        total_time = 0
        total_time2 = 0
        total_time3 = 0
        start_func_time = time.time()
        
        for u in range(t+1, 255): # find 2nd region threshold
            for v in range(u+1, 255): # find 3rd region threshold
                start_mid_time = time.time()
                start_mid2_time = time.time()

                # intensities that belong in the background vs foreground
                background = np.array(intensity[0:t])
                intermediate = np.array(intensity[t:u])
                intermediate2 = np.array(intensity[u:v])
                foregroud = np.array(intensity[v:256])
                histogram_left = np.array(histogram[0:t])
                histogram_middle = np.array(histogram[t:u])
                histogram_middle2 = np.array(histogram[u:v])
                histogram_right = np.array(histogram[v:256])
                histogram_left_sum = np.sum(intensity[0:t])
                histogram_mid_sum = np.sum(intensity[t:u])
                histogram_mid2_sum = np.sum(intensity[u:v])
                histogram_right_sum = np.sum(intensity[v:256])

                start_mid2_time = time.time()
                # calculate mean gray values for both [with library]
                #print(np.sum(histogram[0:t]), flush=True)

                m1 = 1 if histogram_left_sum == 0 else np.dot(histogram_left, background) / histogram_left_sum
                m_mid = 1 if histogram_mid_sum == 0 else np.dot(histogram_middle, intermediate) / histogram_mid_sum
                m_mid2 = 1 if histogram_mid2_sum == 0 else np.dot(histogram_middle2, intermediate2) / histogram_mid2_sum
                m2 = 1 if histogram_right_sum == 0 else np.dot(histogram_right, foregroud) / histogram_right_sum
                end_mid2_time = time.time()

                # calculate weights
                w1 = (histogram_left_sum / totalPixels)
                w_mid = (histogram_mid_sum / totalPixels)
                w_mid2 = (histogram_mid2_sum / totalPixels)
                w2 = (histogram_right_sum / totalPixels)

                #end_mid2_time = time.time()

                # calc varience ((intensity[i] - mean)**2) * hist[i]
                # find first variance
                v1_diff = []
                i = 0
                v1_start_time = time.time()
                v1_diff = np.multiply((histogram_left - m1)**2,background)
                
                v1_sum = np.sum(v1_diff)
                v1 = 1 if histogram_left_sum == 0 else v1_sum / histogram_left_sum

                # find second variance
                v2_diff = []
                v2_start_time = time.time()
                v2_diff = np.multiply((histogram_right - m2)**2,foregroud)

                v2_end_time = time.time()
                v2_sum = np.sum(v2_diff)
                v2 = 1 if histogram_right_sum == 0 else v2_sum / histogram_right_sum

                # find middle region variance
                v3_diff = []
                i=0
                v3_start_time = time.time()
                v3_diff = np.multiply((histogram_middle - m_mid)**2,intermediate)
                v3_end_time = time.time()
                v3_sum = np.sum(v3_diff)
                i=0
                v3 = 1 if histogram_mid_sum == 0 else v3_sum / histogram_mid_sum

                # find last region variance
                v4_diff = []
                i=0
                v4_start_time = time.time()
                v4_diff = np.multiply((histogram_middle2 - m_mid2)**2,intermediate2)
                v4_end_time = time.time()
                v4_sum = np.sum(v4_diff)
                i=0
                v4 = 1 if histogram_mid2_sum == 0 else v4_sum / histogram_mid2_sum

                v1_end_time = time.time()

                # find class variance  
                wcv = w1*v1 + w2*v2 + w_mid*v3 + w_mid2*v4
                
                #DEBUG
                #var_arr.append(wcv)
                #var_arr3.append((histogram_left, histogram_right, histogram_left_sum, histogram_right_sum, w1, w2, m1, m2, v1, v2))
                #var_arr3.append((m1, m2, v1, v2))
                #var_arr3.append((histogram_left_sum, histogram_right_sum))

                # compare variences to minimize it
                if wcv < minVariance:
                    #print("Threshold Found: ", t, " @ var: ", wcv)
                    minVariance = wcv
                    thres = (t, u, v)
                end_mid_time = time.time()
                
                #total_time += (v1_end_time - v1_start_time + v2_end_time - v2_start_time + v3_end_time - v3_start_time)
                total_time2 += (v1_end_time - v1_start_time)
                total_time += end_mid2_time - start_mid2_time
                total_time3 += end_mid_time - start_mid_time

        end_func_time = time.time()
        #print(end_func_time - start_func_time)
        #print(total_time)
        #print(total_time2)
        #print(total_time3)

    print("Otsu's Threshold Computed: ", thres)
    print("Otsu's Variance: ", minVariance)
            
    #DEBUG
    #print("Varience Vector length: ", len(var_arr))
    #print("Comparing Otsu and CV: ", var_arr[thres], var_arr[108])

    # apply threshold
    image_size = (img.shape[0],img.shape[1])
    final_image = np.zeros(image_size)
    print("Applying Threshold...")

    # loop over image to apply threshold
    for r in range(0, img.shape[0]):
        for c in range(0, img.shape[1]):
            # apply threshold
            if 0 <= img[r, c] < thres[0]:
                final_image[r, c] = 0
            elif thres[0] <= img[r,c] < thres[1]:
                final_image[r,c] = 80
            elif thres[1] <= img[r,c] < thres[2]:
                final_image[r,c] = 160
            else:
                final_image[r,c] = 255

    # return values
    return final_image, thres, minVariance


# main funtion that takes in the test images and applies 
# the otsu function to find regions and thresholds
def main():

    # read image
    print("chosen image: ", sys.argv[1])
    first_img = cv2.imread(f"images/{sys.argv[1]}")
    im_gray = cv2.imread(f"images/{sys.argv[1]}", cv2.IMREAD_GRAYSCALE)


    # show image
    cv2.imshow('first image read',first_img)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys the window showing image

    # turn image to grayscale
    print("transforming to grayscale...")
    # 𝐼 = 𝑅ound(0.299𝑅 + 0.587𝐺 + 0.114𝐵) 
    for r in range(len(first_img)):
        for c in range(len(first_img[0])):
            b,g,red = first_img[r][c]
            red = (0.299*red)
            g = (0.587*g)
            b = (0.114*b)
            im_gray[r][c] = round(b+g+red)
            first_img[r][c] = round(b+g+red)

    first_img = im_gray

    #print(f"gray image shape {im_gray.shape}", flush=True)
    #print(f"first image shape {first_img.shape}", flush=True)

    # show image
    print("display grayscale image...")
    cv2.imshow('gray image read', first_img)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys the window showing image

    # run otsu (for 2 regions) to gain threshold values
    img_res1, thres1, var1 = otsu(first_img) 
    cv2.imshow('Otsu\'s algorithm resulting image', img_res1)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys the window showing image
    #print(type(img_res1))
    


    '''
    # Check using cv2 thresholding:
    otsu_threshold, image_result = cv2.threshold(
        im_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )    
    print("Otsu's algorithm implementation thresholding result: ", otsu_threshold)
    cv2.imshow('final image', image_result)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys the window showing image
    '''

    # Call multi_otsu using final_image (here we have 1 threshold - 
    # background and foreground at the moment)
    # use total variance to determine regions

    # run otsu (for 3 regions) to gain threshold values
    img_res2, thres2, var2 = multi_otsu_3regions(first_img) 
    cv2.imshow('Otsu\'s algorithm resulting image', img_res2)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys the window showing image

    # run otsu (for 4 regions) to gain threshold values
    img_res3, thres3, var3 = multi_otsu_4regions(first_img) 
    cv2.imshow('Otsu\'s algorithm resulting image', img_res3)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys the window showing image

    # compare variances to determind which is the right fit
    # should be a big difference in between vars to change region number
    print("Variances for", sys.argv[1], ": ")
    print(var1, var2, var3)

    # compare variances to determine the number of regions
    filename = sys.argv[1]
    name = filename.split(".")
    if ((var1 - var2)/var1) > (0.5):
        # go to region 3
        #print("Regions = 3")
        if ((var2 - var3)/var2) > (0.4):
            # go to region 4
            print("Regions = 3")
            # save image
            pictureName = name[0] + "-out.bmp"
            im = Image.fromarray(img_res2)
            if im.mode != 'RGB':
                im = im.convert('RGB')
            im.save(pictureName)
        else:
            # region 3
            print("Regions = 4") 
            #save image
            pictureName = name[0] + "-out.bmp"
            im = Image.fromarray(img_res3)
            if im.mode != 'RGB':
                im = im.convert('RGB')
            im.save(pictureName)                                                                                         
        
    else:
        # region 2 
        print("Regions = 2")
        # save image
        pictureName = name[0] + "-out.bmp"
        im = Image.fromarray(img_res1)
        if im.mode != 'RGB':
            im = im.convert('RGB')
        im.save(pictureName)


# call main function to start otsu
main()
