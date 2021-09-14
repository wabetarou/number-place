import sys

# 数独のテキストデータから答えを出力
# 普通、クロスに対応

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
            # if self.pos == [5,2]:
            #     print(self.candidate)
            #     print(self.candidate[0])
            self.candidate.remove(number)
            self.confirm()

    # 候補が一つの場合数字を確定する。その後boxに対して情報を与える
    def confirm(self):
        if len(self.candidate) == 1:
            self.number = self.candidate[0]
            for box in self.boxes:
                box.update(self)
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
    def search(self):
        for number in self.unused:
            candidate_square = None
            candidate_flag = True
            for square in self.squares:
                if number in square.candidate:
                    if candidate_square is None:
                        candidate_square = square
                    else:
                        candidate_flag = False
            if candidate_flag and candidate_square is not None:
                candidate_square.insert(number)
            
                

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
        self.boxes.append(box([self.squares[i][i] for i in range(0,9)]))
        self.boxes.append(box([self.squares[i][8-i] for i in range(0,9)]))

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

    def end(self):
        for row in self.squares:
            for square in row:
                if square.number == -1:
                    return False
        return True

table = [[int(num) for num in list(line) if num != "\n"]
            for line in open('data/testx51.txt','r')]

en = entire()
for i in range(0,9):
    for j in range(0,9):
        if table[i][j] != 0:
            en.insert(table[i][j]-1, i,j)
en.show()
print()
# print([[en.squares[8][0].boxes[i].squares[j].pos for j in range(9)] for i in range(3)])
time = 0
while(not en.end()):
    en.update()
    en.search()
    time+=1
    if time > 100: break
en.show()
