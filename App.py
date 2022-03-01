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
        graph.GAME = Button(self.canva, **graph.initiative_button_1, command = lambda m = const.REGIME.move: self.change_regime(m))
        
        
    
    def clean(self, l):
        for tag in l:
            self.canva.delete(tag)
        
    def quit(self):
        if graph.quit_message():
            self.destroy()
    
    def check_map(self):
        if self.net.get():
            self.draw_net()
        else:
            self.clean(['net'])
    
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
           
    def draw_net(self):
        h, w, c = self.field.height, self.field.width, self.cell_size
        x_0, y_0 = const.get_min_coords(h, w, c, self.regime)
        for i in range(self.field.height+1):
            self.canva.create_line(x_0, y_0+c*i, x_0+c*w, y_0+c*i, tag="net")
        for i in range(self.field.width+1):
            self.canva.create_line(x_0+c*i, y_0, x_0+c*i, y_0+c*h, tag="net")
    
    def draw_cells(self):
        h, w, c = self.field.height, self.field.width, self.cell_size
        img = True if self.field_image else False
        for i in range(h):
            for j in range(w):
                config = graph.cells(self.regime, self.field.net[i][j].occupied, img)
                if config:
                    self.canva.create_rectangle(const.get_cell_coords(i, j, h, w, c, self.regime), config)
        
        
    # MAP EDITOR
    
    def load_editor_interface(self):
        self.canva.create_rectangle(const.editor_bg(), graph.bg)   
        
        graph.load_editor_interface()

        self.map_mode.set(1)
        graph.NET_W.insert(0, self.field.width)
        graph.NET_H.insert(0, self.field.height)
        
    
    def load_map_image(self):
        self.field_image = Image.open(self.field.image) if self.field.image else None
        if self.field.image:
            image = Image.open(self.field.image)
            size = const.get_field_size(self.field.height, self.field.width, self.cell_size)
            self.field_image = ImageTk.PhotoImage(image.resize(size))
    
    def draw_map_tokens(self, coords):
        if coords:
            c = self.cell_size
            x_0, y_0 = const.get_min_coords(self.field.height, self.field.width, c, self.regime)
            for x, y in coords:
                s = self.field.net[x][y].token.size
                self.canva.create_oval(x_0+c*y, y_0+c*x, x_0+c*(y+s), y_0+c*(x+s), graph.map_tokens)        
    
    
    def check_mode(self):
        return f.OCCUPIED(self.map_mode.get())
    
    def change_cells(self, event):
        x, y = event.x, event.y
        coords = const.check_field_coords(x, y, self.field.height, self.field.width, self.cell_size, self.regime)
        if coords:
            j, i = coords
            self.field.change_cell(i, j, self.check_mode())
            self.clean(["cell"])
            self.draw_cells()
    
    def save_map(self):
        file = graph.saving_message()
        if file:
            file.write(f.save_file(self.field, self.regime))
            file.close()
        
    def load_img(self):
        filename = graph.load_img_message()
        if filename:
            self.field.image = filename
            self.field_image = Image.open(filename)
            self.clean(["cell", "map", "net", "token"])
            self.load_map_image()
            self.draw_map()
            
    def new_map(self):
        if graph.again_message():
            new_h, new_w = int(graph.NET_H.get()), int(graph.NET_W.get())
            const.net_width, const.net_height
            if new_w > 0 and new_h > 0 and new_w < const.max_field_l+1 and new_h < const.max_field_l+1:
                self.tokens_to_put = []
                self.field = f.Field(new_w, new_h)
                self.load_map_image()
                self.cell_size = const.get_cell_size(self.field.height, self.field.width)
                self.clean(["cell", "map", "net", "token"])
                self.draw_map()
            elif new_w <= 0:
                graph.errors("Ширина может быть только > 0")
            elif new_h <= 0:
                graph.errors("Высота может быть только > 0")
            else:
                graph.errors("Слишком большие размеры поля") 
    
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
    
    
    def to_editor(self):
        self.load_editor_interface()
        
        self.cell_size = const.get_cell_size(self.field.height, self.field.width)
        self.load_map_image()
        self.draw_map()
        
        self.canva.bind('<Button-1>', self.change_cells)
        self.canva.bind('<B1-Motion>', self.change_cells)
        
    def out_editor(self):
        self.clean(["cell", "map", "net", "bg", "token"])
        graph.del_editor_settings()       
        
    def load_game(self):
        self.out_editor()
        self.canva.unbind('<Button-1>')
        self.canva.unbind('<B1-Motion>')        
        self.to_game()
    
    
    # GAME 
    
    
    def load_game_interface(self):
        self.canva.create_rectangle(const.game_bg_1(), graph.bg)
        self.canva.create_rectangle(const.game_bg_2(), graph.bg)
        
        graph.load_game_interface()
        
        graph.COLOR_BUT = self.canva.create_rectangle(const.color_change(), graph.change_color(self.token_color, "button"))
        self.canva.tag_bind(graph.COLOR_BUT, '<Double-Button-1>', self.open_colors)
        self.canva.tag_bind(graph.COLOR_BUT, '<Button-3>', self.open_colors)
        self.canva.tag_bind(graph.COLOR_BUT, '<Button-1>', self.coloring)        
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
          
    def load_cc_settings(self, mode):
        for i in range(3):
            for j in range(3):
                color = graph.token_colors[3*i+j]
                r = self.canva.create_rectangle(const.colors_button(i, j), graph.change_color(color, "color"))
                self.canva.tag_bind(r, '<Button-1>', lambda event, c = color, m = mode: self.change_color(event, c, mode))

    def load_line_settings(self, event):
        self.canva.itemconfig(graph.AREA[f.FIGURE.l], graph.area_button_change)
        self.figure = f.Line(self.field.height, self.field.width, IntVar(), IntVar(), StringVar())
        self.figure.length.set(5)
        self.figure.width.set(5)
        self.figure.orientation.set('n')
        graph.DIM_1.config(variable = self.figure.length)
        graph.DIM_2.config(variable = self.figure.width)
        
        self.change_regime(const.REGIME.select)
        graph.load_line_settings()
        
    def load_sphere_settings(self, event):
        self.canva.itemconfig(graph.AREA[f.FIGURE.s], graph.area_button_change)
        self.figure = f.Sphere(self.field.height, self.field.width, IntVar())
        graph.load_sphere_settings()
        graph.DIM_1.config(variable = self.figure.radius)
        self.figure.radius.set(5)
        self.change_regime(const.REGIME.select)
        
    def load_cone_settings(self, event):
        self.canva.itemconfig(graph.AREA[f.FIGURE.co], graph.area_button_change)
        self.figure = f.Cone(self.field.height, self.field.width, IntVar(), StringVar())
        graph.DIM_1.config(variable = self.figure.width)
        self.figure.width.set(5)
        self.figure.orientation.set('n')
        
        self.change_regime(const.REGIME.select)
        graph.load_cone_settings()
        
    def load_cube_settings(self, event):
        self.canva.itemconfig(graph.AREA[f.FIGURE.cu], graph.area_button_change)
        self.figure = f.Cube(self.field.height, self.field.width, IntVar())
        self.figure.length.set(5)
        graph.DIM_1.config(variable = self.figure.length)
        
        self.change_regime(const.REGIME.select)
        graph.load_cube_settings()
        
    def load_cylinder_settings(self, event):
        self.canva.itemconfig(graph.AREA[f.FIGURE.cy], graph.area_button_change)
        self.figure = f.Cylinder(self.field.height, self.field.width, IntVar(), IntVar())
        self.figure.length.set(5)
        self.figure.width.set(5)
        graph.DIM_1.config(variable = self.figure.length)
        graph.DIM_2.config(variable = self.figure.width)
        
        self.change_regime(const.REGIME.select)
        graph.load_cylinder_settings()

    
    def del_cc_settings(self):
        self.clean(["color"])
        graph.COLOR.place_forget()
    
    def del_info_settings(self):
        graph.del_info_settings()
        graph.GROUP.config(graph.group_set(self.token_group.get()))
    
    def del_select_settings(self):
        for butt in graph.AREA.values():
            self.canva.itemconfig(butt, graph.area_button)
        graph.del_select_settings()
    
    
    
    def change_regime(self, new):
        #print(self.regime, ' - ', new)
        self.clean(['highlight'])
        if self.regime == const.REGIME.editor:
            
            graph.TOKENS.config(graph.tokens_button_1)
            graph.RULER.config(graph.ruler_button_1)
            graph.DELETE.config(graph.delete_button_1)
            graph.GAME.config(graph.initiative_button_1)
            self.token_color = graph.token_colors[0]
            self.token_size_foot.set(5)
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
            self.canva.tag_bind(graph.COLOR_BUT, '<Button-1>', self.coloring)
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
            self.adding_token()
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
    
    
    def draw_token(self, t):
        h, w, c = self.field.height, self.field.width, self.cell_size
        return self.canva.create_oval(const.get_token_coords(t, h, w, c, self.regime), graph.token(t, c))
    
    def draw_tokens(self):
        for i,j in self.tokens_to_put:
            self.field.net[i][j].token.ID = self.draw_token(self.field.net[i][j].token)
        self.tokens_to_put = []
    
    def get_token_size(self):
        return self.token_size_foot.get() // 5
    
    def move_object(self, event):
        c = self.cell_size//2
        if self.area:
            for i, t in enumerate(self.area.tokens):
                self.canva.coords(self.moving_obj[i], self.area.get_coords(t, event.x, event.y, c))
        else:
            n = 2*self.get_token_size()-1
            self.canva.coords(self.moving_obj[0], event.x-c, event.y-c, event.x+n*c, event.y+n*c)
    
    def move_token(self, event):
        x, y = event.x, event.y
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        coords = const.check_field_coords(x, y, h, w, c, m)
        if coords:
            j, i = coords
            t = self.field.net[i][j].token
            if t:
                self.token_size_foot.set(t.size*5)
                self.moving_obj.append(self.canva.create_rectangle(const.get_token_coords(t, h, w, c, m),
                                                              graph.moving_object(t, c)))
                self.moving_token = t
                self.change_regime(const.REGIME.moving)
                        
    def put_check(self, i, j, size, h, w, c, m):
        t = self.moving_token
        if self.field.check_cells(i, j, size):
            t.change_coords(i, j)
            t.size = size
            self.canva.coords(t.ID, const.get_token_coords(t, h, w, c, m))
        return t
        
    def put_object(self, event):
        x, y = event.x, event.y
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        coords = const.check_field_coords(x, y, h, w, c, m)
        if coords:
            j, i = coords
            if self.moving_token:
                t = self.moving_token
                self.field.delete_token(t)
                t = self.put_check(i, j, self.get_token_size(), h, w, c, m)
                self.field.add_token(t)
                self.change_regime(const.REGIME.move)
                
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
                        new_area.append(self.put_check(i + t.x - x_0, j + t.y - y_0, t.size, h, w, c, m))
                    self.area = f.Area(new_area)
                for t in self.area.tokens:
                    self.field.add_token(t)
                self.change_regime(const.REGIME.together)
        elif self.moving_token:
            self.change_regime(const.REGIME.move)
        else:
            self.change_regime(const.REGIME.together)
    
    def adding_token(self):
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        t = f.Token(0, 0, color = self.token_color, group = self.token_group.get())
        self.moving_obj.append(self.canva.create_oval(const.get_new_coords(self.get_token_size(), h, w, c, m),
                                                  graph.token(t, c)))        
    
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
        self.change_regime(const.REGIME.move)
       
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
    
    def clean_field(self):
        if graph.delete_message():
            for t in self.field.get_tokens():
                self.clean([t.ID])
                self.field.delete_token(self.field.net[t.x][t.j].token)
    
    def open_colors(self, event):
        self.change_regime(const.REGIME.color)
    
    def change_color(self, event, c, mode):
        self.token_color = c
        self.canva.itemconfig(graph.COLOR_BUT, fill = c)
        if mode == const.REGIME.ruler:
            graph.ruler_color = c
        elif mode == const.REGIME.info or mode == const.REGIME.select:
            graph.highlight_color = c
        self.change_regime(mode)
    
    def set_color(self):
        color = graph.ask_color()
        if color:
            self.change_color(None, color, const.REGIME.move)
            
    def coloring(self, event):
        self.change_regime(const.REGIME.coloring)
            
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
            
    def end_count(self, event):
        x, y = event.x, event.y
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        coords = const.check_field_coords(x, y, h, w, c, m)
        if coords:
            self.canva.unbind('<Motion>')
            self.canva.unbind('<Button-1>')
            self.canva.bind('<Button-1>', self.start_count)            
    
    def highlight_token(self):
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        if self.area:
            for t in self.area.tokens:
                self.canva.create_rectangle(const.get_area_coords(t, h, w, c, m), graph.highlight())
        if self.chosen_token:
            self.canva.create_rectangle(const.get_area_coords(self.chosen_token, h, w, c, m), graph.highlight())
    
    def load_info(self):
        graph.NAME.insert(0, self.chosen_token.name)
        graph.SPEED.insert(0, self.chosen_token.speed)
        graph.INIC.insert(0, self.chosen_token.initiative)
        graph.HP.insert(0, self.chosen_token.hp)
        graph.AC.insert(0, self.chosen_token.ac)
        self.token_group.set(self.chosen_token.group)
        graph.GROUP.config(graph.group_set(self.token_group.get()))        
    
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
    
    def end_info(self, event):
        self.change_regime(const.REGIME.move)
    
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
        
    
    def save_info(self):
        if self.chosen_token:
            i, j = self.chosen_token.x, self.chosen_token.y
            self.field.net[i][j].token.name = graph.NAME.get()
            self.field.net[i][j].token.speed = int(graph.SPEED.get())
            self.field.net[i][j].token.initiative = int(graph.INIC.get())
            self.field.net[i][j].token.hp = graph.HP.get()
            self.field.net[i][j].token.ac = graph.AC.get()
    
    def info_return(self, event):
        self.save_info()     
        self.end_info(None)
    
    def create_area(self, event):
        self.canva.unbind('<Motion>')
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        x_0, y_0 = const.get_min_coords(h, w, c, m)        
        self.chose_tokens(self.figure.count_coords(int((event.y-y_0)//c), int((event.x-x_0)//c)))
        if self.area:
            self.change_regime(const.REGIME.together)
        else:
            self.change_regime(const.REGIME.move)
    
    def select_area(self, event):
        self.clean(['highlight'])
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        x_0, y_0 = const.get_min_coords(h, w, c, m)
        for x, y in self.figure.count_coords(int((event.y-y_0)//c), int((event.x-x_0)//c)):
            self.canva.create_rectangle(const.get_cell_coords(x, y, h, w, c, m), graph.highlight())  
    
    def chose_tokens(self, area):
        new_area = []
        for i, j in area:
            t = self.field.net[i][j].token
            if t and t not in new_area:
                new_area.append(t)
        if new_area:
            self.area = f.Area(new_area)
    
    def set_but_text(self, t):
        self.figure.orientation.set(t)
     
    def move_together(self, event):
        x, y = event.x, event.y
        h, w, c, m = self.field.height, self.field.width, self.cell_size, self.regime
        coords = const.check_field_coords(x, y, h, w, c, m)
        if coords:
            j, i = coords
            t = self.field.net[i][j].token
            if t in self.area.tokens:
                for t in self.area.tokens:
                    self.moving_obj.append(self.canva.create_rectangle(const.get_token_coords(t, h, w, c, m), 
                                                                       graph.moving_object(t, c)) )
                self.change_regime(const.REGIME.moving)
            else:
                self.end_together()
    
    def end_together(self):
        self.change_regime(const.REGIME.move)
    
    def to_game(self):
        self.change_regime(const.REGIME.move)
        
        self.load_game_interface()
        
        self.draw_map()
        self.draw_tokens()
                
        
    def out_game(self):
        self.change_regime(const.REGIME.editor)
        
        self.tokens_to_put = self.field.get_tokens_coords()
        
        self.to_editor()
        
        
''' END OF APP '''


if __name__ == '__main__':
    app = App()
    app.mainloop()