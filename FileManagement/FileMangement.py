# author @Arya Kulkarni

import os
import shutil
from os import listdir
from os.path import isfile, join

# functions to sort files
def sortFiles(myPath):
    # get into Downloads folder and then sort files
    # create a list of files
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    file_extentions=[]
    folder_dict={}

    for file in files:
        filetype = file.split('.')[1]
        if filetype not in file_extentions:
            file_extentions.append(filetype)
            new_folder_name = mypath + '/' + filetype + '_folder'
            folder_dict[str(filetype)] = str(new_folder_name)
            if os.path.isdir(new_folder_name)==True:  #folder exists
                continue
            else:
                os.mkdir(new_folder_name)


    for file in files:
        src_path = mypath + '/' + file
        filetype = file.split('.')[1]
        if filetype in folder_dict.keys():
            dest_path = folder_dict[str(filetype)]
            shutil.move(src_path,dest_path)

    print(src_path + '>>>' + dest_path)

# main 
if __name__ == "__main__":
    mypath = '[your source path]'
    sortFiles(mypath)
