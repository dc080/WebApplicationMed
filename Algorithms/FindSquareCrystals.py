import os.path
import time

import cv2
import numpy as np


class FindSquareCrystals:
    image = []
    grayImg = []
    light = 150
    dark = 200
    median = 0
    path = ""
    contours = []

    def __init__(self):
        self.image = []
        self.grayImg = []
        self.light = 150
        self.dark = 200
        self.median = 0
        self.path = ""
        self.contours = []

    def loadImage(self, pic): # Загрузка изображения и превращение его в массив цветов?
        self.image = open(pic, 'rb')
        self.path = os.path.dirname(pic)
        chunk = self.image.read()
        chunkArr = np.frombuffer(chunk, dtype=np.uint8)
        self.image = cv2.imdecode(chunkArr, cv2.IMREAD_COLOR)

    def editImage(self):
        img = self.image.copy()
        img = cv2.bitwise_not(img)  # Реверс цветов изображения
        imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Приведение изображения к HSV

        lightBlack = (0, 0, self.light)  # Цвет темной границы
        darkBlack = (0, 0, self.dark)  # Цвет светлой границы

        mask = cv2.inRange(imgHsv, lightBlack, darkBlack)  # Расчет маски на изображении

        lightWhite = (0, 0, 100)  # Ещё одни границы, нафига - я не понимаю
        darkWhite = (0, 0, 74)

        maskWhite = cv2.inRange(imgHsv, lightWhite, darkWhite)  # Расчет второй маски на изображении

        result = cv2.bitwise_and(img, img, mask=(mask + maskWhite))  # Применение двух масок на исходное изображение

        self.grayImg = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)  # Приведение изображения к оттенкам серого

        self.median = np.median(self.grayImg)  # Поиск среднего значения серого
        ret, thresh = cv2.threshold(self.grayImg, 127, 255, 0) # ???
        self.grayImg = cv2.bilateralFilter(thresh, 11, 41, 21)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed = cv2.morphologyEx(self.grayImg, cv2.MORPH_CLOSE, kernel)

        contours = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, # Поиск контуров
            cv2.CHAIN_APPROX_NONE)
        self.contours = self.grabContours(contours) # Выделение массива контуров через дополнительную функцию

        contourImage = closed.copy() # Создание измененного изображения

        cv2.fillPoly(contourImage, self.contours, color=(150, 50, 10)) # Закрашивание контуров
        cv2.imwrite(os.path.join(self.path, "tempimg.jpg"), contourImage) # Запись контуров в файл.

    def grabContours(self, contours):
        if len(contours) == 2:
            return contours[0]
        elif len(contours) == 3:
            return contours[1]

    def resolveSquare(self): # Расчет общей площади контуров
        square = 0
        for contour in self.contours:
            area = cv2.contourArea(contour)
            if area != 0:
                square += area
        return square

    def runThisShit(self, pic, light, dark): # Отладочная функция, которую мне надо будет удалить
        #startTime = time.time()
        self.loadImage(pic)
        self.light = light
        self.dark = dark
        self.editImage()
        return self.resolveSquare()
        #print(time.time() - startTime)
