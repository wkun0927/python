#encoding=utf-8

import cv2 as cv
import matplotlib.pyplot as plt

if __name__ == '__main__':
    for k in range(2,1000):
        try:
            img=cv.imread("F:/PycharmProjects/CnkjProjects/zpzzq/images//"+str(k)+".jpg",0)
        except :
            continue

        ret, thresh1 = cv.threshold(img, 100, 255, cv.THRESH_BINARY)
        ret, thresh2 = cv.threshold(img, 100, 255, cv.THRESH_BINARY_INV)
        ret, thresh3 = cv.threshold(img, 100, 255, cv.THRESH_TRUNC)
        ret, thresh4 = cv.threshold(img, 100, 255, cv.THRESH_TOZERO)
        #ret, thresh5 = cv.threshold(img, 100, 255, cv.THRESH_TOZERO_INV)
        ret, thresh5 = cv.threshold(img, 0, 255, cv.THRESH_OTSU)
        
        #ret, thresh = cv.threshold(img, 100, 255, cv.THRESH_OTSU)

        titles = ['Original Image', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
        images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
        # i=0
        # for i in range(6):
        #     plt.subplot(2, 3, i + 1), plt.imshow(images[i], 'gray')
        #     plt.title(titles[i])
        #     plt.xticks([]), plt.yticks([])
        # plt.show()



