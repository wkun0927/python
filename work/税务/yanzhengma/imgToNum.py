#encoding=utf-8

import pytesseract
import cv2
for i in range(1,10):
    # cv2.namedWindow('show', cv2.WINDOW_NORMAL)  # 创建窗口
    # cv2.resizeWindow("show", 200, 100)  # 调整窗口大小
    img=cv2.imread(str(i)+'.jpg',0)
    ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    text=pytesseract.image_to_string(thresh1)
    print(text)
    # cv2.imshow('show', thresh1)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()