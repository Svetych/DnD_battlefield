# -*- coding: utf-8 -*-
import Consts as const

from enum import Enum
from math import *

OCCUPIED = Enum('OCCUPIED', 'barrier dt terrain', start = 1)
FIGURE = Enum('FIGURE', 'l s cu co cy', start = 0)
GROUPS = ["silver", "brown", "gold", "azure", "green", "snow"]
# figure orientation: {orientation : (di, dj)}
ORIENT = {'n': (-1,0), 'ne': (-1,1), 'e': (0,1), 'se': (1,1),
          's': (1,0), 'sw': (1,-1), 'w': (0,-1), 'nw': (-1,-1)}


class Token():
    def __init__(self, x, y, size = 1, color = "red", group = GROUPS[0],
                 name = 'Noname', speed = 30, hp = 10, ac = 10, initiative = 10):
        self.ID = 0
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.group = group
        
        self.name = name
        self.speed = speed
        self.hp = hp
        self.ac = ac
        self.initiative = initiative
    
    # поменять координаты фишки на сетке
    def change_coords(self, x, y):
        self.x = x
        self.y = y
    
    # посчитать координаты всех занимаемых фишкой клеток на поле
    def count_coords(self):
        res = []
        for i in range(self.size):
            for j in range(self.size):
                res.append((self.x+i, self.y+j))
        return res
    
    # получить словарь из значений полей
    def get_config(self):
        config = {}
        config['x'] = self.x
        config['y'] = self.y
        config['size'] = self.size
        config['color'] = self.color
        config['group'] = self.group
        config['name'] = self.name
        config['speed'] = self.speed
        config['hp'] = self.hp
        config['ac'] = self.ac
        config['initiative'] = self.initiative
                
        return config
    
    
class Field():
    def __init__(self, w = 30, h = 30, img = ''):
        self.width = w
        self.height = h
        self.image = img
        
        self.net = []
        for i in range(h):
            s = []
            for j in range(w):
                s.append(Cell())
            self.net.append(s)
    
    # поменять вид клетки (x, y) на o
    def change_cell(self, x, y, o):
        self.net[x][y].occupied = o
    
    # добавить фишку t на поле
    def add_token(self, t):
        for i, j in t.count_coords():
            self.net[i][j].token = t
            
    # удалить фишку t с поля
    def delete_token(self, t):
        for i, j in t.count_coords():
            self.net[i][j].token = None 
    
    # проверить, можно ли поставить фишку размера size на место (x, y)
    def check_cells(self, x, y, size):
        if x+size > self.height or y+size > self.width:
            return False
        for i in range(size):
            for j in range(size):
                if self.net[x+i][y+j].token or self.net[x+i][y+j].occupied == OCCUPIED.barrier:
                    return False
        return True
    
    # проверить, заденет ли фишка размера size и с (x, y) труднопроходимую клетку
    def check_terrain(self, x, y, size):
        for i in range(size):
            for j in range(size):
                if self.net[x+i][y+j].occupied == OCCUPIED.dt:
                    return True
        return False
    
    # получить массив словарей из значений полей каждой фишки на поле
    def make_config(self):
        configs = []
        tokens = set([])
        for i in range(self.height):
            for j in range(self.width):
                t = self.net[i][j].token
                if t and t.ID not in tokens:
                    tokens.add(t.ID)
                    configs.append(t.get_config())
        return configs
    
    # получить массив из фишек на поле
    def get_tokens(self):
        res = []
        for i in range(self.height):
            for j in range(self.width):
                t = self.net[i][j].token
                if t and t not in res:
                    res.append(t)
        return res
    
    # получить массив из координат фишек на поле
    def get_tokens_coords(self):
        res = []
        tokens = set([])
        for i in range(self.height):
            for j in range(self.width):
                t = self.net[i][j].token
                if t and t.ID not in tokens:
                    res.append((i, j))
                    tokens.add(t.ID)
        return res    
    

class Cell():
    def __init__(self):
        self.occupied = OCCUPIED.terrain
        self.token = None
    

class Figure():
    def __init__(self, h, w):
        self.max_height = h
        self.max_width = w
        
    # проверка выхода за границы при расчете координат области
    def check_borders(self, i, j):
        return i >= 0 and i < self.max_height and j >= 0 and j < self.max_width
    
    # перевести размер x в футах в клетки
    def get_true_size(self, x):
        return x // const.cell_foot_size

class Line(Figure):
    def __init__(self, m_h, m_w, l, w, o):
        super().__init__(m_h, m_w)
        
        self.length = l
        self.width = w
        self.orientation = o
        
    # рассчитать координаты области с началом в клетке с координатами (x,y)
    def count_coords(self, x, y):
        res = []
        dx, dy = ORIENT[self.orientation.get()]
        length, width = self.get_true_size(self.length.get()), self.get_true_size(self.width.get())
        if self.orientation.get() in ['n', 's']:
            for i in range(width):
                for j in range(length):
                    x_0, y_0 = x+j*dx, i+y+j*dy
                    if self.check_borders(x_0, y_0):
                        res.append((x_0, y_0))
        else:
            l = round(length/sqrt(2)) if self.orientation.get() in ['nw', 'sw', 'ne', 'se'] else length
            for i in range(width):
                for j in range(l):
                    x_0, y_0 = i+x+j*dx, y+j*dy
                    if self.check_borders(x_0, y_0):
                        res.append((x_0, y_0))

        return res

class Sphere(Figure):
    def __init__(self, m_h, m_w, r):
        super().__init__(m_h, m_w)
        
        self.radius = r
        
    # рассчитать координаты области с началом в клетке с координатами (x,y)
    def count_coords(self, x, y):
        res = []
        radius = self.get_true_size(self.radius.get())
        cx, cy = x + radius - 0.5, y + radius - 0.5
        for i in range(x, x + 2*radius + 1):
            for j in range(y, y + 2*radius + 1):
                if sqrt((cx - i)**2 + (cy - j)**2) <= radius:
                    if self.check_borders(i, j):
                        res.append((i, j))
        return res

class Cube(Figure):
    def __init__(self, m_h, m_w, l ):
        super().__init__(m_h, m_w)
        
        self.length = l
        
    # рассчитать координаты области с началом в клетке с координатами (x,y)
    def count_coords(self, x, y):
        res = []
        length = self.get_true_size(self.length.get())
        for i in range(x, x + length):
            for j in range(y, y + length):
                if self.check_borders(i, j):
                    res.append((i, j))
        return res

class Cylinder(Figure):
    def __init__(self, m_h, m_w, l, w):
        super().__init__(m_h, m_w)
        
        self.length = l
        self.width = w
        
    # рассчитать координаты области с началом в клетке с координатами (x,y)
    def count_coords(self, x, y):
        res = []
        length, width = self.get_true_size(self.length.get()), self.get_true_size(self.width.get())
        for i in range(x, x + width):
            for j in range(y, y + length):
                if self.check_borders(i, j):
                    res.append((i, j))
        return res

class Cone(Figure):
    def __init__(self, m_h, m_w, w, o):
        super().__init__(m_h, m_w)
        
        self.width = w
        self.orientation = o
        
    # рассчитать координаты области с началом в клетке с координатами (x,y)
    def count_coords(self, x, y):
        res = []
        width = self.get_true_size(self.width.get())
        dx, dy = ORIENT[self.orientation.get()]
        if self.orientation.get() in ['nw', 'sw', 'ne', 'se']:
            for i in range(width):
                for j in range(width-i):
                    x_0, y_0 = x+i*dx, y+j*dy
                    if self.check_borders(x_0, y_0):
                        res.append((x_0, y_0))
        elif self.orientation.get() in ['n', 's']:
            a, b, flag = y, y, True
            for i in range(width):
                if flag:
                    b += 1
                    flag = False
                else:
                    a -= 1
                    flag = True
                for j in range(a, b):
                    x_0 = x+i*dx
                    if self.check_borders(x_0, j):
                        res.append((x_0, j))
        else:
            a, b, flag = x, x, True
            for i in range(width):
                if flag:
                    b += 1
                    flag = False
                else:
                    a -= 1
                    flag = True
                for j in range(a, b):
                    y_0 = y+i*dy
                    if self.check_borders(j, y_0):
                        res.append((j, y_0))
        return res
    

class Area():
    def __init__(self, tokens):
        self.tokens = tokens
        x_0, y_0 = self.get_min_coords()
        self.x = x_0
        self.y = y_0
        
    # найти левую верхнюю координату области
    def get_min_coords(self):
        x_0, y_0 = self.tokens[0].x, self.tokens[0].y
        for t in self.tokens:
            x_0, y_0 = min(x_0, t.x), min(y_0, t.y)
        return x_0, y_0
    
    # найти смещение абсолютной координаты фишки t относительно курсора (x, y) при c = половине длины клетки
    def get_coords(self, t, x, y, c):
        i_0, j_0 = self.x, self.y
        n_0, m_0, n_1, m_1 = 2*(t.x-i_0)-1, 2*(t.y-j_0)-1, 2*(t.x-i_0+t.size)-1, 2*(t.y-j_0+t.size)-1
        return x + m_0*c, y + n_0*c, x + m_1*c, y + n_1*c
    
class Game():
    def __init__(self, tokens, strvar):
        self.initiative = sorted(tokens, key = lambda x: x.initiative)
        self.initiative.reverse()
        self.turn = 0
        self.end_of_turn = strvar
        self.end_of_turn.set('')
        self.player = self.initiative[0]
        self.speed = self.player.speed // const.cell_foot_size
        self.coords = (self.player.x, self.player.y)
        self.path = [self.coords]
        self.flag_diag = True
        
    # получить координаты для следующего хода на поле field
    def get_next_step(self, field):
        x, y = self.path[-1]
        res = []
        coords = [(x-1, j) for j in range(y-1, y+1+self.player.size)]
        coords.extend([(i, y+self.player.size) for i in range(x, x+1+self.player.size)])
        coords.extend([(x+self.player.size, j) for j in range(y-1, y+self.player.size)])
        coords.extend([(i, y-1) for i in range(x, x+self.player.size)])
        for i, j in coords:
            if i < field.height and j < field.width:
                res.append((i, j))
        return res
    
    # проверка конца хода на поле field
    def check_speed(self, field):
        if self.speed == 0:
            return True
        i_0, j_0 = self.path[-1]
        size = self.player.size        
        coords = self.get_next_step(field)
        diag = [(i_0-1, j_0-1), (i_0-1, j_0+size), (i_0+size, j_0+1), (i_0+size, j_0+size)]
        for i, j in coords:
            if field.check_cells(i, j, size):
                if (i, j) in diag:
                    terrain = 2 if field.check_terrain(i, j, size) else 1
                    new_s = self.speed - 1*terrain if self.flag_diag else self.speed - 2*terrain
                    if new_s >= 0:
                        return False
                else:
                    new_s = self.speed - 2 if field.check_terrain(i, j, size) else self.speed - 1
                    if new_s >= 0:
                        return False
        return True
    
    # получить координаты фишки размера size на следующем шаге при выборе координат (x, y) 
    def get_new_coords(self, x, y, size):
        x_0, y_0 = self.path[-1]
        dx, dy = 0, 0
        if x == x_0+size:
            dx = 1
        elif x == x_0-1:
            dx = -1
        if y == y_0+size:
            dy = 1
        elif y == y_0-1:
            dy = -1
        return x_0+dx, y_0 + dy
    
    # сделать следующий шаг при выборе координат (x, y) на поле field
    def do_next_step(self, x, y, field):
        x_0, y_0 = self.path[-1]
        size = self.player.size
        i, j = self.get_new_coords(x, y, size)
        field.delete_token(self.player)
        if field.check_cells(i, j, size):
            diag = [(x_0-1, y_0-1), (x_0-1, y_0+size), (x_0+size, y_0+1), (x_0+size, y_0+size)]
            coords = self.get_next_step(field)
            if (x, y) in coords:
                if (x, y) in diag:
                    terrain = 2 if field.check_terrain(i, j, size) else 1
                    new_s = self.speed - 1*terrain if self.flag_diag else self.speed - 2*terrain
                    if new_s >= 0:
                        self.flag_diag = not(self.flag_diag)
                else:
                    new_s = self.speed - 2 if field.check_terrain(i, j, size) else self.speed - 1
                if new_s >= 0:
                    self.speed = new_s
                    self.path.append((i, j))
                    if self.check_speed(field):
                        self.end_of_turn.set('Конец хода!')
                    field.add_token(self.player)
                    return True
        field.add_token(self.player)
        return False
     
    # сбросить ход
    def renew(self):
        self.end_of_turn.set('')
        self.player = self.initiative[self.turn]
        self.speed = self.player.speed // 5
        self.coords = (self.player.x, self.player.y)
        self.path = [self.coords]
        self.flag_diag = True
    
    # перезапустить ход
    def reset_turn(self):
        self.renew()
        
    # следующий раунд
    def next_round(self):
        self.turn = 0
        self.renew()
        
    # передать ход
    def next_turn(self):
        self.turn += 1
        if self.turn == len(self.initiative):
            self.next_round()
        else:
            self.renew()
            
    # пересчитать инициативу и перезапустить раунд
    def reset_initiative(self):
        self.initiative = sorted(self.initiative, key = lambda x: x.initiative)
        self.initiative.reverse()
        self.next_round()
            
    # перезаписать фишку token
    def change_info(self, token):
        i = -1
        for j, t in enumerate(self.initiative):
            if t.ID == token.ID:
                i == j
        if i > -1:
            self.initiative.pop(i)
            self.append(token)
        
    # удалить фишку token из инициативы
    def remove_toke(self, token):
        self.initiative.remove(token)
        if self.initiative:
            self.reset_initiative()
            return True
        return False
        
    # добавить фишку token в инициативу
    def add_toke(self, token):
        self.initiative.append(token)
        self.reset_initiative()
        
    # получить список из строк текста для отображения инициативы
    def give_inic(self):
        res = []
        for i in range(self.turn, len(self.initiative)):
            name = self.initiative[i].name
            if len(name) > const.max_str_len-3:
                name = name[:const.max_str_len-7]
                name += '...'
            for j in range(len(name), const.max_str_len-3):
                name += ' '
            res.append(name + str(self.initiative[i].initiative)[:2])
        res.extend(['', '   ~~~ next turn ~~~', ''])
        for i in range(self.turn):
            name = self.initiative[i].name
            if len(name) > const.max_str_len-3:
                name = name[:const.max_str_len-7]
                name += '...'
            for j in range(len(name), const.max_str_len-3):
                name += ' '
            res.append(name + str(self.initiative[i].initiative)[:2])
        return res
        

# SAVING FUNCTIONS
def save_file(field, mode):
    res = ''
    res += str(field.width) + '\n'
    res += str(field.height) + '\n'
    res += field.image
    for s in field.net:
        res += '\n'
        for cell in s:
            if cell.occupied == OCCUPIED.barrier:
                res += '#'
            elif cell.occupied == OCCUPIED.dt:
                res += '-'
            else:
                res += ' '
    configs = field.make_config()
    res += '\n' + str(len(configs))
    if mode != const.REGIME.editor:
        for config in configs:
            res += '\n'
            for c in config.values():
                res += str(c) + ','
            res = res[:-1]
    return res
    
def make_configs(config):
    res = {}
    config = config.split(',')
    res['x'] = int(config[0])
    res['y'] = int(config[1])
    res['size'] = int(config[2])
    res['color'] = config[3].replace('\'','')
    res['group'] = config[4].replace('\'','')
    res['name'] = config[5].replace('\'','')
    res['speed'] = int(config[6])
    res['hp'] = int(config[7])
    res['ac'] = int(config[8])   
    res['initiative'] = int(config[9])  
    return res

