from sense_hat import SenseHat
import time

import numpy as np

### some test methods to use numpy array to represent
### the led matrix as numeric matrix
### this makes it much more easier to maipulate the rgb matrix
### for instance darken or lighten the colors by simply multiplying

def darken_matrix_rel(matrix):
    return ((matrix*0.9).astype(int))

def lighten_matrix_rel(matrix):
    matrix = (matrix*1.1).astype(int)
    matrix[matrix > 255] = 255
    return (matrix)

def fade_in_out(matrix,rounds):
    displayMatrix(matrix)
    for r in range(rounds):
        for i in range(15):    
            matrix = darken_matrix_rel(matrix)
            displayMatrix(matrix)
            time.sleep(0.02)
            #print(i)
        for i in range(18):    
            matrix = lighten_matrix_rel(matrix)
            displayMatrix(matrix)
            time.sleep(0.02)
            #print(i)
                
# take the numpy matrix and transfrom it
# into a list of rgb values to pass to the sensehat
def displayMatrix(matrix):
    # back to list of rgb values
    display = matrix.tolist()
    # Flatten the list one more layer
    display = [item for sublist in display for item in sublist]
    sense.set_pixels(display)
    

sense = SenseHat()

height = 8
width = 8
depth = 3

#matrix = np.zeros([height,width,depth],dtype=np.uint8)

# read the current pixels and transform it to a 3d matrix
matrix = np.array(sense.get_pixels(),dtype=np.uint8).reshape(8,8,3)
# change color
matrix[:,:] = [255,100,0]


#print(matrix)
#print((matrix*0.5).astype(int))
displayMatrix(matrix)
# color the 2nd row white
matrix[1:2,:] = [128,255,128]
# color the 2 col white
matrix[:,1:2] = [128,128,255]


fade_in_out(matrix,2)

background = [255,34,34]
matrix[:,:] = background
displayMatrix(matrix)

# make some animations using a sliding bar of white
for i in range(30):
    for j in range(8):
        matrix[:,:] = background
        matrix[j:(j+1),:] = [255,255,255]
        displayMatrix(matrix)
        time.sleep(0.05)
        
    for j in range(8):
        matrix[:,:] = background
        matrix[(8-j):(8-j+1),:] = [255,255,255]
        displayMatrix(matrix)
        time.sleep(0.05)
    