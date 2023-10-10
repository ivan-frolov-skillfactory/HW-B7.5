from random import randint

class Field:
    def __init__(self, hid = False, size = 6):
        self.size = size
        self.hid = hid        
        self.count = 0
        self.field = [ ["O"]*size for _ in range(size) ]        
        self.busy = []
        self.ships = []
    
    def add_ship(self, ship):
        for d in ship.fields:
            if self.out(d) or d in self.busy:
                raise FieldWrongShipGame()
        for d in ship.fields:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)
        
        self.ships.append(ship)
        self.contour(ship)


    def contour(self, ship, verb = False):    
        near = [
            (-1, -1), (-1, 0) , (-1, 1),
            (0, -1), (0, 0) , (0 , 1),
            (1, -1), (1, 0) , (1, 1)
        ]
        for d in ship.fields:
            for dx, dy in near:
                cur = Сomparison(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)
    
    def __str__(self):
        res = ""
        res += "  |  1  |  2  |  3  |  4  |  5  |  6  |"
        for i, row in enumerate(self.field):
            res += f"\n{i+1} |  " + "  |  ".join(row) + "  |"        
        if self.hid:
            res = res.replace("■", "O")
        return res
    
    def out(self, d):
        return not((0<= d.x < self.size) and (0<= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise ShotOutOfBounds()        
        if d in self.busy:
            raise RepeatInput()        
        self.busy.append(d) 
        for ship in self.ships:
            if d in ship.fields:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb = True)
                    print("Все корабли уничтожены!")
                    return False
                else:
                    print("Корабль подбит!")
                    return True        
        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False
    
    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)

class Game:
    player_1 = input('Введите имя. \n')
    def __init__(self, size = 6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True        
        self.ai = AI(co, pl)
        self.us = User(pl, co)
    
    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board
    
    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Field(size = self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Сomparison(randint(0, self.size), randint(0, self.size)), l, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except FieldWrongShipGame:
                    pass
        board.begin()
        return board


    def loop(self):
        num = 0
        while True:            
            print(f"{Game.player_1}, это Ваше игровое поле:")
            print(self.us.board)            
            print("Игровое поле ИИ:")
            print(self.ai.board)
            if num % 2 == 0: 
                repeat = self.us.move()
            else:          
                repeat = self.ai.move()
            if repeat:
                num -= 1
            
            if self.ai.board.defeat():
                print(f"{Game.player_1}, победа!")
                break
            
            if self.us.board.defeat():                
                print(f"Поражение!")
                break
            num += 1
            
    def start(self):
        self.loop()

class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property   
    def fields(self):
        ship_fields = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y
            if self.o == 0:
                cur_x += i
            elif self.o == 1:
                cur_y += i
            ship_fields.append(Сomparison(cur_x, cur_y))        
        return ship_fields
    
    def shooten(self, shot):
        return shot in self.fields  

class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy
    
    def ask(self):
        raise NotImplementedError()
    
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except FeaturesGame as e:
                print(e)

class AI(Player):
    def ask(self):
        d = Сomparison(randint(0,5), randint(0, 5))
        print(f"Мой ход: {d.x+1} {d.y+1}")
        return d

class User(Player):
    def ask(self):
        while True:
            cords = input(f"{Game.player_1}, Ваш ход:\n ").split()
            
            if len(cords) != 2:
                print(f"{Game.player_1}, введите две координаты хода через пробел:\n")
                continue            
            x, y = cords            
            if not(x.isdigit()) or not(y.isdigit()):
                print(f"{Game.player_1}, введите числа:\n")
                continue            
            x, y = int(x), int(y)            
            return Сomparison(x-1, y-1)
        
class FeaturesGame(Exception):
    pass

class ShotOutOfBounds(FeaturesGame):
    def __str__(self):
        return f"Выстрел за пределы поля!"
    
class RepeatInput(FeaturesGame):
    def __str__(self):
        return "Попадание уже было!"
    
class FieldWrongShipGame(FeaturesGame):
    pass

class Сomparison:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return f"Сomparison({self.x}, {self.y})"
    
game = Game()
game.start()