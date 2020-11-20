# %%
import numpy as np
import cv2
import os
import sys

# %%
os.getcwd()
# %%
os.chdir('c:\\git\\cv\\images\\Ch02\\02_01 Begin')

# %%
print(np.__version__)
print(cv2.__version__)


# %% 
img = cv2.imread('opencv-logo.png')

# initalise a named window

cv2.namedWindow('image', cv2.WINDOW_NORMAL)

cv2.imshow('image', img)

cv2.waitKey(0)
# %%

cv2.imwrite('output.jpg', img)

# %%
