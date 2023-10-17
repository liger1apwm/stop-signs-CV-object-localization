Kmeans algorithm parameters explanation 

My kmeans Algorithm was compose of the following parameters:

pixel_vals, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS

pixel_vals: the vector containing the array of pixel values after it wa flattened

k: the number of clusters for the algorithm to paratition the data into where the data will be assigned
to one of the k centroids

this is one of the most important parameters since it will help categorize our pictures in different 
group of colors. Having a lower K may not capture the full range of colors and having a too high K may
over categorize the colors. I experimented with K's ranging from 3 to 16 and this affected the algorithm
runtime directly. as k went up the algorithm took more time to run.
After for k less than 7 and K greater than 9 my algorithm started to falter catching up correct images,
I found the best classifications with K being 8.

None: In this position we can set our own centroid if we desire it but we opting for define another way 
to intialize our centroid in the next parameter criteria

Criteria: list of conditions for our Kmeans to terminate or iterate for, the following conditions were
used criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.05):

        cv2.TERM_CRITERIA_EPS : is the maximun allowed error epsilon on where the algorithm will end
        and converge. This means that if in two consecutives runs the algorithm check if the change in 
        centers is less than epsilon and then stop if is true. Epsilon values can be changed and defined
        the end

        cv2.TERM_CRITERIA_MAX_ITER: if the centroid dont converge using epsilon, this will define when the
        algorithm should stop based on the maximun amount of iteration allowed in this parameter.

        we used both together thats why they are have a plus.

        100: the maximung amount iterations used for cv2.TERM_CRITERIA_MAX_ITER
        this parameter really didnt affect to much the kmeans runtime since it looks like it never reached max iteration.

        0.05: the value of epsilon defined by us to be used by cv2.TERM_CRITERIA_EPS
        I noticed the more I reduced epsilon, the more time it take to run the algorithm since we are looking 
        for higher precision in terms on deciding when the centroid is no longer relevant to update.

10: this is the amount of times the kmeans will be run  with different inzializations to the return
the values for the best run to help reduce error due to center inizialization

Didnt affect to much the runtime when I changed the number of run for the kmeans, it looks like the 
amount of times we runned didnt affect the outcome. 

cv2.KMEANS_PP_CENTERS: this let the kmeans knows to use the  "k-means++" initialization method to intialize
our centroids. is said to be a better initilization compared to a random inizialization since it spreads 
the initial centroids more spread across all the data.

Using KMEANS_PP_CENTERS seemed to be better instead of using the random center assigments. When I implemented
this type of center inizialition , the convergence proved to be faster, reducing runtime significany.


I believe my kmeans algorithm is still not doing well for pictures with a lot of colors or quality going
on, I notice that image 14 and 16 have a larger pallete of colors and my algorithm fail to find the stop 
sign on those case. 







