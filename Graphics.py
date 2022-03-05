# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from tkinter.colorchooser import askcolor
import os
from enum import Enum

import Field as f
import Consts as const

#COLORS:
canva_color = "alice blue"
token_colors = ["red", "orange", "yellow", "green", "blue", "pink", "sienna", "black", "white"]

def map_color(mode):
    if mode == const.REGIME.editor:
        return "green"
    else:
        return "pale green"

ruler_color = "black"
highlight_color = "azure"
def step_color(n):
    if n % 2:
        return {'fill' : "gold", 'stipple' : "gray50", 'tag' : 'step'}
    else:
        return {'fill' : "dark orange", 'stipple' : "gray50", 'tag' : 'step'}


# CONFIGS:
def cells(mode, oc, img):
    res = {'tag':'cell'}
    if oc == f.OCCUPIED.barrier:
        if mode == const.REGIME.editor:
            res['fill'] = "red"
        else:
            if img:
                res['fill'] = "coral"
                res['stipple'] = "gray12"
            else:
                res['fill'] = "RosyBrown4"      
            
    elif oc == f.OCCUPIED.dt:
        if mode == const.REGIME.editor:
            res['fill'] = "yellow"
        else:
            if img:
                res['fill'] = "khaki"
                res['stipple'] = "gray12"
            else:
                res['fill'] = "yellowgreen"            
    else:
        return None
    return res

map_tokens = {'fill' : "deep pink",
              'tag'  : 'token'}

def token(t, c):
    res = {}
    res['fill'] = t.color
    res['outline'] = t.group
    res['width'] = c//5
    res['tag'] = 'token'
    return res

def moving_object(t, c):
    res = {'stipple' : "gray50", 'tag' : 'moving'}
    res['fill'] = t.color
    res['outline'] = t.group
    res['width'] = c//5
    return res

def ruler():
    return {'fill' : ruler_color, 'width' : 3, 'arrow' : BOTH}

def highlight():
    return {'fill' : "", 'outline' : highlight_color, 'width' : 3, 'tag' : 'highlight'}

bg = {'fill'    : "SystemMenu",
      'width'   : 3,
      'outline' : "White",
      'tag'     : 'bg'}

listbox = {'bg'    : "SystemMenu",
           'selectmode' : BROWSE,
           #'selectbackground' : "SystemMenu",
           'width' : const.max_str_len,
           'font'  : 'TkFixedFont'}

star = {'fill'    : 'red',
        'width'   : 2,
        'outline' : 'black',
        'tag'     : 'star'}

# Buttons configs:
exit_button = {'text' : 'Выход',
               'fg'   : "white",
               'bg'   : "tomato",
               'font' : const.text_size_big}

again_button = {'text' : 'Заново',
                'fg'   : "white",
                'bg'   : "blue",
                'font' : const.text_size_large}

save_button_1 = {'text' : 'Сохранить',
               'fg'   : "white",
               'bg'   : "blue",
               'font' : const.text_size_large}

save_button_2 = {'text' : 'Сохранить',
                 'fg'   : "white",
                 'bg'   : "blue",
                 'font' : const.text_size_big}

load_button = {'text' : 'Загрузить',
               'fg'   : "white",
               'bg'   : "blue",
               'font' : const.text_size_large}

play_button = {'text' : 'Играть',
               'fg'   : "white",
               'bg'   : "IndianRed1",
               'font' : const.text_size_large}

check_b = {'text' : 'непроходимая',
           'bg'   : "SystemMenu",
           'font' : const.text_size_small}

check_d = {'text' : 'труднопроходимая',
           'bg'   : "SystemMenu",
           'font' : const.text_size_small}

check_t = {'text' : 'обычная',
           'bg'   : "SystemMenu",
           'font' : const.text_size_small}

check_n = {'text' : 'отображать',
           'bg'   : "SystemMenu",
           'font' : const.text_size_small}

text_1 = {'text' : 'Местность:',
          'font' : const.text_size_medium}

text_2 = {'text' : 'Ширина:',
          'font' : const.text_size_medium}

text_3 = {'text' : 'Высота:',
          'font' : const.text_size_medium}

text_4 = {'text' : 'Сетка:',
          'font' : const.text_size_medium}

net_size = {'width' : 3,
            'font'  : const.text_size_big}

load_img = {'text' : 'Открыть картинку',
            'font' : const.text_size_small}


editor_button = {'text' : 'Редактор',
                 'fg'   : "white",
                 'bg'   : "IndianRed1",
                 'font' : const.text_size_big}

tokens_button_1 = {'text' : 'Фишки',
                   'fg'   : "black",
                   'bg'   : "IndianRed1",
                   'font' : const.text_size_big,
                   'activebackground' : "salmon",
                   'activeforeground' : "gray"}

tokens_button_2 = {'fg' : "gray",
                   'bg' : "salmon"}

ruler_button_1 = {'text' : 'Линейка',
                  'fg'   : "black",
                  'bg'   : "light goldenrod",
                  'font' : const.text_size_big,
                  'activebackground' : "khaki1",
                  'activeforeground' : "gray"}

ruler_button_2 = {'fg' : "gray",
                  'bg' : "khaki1"}

delete_button_1 = {'text' : 'X',
                  'fg'   : "black",
                  'bg'   : "LightBlue1",
                  'font' : const.text_size_big,
                  'activebackground' : "light cyan",
                  'activeforeground' : "gray"}

delete_button_2 = {'fg' : "gray",
                   'bg' : "light cyan"}

initiative_button_1 = {'text' : 'Играть',
                       'fg'   : "black",
                       'bg'   : "SeaGreen1",
                       'font' : const.text_size_big,
                       'activebackground' : "green yellow",
                       'activeforeground' : "gray"}

initiative_button_2 = {'fg' : "gray",
                       'bg' : "green yellow"}

def change_color(c, tag):
    res = {'tag' : tag}
    res['fill'] =  c
    return res

area_button = {'tag'  : 'button',
               'fill' : "AntiqueWhite1"}

area_button_il = {'tag'   : 'button',
                  'width' : 3}

area_button_i = {'tag'     : 'button',
                 'fill'    : "",
                 'outline' : "black",
                 'width'   : 3}

area_button_change = {'fill' : "snow"}

def setting_text(text):
    res = {'font' : const.text_size_medium}
    res['text'] = text
    return res

def scale_text(text):
    res = {'font' : const.text_size_exsmall}
    res['text'] = text
    return res    

del_all = {'text' : 'Очистить поле',
           'font' : const.text_size_medium}

more_colors = {'text' : 'Больше цветов',
               'font' : const.text_size_medium}

coloring = {'width'   : 5,
            'outline' : "cyan"}

stop_coloring = {'width'   : 1,
                 'outline' : "black"}

check_f = {'text' : 'футах',
           'bg'   : "SystemMenu",
           'font' : const.text_size_small}

check_c = {'text' : 'клетках',
           'bg'   : "SystemMenu",
           'font' : const.text_size_small}

def ruler_set():
    return {'fill' : ruler_color, 'font' : const.text_size_big}

dim = {'width' : 3,
       'font'  : const.text_size_medium}


text_5 = {'text' : 'И\nН\nФ\nО',
          'font' : const.text_size_medium}

name = {'text' : 'Имя:',
        'font' : const.text_size_exsmall}

speed = {'text' : 'Скорость:',
         'font' : const.text_size_exsmall}

inic = {'text' : 'Инициатива:',
        'font' : const.text_size_exsmall}

hp = {'text' : 'Здоровье:',
      'font' : const.text_size_exsmall}

ac = {'text' : 'Защита:',
      'font' : const.text_size_exsmall}

group = {'text' : 'Группа:',
         'font' : const.text_size_exsmall}

info = {'text' : 'Сохранить'}

info_set = {'width' : const.max_str_len}

def group_set(c):
    res = {'font' : const.text_size_exsmall}
    res['bg'] = c
    res['fg'] = "white" if c == "brown" else "black"
    res['relief'] = RIDGE
    return res

turn_again = {'text'   : 'Заново',
              'height' : 2,
              'bg'     : "sandy brown",
              'font'   : const.text_size_exsmall}

turn_next = {'text'   : 'Вперед',
             'height' : 2,
             'bg'     : "SpringGreen4",
             'fg'     : "white",
             'font'   : const.text_size_exsmall}

round_button = {'text'   : 'Раунд',
                'height' : 2,
                'bg'     : "light goldenrod",             
                'font'   : const.text_size_exsmall}

text_6 = {'font' : const.text_size_exsmall}


# VIGETS:
# Buttons:
EXIT = None
SAVE = None
LOAD = None
AGAIN = None
PLAY = None
CHECK_B = None
CHECK_D = None
CHECK_T = None
NET_W = None
NET_H = None
LOAD_IMG = None

EDITOR = None
TOKENS = None
RULER = None
DELETE = None
SIZE_S = None
DEL_ALL = None
GAME = None
COLOR = None
DIM_1 = None
DIM_2 = None
OR_NW = None
OR_N = None
OR_NE = None
OR_E = None
OR_SE = None
OR_S = None
OR_SW = None
OR_W = None

INFO = None
NAME = None
SPEED = None
INIC = None
HP = None
AC = None
GROUP = None
TURN_AGAIN = None
TURN_NEXT = None
ROUND = None
INITIATIVE = None
SCROLL = None

# Texts:
TEXT_1 = None
TEXT_2 = None
TEXT_3 = None
TEXT_4 = None
TEXT_5 = None
TEXT_6 = None
SETTING = None
NAME_T = None
SPEED_T = None
INIC_T = None
HP_T = None
AC_T = None
GROUP_T = None

# Canva objects:
COLOR_BUT = 0
AREA = {f.FIGURE.l : 0, f.FIGURE.s : 0, f.FIGURE.co : 0, f.FIGURE.cu : 0, f.FIGURE.cy : 0}

# INTERFACE FUNCTIONS:

def load_editor_interface():
    EXIT.place(const.exit_button_1())
    AGAIN.place(const.again_button())
    SAVE.place(const.save_button_1())
    LOAD.place(const.load_button())
    PLAY.place(const.play_button())
    
    TEXT_1.place(const.setting_1(1, 'sw'))
    CHECK_B.place(const.setting_1(1, 'nw'))
    CHECK_D.place(const.setting_1(2, 'nw'))
    CHECK_T.place(const.setting_1(3, 'nw'))
    TEXT_2.place(const.setting_1(5, 'sw'))
    NET_W.place(const.setting_1(5, 'nw'))
    TEXT_3.place(const.setting_1(7, 'sw'))
    NET_H.place(const.setting_1(7, 'nw'))
    LOAD_IMG.place(const.setting_1(8, 'nw'))
    TEXT_4.place(const.setting_1(10, 'sw'))
    NET.place(const.setting_1(10, 'nw'))

    SAVE.config(save_button_1)

def load_game_interface():    
    SAVE.place(const.save_button_2())
    EDITOR.place(const.editor_button())
    
    TOKENS.place(const.tokens_button())
    RULER.place(const.ruler_button())
    DELETE.place(const.delete_button())
    
    TEXT_5.place(const.text_5())
    GAME.place(const.initiative_button())
    
    SAVE.config(save_button_2)

def load_size_settings():
    SIZE_S.place(const.scale(1))
    SIZE_S.config(label = "Размер фишки:")

def load_del_settings():
    DEL_ALL.place(const.setting('n', 1, 0))

def load_ruler_settings():
    SETTING.config(setting_text('Измерять в:'))
    SETTING.place(const.setting('nw', 1, 0))
    CHECK_F.place(const.setting('nw', 2, 0))
    CHECK_C.place(const.setting('nw', 3, 0)) 

def load_info_settings():
    NAME_T.place(const.info_set(1, 0))
    SPEED_T.place(const.info_set(2, 0))
    INIC_T.place(const.info_set(3, 0))
    HP_T.place(const.info_set(4, 0))
    AC_T.place(const.info_set(5, 0))
    GROUP_T.place(const.info_set(6, 0))
    NAME.place(const.info_set(1, 1))
    SPEED.place(const.info_set(2, 1))
    INIC.place(const.info_set(3, 1))
    HP.place(const.info_set(4, 1))
    AC.place(const.info_set(5, 1))
    GROUP.place(const.info_set(6, 1))
    INFO.place(const.save_info())

def load_line_settings():
    DIM_1.place(const.scale(1))
    DIM_1.config(label = "Длина:")
    DIM_2.place(const.scale(4))
    DIM_2.config(label = "Ширина:")
    SETTING.place(const.setting('nw', 7, 0))
    SETTING.config(scale_text('Направление:'))
    OR_NW.place(const.setting('nw', 8, 0), **const.button())
    OR_N.place(const.setting('nw', 8, 1), **const.button())
    OR_NE.place(const.setting('nw', 8, 2), **const.button())
    OR_W.place(const.setting('nw', 10, 0), **const.button())
    OR_E.place(const.setting('nw', 10, 2), **const.button())
    OR_SW.place(const.setting('nw', 12, 0), **const.button())
    OR_S.place(const.setting('nw', 12, 1), **const.button())
    OR_SE.place(const.setting('nw', 12, 2), **const.button())

def load_sphere_settings():
    DIM_1.place(const.scale(1))
    DIM_1.config(label = "Радиус:")

def load_cone_settings():
    DIM_1.place(const.scale(1))
    DIM_1.config(label = "Ширина:")
    SETTING.place(const.setting('nw', 4, 0))
    SETTING.config(scale_text('Направление:'))
    OR_NW.place(const.setting('nw', 5, 0), **const.button())
    OR_N.place(const.setting('nw', 5, 1), **const.button())
    OR_NE.place(const.setting('nw', 5, 2), **const.button())
    OR_W.place(const.setting('nw', 7, 0), **const.button())
    OR_E.place(const.setting('nw', 7, 2), **const.button())
    OR_SW.place(const.setting('nw', 9, 0), **const.button())
    OR_S.place(const.setting('nw', 9, 1), **const.button())
    OR_SE.place(const.setting('nw', 9, 2), **const.button())
    
def load_cube_settings():
    DIM_1.place(const.scale(1))
    DIM_1.config(label = "Сторона:")

def load_cylinder_settings():
    DIM_1.place(const.scale(1))
    DIM_1.config(label = "Длина:")
    DIM_2.place(const.scale(4))
    DIM_2.config(label = "Ширина:")
    
def load_together_settings():
    GROUP_T.place(const.info_set(6, 0))
    GROUP.place(const.info_set(6, 1))

def load_playing_settings():
    TURN_AGAIN.place(const.turn_again())
    TURN_NEXT.place(const.turn_next())
    ROUND.place(const.round_button())
    TEXT_6.place(const.text_6())
    INITIATIVE.place(const.initiative())
    SCROLL.place(const.scroll())
    
def upload_listbox(text):
    INITIATIVE.delete(0, INITIATIVE.size())
    for s in text:
        INITIATIVE.insert(END, s)      


def del_editor_settings():
    AGAIN.place_forget()
    SAVE.place_forget()
    LOAD.place_forget()
    PLAY.place_forget()
    CHECK_B.place_forget()
    CHECK_D.place_forget()
    CHECK_T.place_forget()
    NET.place_forget()
    TEXT_1.place_forget()
    TEXT_2.place_forget()
    TEXT_3.place_forget()
    TEXT_4.place_forget()
    NET_W.place_forget()
    NET_H.place_forget()
    LOAD_IMG.place_forget()
    
    NET_W.delete(0, END) 
    NET_H.delete(0, END)
    
def del_size_settings():
    SIZE_S.place_forget()

def del_del_settings():
    DEL_ALL.place_forget()

def del_ruler_settings():
    SETTING.place_forget()
    SETTING.config(setting_text(''))      
    CHECK_F.place_forget()
    CHECK_C.place_forget()

def del_select_settings():
    SETTING.place_forget()
    DIM_1.place_forget()
    DIM_2.place_forget()
    OR_NW.place_forget()
    OR_N.place_forget()
    OR_NE.place_forget()
    OR_W.place_forget()
    OR_E.place_forget()
    OR_SW.place_forget()
    OR_S.place_forget()
    OR_SE.place_forget()    

def del_info_settings():
    NAME_T.place_forget()
    SPEED_T.place_forget()
    INIC_T.place_forget()
    HP_T.place_forget()
    AC_T.place_forget()
    GROUP_T.place_forget()
    NAME.place_forget()
    SPEED.place_forget()
    INIC.place_forget()
    HP.place_forget()
    AC.place_forget()
    GROUP.place_forget()        
    INFO.place_forget()
    
    NAME.delete(0, END)
    SPEED.delete(0, END)
    INIC.delete(0, END)
    HP.delete(0, END)
    AC.delete(0, END)

def del_playing_settings():
    TURN_AGAIN.place_forget()
    TURN_NEXT.place_forget()
    ROUND.place_forget()
    TEXT_6.place_forget()
    INITIATIVE.place_forget()
    SCROLL.place_forget()
    
    INITIATIVE.delete(0, INITIATIVE.size())

def del_game_settings():
    EDITOR.place_forget()
    TOKENS.place_forget()
    RULER.place_forget()
    DELETE.place_forget()
    TEXT_5.place_forget()
    GAME.place_forget() 


# MESSAGES:
def errors(error):
    mb.showerror("Ошибка", error)
    
def saving_message():
    return fd.asksaveasfile(title="Сохранить файл", filetypes=(("Любой", "*"),))
        
def load_img_message():
    filetypes = (("Изображение", "*.jpg *.gif *.png"),)
    return fd.askopenfilename(title="Открыть изображение", initialdir=os.getcwd(), filetypes=filetypes)

def load_message():
    filetypes = (("Любой", "*"),
                ("Текстовый файл", "*.txt"))
    return fd.askopenfilename(title="Открыть файл", initialdir=os.getcwd(), filetypes=filetypes)

def again_message():
    return mb.askyesno('Новая карта', 'Начать заново?')

def quit_message():
    return mb.askyesno('Выход', 'Вы действительно хотите выйти? Несохраненные данные будут утеряны.')

def delete_message():
    return mb.askyesno('Очистить поле', 'Вы действительно хотите удалить все фишки?')

def ask_color():
    return askcolor()[1]

