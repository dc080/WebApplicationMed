import cv2
import numpy as np
import math
import os

class DrawLines:
    length_l = 0
    length_arr = []

    def drawLine(self, path, firstPoint, secondPoint, savePath):

        img = open(path, 'rb')
        chunk = img.read()
        chunkArr = np.frombuffer(chunk, dtype=np.uint8)
        img = cv2.imdecode(chunkArr,cv2.IMREAD_COLOR)
        height, width, _ = img.shape
        imgShape = np.array([width, height])
        firstPoint = np.array(firstPoint)
        secondPoint = np.array(secondPoint)
        firstPoint = np.round(firstPoint * imgShape, 0).astype(int)
        secondPoint = np.round(secondPoint * imgShape, 0).astype(int)
        self.length_l = math.hypot(firstPoint[0] - secondPoint[0], firstPoint[1] - secondPoint[1])
        cv2.line(img, firstPoint, secondPoint, (0,0,255), 2)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, f'length: {round(self.length_l, 3)}', (secondPoint[0]+15, secondPoint[1]+25), font,
                    0.6, (180,130,70),2, cv2.LINE_AA)
        self.length_arr.append(round(self.length_l, 3))
        cv2.imwrite(savePath, img)
        return img

    def clearLengthArr(self):
        if(len(self.length_arr) != 0):
            self.length_arr.clear()
