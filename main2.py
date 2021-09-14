# 数独の画像から答えを出力
# 普通、クロス、ジグソー、クロスジグソーに対応

# 画像を認識する

import cv2
import numpy as np

def scale_to_width(img, width):
    """幅が指定した値になるように、アスペクト比を固定して、リサイズする。
    """
    h, w = img.shape[:2]
    height = round(h * (width / w))
    dst = cv2.resize(img, dsize=(width, height))

    return dst

# 画像からテキストデータを抽出
def image_to_data(img):
    width, height = img.shape[1], img.shape[0]
    tableX, tableY = 5, 85
    squareLength = 82
    imageNumberRaw = [cv2.imread("number/"+str(i)+".png",0) for i in range(1,10)]
    imageNumber = [scale_to_width(imageNumberRaw[i], int((width-150)/9)) for i in range(9)]
    newTable = [[0 for i in range(9)] for j in range(9)]
    for i in range(1,10):
        res = cv2.matchTemplate(img, imageNumber[i-1], cv2.TM_CCOEFF_NORMED)
        ys, xs = np.where(res > 0.9)
        for x,y in zip(xs, ys):
            posX = int((x+squareLength/2-tableX)/squareLength)
            posY = int((y+squareLength/2-tableY)/squareLength)
            if newTable[posY][posX] == 0:
                newTable[posY][posX] = i
    return newTable

imageEntire = cv2.imread("image/IMG_8338.PNG",0)
print(image_to_data(imageEntire))


        



cv2.imshow("fae",imageEntire)
cv2.waitKey(0)
cv2.destroyAllWindows()