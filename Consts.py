# -*- coding: utf-8 -*-
import Field as f

from enum import Enum

max_str_len = 24
max_field_l = 300

cell_foot_size = 5

# Enums:
class REGIME(Enum):
    editor = 0
    move = 1
    moving = 2
    add = 3
    color = 4
    coloring = 5
    delete = 6
    ruler = 7
    select = 8
    together = 9
    info = 10

# Graphic consts:
canva_height, canva_width = 0, 0
net_height, net_width = 0, 0

indent_1, indent_2, indent_3, indent_4 = 5, 10, 200, 150
button_size = 60

indent_5, indent_6 = 40, 30

text_size_large = ('','30')
text_size_big = ('','20')
text_size_medium = ('','16')
text_size_small = ('','14')
text_size_exsmall = ('','11')

tokens_scale, buttons_scale = 6, 0.8

# Calculating consts:
def get_net_size():
    net_h = canva_height - 2*indent_1 - indent_2 - indent_4
    net_w = canva_width - 2*indent_1 - indent_2 - indent_3
    return (net_h, net_w)
    
def get_cell_size(field_h, field_w):
    return min(int(net_height/field_h), int(net_width/field_w))

def get_min_coords(field_h, field_w, c, mode):
    if mode == REGIME.editor:
        x_m = net_width/2 + indent_2 - field_w/2*c
        y_m = net_height/2 + 2*indent_1 + indent_4 - field_h/2*c 
    else:
        x_m = net_width/2 + indent_1 + indent_2 + indent_3 - field_w/2*c
        y_m = net_height/2 + indent_1 + indent_2 + indent_4 - field_h/2*c
    return int(x_m), int(y_m)

def get_max_coords(field_h, field_w, c, mode):
    if mode == REGIME.editor:
        x_m = net_width/2 + indent_2 + field_w/2*c
        y_m = net_height/2 + 2*indent_1 + indent_4 + field_h/2*c         
    else:
        x_m = net_width/2 + indent_1 + indent_2 + indent_3 + field_w/2*c
        y_m = net_height/2 + indent_1 + indent_2 + indent_4 + field_h/2*c
    return int(x_m), int(y_m)

def get_field_coords(field_h, field_w, c, mode):
    x_0, y_0 = get_min_coords(field_h, field_w, c, mode)
    x_m, y_m = get_max_coords(field_h, field_w, c, mode)
    return x_0, y_0, x_m, y_m

def get_field_size(field_h, field_w, c):
    return (int(field_w*c), int(field_h*c))

def get_cell_coords(i, j, field_h, field_w, c, mode):
    x_0, y_0 = get_min_coords(field_h, field_w, c, mode)
    return x_0+c*j, y_0+c*i, x_0+c*(j+1), y_0+c*(i+1)

def get_area_coords(t, field_h, field_w, c, mode):
    x_0, y_0 = get_min_coords(field_h, field_w, c, mode)
    return x_0+c*t.y, y_0+c*t.x, x_0+c*(t.y+t.size), y_0+c*(t.x+t.size)

def check_field_coords(x, y, field_h, field_w, c, mode):
    x_0, y_0, x_m, y_m = get_field_coords(field_h, field_w, c, mode)
    if x > x_0 and x < x_m and y < y_m and y > y_0:
        return int((x-x_0)//c), int((y-y_0)//c)
    return 0

def get_token_coords(t, field_h, field_w, c, mode):
    x_0, y_0 = get_min_coords(field_h, field_w, c, mode)
    s = tokens_scale
    return x_0+c*t.y + c//s, y_0+c*t.x + c//s, x_0+c*(t.y+t.size) - c//s, y_0+c*(t.x+t.size) - c//s

def get_new_coords(t, field_h, field_w, c, mode):
    x_0, y_0 = get_min_coords(field_h, field_w, c, mode)
    s = tokens_scale
    return x_0+c*t - c//s, y_0+c*t - c//s, x_0+c*t - c//s, y_0+c*t - c//s  

def editor_bg():
    return (canva_width - indent_1 - indent_3, 2*indent_1 + indent_4,
            canva_width, canva_height - indent_1 - indent_2 - indent_3)

def game_bg_1():
    return (indent_1, indent_1, indent_1 + indent_3, canva_height-indent_1)

def game_bg_2():
    return (indent_1 + 2*indent_2 + indent_3 + indent_4, indent_1,
            canva_width - indent_1 - indent_2 - indent_4, indent_1 + indent_4)


def button():
    res = {}
    res['height'] = button_size
    res['width'] = button_size
    return res

def exit_button_1():
    res = {'anchor' : 'ne'}
    res['x'] = canva_width - indent_1
    res['y'] = indent_1
    res['width'] = indent_4
    res['height'] = indent_4
    return res

def exit_button_2():
    res = {'anchor' : 'ne'}
    res['x'] = canva_width - indent_1
    res['y'] = indent_1
    res['width'] = indent_4
    res['height'] = indent_4//2
    return res

def again_button():
    res = {'anchor' : 'nw'}
    res['x'] = indent_2
    res['y'] = indent_1
    res['width'] = int((canva_width-indent_4)/3*buttons_scale)
    res['height'] = indent_4
    return res

def save_button_1():
    res = {'anchor' : 'ne'}
    res['x'] = canva_width - indent_1 - indent_2 - indent_4
    res['y'] = indent_1
    res['width'] = int((canva_width-indent_4)/3*buttons_scale)
    res['height'] = indent_4
    return res

def save_button_2():
    res = {'anchor' : 'nw'}
    res['x'] = indent_1 + indent_2 + indent_3
    res['y'] = indent_1
    res['width'] = indent_4
    res['height'] = indent_4//2
    return res

def load_button():
    res = {'anchor' : 'n'}
    res['x'] = (canva_width-indent_4)//2
    res['y'] = indent_1
    res['width'] = int((canva_width-indent_4)/3*buttons_scale)
    res['height'] = indent_4
    return res
     
def play_button():
    res = {'anchor' : 'se'}
    res['x'] = canva_width - indent_1
    res['y'] = canva_height - indent_2
    res['width'] = indent_3
    res['height'] = indent_3
    return res

def setting_1(n, a):
    res = {'anchor' : a}
    res['x'] = canva_width - indent_3
    res['y'] = 2*indent_1 + indent_2 + indent_4 + n*indent_5
    return res

def editor_button():
    res = {'anchor' : 'sw'}
    res['x'] = indent_1 + indent_2 + indent_3
    res['y'] = indent_1 + indent_4
    res['width'] = indent_4
    res['height'] = indent_4//2
    return res

def tokens_button():
    res = {'anchor' : 'n'}
    res['x'] = indent_1 + indent_3 // 2
    res['y'] = 3*indent_1 + indent_2 + 3*button_size
    res['height'] = button_size
    return res

def ruler_button():
    res = {'anchor' : 'n'}
    res['x'] = indent_1 + indent_3 // 2
    res['y'] = indent_1 + indent_2
    res['height'] = button_size
    return res

def delete_button():
    res = {'anchor' : 'se'}
    res['x'] = indent_1 + indent_3 - indent_2
    res['y'] = canva_height - indent_1 - indent_2
    res['width'] = button_size
    res['height'] = button_size
    return res

def initiative_button():
    res = {'anchor' : 'nw'}
    res['x'] = indent_1 + 4*indent_2 + indent_3 + 3*indent_4
    res['y'] = 2*indent_1
    res['height'] = button_size
    res['width'] = 2*button_size + indent_1
    return res

def color_change():
    return (indent_1 + indent_2, 4*indent_1 + indent_2 + 4*button_size,
            indent_1 + indent_2 + button_size, 4*indent_1 + indent_2 + 5*button_size)

def area_l():
    return (indent_1 + indent_2, 2*indent_1 + indent_2 + button_size,
            indent_1 + indent_2 + button_size, 2*indent_1 + indent_2 + 2*button_size)

def area_s():
    return (indent_1 + indent_2 + button_size, 2*indent_1 + indent_2 + button_size,
            indent_1 + indent_2 + 2*button_size, 2*indent_1 + indent_2 + 2*button_size)

def area_co():
    return (indent_1 + indent_2, 2*indent_1 + indent_2 + 2*button_size,
            indent_1 + indent_2 + button_size, 2*indent_1 + indent_2 + 3*button_size)

def area_cu():
    return (indent_1 + indent_2 + button_size, 2*indent_1 + indent_2 + 2*button_size,
            indent_1 + indent_2 + 2*button_size, 2*indent_1 + indent_2 + 3*button_size)

def area_cy():
    return (indent_1 + indent_2 + 2*button_size, 2*indent_1 + indent_2 + button_size,
            indent_1 + indent_2 + 3*button_size, 2*indent_1 + indent_2 + 3*button_size)

def area_l_i():
    center = button_size // 2
    return (indent_1 + 2*indent_2, 2*indent_1 + indent_2 + button_size + center,
            indent_1 + button_size, 2*indent_1 + indent_2 + button_size + center)
def area_s_i():
    x_0, y_0, x_1, y_1 = area_s()
    return (x_0 + indent_2, y_0 + indent_2, x_1 - indent_2, y_1 - indent_2)

def area_co_i():
    x_0, y_0, x_1, y_1 = area_co()
    return (x_0 + indent_2, y_0 + button_size // 2,
            x_1 - indent_2, y_0 + indent_2,
            x_1 - indent_2, y_1 - indent_2)

def area_cu_i():
    x_0, y_0, x_1, y_1 = area_cu()
    return (x_0 + indent_2, y_0 + indent_2, x_1 - indent_2, y_1 - indent_2)

def area_cy_i():
    center = button_size // 2
    x_0, y_0, x_1, y_1 = area_cy()
    return (x_0 + indent_2, y_0 + center, x_1 - indent_2, y_1 - center)

def setting(a, i, j):
    res = {'anchor' : a}
    if a == 'nw':
        res['x'] = indent_1 + indent_2  + button_size*j
    elif a == 'n':
        res['x'] = indent_1 + indent_3 // 2
    res['y'] = 5*indent_1 + indent_2 + 7*button_size + (i-1)*indent_6
    return res

scale_size_1 = {'length'       : indent_3 - indent_1 - indent_2,
                'from_'        : cell_foot_size,
                'to'           : 4*cell_foot_size,
                'tickinterval' : cell_foot_size,
                'resolution'   : cell_foot_size,
                'font'         : text_size_medium}

scale_size_2 = {'length'       : indent_3 - indent_1 - indent_2,
                'from_'        : 0,
                'to'           : 20*cell_foot_size,
                'tickinterval' : 4*cell_foot_size,
                'resolution'   : cell_foot_size,
                'font'         : text_size_exsmall}


def scale(n):
    res = {'anchor' : 'nw'}
    res['x'] = 2*indent_1
    res['y'] = 5*indent_1 + indent_2 + 7*button_size + (n-1)*indent_6
    return res

def colors_button(i, j):
    return (indent_1 + indent_2 + button_size*j, 4*indent_1 + indent_2 + (i+4)*button_size,
            indent_1 + indent_2 + button_size*(j+1), 4*indent_1 + indent_2 + (i+5)*button_size)

def ruler_res(x_1, y_1, u):
    if u:
        return x_1, y_1 + 2*indent_2
    else:
        return x_1, y_1 - indent_2


def text_5():
    res = {'anchor' : 'w'}
    res['x'] = indent_1 + 3*indent_2 + indent_3 + indent_4
    res['y'] = indent_1 + indent_4 // 2
    return res

def info_set(i, j):
    res = {'anchor' : 'nw'}
    x = indent_1 + 3*indent_2 + indent_3 + indent_4
    x += indent_4*j if j else indent_5
    res['x'] = x
    res['y'] = 2*indent_1 + (i-1) * 2*indent_2

    return res

def save_info():
    res = {'anchor' : 'se'}
    res['x'] = indent_1 + 3*indent_2 + indent_3 + 3*indent_4
    res['y'] = indent_4
    return res

def turn_again():
    res = {'anchor' : 'sw'}
    res['x'] = indent_1 + 4*indent_2 + indent_3 + 3*indent_4
    res['y'] = indent_4
    res['width'] = button_size
    return res

def text_6():
    res = {'anchor' : 'nw'}
    res['x'] = 2*indent_1 + 4*indent_2 + indent_3 + 3*indent_4
    res['y'] = 2*indent_1 + button_size
    return res

def turn_next():
    res = {'anchor' : 'sw'}
    res['x'] = 2*indent_1 + 4*indent_2 + indent_3 + 3*indent_4 + button_size
    res['y'] = indent_4
    res['width'] = button_size
    return res

def round_button():
    res = {'anchor' : 'sw'}
    res['x'] = 4*indent_1 + 5*indent_2 + 2*indent_3 + 3*indent_4 + 2*button_size
    res['y'] = indent_4
    res['width'] = button_size
    return res

def initiative():
    res = {'anchor' : 'nw'}
    res['x'] = 3*indent_1 + 4*indent_2 + indent_3 + 3*indent_4 + 2*button_size
    res['y'] = 2*indent_1
    res['height'] = indent_4 - 2*indent_1
    return res

def scroll():
    res = {'anchor' : 'nw'}
    res['x'] = 2*indent_1 + 4*indent_2 + 2*indent_3 + 3*indent_4 + 2*button_size
    res['y'] = 2*indent_1
    res['height'] = indent_4 - 2*indent_1
    return res

def star_coords(t, field_h, field_w, c, mode):
    star = (0, 12, 10, 10, 15, 0, 20, 10, 30, 12, 23, 19, 25, 28, 15, 25, 5, 28, 7, 19)
    
    x_0, y_0, x_1, y_1 = get_token_coords(t, field_h, field_w, c, mode)
    star = [i*(x_1 - x_0) // 30 for i in star]
    for i in range(0, len(star), 2):
        star[i] += x_0
    for i in range(1, len(star), 2):
        star[i] += y_0
    return tuple(star)