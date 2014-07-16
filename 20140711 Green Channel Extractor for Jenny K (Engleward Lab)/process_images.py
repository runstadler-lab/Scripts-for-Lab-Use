"""
Author: Eric J. Ma, for Jenny Kay (Engleward Lab)
Affiliation: Massachusetts Institute of Technology

Script Requirements:
-	Python (version 2.7.2 or higher)
-	Python Imaging Library (PIL)
-	scikit-image

Purpose of this script:
- 	Jenny's images have been stored with full RGB, though only the green channel is visible.
-	This script will extract only the Green channel and save it separately.
"""


from skimage.io import imread, imshow, imsave
from os import listdir, getcwd

#################### BEGIN HELPER FUNCTIONS ###################################
def is_extension(filename, extension):
    """
    This function takes in a file name (of type string), and returns 
    Boolean whether it ends in the extension specified (type string)
    """
    
    split = filename.split('.')
    if split[-1] == extension:
        return True
    else:
        return False
#################### END HELPER FUNCTIONS #####################################

if __name__ == "__main__":

    # Get the filenames present in the directory
    filenames = listdir(getcwd())

    # Iterate over all the files that are JPG in extension,
    # save just the green channel (channel "1" in R(0), G(1), B(2))
    for f in filenames:
        if is_extension(f, 'jpg'):
            fname = f.split('.')[0]
            newfname = fname + '_processed.jpg'
            
            
            imsave(newfname, imread(f)[:,:,1]) 
            #Green is on channel 1         ^
            #							   |
            #RGB data is stored in 3rd dimension of image matrix.

