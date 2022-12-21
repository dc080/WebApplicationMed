import cv2
import numpy as np
import os
from numpy import array, sqrt


def click_exit():
    exit(0)


class ImageLoad:
    image = []
    grayImg = []
    s = 0.33
    v = 0
    light_b = 200
    dark_b = 150
    area_arr = []
    lengh_arr = []
    ploshad = 0

    def grab_contours(cnts):
        if len(cnts) == 2:
            return cnts[0]
        elif len(cnts) == 3:
            return cnts[1]

    def auto_canny(self, path):
        self.area_arr.clear()
        self.image = open(path, 'rb')
        chunk = self.image.read()
        chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
        self.image = cv2.imdecode(chunk_arr, cv2.IMREAD_COLOR)
        self.findCanny()

    def findCanny(self):
        self.ploshad = 0
        img = self.image.copy()
        img = cv2.bitwise_not(img)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        light_black = (0, 0, self.light_b)
        dark_black = (0, 0, self.dark_b)
        mask = cv2.inRange(img_hsv, light_black, dark_black)

        light_white = (0, 0, 100)
        dark_white = (0, 0, 74)

        mask_white = cv2.inRange(img_hsv, light_white, dark_white)

        result = cv2.bitwise_and(img, img, mask=(mask + mask_white))

        self.grayImg = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)
        self.grayImg = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

        self.v = np.median(self.grayImg)  # Ищет среднее значение серого для Canny
        ret, thresh = cv2.threshold(self.grayImg, 127, 255, 0)
        # self.grayImg = cv2.medianBlur(thresh, 3 )
        self.grayImg = cv2.bilateralFilter(thresh, 11, 41, 21)

        self.area_arr.clear()
        lower = int(max(0, self.v - self.v * 0.3))
        upper = int(min(255, (1.0 + self.s) * self.v))

        # edged = cv2.Canny(self.grayImg, lower, upper)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed = cv2.morphologyEx(self.grayImg, cv2.MORPH_CLOSE, kernel)

        cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_NONE)
        cnts = ImageLoad.grab_contours(cnts)

        contour_image = closed.copy()
        area = 0
        for c in cnts:
            area = cv2.contourArea(c)
            cv2.drawContours(contour_image, [c], 0, (150, 50, 10), 1)
            if area != 0:
                # cm_ar = (area / 1428.46202)/40
                # cm_ar = (area / 37.938105)/40
                self.ploshad += area  # cm_ar
                # cm_ar = str(cm_ar)

                str_area = str(area) + "px"  # Перевел все только в пиксели
                self.area_arr.append(str_area)  # Заношу в массив

                # cm_ar += "см^2/" + str(area) + "px\n"
                # self.area_arr.append(cm_ar)
                # print((area / 37.938105)/40 , "см^2/", area, "px")

        cv2.fillPoly(contour_image, cnts, color=((150, 50, 10)))
        # cv2.imshow("area", contour_image)
        k = cv2.waitKey(0)
        if k == 27:
            cv2.destroyAllWindows()
        cv2.imwrite(os.path.join('', 'tempimg.jpg'), contour_image)
        return (self.ploshad)  # Возвращает итоговое значение площади
