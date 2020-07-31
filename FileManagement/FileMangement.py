import os
import shutil
from os import listdir
from os.path import isfile, join

# functions to sort files
def sortFiles(myPath):
    file_extension_list = []
    folder_path_dict = {}
    # get files on path
    files = [f for f in listdir(myPath) if isfile(join(myPath, f))]
    for f in files:
        file_extension = f.split(".")[1]
        #print(file_extension) 
        if file_extension not in file_extension_list:
            file_extension_list.append(file_extension)
            #create new path
            new_folder_path = myPath + '/' + file_extension + '_folder'
            folder_path_dict[str(file_extension)] = str(new_folder_path)
        
            # check if folder exists
            if os.path.isdir(new_folder_path) == True:
                continue #do nothing
            else:
                os.mkdir(new_folder_path)

    for f in files:
        source_path = myPath + '/' + f
        file_extension = f.split(".")[1]
        if file_extension in folder_path_dict.keys():
            destination = folder_path_dict[str(file_extension)]
            shutil.move(source_path, destination)
    
    print(source_path + ' to ' + destination)

# main 
if __name__ == "__main__":
    mypath = '[your file path]'
    sortFiles(mypath)
