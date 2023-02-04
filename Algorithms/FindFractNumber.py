import os

import cv2
import numpy as np
from matplotlib import pyplot as plt

class FindFractNumber:
    def resolveFractNumber(self, pic):
        path = os.path.dirname(pic)
        img = cv2.imread(pic, cv2.IMREAD_UNCHANGED)  # читаем

        img = cv2.medianBlur(img, 5)  # размытие
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # в серый
        th3 = cv2.adaptiveThreshold(grayImg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5,
                                    10)  # адаптивный порог цвета
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        closed = cv2.morphologyEx(th3, cv2.MORPH_OPEN, kernel)
        closed = cv2.erode(closed, None, iterations=1)
        closed = cv2.dilate(closed, None, iterations=1)
        contours, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # находим контура
        imgContours = np.zeros(img.shape)  # добавляем контуры в лист
        cv2.drawContours(imgContours, contours, -1, (255, 255, 255), 1)  # рисуем контуры
        imgContours = imgContours.astype(np.uint8)
        image = cv2.bitwise_not(imgContours)

        # #############################  Шаг 2: Создание списка масштабов
        scales = []
        scales = [int(min(image.shape[1], image.shape[0]) / l) for l in range(3, 100, 2)]
        scales = list(dict.fromkeys(scales))
        for i in range(len(scales)):
            if scales[i] == 1:
                scales.remove(scales[i])

        # ############################## Шаг 3: Нарисовать сетку, закрасить и посчитать кол-во закрашенных ячеек
        N = []
        for k in scales:  # Сетка
            xticks = np.arange(0, image.shape[1], k)
            yticks = np.arange(0, image.shape[0], k)
            n = 0  # цвет и количество квадратов
            for i in range(len(xticks) - 1):
                for j in range(len(yticks) - 1):
                    for (x, y) in [(x, y) for x in range(xticks[i], xticks[i + 1], 1) for y in
                                   range(yticks[j], yticks[j + 1], 1)]:
                        if (image[y, x] == 0).any():
                            n += 1
                            break
                        else:
                            continue
            N.append(n)

        # ############################## Шаг 4: Нахождение box dimension
        Polyfit = np.polyfit(np.log(scales), np.log(N), 1)

        # ############################## Шаг 5: График линейной регрессии
        #plt.clf()
        #plt.plot(np.log(scales), np.log(N), 'o', mfc='none')
        #plt.plot(np.log(scales), np.polyval(Polyfit, np.log(scales)))
        #plt.xlabel('log $\\ delta$')
        #plt.ylabel('log N')
        #plt.savefig(os.path.join(path, 'graf.png'), dpi=500)  # Создание картинки graf.png

        return str(round(-Polyfit[0], 3)) + '\n'  # Упаковка в String и вывод фрактмальная размерность
