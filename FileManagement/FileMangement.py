# author @Arya Kulkarni

import os
import shutil
from os import listdir
from os.path import isfile, join

def sortFiles(myPath):
    # get into Downloads folder and then sort files
    # create a list of files
    files = os.listdir(myPath)
    for f in files:
        print(f)
        filename, file_extension = os.path.splitext(f)
        print(file_extension)
        print("===================", filename)



my_path = '/Users/aryakulkarni/Downloads/'
sortFiles(my_path)
