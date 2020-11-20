# %%
import numpy as np
import cv2
import os
import sys

# %%
os.getcwd()
# %%
os.chdir('c:\\git\\cv\\images\\Ch02\\02_02 Begin')

# %%
print(np.__version__)
print(cv2.__version__)

# %% 
img = cv2.imread('opencv-logo.png', 1)

# %%
img

# %%
type(img)

# %%
print('number of rows ', len(img))
print('number colmuns ', len(img[0]))
print(img.shape)
# %%
img[:,:,0]


# %%
