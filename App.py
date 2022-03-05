# -*- coding: utf-8 -*-
from tkinter import *
from PIL import Image, ImageTk
from math import *

import Field as f
import Consts as const
import Graphics as graph

class App(Tk):
    def __init__(self):
        super().__init__()
        
        # window
        self.title("Игровое поле")
        self.attributes('-fullscreen', True)
        
        # canva
        const.canva_height = self.winfo_screenheight()
        const.canva_width = self.winfo_screenwidth()
        const.net_height, const.net_width = const.get_net_size()
        self.canva = Canvas(self, height = const.canva_height, width = const.canva_width, bg = graph.canva_color)
        self.canva.pack()
        
        # field
        self.field = f.Field()
        self.cell_size = const.get_cell_size(self.field.height, self.field.width)
        self.field_image = None
        self.net = IntVar()
        
        # tokens:
        self.tokens_to_put = []
        
        # area
        self.figure = None
        self.area = None
        
        # playing
        self.helper = None
        
        # for editor:
        self.map_mode = IntVar()
        
        # for game:
        self.token_size_foot = IntVar()
        self.token_color = graph.token_colors[0]
        self.token_group = StringVar()
        self.token_group.set(f.GROUPS[0])
        self.moving_obj = []
        self.moving_token = None
        self.chosen_token = None
        self.ruler_mode = IntVar()
        self.ruler_text = ''
        self.ruler = (0, 0)
        
        self.buttons_init()
        
        self.net.set(1)
        self.regime = const.REGIME.editor
        self.to_editor()
        
    # инициализация кнопок
    def buttons_init(self):
        graph.EXIT = Button(self.canva, **graph.exit_button, command = self.quit)
        graph.AGAIN = Button(self.canva, **graph.again_button, command = self.new_map)
        graph.SAVE = Button(self.canva, **graph.save_button_1, command = self.save_map)
        graph.LOAD = Button(self.canva, **graph.load_button, command = self.load_map)
        graph.PLAY = Button(self.canva, **graph.play_button, command = self.load_game)
        graph.CHECK_B = Radiobutton(self.canva, variable = self.map_mode, value=1, **graph.check_b)
        graph.CHECK_D = Radiobutton(self.canva, variable = self.map_mode, value=2, **graph.check_d)
        graph.CHECK_T = Radiobutton(self.canva, variable = self.map_mode, value=3, **graph.check_t)
        graph.NET = Checkbutton(self.canva, variable = self.net, onvalue = 1, offvalue = 0, command = self.check_map, **graph.check_n)
        graph.TEXT_1 = Label(self.canva, graph.text_1)
        graph.TEXT_2 = Label(self.canva, graph.text_2)
        graph.TEXT_3 = Label(self.canva, graph.text_3)
        graph.TEXT_4 = Label(self.canva, graph.text_4)
        graph.NET_W = Entry(self.canva, graph.net_size)
        graph.NET_H = Entry(self.canva, graph.net_size)
        graph.LOAD_IMG = Button(self.canva, **graph.load_img, command = self.load_img)
        
        graph.EDITOR = Button(self.canva, **graph.editor_button, command = self.out_game)
        graph.TOKENS = Button(self.canva, **graph.tokens_button_1, command = lambda m = const.REGIME.add: self.change_regime(m))
        graph.RULER = Button(self.canva, **graph.ruler_button_1, command = lambda m = const.REGIME.ruler: self.change_regime(m))        
        graph.DELETE = Button(self.canva, **graph.delete_button_1, command = lambda m = const.REGIME.delete: self.change_regime(m))
        graph.SETTING = Label(self.canva, graph.setting_text(''))
        graph.SIZE_S = Scale(self.canva, orient=HORIZONTAL, variable = self.token_size_foot, **const.scale_size_1)
        graph.DEL_ALL = Button(self.canva, **graph.del_all, command = self.clean_field)
        graph.COLOR = Button(self.canva, **graph.more_colors, command = self.set_color)
        graph.CHECK_F = Radiobutton(self.canva, variable = self.ruler_mode, value=1, **graph.check_f)
        graph.CHECK_C = Radiobutton(self.canva, variable = self.ruler_mode, value=2, **graph.check_c)     
        graph.TEXT_5 = Label(self.canva, graph.text_5)
        graph.TEXT_6 = Label(self.canva, graph.text_5)
        graph.DIM_1 = Scale(self.canva, orient=HORIZONTAL, **const.scale_size_2)
        graph.DIM_2 = Scale(self.canva, orient=HORIZONTAL, **const.scale_size_2)
        graph.OR_NW = Button(self.canva, **graph.setting_text('nw'), command = lambda t = 'nw': self.set_but_text(t))
        graph.OR_N = Button(self.canva, **graph.setting_text('n'), command = lambda t = 'n': self.set_but_text(t))
        graph.OR_NE = Button(self.canva, **graph.setting_text('ne'), command = lambda t = 'ne': self.set_but_text(t))
        graph.OR_E = Button(self.canva, **graph.setting_text('e'), command = lambda t = 'e': self.set_but_text(t))
        graph.OR_SE = Button(self.canva, **graph.setting_text('se'), command = lambda t = 'se': self.set_but_text(t))
        graph.OR_S = Button(self.canva, **graph.setting_text('s'), command = lambda t = 's': self.set_but_text(t))
        graph.OR_SW = Button(self.canva, **graph.setting_text('sw'), command = lambda t = 'sw': self.set_but_text(t))
        graph.OR_W = Button(self.canva, **graph.setting_text('w'), command = lambda t = 'w': self.set_but_text(t))
        
        graph.INFO = Button(self.canva, **graph.info, command = self.save_info)
        graph.NAME_T = Label(self.canva, graph.name)
        graph.SPEED_T = Label(self.canva, graph.speed)
        graph.INIC_T = Label(self.canva, graph.inic)
        graph.HP_T = Label(self.canva, graph.hp)
        graph.AC_T = Label(self.canva, graph.ac)
        graph.GROUP_T = Label(self.canva, graph.group)
        graph.NAME = Entry(self.canva, graph.info_set)
        graph.SPEED = Entry(self.canva, graph.info_set)
        graph.INIC = Entry(self.canva, graph.info_set)
        graph.HP = Entry(self.canva, graph.info_set)
        graph.AC = Entry(self.canva, graph.info_set)
        graph.GROUP = Button(self.canva, textvariable = self.token_group, **graph.group_set(f.GROUPS[0]), command = self.change_group)
        graph.GAME = Button(self.canva, **graph.initiative_button_1, command = self.start_playing)
        graph.TURN_AGAIN = Button(self.canva, **graph.turn_again, command = self.turn_again)
        graph.TURN_NEXT = Button(self.canva, **graph.turn_next, command = lambda e = None : self.turn_next(e))
        graph.ROUND = Button(self.canva, **graph.round_button, command = self.next_round)
        graph.SCROLL = Scrollbar(self)
        graph.INITIATIVE = Listbox(self.canva, **graph.listbox, yscrollcommand = graph.SCROLL.set)
        graph.SCROLL.config(command = graph.INITIATIVE.yview)
        graph.TEXT_6 = Label(self.canva, graph.text_6)
        
            
    # очистка поля от объектов канвы с тегами из массива tags
    def clean(self, tags):
        for tag in tags:
            self.canva.delete(tag)
        
    # выход из приложения
    def quit(self):
        if graph.quit_message():
            self.destroy()
    
    # проверка: отображать ли сетку на поле
    def check_map(self):
        if self.net.get():
            self.draw_net()
        else:
            self.clean(['net'])
    
    # функция отрисовки игрового поля
    def draw_map(self):
        if self.field.image:
            self.canva.create_image(const.get_min_coords(self.field.height, self.field.width, self.cell_size, self.regime),
                                    anchor = 'nw', image = self.field_image, tag = "map")
        else:
            coords = const.get_field_coords(self.field.height, self.field.width, self.cell_size, self.regime)
            self.canva.create_rectangle(coords, fill = graph.map_color(self.regime), tag = "map")
        if self.net.get() == 1:
            self.draw_net()
        self.draw_cells()
        if self.regime == const.REGIME.editor:
            self.draw_map_tokens(self.tokens_to_put)
           
    # функция отрисовки сетки на игровом поле
    def draw_net(self):
        h, w, c = self.field.height, self.field.width, self.cell_size
        x_0, y_0 = const.get_min_coords(h, w, c, self.regime)
        for i in range(self.field.height+1):
            self.canva.create_line(x_0, y_0+c*i, x_0+c*w, y_0+c*i, tag="net")
        for i in range(self.field.width+1):
            self.canva.create_line(x_0+c*i, y_0, x_0+c*i, y_0+c*h, tag="net")
    
    # функция отрисовки клеток на игровом поле
    def draw_cells(self):
        h, w, c = self.field.height, self.field.width, self.cell_size
        img = True if self.field_image else False
        for i in range(h):
            for j in range(w):
                config = graph.cells(self.regime, self.field.net[i][j].occupied, img)
                if config:
                    self.canva.create_rectangle(const.get_cell_coords(i, j, h, w, c, self.regime), config)
        
        
    # MAP EDITOR
    
    # загрузка интерфейса редактора карт
    def load_editor_interface(self):
        self.canva.create_rectangle(const.editor_bg(), graph.bg)   
        
        graph.load_editor_interface()

        self.map_mode.set(1)
        graph.NET_W.insert(0, self.field.width)
        graph.NET_H.insert(0, self.field.height)
        
    
    # отрисовка изображения для фона поля
    def draw_map_image(self):
        self.field_image = Image.open(self.field.image) if self.field.image else None
        if self.field.image:
            image = Image.open(self.field.image)
            size = const.get_field_size(self.field.height, self.field.width, self.cell_size)
            self.field_image = ImageTk.PhotoImage(image.resize(size))
    
    # функция отрисовки фишек по координатам из coords при загрузке в редакторе карт
    def draw_map_tokens(self, coords):
        if coords:
            c = self.cell_size
            x_0, y_0 = const.get_min_coords(self.field.height, self.field.width, c, self.regime)
            for x, y in coords:
                s = self.field.net[x][y].token.size
                self.canva.create_oval(x_0+c*y, y_0+c*x, x_0+c*(y+s), y_0+c*(x+s), graph.map_tokens)        
    
    
    # функция обновления поля при нажатии мыши (event)
    def change_cells(self, event):
        x, y = event.x, event.y
        coords = const.check_field_coords(x, y, self.field.height, self.field.width, self.cell_size, self.regime)
        if coords:
            j, i = coords
            self.field.change_cell(i, j, f.OCCUPIED(self.map_mode.get()))
            self.clean(["cell"])
            self.draw_cells()
    
    # сохранение карты
    def save_map(self):
        file = graph.saving_message()
        if file:
            file.write(f.save_file(self.field, self.regime))
            file.close()
        
    # загрузка изображения для фона поля
    def load_img(self):
        filename = graph.load_img_message()
        if filename:
            self.field.image = filename
            self.field_image = Image.open(filename)
            self.clean(["cell", "map", "net", "token"])
            self.draw_map_image()
            self.draw_map()
            
    # создание нового поля
    def new_map(self):
        if graph.again_message():
            new_h, new_w = int(graph.NET_H.get()), int(graph.NET_W.get())
            const.net_width, const.net_height
            if new_w > 0 and new_h > 0 and new_w < const.max_field_l+1 and new_h < const.max_field_l+1:
                self.tokens_to_put = []
                self.field = f.Field(new_w, new_h)
                self.draw_map_image()
                self.cell_size = const.get_cell_size(self.field.height, self.field.width)
                self.clean(["cell", "map", "net", "token"])
                self.draw_map()
            elif new_w <= 0:
                graph.errors("Ширина может быть только > 0")
            elif new_h <= 0:
                graph.errors("Высота может быть только > 0")
            else:
                graph.errors("Слишком большие размеры поля") 
    
    # загрузка карты из файла
    def load_map(self):
        filename = graph.load_message()
        if filename:
            file = open(filename, 'r')
            tokens_coords = []
            new_f = f.Field(int(file.readline()), int(file.readline()), file.readline()[0:-1])
            for i in range(new_f.height):
                for j, symbol in enumerate(file.readline()):
                    if symbol == ' ':
                        new_f.change_cell(i, j, f.OCCUPIED.terrain)
                    elif symbol == '#':
                        new_f.change_cell(i, j, f.OCCUPIED.barrier)
                    elif symbol == '-':
                        new_f.change_cell(i, j, f.OCCUPIED.dt)
            
            configs = int(file.readline())
            for i in range(configs):
                t = f.Token(** f.make_configs(file.readline()))
                new_f.add_token(t)
                tokens_coords.append((t.x, t.y))
            file.close()
            self.field = new_f
            self.tokens_to_put = tokens_coords
            self.out_editor()            
            self.to_editor()
    
    
    # загрузка режима редактора карт
    def to_editor(self):
        self.load_editor_interface()
        
        self.cell_size = const.get_cell_size(self.field.height, self.field.width)
        self.draw_map_image()
        self.draw_map()
        
        self.canva.bind('<Button-1>', self.change_cells)
        self.canva.bind('<B1-Motion>', self.change_cells)
        
    # завершение режима редактора карт
    def out_editor(self):
        self.clean(["cell", "map", "net", "bg", "token"])
        graph.del_editor_settings()       
        
    # загрузка режима игры
    def load_game(self):
        self.out_editor()
        self.canva.unbind('<Button-1>')
        self.canva.unbind('<B1-Motion>')        
        self.to_game()
    
    
    # GAME 
    
    # загрузка интерфейса игры
    def load_game_interface(self):
        self.canva.create_rectangle(const.game_bg_1(), graph.bg)
        self.canva.create_rectangle(const.game_bg_2(), graph.bg)
        
        graph.load_game_interface()
        
        graph.COLOR_BUT = self.canva.create_rectangle(const.color_change(), graph.change_color(self.token_color, "button"))
        self.canva.tag_bind(graph.COLOR_BUT, '<Double-Button-1>', self.open_colors)
        self.canva.tag_bind(graph.COLOR_BUT, '<Button-3>', self.open_colors)
        self.canva.tag_bind(graph.COLOR_BUT, '<Button-1>', lambda event, m = const.REGIME.coloring: self.change_regime(m))        
        graph.AREA[f.FIGURE.l] = self.canva.create_rectangle(const.area_l(), graph.area_button)
        butt = self.canva.create_line(const.area_l_i(), graph.area_button_il)
        self.canva.tag_bind(graph.AREA[f.FIGURE.l], '<ButtonRelease-1>', self.load_line_settings)
        self.canva.tag_bind(butt, '<ButtonRelease-1>', self.load_line_settings)
        graph.AREA[f.FIGURE.s] = self.canva.create_rectangle(const.area_s(), graph.area_button)
        butt = self.canva.create_oval(const.area_s_i(), graph.area_button_i)
        self.canva.tag_bind(butt, '<ButtonRelease-1>', self.load_sphere_settings)
        self.canva.tag_bind(graph.AREA[f.FIGURE.s], '<ButtonRelease-1>', self.load_sphere_settings)
        graph.AREA[f.FIGURE.co] = self.canva.create_rectangle(const.area_co(), graph.area_button)
        butt = self.canva.create_polygon(const.area_co_i(), graph.area_button_i)
        self.canva.tag_bind(butt, '<ButtonRelease-1>', self.load_cone_settings)
        self.canva.tag_bind(graph.AREA[f.FIGURE.co], '<ButtonRelease-1>', self.load_cone_settings)
        graph.AREA[f.FIGURE.cu] = self.canva.create_rectangle(const.area_cu(), graph.area_button)
        butt = self.canva.create_rectangle(const.area_cu_i(), graph.area_button_i)
        self.canva.tag_bind(butt, '<ButtonRelease-1>', self.load_cube_settings)
        self.canva.tag_bind(graph.AREA[f.FIGURE.cu], '<ButtonRelease-1>', self.load_cube_settings)
        graph.AREA[f.FIGURE.cy] = self.canva.create_rectangle(const.area_cy(), graph.area_button)
        butt = self.canva.create_rectangle(const.area_cy_i(), graph.area_button_i)
        self.canva.tag_bind(butt, '<ButtonRelease-1>', self.load_cylinder_settings)
        self.canva.tag_bind(graph.AREA[f.FIGURE.cy], '<ButtonRelease-1>', self.load_cylinder_settings)
          
    # загрузка интерфейса инструмента «изменение цвета» при следующем режиме mode
    def load_cc_settings(self, mode):
        for i in range(3):
            for j in range(3):
                color = graph.token_colors[3*i+j]
                r = self.canva.create_rectangle(const.colors_button(i, j), graph.change_color(color, "color"))
                self.canva.tag_bind(r, '<Button-1>', lambda event, c = color, m = mode: self.change_color(event, c, mode))

    # загрузка интерфейса инструмента «выделение по линии» при нажатии мыши (event)
    def load_line_settings(self, event):
        self.canva.itemconfig(graph.AREA[f.FIGURE.l], graph.area_button_change)
        self.figure = f.Line(self.field.height, self.field.width, IntVar(), IntVar(), StringVar())
        self.figure.length.set(const.cell_foot_size)
        self.figure.width.set(const.cell_foot_size)
        self.figure.orientation.set('n')
        graph.DIM_1.config(variable = self.figure.length)
        graph.DIM_2.config(variable = self.figure.width)
        
        self.change_regime(const.REGIME.select)
        graph.load_line_settings()
        
    # загрузка интерфейса инструмента «выделение в сфере» при нажатии мыши (event)
    def load_sphere_settings(self, event):
        self.canva.itemconfig(graph.AREA[f.FIGURE.s], graph.area_button_change)
        self.figure = f.Sphere(self.field.height, self.field.width, IntVar())
        graph.load_sphere_settings()
        graph.DIM_1.config(variable = self.figure.radius)
        self.figure.radius.set(const.cell_foot_size)
        self.change_regime(const.REGIME.select)
        
    # загрузка интерфейса инструмента «выделение в конусе» при нажатии мыши (event)
    def load_cone_settings(self, event):
        self.canva.itemconfig(graph.AREA[f.FIGURE.co], graph.area_button_change)
        self.figure = f.Cone(self.field.height, self.field.width, IntVar(), StringVar())
        graph.DIM_1.config(variable = self.figure.width)
        self.figure.width.set(const.cell_foot_size)
        self.figure.orientation.set('n')
        
        self.change_regime(const.REGIME.select)
        graph.load_cone_settings()
        
    # загрузка интерфейса инструмента «выделение в кубе» при нажатии мыши (event)
    def load_cube_settings(self, event):
        self.canva.itemconfig(graph.AREA[f.FIGURE.cu], graph.area_button_change)
        self.figure = f.Cube(self.field.height, self.field.width, IntVar())
        self.figure.length.set(const.cell_foot_size)
        graph.DIM_1.config(variable = self.figure.length)
        
        self.change_regime(const.REGIME.select)
        graph.load_cube_settings()
        
    # загрузка интерфейса инструмента «выделение в цилиндре» при нажатии мыши (event)
    def load_cylinder_settings(self, event):
        self.canva.itemconfig(graph.AREA[f.FIGURE.cy], graph.area_button_change)
        self.figure = f.Cylinder(self.field.height, self.field.width, IntVar(), IntVar())
        self.figure.length.set(const.cell_foot_size)
        self.figure.width.set(const.cell_foot_size)
        graph.DIM_1.config(variable = self.figure.length)
        graph.DIM_2.config(variable = self.figure.width)
        
        self.change_regime(const.REGIME.select)
        graph.load_cylinder_settings()

    
    # удаление интерфейса инструмента «изменение цвета»
    def del_cc_settings(self):
        self.clean(["color"])
        graph.COLOR.place_forget()
    
    # удаление интерфейса инструмента «редактирование информации»
    def del_info_settings(self):
        graph.del_info_settings()
        graph.GROUP.config(graph.group_set(self.token_group.get()))
    
    # удаление интерфейса инструмента «выделение…»
    def del_select_settings(self):
        for butt in graph.AREA.values():
            self.canva.itemconfig(butt, graph.area_button)
        graph.del_select_settings()
    
    
    
    # функция управления сменой режимов на new
    def change_regime(self, new):
        #print(self.regime, ' - ', new)
        self.clean(['highlight'])
        if self.regime == const.REGIME.editor:
            
            graph.TOKENS.config(graph.tokens_button_1)
            graph.RULER.config(graph.ruler_button_1)
            graph.DELETE.config(graph.delete_button_1)
            graph.GAME.config(graph.initiative_button_1)
            self.token_color = graph.token_colors[0]
            self.token_size_foot.set(const.cell_foot_size)
            self.ruler_mode.set(1)
            self.ruler_text = ''
            self.token_group.set(f.GROUPS[0])
            self.figure = None
            self.area = None
            
            self.canva.bind('<Button-1>', self.move_token)
            self.canva.bind('<Button-3>', self.info_token)
            
        elif self.regime == const.REGIME.move:
            if new != const.REGIME.moving:
                graph.del_size_settings()
            self.canva.unbind('<Button-1>')
        
        elif self.regime == const.REGIME.moving:          
            self.clean(self.moving_obj)
            self.moving_obj, self.moving_token = [], None
            self.canva.unbind('<Button-1>')
            self.canva.unbind('<Motion>')
            
        elif self.regime == const.REGIME.add:
            self.clean(self.moving_obj)
            graph.del_size_settings()
            graph.TOKENS.config(graph.tokens_button_1)
            self.canva.unbind('<Button-1>')
            self.canva.unbind('<Motion>')
            self.moving_obj = []
            
        elif self.regime == const.REGIME.delete:
            graph.del_del_settings()
            graph.DELETE.config(command = lambda m = const.REGIME.delete: self.change_regime(m),
                                **graph.delete_button_1)
            self.canva.unbind('<Button-1>')
        
        elif self.regime == const.REGIME.color:
            self.del_cc_settings()
            
        elif self.regime == const.REGIME.coloring:
            self.canva.unbind('<Button-1>')
            self.canva.tag_unbind(graph.COLOR_BUT, '<Button-1>')
            self.canva.tag_bind(graph.COLOR_BUT, '<Button-1>',
                                lambda event, m = const.REGIME.coloring: self.change_regime(m))
            self.canva.itemconfig(graph.COLOR_BUT, graph.stop_coloring)
            if new == const.REGIME.color:
                self.regime = new
                self.load_cc_settings(const.REGIME.coloring)
                graph.COLOR.place(const.setting('n', 1, 0))
                return
        
        elif self.regime == const.REGIME.ruler:
            self.clean(self.moving_obj)
            self.moving_obj = []
            if new == const.REGIME.color:
                self.regime = new
                self.load_cc_settings(const.REGIME.ruler)
                self.highlight_token()
                return
            self.ruler_text = str(0)
            self.ruler = (0, 0)
            graph.del_ruler_settings()
            graph.RULER.config(command = lambda m = const.REGIME.ruler: self.change_regime(m),
                                **graph.ruler_button_1)
            self.canva.unbind('<Button-1>')
            self.canva.unbind('<Motion>')
        
        elif self.regime == const.REGIME.info:     
            if new != const.REGIME.info:
                self.chosen_token = None
            self.token_group.set(f.GROUPS[0])
            self.unbind('<Return>')
            self.canva.unbind('<Button-1>')
            if new == const.REGIME.color:
                self.regime = new
                self.load_cc_settings(const.REGIME.info)
                self.highlight_token()
                return
            self.del_info_settings()
        
        elif self.regime == const.REGIME.select:
            self.canva.unbind('<Motion>')
            self.canva.unbind('<Button-1>')
            if new == const.REGIME.color:
                self.regime = new
                self.load_cc_settings(const.REGIME.select)
                return
            self.del_select_settings()
        
        elif self.regime == const.REGIME.together:
            if new == const.REGIME.info:
                if self.chosen_token in self.area.tokens:
                    self.del_info_settings()
                    graph.load_info_settings()
                    self.load_info()
                    self.highlight_token()
                    return
                self.del_info_settings()
            else:
                self.token_group.set(f.GROUPS[0])
                self.del_info_settings()
                self.chosen_token = None
                
            if new != const.REGIME.moving:
                self.area = None
                
            if new == const.REGIME.color:
                self.regime = new
                self.load_cc_settings(const.REGIME.select)
                return            
            self.canva.unbind('<Button-1>')
            self.unbind('<Return>')
        
        self.regime = new
        self.highlight_token()
        
        if new == const.REGIME.move:
            self.canva.bind('<Button-1>', self.move_token)
            graph.load_size_settings()
        
        elif new == const.REGIME.moving:
            self.canva.bind('<Button-1>', self.put_object)
            self.canva.bind('<Motion>', self.move_object)
        
        elif new == const.REGIME.add:
            graph.TOKENS.config(graph.tokens_button_2)
            graph.load_size_settings() 
            self.create_token()
            self.canva.bind('<Button-1>', self.add_token)
            self.canva.bind('<Motion>', self.move_object)
        
        elif new == const.REGIME.delete:
            graph.DELETE.config(command = lambda m = const.REGIME.move: self.change_regime(m),
                                **graph.delete_button_2)
            graph.load_del_settings()
            self.canva.bind('<Button-1>', self.del_token)
            
        elif new == const.REGIME.color:
            self.load_cc_settings(const.REGIME.move)
            graph.COLOR.place(const.setting('n', 1, 0))
            
        elif new == const.REGIME.coloring:
            self.canva.itemconfig(graph.COLOR_BUT, graph.coloring)
            self.canva.bind('<Button-1>', self.change_token_color)
            self.canva.tag_unbind(graph.COLOR_BUT, '<Button-1>')
            self.canva.tag_bind(graph.COLOR_BUT, '<Button-1>',
                                lambda event, m = const.REGIME.move: self.change_regime(m))
        
        elif new == const.REGIME.ruler:
            graph.RULER.config(command = lambda m = const.REGIME.move: self.change_regime(m),
                                **graph.ruler_button_2)
            graph.load_ruler_settings()
            self.canva.bind('<Button-1>', self.start_count)
            
        elif new == const.REGIME.info:
            graph.load_info_settings()
            self.load_info()
            self.canva.bind('<Button-1>', self.end_info)
            self.bind('<Return>', self.info_return)

        elif new == const.REGIME.select:
            self.canva.bind('<Button-1>', self.create_area)
            self.canva.bind('<Motion>', self.select_area)
            
        elif new == const.REGIME.together:
            graph.load_together_settings()
            self.canva.bind('<Button-1>', self.move_together)   
            self.bind('<Return>', self.info_return)
            
        elif new == const.REGIME.editor:
            self.clean(["cell", "map", "net", "bg", "button", "token"])
            graph.del_game_settings()
            self.end_playing()
    
    
    
    # функция создания изображения фишки t, возвращает id изображения
    def draw_token(self, t):
        h, w, c = self.field.height, self.field.width, self.cell_size
        return self.canva.create_oval(const.get_token_coords(t, h, w, c, self.regime), graph.token(t, c))
    
    # функция отрисовки фишек на поле в режиме игры
    def draw_tokens(self):
        for i,j in self.tokens_to_put:
            self.field.net[i][j].token.ID = self.draw_token(self.field.net[i][j].token)
        self.tokens_to_put = []
    
    # получить размер фишки в клетках
    def get_token_size(self):
        return self.token_size_foot.get() // const.cell_foot_size
    
    # функция передвижения объекта за мышью (event)
    def move_object(self, event):
        c = self.cell_size//2
        if self.area:
            for i, t in enumerate(self.area.tokens):
                self.canva.coords(self.moving_obj[i], self.area.get_coords(t, event.x, event.y, c))
        else:
            n = 2*self.get_token_size()-1
            self.canva.coords(self.moving_obj[0], event.x-c, event.y-c, event.x+n*c, event.y+n*c)
    
    # определить фишку для передвижения по нажатию мыши (event)
    def move_token(self, event):
        x, y = event.x, event.y
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        coords = const.check_field_coords(x, y, h, w, c, m)
        if coords:
            j, i = coords
            t = self.field.net[i][j].token
            if t:
                if self.helper:
                    if t.ID == self.helper.player.ID:
                        self.make_step(i, j)
                        return
                self.token_size_foot.set(t.size*const.cell_foot_size)
                self.moving_obj.append(self.canva.create_rectangle(const.get_token_coords(t, h, w, c, m),
                                                              graph.moving_object(t, c)))
                self.moving_token = t
                self.change_regime(const.REGIME.moving)
                
            elif self.helper:
                self.make_step(i, j)
                        
    # перемещение фишки нового размера size: проверка координат (i, j) по параметрам поля h, w, c, m
    def put_token(self, i, j, size, h, w, c, m):
        t = self.moving_token
        if self.field.check_cells(i, j, size):
            t.change_coords(i, j)
            t.size = size
            self.canva.coords(t.ID, const.get_token_coords(t, h, w, c, m))
        return t
        
    # переместить объект на указанное мышью (event) место
    def put_object(self, event):
        x, y = event.x, event.y
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        coords = const.check_field_coords(x, y, h, w, c, m)
        if coords:
            j, i = coords
            if self.moving_token:
                t = self.moving_token
                self.field.delete_token(t)
                t = self.put_token(i, j, self.get_token_size(), h, w, c, m)
                self.field.add_token(t)
                self.change_regime(const.REGIME.move)
                if self.helper:
                    self.helper.change_info(t)
            else:
                put_check = True
                x_0, y_0 = self.area.x, self.area.y
                for t in self.area.tokens:
                    self.field.delete_token(t)
                    put_check = put_check and self.field.check_cells(i + t.x - x_0, j + t.y - y_0, t.size)
                if put_check:
                    new_area = []
                    for t in self.area.tokens:
                        self.moving_token = t
                        new_area.append(self.put_token(i + t.x - x_0, j + t.y - y_0, t.size, h, w, c, m))
                        if self.helper:
                            self.helper.change_info(t)
                    self.area = f.Area(new_area)
                for t in self.area.tokens:
                    self.field.add_token(t)
                self.change_regime(const.REGIME.together)
        elif self.moving_token:
            self.change_regime(const.REGIME.move)
        else:
            self.change_regime(const.REGIME.together)
    
    # создание новой фишки
    def create_token(self):
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        t = f.Token(0, 0, color = self.token_color, group = self.token_group.get())
        self.moving_obj.append(self.canva.create_oval(const.get_new_coords(self.get_token_size(), h, w, c, m),
                                                  graph.token(t, c)))        
    
    # разместить новую фишку на указанное мышью (event) место
    def add_token(self, event):
        x, y = event.x, event.y
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        coords = const.check_field_coords(x, y, h, w, c, m)
        if coords:
            j, i = coords
            if self.field.check_cells(i, j, self.get_token_size()):
                t = f.Token(i, j, self.get_token_size(), self.token_color, self.token_group.get())
                t.ID = self.draw_token(t)
                self.field.add_token(t)
                if self.helper:
                    self.helper.add_toke(t)
                    self.next_round()
        self.change_regime(const.REGIME.move)
       
    # удалить фишку на указанном мышью (event) месте
    def del_token(self, event):
        x, y = event.x, event.y
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        coords = const.check_field_coords(x, y, h, w, c, m)
        if coords:
            j, i = coords
            t = self.field.net[i][j].token
            if t:
                self.clean([t.ID])
                self.field.delete_token(t)
                if self.helper:
                    self.helper.remove_toke(t)
                    self.next_round()
    
    # удалить все фишки с поля
    def clean_field(self):
        if graph.delete_message():
            for t in self.field.get_tokens():
                self.clean([t.ID])
                self.field.delete_token(self.field.net[t.x][t.y].token)
            if self.helper:
                self.end_playing()
    
    # открыть панель для смены цвета при нажатии мыши (event)
    def open_colors(self, event):
        self.change_regime(const.REGIME.color)
    
    # изменить цвет на c при выборе мышью (event) настроек в зависимости от mode
    def change_color(self, event, c, mode):
        self.token_color = c
        self.canva.itemconfig(graph.COLOR_BUT, fill = c)
        if mode == const.REGIME.ruler:
            graph.ruler_color = c
        elif mode == const.REGIME.info or mode == const.REGIME.select:
            graph.highlight_color = c
        self.change_regime(mode)
    
    # выбор цвета из расширенной палитры
    def set_color(self):
        color = graph.ask_color()
        if color:
            self.change_color(None, color, const.REGIME.move)
            
    # изменить цвет фишки при выборе мышью (event)
    def change_token_color(self, event):
        x, y = event.x, event.y
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        coords = const.check_field_coords(x, y, h, w, c, m)
        if coords:
            j, i = coords
            t = self.field.net[i][j].token
            if t:
                self.field.net[i][j].token.color = self.token_color
                self.canva.itemconfig(t.ID, fill = self.token_color)
                
    # функция передвижения линейки за мышью (event)
    def move_ruler(self, event):
        x_0, y_0 = self.ruler
        x_1, y_1 = event.x, event.y
        self.canva.coords(self.moving_obj[0], x_0, y_0, x_1, y_1)
        r = sqrt((x_1-x_0)**2 + (y_1-y_0)**2) / self.cell_size
        self.ruler_text = str(round(r*5, 1)) if self.ruler_mode.get() == 1 else str(round(r, 1))
        self.canva.coords(self.moving_obj[1], const.ruler_res(x_1, y_1, y_1 > y_0))
        if y_1 > y_0:
            self.canva.itemconfig(self.moving_obj[1], anchor = 'n', text = self.ruler_text)
        else:
            self.canva.itemconfig(self.moving_obj[1], anchor = 's', text = self.ruler_text)
    
    # функция начала отсчета инструмента «линейка» при нажатии мышью (event)
    def start_count(self, event):
        self.clean(self.moving_obj)
        self.moving_obj = []
        x, y = event.x, event.y
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        coords = const.check_field_coords(x, y, h, w, c, m)
        if coords:
            self.ruler = (x, y)
            self.moving_obj.append(self.canva.create_line(x, y, x+1, y+1, graph.ruler()))
            self.moving_obj.append(self.canva.create_text(x, y+10, **graph.ruler_set()))
            self.canva.bind('<Motion>', self.move_ruler)
            self.canva.unbind('<Button-1>')
            self.canva.bind('<Button-1>', self.end_count)
            
    # функция окончания отсчета инструмента «линейка» при нажатии мышью (event)
    def end_count(self, event):
        x, y = event.x, event.y
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        coords = const.check_field_coords(x, y, h, w, c, m)
        if coords:
            self.canva.unbind('<Motion>')
            self.canva.unbind('<Button-1>')
            self.canva.bind('<Button-1>', self.start_count)            
    
    # выделение фишек на поле
    def highlight_token(self):
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        if self.area:
            for t in self.area.tokens:
                self.canva.create_rectangle(const.get_area_coords(t, h, w, c, m), graph.highlight())
        if self.chosen_token:
            self.canva.create_rectangle(const.get_area_coords(self.chosen_token, h, w, c, m), graph.highlight())
    
    # загрузка информации о персонаже
    def load_info(self):
        graph.NAME.insert(0, self.chosen_token.name)
        graph.SPEED.insert(0, self.chosen_token.speed)
        graph.INIC.insert(0, self.chosen_token.initiative)
        graph.HP.insert(0, self.chosen_token.hp)
        graph.AC.insert(0, self.chosen_token.ac)
        self.token_group.set(self.chosen_token.group)
        graph.GROUP.config(graph.group_set(self.token_group.get()))        
    
    # функция определения персонажа для отображения информации по нажатию мыши (event)
    def info_token(self, event):
        x, y = event.x, event.y
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        coords = const.check_field_coords(x, y, h, w, c, m)
        if coords:
            j, i = coords
            t = self.field.net[i][j].token
            if t:
                self.chosen_token = t
                self.change_regime(const.REGIME.info)
    
    # функция завершения отображения информации при нажатии мыши (event)
    def end_info(self, event):
        if self.helper:
            if event:
                x, y = event.x, event.y
                h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
                coords = const.check_field_coords(x, y, h, w, c, m)
                if coords:
                    j, i = coords
                    self.make_step(i, j)
        self.change_regime(const.REGIME.move)
    
    # смена группы у фишек
    def change_group(self):
        num = f.GROUPS.index(self.token_group.get())
        if num == len(f.GROUPS)-1:
            num = 0
        else:
            num += 1
        self.token_group.set(f.GROUPS[num])
        color = self.token_group.get()
        
        if self.regime == const.REGIME.together:
            for t in self.area.tokens:
                self.canva.itemconfig(t.ID, outline = color)
                self.field.net[t.x][t.y].token.group = color
        else:
            t = self.chosen_token
            self.canva.itemconfig(t.ID, outline = color)
            self.field.net[t.x][t.y].token.group = color
        
        graph.GROUP.config(graph.group_set(color))
        
    
    # сохранение информации о персонаже 
    def save_info(self):
        if self.chosen_token:
            i, j = self.chosen_token.x, self.chosen_token.y
            self.field.net[i][j].token.name = graph.NAME.get()
            self.field.net[i][j].token.speed = int(graph.SPEED.get())
            self.field.net[i][j].token.initiative = int(graph.INIC.get())
            self.field.net[i][j].token.hp = graph.HP.get()
            self.field.net[i][j].token.ac = graph.AC.get()
            if self.helper:
                self.helper.change_info(self.field.net[i][j].token)
    
    # сохранение информации о персонаже при нажатии Enter (event)
    def info_return(self, event):
        self.save_info()
        self.end_info(None)
    
    # выделение фишек, попавших в область, при нажатии мыши (event)
    def create_area(self, event):
        self.canva.unbind('<Motion>')
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        x_0, y_0 = const.get_min_coords(h, w, c, m)        
        self.chose_tokens(self.figure.count_coords(int((event.y-y_0)//c), int((event.x-x_0)//c)))
        if self.area:
            self.change_regime(const.REGIME.together)
        else:
            self.change_regime(const.REGIME.move)
    
    # выделение области по положению мыши (event)
    def select_area(self, event):
        self.clean(['highlight'])
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        x_0, y_0 = const.get_min_coords(h, w, c, m)
        for x, y in self.figure.count_coords(int((event.y-y_0)//c), int((event.x-x_0)//c)):
            self.canva.create_rectangle(const.get_cell_coords(x, y, h, w, c, m), graph.highlight())  
    
    # функция определения фишек, попавших в выделенную область area
    def chose_tokens(self, area):
        new_area = []
        for i, j in area:
            t = self.field.net[i][j].token
            if t and t not in new_area:
                new_area.append(t)
        if new_area:
            self.area = f.Area(new_area)
    
    # изменить направление для фигурной области на t
    def set_but_text(self, t):
        self.figure.orientation.set(t)
     
    # определить выделенные фишки для передвижения по нажатию мыши (event)
    def move_together(self, event):
        x, y = event.x, event.y
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        coords = const.check_field_coords(x, y, h, w, c, m)
        if coords:
            j, i = coords
            t = self.field.net[i][j].token
            if t in self.area.tokens:
                if self.helper:
                    tokens = self.area.tokens
                    if self.helper.player in tokens:
                        tokens.remove(self.helper.player)
                        self.area = f.Area(tokens)
                for t in self.area.tokens:
                    self.moving_obj.append(self.canva.create_rectangle(const.get_token_coords(t, h, w, c, m), 
                                                                       graph.moving_object(t, c)) )
                self.change_regime(const.REGIME.moving)
                return
            elif self.helper:
                if self.make_step(i, j):
                    return
        self.change_regime(const.REGIME.move)    
    
    
    # нарисовать звезду
    def draw_star(self):
        self.clean(['star'])
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        self.canva.create_polygon(const.star_coords(self.helper.player, h, w, c, m), graph.star)
    
    # отрисовать выбранный шаг на клетку (i, j) n-ый раз
    def draw_step(self, i, j, n):
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        for dx in range(self.helper.player.size):
            for dy in range(self.helper.player.size):
                self.canva.create_rectangle(const.get_cell_coords(i+dx, j+dy, h, w, c, m), graph.step_color(n))
    
    # сделать шаг на клетку (x, y), возвращает успешность
    def make_step(self, x, y):
        if self.helper.do_next_step(x, y, self.field):
            self.clean(['step'])
            for i, j in self.helper.path:
                self.draw_step(i, j, self.helper.path.count((i, j)))
            return True
        return False
           
    # начать пошаговую игру
    def start_playing(self):
        tokens = self.field.get_tokens()
        if tokens:
            self.helper = f.Game(tokens, StringVar())
            self.draw_star()
            graph.GAME.config(**graph.initiative_button_2, command = self.end_playing)
            graph.TEXT_6.config(textvariable = self.helper.end_of_turn)
            graph.load_playing_settings()
            graph.upload_listbox(self.helper.give_inic())
            self.bind('<space>', self.turn_next)
    
    # начать ход заново
    def turn_again(self):
        self.clean(['step'])
        if self.regime == const.REGIME.moving:
            if self.area:
                self.change_regime(const.REGIME.together)
            else:
                self.change_regime(const.REGIME.move)        
        self.helper.reset_turn()
    
    # передать ход при нажатии на пробел (event) или на кнопку
    def turn_next(self, event):
        self.clean(['step'])
        if self.regime == const.REGIME.moving:
            if self.area:
                self.change_regime(const.REGIME.together)
            else:
                self.change_regime(const.REGIME.move)
        i, j = self.helper.path[-1]
        t = self.helper.player
        self.field.delete_token(t)
        t.change_coords(i, j)
        self.field.add_token(t)
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        self.canva.coords(t.ID, const.get_token_coords(t, h, w, c, m))
        self.helper.next_turn()
        
        self.draw_star()
        
        graph.upload_listbox(self.helper.give_inic())
    
    # начать следующий раунд
    def next_round(self):
        self.clean(['step'])
        if self.regime == const.REGIME.moving:
            if self.area:
                self.change_regime(const.REGIME.together)
            else:
                self.change_regime(const.REGIME.move)        
        self.helper.next_round()
        self.draw_star()
        graph.upload_listbox(self.helper.give_inic())
    
    # закончить пошаговую игру
    def end_playing(self):
        graph.GAME.config(**graph.initiative_button_1, command = self.start_playing)
        graph.del_playing_settings()
        self.helper = None
        self.clean(['star', 'step'])
        self.unbind('<space>')
    
    # загрузка режима игры
    def to_game(self):
        self.change_regime(const.REGIME.move)
        
        self.load_game_interface()
        
        self.draw_map()
        self.draw_tokens()
                
    # завершение режима игры 
    def out_game(self):
        self.change_regime(const.REGIME.editor)
        
        self.tokens_to_put = self.field.get_tokens_coords()
        self.to_editor()
        
        
''' END OF APP '''


if __name__ == '__main__':
    app = App()
    app.mainloop()