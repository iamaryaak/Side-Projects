## Arya Kulkarni
## ak9354
## Project 2: Face Recognition

import glob
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv2
import os
from PIL import Image
import PIL
from numpy.linalg import eig

# save numpy array (mean face) as csv file
from numpy import asarray
from numpy import savetxt

# use libraries for matrix and vector operations, and the computations 
# of eigenvalues and eigenvectors and reading and writing images

def main():
    print("Main method for facial recognition\n")

    '''
    TRAINING EIGENFACES RECOGNITION ALGO -----------------------------------------------------------------------------
    '''
    # 231x195
    height = 231 # image height
    width = 195 # image width

    # read images from Training dataset
    print('Training Images Loading...')

    # training image names
    dataset_path = 'Training/'
    train_image_names = ['subject01.happy.jpg', 'subject02.normal.jpg', 'subject03.normal.jpg', 
    'subject07.centerlight.jpg', 'subject10.normal.jpg', 'subject11.normal.jpg', 
    'subject14.normal.jpg', 'subject15.normal.jpg']
    
    # loop through and show training images
    # vector of N2 x 1
    training_vector = np.ndarray(shape=(len(train_image_names), height * width))

    # loop through and add image to training_vector - collection of N2 x 1 vectors
    print("Creating training vectors...")
    for i in range(len(train_image_names)):
        gray_img = plt.imread(dataset_path + train_image_names[i])
        image_arr = np.array(gray_img).flatten()

        # add image vector to vector array
        training_vector[i,:] = image_arr
        #print("Image shape: ", image_arr.shape, "\n")
        plt.imshow(gray_img, cmap='gray')
    #print("Matrix R shape: ", training_vector.shape)


    # Find Mean Eigenface from training data
    # make a N^2 X 1 vector
    mean_face = np.zeros((1, height * width))
    for i in training_vector:
        mean_face = np.add(mean_face, i)
    #print(mean_face.shape)
    
    # create mean face vector
    mean_face = np.divide(mean_face, float(len(train_image_names))).flatten()
    plt.title("Mean Face: m")
    plt.imshow(mean_face.reshape(height, width), cmap='gray')
    plt.show()

    # save mean face for PDF
    #mean_face_im = Image.fromarray(mean_face.reshape(height, width))
    #mean_face_im.convert("L").save("mean_face.jpeg")


    # subtract mean face from each training image
    #print("\nSubtracting mean face from training faces")
    norm_training_vector = np.ndarray(shape=(len(train_image_names), height*width))
    for i in range(len(train_image_names)):
        norm_training_vector[i] = np.subtract(training_vector[i], mean_face)
    #print("Matrix R bar shape: ", norm_training_vector.shape, "\n")

    # set up covariance matrix
    covariance = np.cov(norm_training_vector)
    covariance = np.divide(covariance,8.0)
    #print("Matrix Covariance shape:\n", covariance.shape)
    #print("Covariance matrix: \n", covariance)

    eigenvalues, eigenvectors, = np.linalg.eig(covariance)
    #print('Eigenvectors of Cov(X): \n%s' %eigenvectors)
    #print('\nEigenvalues of Cov(X): \n%s' %eigenvalues)

    #print("\nEigenvector shape: ", eigenvectors.shape)
    #print("Norm shape: ", norm_training_vector.T.shape)
    # find eigenvectors of C
    U = np.matmul(norm_training_vector.T, eigenvectors)
    # print eigenfaces
    for i in range(len(train_image_names)):
        #print("Shape: ", U.T[i].shape)
        plt.subplot(2,4,1+i)
        plt.imshow(U.T[i].reshape(height, width), cmap='gray')
        plt.tick_params(labelleft='off', labelbottom='off', bottom='off',top='off',right='off',left='off', which='both')
    plt.suptitle("Eigenface Images")
    plt.show()


    # find projections
    print("\n")
    print("Eigenface Coefficients for Traning Images: ")
    projections = np.ndarray(shape=(len(train_image_names), len(train_image_names)))
    j = 0
    for i in norm_training_vector:
        omega = np.matmul(U.T, i)
        projections[j] = omega
        j+=1
        print("Eigenface Coefficient for Training Image %d:" %j, "\n", omega)
    print("\n")    
    #print("Omega shape: ", projections.shape)

    '''
    Recognize Image by computing the distance between input image projections and training data ---------------------------------
    '''

    print("Test Images Loading...\n")
    # training image names
    testing_path = 'Testing/'
    test_image_names = ['subject01.normal.jpg', 'subject07.happy.jpg', 'subject07.normal.jpg', 
    'subject11.happy.jpg', 'subject14.happy.jpg', 'subject14.sad.jpg']

    
    # find eigenface coeffiecients of test images
    #test1 = plt.imread('Testing/subject14.sad.jpg')
    #test1_vector = np.array(test1, dtype='float64').flatten()

    for i in range(len(test_image_names)):
        test1 = plt.imread(testing_path+test_image_names[i])
        test1_vector = np.array(test1, dtype='float64').flatten()

        plt.subplot(2,4,1+i)
        plt.imshow(test1, cmap='gray')
        plt.tick_params(labelleft='off', labelbottom='off', bottom='off',top='off',right='off',left='off', which='both')
    plt.suptitle("Testing Images")
    plt.show()

    # subtract mean face from input image
    #test1_norm = np.subtract(test1_vector, mean_face)
    #print("Input image shape: ", test1_norm.T.shape)
    succ = 0
    k = 0
    print("\n")
    print("Eigenface Coefficients for Test Images: ")
    for k in range(len(test_image_names)):
        test1 = plt.imread(testing_path+test_image_names[k])
        test1_vector = np.array(test1, dtype='float64').flatten()
        test1_norm = np.subtract(test1_vector, mean_face)
        #print("Input image shape: ", test1_norm.T.shape)
   
        # compute projection
        j = 0
        omega = np.matmul(U.T, test1_norm.T)
        print("Eigenface coefficient for test image %d:" %k, "\n", omega)
    
        # find distance between input image proj and training projections
        distArr = []
        for i in projections:
            dist = np.linalg.norm(omega - i)
            #print("dist: ", dist)
            distArr.append(dist)
        minIndex = np.argmin(distArr)
        #print("result @ ", minIndex)
        if train_image_names[minIndex][0:9] == test_image_names[k][0:9]:
            succ+=1

        # print image that is the result
        res_img = plt.imread(dataset_path + train_image_names[minIndex])
        #print("Showing Algorithm Results...\n")
        plt.subplot(2,4,1+k)
        plt.imshow(res_img, cmap='gray')
        plt.tick_params(labelleft='off', labelbottom='off', bottom='off',top='off',right='off',left='off', which='both')
    plt.suptitle("Eigenface Recognition Results")
    plt.show()

    # get accuracy 
    print("Accuracy: ", round(float(succ/len(test_image_names)*100), 2), "%\n")


# call to run Eigenface Recognition Algorithm
main()