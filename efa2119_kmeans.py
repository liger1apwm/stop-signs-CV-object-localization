import cv2
import os
import time
import numpy as np
import math
    
# this helper function code will take the centers produced by the kmeans and find the index for the center 
# that is closer to red 
def closer_cluster(centers):
    RED = (210,0,0)

    #distance list to the red value for all clusters centers
    distance_list = []

    #iterate all the cluster centers
    for i in range(0,len(centers)):

        #distance from the cluster center i to the red
        distance = math.dist(RED,centers[i])
        distance_list.append(distance)

    #return the index corresponding to the cluster center closer in eucledean distance to red
    return np.argmin(distance_list)

def get_box(img):
    
    #convert image to rgb
    image_conv = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Reshaping the image to 2d by multiplying 1st and 2nd shape, making the array to float values
    pixel_vals = image_conv.reshape((image_conv.shape[0]*image_conv.shape[1],3))
    pixel_vals = np.float32(pixel_vals)
    pixel_vals
    
    #criteria to run the kmeans, more about in the README file
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.2)

    k = 10

    #running kmeans algorithm with the previous criteria and Kmeans_PP_centers(Kmeans++) to have a
    #better inizializations of the centers. Retrieve the labels and centers
    _, labels, centers = cv2.kmeans(pixel_vals, k, None, criteria, 5, cv2.KMEANS_PP_CENTERS)

    #convert centers to uint8
    centers = np.uint8(centers)
    
    #reshape the labels into the original image shape
    labels_reshape = labels.reshape(image_conv.shape[0], image_conv.shape[1])


    BLUE = (0,0,255)
    # RED = (255,0,0)

    #use the helper function closer_cluster to find the center that is closer to the red color
    cluster = closer_cluster(centers)

    #make a copy of the original converted image
    masked_image = np.copy(image_conv)

    #change the all the pixeles labeled to blue with the cluster center that is closest to red 
    masked_image[labels_reshape == cluster] = [BLUE]

    #chance the masked image from rbg to LAB space to be able to analize and separate better 
    # the intense blue applied from the mask
    lab_img = cv2.cvtColor(masked_image, cv2.COLOR_RGB2LAB)

    #define a lower and upper limit for our blue. Values were found by first finding what blue is in 
    # LAB by using this code: 
    # blue = np.uint8([[[255,0,0]]])
    # lab_blue = cv2.cvtColor(blue,cv2.COLOR_BGR2LAB), then print this to see the color.
    lower_blue = (82,207,15)
    upper_blue = (82,207,20)

    #convert the lower and upper blue in arrays of type uint8 to create a treshhold limit
    COLOR_MIN = np.array([lower_blue],np.uint8)
    COLOR_MAX = np.array([upper_blue],np.uint8)
    frame_threshed = cv2.inRange(lab_img, COLOR_MIN, COLOR_MAX)

    #create a color treshhold to find the places with intense blue in our specific range
    _,thresh = cv2.threshold(frame_threshed,127,255,0)

    #retrieve our matching countours for the threshhold we created
    #cv2.RETR_TREE gives a nested tree of our relevant countours for the picture
    #cv2.CHAIN_APPROX_SIMPLE leave only the important points in our contour in our case we are interested 
    #in the corner of our rectangle
    contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # Find the index of the largest contour from the previous countours tree
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    cnt=contours[max_index]

    #convert our maximun countour into bounding rectancle and get the x,y,width and height from this.
    x,y,w,h = cv2.boundingRect(cnt)

    #variables to add some padding so the contour look better around the stop sign
    pad_w = 3
    pad_h = 4
    pad_x = 3
    pad_y = 4

    #return the values for our corner points that will represent our rectangle countour
    return x-pad_x, y-pad_y, x+w+pad_w, y+h+pad_h

if __name__ == "__main__":

    start_time = time.time()

    dir_path = './images/'
    for i in range(1, 25):
        img_name = f'stop{i}.png'
        img_path = os.path.join(dir_path, img_name)
        img = cv2.imread(img_path)
        # Get the coordinators of the box
        xmin, ymin, xmax, ymax = get_box(img)
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
        output_path = f'./results/{img_name}'
        cv2.imwrite(output_path, img)

    end_time = time.time()
    # Make it < 30s
    print(f"Running time: {end_time - start_time} seconds")

