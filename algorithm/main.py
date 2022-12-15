import os
import cv2 as cv
import fire
import numpy as np
import pylab as pl
from PIL import Image, ImageOps
from matplotlib import pyplot as plt
#from core import *
from core import ImageLoad


class Analysis(object):

    def FractAnalysis(self, pic):
        name = os.path.basename(pic)
        path = os.path.dirname(pic)

        img = cv.imread(pic, cv.IMREAD_UNCHANGED)  # читаем

        img = cv.medianBlur(img, 5)  # размытие
        img_grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # в серый
        th3 = cv.adaptiveThreshold(img_grey, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 5, 10)  # адаптивный порог цвета
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 1))
        closed = cv.morphologyEx(th3, cv.MORPH_OPEN, kernel)
        closed = cv.erode(closed, None, iterations=1)
        closed = cv.dilate(closed, None, iterations=1)
        contours, hierarchy = cv.findContours(closed.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)  # находим контура
        img_contours = np.zeros(img.shape)  # добавляем контуры в лист
        cv.drawContours(img_contours, contours, -1, (255, 255, 255), 1)  # рисуем контуры
        cv.imwrite(os.path.join(path, 'contours.jpg'), img_contours)  # сохраняем как картинку # Реверснутая картинка?
        img = Image.open(os.path.join(path, 'contours.jpg'))  # делаем реверс цвета
        inverted_image = ImageOps.invert(img)
        inverted_image = inverted_image.convert('1')
        inverted_image.save('img.png') # Сохраняется изображение img.png в папку, откуда был запущен код
        image = pl.imread('img.png')  #читаем изображение, создаем массив
        ax = plt.gca()  # оси

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
            xt = ax.set_xticks(xticks)
            yt = ax.set_yticks(yticks)

            n = 0  # цвет и количество квадратов
            for i in range(len(xticks) - 1):
                for j in range(len(yticks) - 1):
                    l = xticks[i]
                    m = yticks[j]
                    for (x, y) in [(x, y) for x in range(xticks[i], xticks[i + 1], 1) for y in
                                   range(yticks[j], yticks[j + 1], 1)]:
                        if image[y, x] == 0:
                            n += 1
                            break
                        else:
                            continue
            N.append(n)

        # ############################## Шаг 4: Нахождение box dimension
        Polyfit = np.polyfit(np.log(scales), np.log(N), 1)
        #print('Соответствующий многочлен от N равен:', Polyfit[0], 'x + ', Polyfit[1], '\n') # Я так понимаю, это была отладочная информация
        #print('Следовательно, box dimension равен ', round(-Polyfit[0], 3), '.\n')

        # ############################## Шаг 5: График линейной регрессии
        plt.clf()
        pl.plot(np.log(scales), np.log(N), 'o', mfc='none')
        pl.plot(np.log(scales), np.polyval(Polyfit, np.log(scales)))
        pl.xlabel('log $\\ delta$')
        pl.ylabel('log N')
        plt.savefig(os.path.join(path, 'graf.png'), dpi = 500) # Создание картинки graf.png (Нужен ли другой формат?)
        print('Значение фрактальной размерности', round(-Polyfit[0], 3), '\n') # Упаковать в string и возвращать как результат функции???
        with open("test.txt", "a") as obj_file: # Нужен ли данный файл в принципе? Он его не перезаписывает, а добавляет туда
            print(name, " - ", round(-Polyfit[0], 3), "\n", file=obj_file)
        pass

    def SquareNLinesAnalysis(self, pic, light, dark):
        img = ImageLoad()
        img.auto_canny(pic)
        img.dark_b = dark
        img.light_b = light
        img.findCanny()
        print('Общая площадь: ', img.ploshad)
        print('Массив:\n', str(img.area_arr))
        pass
        #return 0;

if __name__ == '__main__':
    fire.Fire(Analysis)