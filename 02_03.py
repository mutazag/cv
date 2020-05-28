# %%
import numpy as np
import cv2
import os
import sys

# %%
os.getcwd()
# %%
os.chdir('c:\\git\\cv\\images\\Ch02\\02_03 Begin')

# %%
print(np.__version__)
print(cv2.__version__)
# %%
# create a zeros array 
black = np.zeros([150,200,1], 'uint8') # 150x200 black and white all black 
# cv2.namedWindow('black', cv2.WINDOW_NORMAL)
cv2.imshow('black', black)



# %%
ones = np.ones([150,200,3], 'uint8')
cv2.imshow('ones', ones)


# %% 
white = np.ones([150, 300, 3], 'uint16')
white *= (2**16-1) # scaling the values up to maximum value of 2^16
cv2.imshow('white', white)

# %% 
color = ones.copy()
color[:,:] = (255,255,255)
color[75,:,:] = (124,124,124)
color[:,99,:] = (0,0,0)
color[:,149,:] = (0,0,0)
color[75:105, 99:149:] = (0,0,220)
cv2.imshow('color',color)
# %%
cv2.waitKey(0)
cv2.destroyAllWindows()