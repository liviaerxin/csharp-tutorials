#!/usr/bin/env python3

import os
import sys
import time
import traceback
import argparse

import numpy as np
import cv2
import pickle

class ImageFileConvertFlattenArrayClass(object):        
    """
    image file convertor to flatten array class
    """
    
    def __init__(self):
        pass
    
    def image_flatten_pixel_nparray_opencv(self, image_path_name, nparray_dimension = "1d", image_resize_factor=None):
        """
        resize and flatten the image from 1d to 2d array              
        :param image_path_name: image path and file name
        :param nparray_dimension: nparray dimension type
        :param image_resize_factor: image resize (reshape) factor
        """
        image_nparray = None
        try:
            image = cv2.imread(image_path_name, cv2.IMREAD_GRAYSCALE)
            image_height, image_width  = image.shape
            if image_resize_factor is not None:
                image_width_resize = int(image_width / image_resize_factor)
                aspect_ratio = image_height / image_width       
                image_height_resize = int(aspect_ratio * image_width_resize)
                 image_dimension = (image_width_resize,         
image_height_resize)                
                  image = cv2.resize(image, image_dimension, interpolation=cv2.INTER_AREA)
                image_width, image_height = image_width_resize, image_height_resize           
            image_nparray = np.fromstring(image.tobytes(), dtype=np.uint8)
            if (nparray_dimension == "1d"):
                image_nparray = image_nparray.reshape((1, image_width_resize * image_height_resize))
        except:
            exception_message = sys.exc_info()[0]
            print("An error occurred. {}".format(exception_message))
        return image_nparray
    
    def print_searchcv_result(self, classifier_model):  
        """
        print grid or randomized search cv results: best score and best parameters
        :param classifier_model: defined classifier model
        :return none
        """
        try:
            print("Scores:")  
            means = classifier_model.cv_results_["mean_test_score"]
            standard_deviations = classifier_model.cv_results_["std_test_score"]
            for mean, standard_deviation, parameter in zip(means, standard_deviations, classifier_model.cv_results_["params"]):
                mean = float("{0:0.3f}".format(mean))
                standard_deviation = float("{0:0.3f}".format(standard_deviation * 2))               
                print("mean:{} (std:+-{}) for {}".format(mean, standard_deviation * 2, parameter))
            print()    
            print("Best Score:")
            print(float("{0:0.3f}".format(classifier_model.best_score_)))    
            print()
            print("Best Parameters:")
            print(classifier_model.best_params_)
            print()    
        except:    
            exception_message = sys.exc_info()[0]
            print("An error occurred. {}".format(exception_message))

    def print_exception_message(self, message_orientation="horizontal"):
        """
        print full exception message
        :param message_orientation: horizontal or vertical
        :return None
        """
        try:
            exc_type, exc_value, exc_tb = sys.exc_info()           
            file_name, line_number, procedure_name, line_code = traceback.extract_tb(exc_tb)[-1]      
            time_stamp = " [Time Stamp]: " + str(time.strftime("%Y-%m-%d %I:%M:%S %p"))
            file_name = " [File Name]: " + str(file_name)
            procedure_name = " [Procedure Name]: " + str(procedure_name)
            error_message = " [Error Message]: " + str(exc_value)       
            error_type = " [Error Type]: " + str(exc_type)                   
            line_number = " [Line Number]: " + str(line_number)               
            line_code = " [Line Code]: " + str(line_code)
            if (message_orientation == "horizontal"):
                print( "An error occurred:{};{};{};{};{};{};{}".format(time_stamp, file_name, procedure_name, error_message, error_type, line_number, line_code))
            elif (message_orientation == "vertical"):
                print( "An error occurred:\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(time_stamp, file_name, procedure_name, error_message, error_type, line_number, line_code))                    
        except:
            pass
            
def main(image_path_name):
    """
    main function start program
    :param image_path_name: image path and file name
    """
    try:
        # instantiate the object for image array flatten class
        image_array_flatten_class = ImageFileConvertFlattenArrayClass()

        # check is image path file name exists
        if (os.path.exists(image_path_name) == False):
            print("File {} not found.".format(image_path_name))
            exit()

        # resize and flatten the image from 2d to 1d array                   
        nparray_dimension = "1d"
        image_resize_factor = 10
        image_1d_nparray = image_array_flatten_class.image_flatten_pixel_nparray_opencv(image_path_name, nparray_dimension, image_resize_factor)
        # create the data frame
        X_real = image_1d_nparray

        # data frame normalization  
        X_min = image_1d_nparray.min()
        X_max = image_1d_nparray.max()
        X_real = (X_real.astype("float32") - X_min) / (X_max - X_min)
        # open and close the mlp classifier pickle model
        project_directory_path = os.path.dirname(os.path.realpath(__file__))                   
        mlp_classifier_model_pkl = open(os.path.join(project_directory_path, "image_classification.pkl"), "rb")                                    
        mlp_classifier_model_file = pickle.load(mlp_classifier_model_pkl)  
        mlp_classifier_model_pkl.close()         

        # run the predict method and validate for image category 1 or 0
        y_predict_file = mlp_classifier_model_file.predict(X_real)
        if y_predict_file == 1:
            print("1")
        else:
            print("0")
    except:
        image_array_flatten_class.print_exception_message()
            
# main top-level start program
if __name__ == '__main__':   
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("-image_path_name")
    arguments = arg_parse.parse_args()
    image_path_name = arguments.image_path_name    
    main(image_path_name)