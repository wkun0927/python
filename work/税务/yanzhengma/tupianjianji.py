#encoding-utf-8

import cv2

img=cv2.imread('yzm.png')
print(img.shape)
img_mod=img[746:776,1040:1110]
cv2.imwrite("img_mod.png",img_mod)
