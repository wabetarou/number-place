import cv2,sys
import numpy as np

class square:
    def __init__(self,pos):
        self.pos = pos
        self.number = -1
        self.candidate = [0,1,2,3,4,5,6,7,8]
        self.boxes = []

    # 数字を入力。所属するbox全て更新
    def insert(self, number):
        self.number = number
        if number != -1:
            self.candidate = [number]
        self.update()

    # 候補から数字を消す。最後の候補か確認
    def remove(self, number):
        if number in self.candidate:
            self.candidate.remove(number)
            self.confirm()

    # 候補が一つの場合数字を確定する。その後boxに対して情報を与える
    def confirm(self):
        if len(self.candidate) == 1:
            self.insert(self.candidate[0])
        elif len(self.candidate) == 0:
            print("候補がありません")
        else:
            # print(len(self.candidate))
            pass

    # 数字が確定した後の処理
    def update(self):
        if self.number != -1:
            for box in self.boxes:
                box.update(self)
    
class box:
    def __init__(self,squares):
        # [[1,1],[1,2],...,[1,9]]
        self.unused = [i for i in range(9)]
        self.squares = squares
        for square in self.squares:
            square.boxes.append(self)

    # 一つの確定マスに対してそれ以外の全てのマスを候補を更新
    def update(self,square):
        if square.number in self.unused:
            self.unused.remove(square.number)
        for each_square in self.squares:
            if each_square.number != square.number:
                each_square.remove(square.number)

    # boxの中で候補が一つだけなら確定
    # 候補が二つある場合同じ候補があるか探す。あったら他を削除
    def search(self):
        numberFreq = [0] * 9
        for number in range(9):
            for square in self.squares:
                if number in square.candidate:
                    numberFreq[number-1] += 1
        for number, freq in enumerate(numberFreq):
            if freq == 1:
                for square in self.squares:
                    if square.number == -1 and number in square.candidate:
                        square.insert(number)
                        break
        # elif 2 in numberFreq:
        #     indexes = [i for i,freq in enumerate(numberFreq) if freq == 2]
        #     numbersIndex = []
        #     numbers = []
        #     flag = False
        #     for i in indexes:
        #         for j in indexes:
        #             if j != i and self.squares[j].candidate == self.squares[i].candidate:
        #                 numbersIndex = [i,j]
        #                 numbers = [self.squares[i].candidate[k] for k in range(2)]
        #                 flag = True
        #                 break
        #         if flag: break
        #     if flag:
        #         for i, square in enumerate(self.squares):
        #             if i in numbersIndex:
        #                 square.candidate = [numbers[k] for k in range(2)]
        #             else:
        #                 for number in numbers:
        #                     if number in square.candidate:
        #                         square.remove(number)
            
class entire:
    def __init__(self):
        self.squares = [[square([i,j]) for j in range(0,9)] for i in range(0,9)]
        self.boxes = []
        # 列、行
        for i in range(0,9):
            self.boxes.append(box([self.squares[i][j] for j in range(0,9)]))
        for j in range(0,9):
            self.boxes.append(box([self.squares[i][j] for i in range(0,9)]))
        # 通常ブロック
        for i in range(0,9):
            self.boxes.append(box([self.squares[i//3*3+j//3][i%3*3+j%3] for j in range(0,9)]))
        # クロス
        # self.boxes.append(box([self.squares[i][i] for i in range(0,9)]))
        # self.boxes.append(box([self.squares[i][8-i] for i in range(0,9)]))



    # 今あるデータを挿入
    def insert(self,number,i,j):
        self.squares[i][j].insert(number)

    # 今あるデータをもとに走査。全てのboxに対して
    def update(self):
        for box in self.boxes:
            for square in box.squares:
                square.update()

    def search(self):
        for box in self.boxes:
            box.search()

    def show(self):
        for i in range(0,9):
            for j in range(0,9):
                print(self.squares[i][j].number+1,end=" ")
            print()

    # 正しいかどうかcheck
    def checkCorrect(self):
        flag = True
        for box in self.boxes:
            unused = [i for i in range(1,10)]
            for square in box.squares:
                if square.number in unused:
                    unused.remove(square.number)
                else:
                    flag = False
            if len(unused) != 0:
                flag = False
        return flag


    def end(self):
        for row in self.squares:
            for square in row:
                if square.number == -1:
                    return False
        return True

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

def show(table):
    for i in range(0,9):
            for j in range(0,9):
                print(table[i][j],end=" ")
            print()
# 画像データ
imageEntire = cv2.imread("image/IMG_8338.PNG",0)
table = image_to_data(imageEntire)

# テキストデータ
# table = [[int(num) for num in list(line) if num != "\n"]
#             for line in open('data/test51.txt','r')]

show(table)
en = entire()
for i in range(0,9):
    for j in range(0,9):
        if table[i][j] != 0:
            en.insert(table[i][j]-1, i,j)
print()
# print([[en.squares[8][0].boxes[i].squares[j].pos for j in range(9)] for i in range(3)])
time = 0
while(not en.end()):
    en.update()
    en.search()
    time+=1
    if time > 100: break
en.show()