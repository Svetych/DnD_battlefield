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
    
    def change_coords(self, x, y):
        self.x = x
        self.y = y
    
    def count_coords(self):
        res = []
        for i in range(self.size):
            for j in range(self.size):
                res.append((self.x+i, self.y+j))
        return res
    
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
    
    def change_cell(self, x, y, o):
        self.net[x][y].occupied = o
    
    def add_token(self, t):
        for i, j in t.count_coords():
            self.net[i][j].token = t
            
    def delete_token(self, t):
        for i, j in t.count_coords():
            self.net[i][j].token = None 
    
    def check_cells(self, x, y, size):
        if x+size > self.height or y+size > self.width:
            return False
        for i in range(size):
            for j in range(size):
                if self.net[x+i][y+j].token or self.net[x+i][y+j].occupied == OCCUPIED.barrier:
                    return False
        return True
    
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
    
    def get_tokens(self):
        res = []
        for i in range(self.height):
            for j in range(self.width):
                t = self.net[i][j].token
                if t and t not in res:
                    res.append(t)
        return res
    
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
        
    def check_borders(self, i, j):
        return i >= 0 and i < self.max_height and j >= 0 and j < self.max_width
    
    def get_true_size(self, x):
        return x // 5    

class Line(Figure):
    def __init__(self, m_h, m_w, l, w, o):
        super().__init__(m_h, m_w)
        
        self.length = l
        self.width = w
        self.orientation = o
        
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
    def __init__(self, area):
        self.tokens = area
        x_0, y_0 = self.get_min_coords()
        self.x = x_0
        self.y = y_0
        
    def get_min_coords(self):
        x_0, y_0 = self.tokens[0].x, self.tokens[0].y
        for t in self.tokens:
            x_0, y_0 = min(x_0, t.x), min(y_0, t.y)
        return x_0, y_0
    
    def get_coords(self, t, x, y, c):
        i_0, j_0 = self.x, self.y
        n_0, m_0, n_1, m_1 = 2*(t.x-i_0)-1, 2*(t.y-j_0)-1, 2*(t.x-i_0+t.size)-1, 2*(t.y-j_0+t.size)-1
        return x + m_0*c, y + n_0*c, x + m_1*c, y + n_1*c
    

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

