from tkinter import  Canvas, Tk, Frame, Button,messagebox, filedialog, Scale, HORIZONTAL,ALL, simpledialog, colorchooser
import PIL.ImageGrab as ImageGrab
from PIL import Image, ImageTk
import tkinter as tk
from Tooltip import Tooltip
import math

class Paint():
    
    def linea_xy(self, event):
        self.linea_x = event.x
        self.linea_y = event.y

    def lapiz(self, event):
        if self.current_tool == "Lápiz":
            self.elementos.append(self.canvas.create_line((self.linea_x, self.linea_y, event.x, event.y), fill=self.color, width=self.espesor_pincel.get()))
            self.linea_x = event.x
            self.linea_y = event.y

    def activar_herramienta_lapiz(self, event=None):
        self.desactivar_herramientas()
        self.current_tool = "Lápiz"
        self.canvas.config(cursor="pencil")
        self.canvas.bind('<Button-1>', self.linea_xy)
        self.canvas.bind('<B1-Motion>', self.lapiz)

    def texto(self, event):
        self.linea_x = event.x
        self.linea_y = event.y
        if self.current_tool == "Texto":
            text = simpledialog.askstring("Entrada de texto", "Ingrese el texto:")
            if text:
                self.elementos.append(self.canvas.create_text(self.linea_x, self.linea_y, text=text, fill=self.color))

    def activar_herramienta_texto(self, event=None):
        self.desactivar_herramientas()
        self.current_tool = "Texto"
        self.canvas.config(cursor="xterm")
        self.canvas.bind("<Button-1>", self.texto)

    def mostrar_color(self, nueva_color): 
        self.color = nueva_color


    def borrar(self, event):
        if self.current_tool == "Borrador":
            x = event.x
            y = event.y
            tamaño = self.espesor_pincel.get()

            x1, y1 = x - tamaño // 2, y - tamaño // 2
            x2, y2 = x + tamaño // 2, y + tamaño// 2

            items = self.canvas.find_overlapping(x1, y1, x2, y2)
            self.elementos.append(items)

            for item in items:
                self.canvas.delete(item)
            
    def activar_herramienta_borrar(self, event=None):
        self.desactivar_herramientas()
        self.current_tool = "Borrador"
        self.canvas.config(cursor="X_cursor")
        self.canvas.bind("<B1-Motion>", self.borrar)
    
    def almacenarlinea(self, event):
        self.linea_x = event.x
        self.linea_y = event.y

    def crearlinea(self, event):
        if self.current_tool == "Linea":
            self.elementos.append(self.canvas.create_line(self.linea_x, self.linea_y, event.x, event.y, fill=self.color, width=self.espesor_pincel.get()))
            
    def activar_herramienta_linea(self, event=None):
        self.desactivar_herramientas()
        self.current_tool = "Linea"
        self.canvas.config(cursor="X_cursor")
        self.canvas.bind("<Button-1>", self.almacenarlinea)
        self.canvas.bind("<ButtonRelease-1>", self.crearlinea)

    def crearRectangulo(self, event):
        if self.current_tool == "Rectángulo":
            self.elementos.append(self.canvas.create_rectangle(self.linea_x, self.linea_y, event.x, event.y, outline=self.color, width=self.espesor_pincel.get()))

    def almacenarRectangulo(self, event):
        self.linea_x = event.x
        self.linea_y = event.y

    def activar_herramienta_rectangulo(self, event=None):
        self.desactivar_herramientas()
        self.current_tool = "Rectángulo"
        self.canvas.config(cursor="plus")
        self.canvas.bind("<Button-1>", self.almacenarRectangulo)
        self.canvas.bind("<ButtonRelease-1>", self.crearRectangulo)

    def CrearOvalo(self, event):
        if self.current_tool == "Óvalo":
            self.elementos.append(self.canvas.create_oval(self.linea_x, self.linea_y, event.x, event.y, outline=self.color, width=self.espesor_pincel.get()))

    def almacenarOvalo(self, event):
        self.linea_x = event.x
        self.linea_y = event.y

    def activar_herramienta_ovalo(self, event=None):
        self.desactivar_herramientas()
        self.current_tool = "Óvalo"
        self.canvas.config(cursor="plus")
        self.canvas.bind("<Button-1>", self.almacenarOvalo)
        self.canvas.bind("<ButtonRelease-1>", self.CrearOvalo)

    def CrearTriangulo(self, event):
        if self.current_tool == "Triangulo":
            mid_x = (self.linea_x + event.x) / 2
            points = [event.x, self.linea_y, self.linea_x, self.linea_y, mid_x, event.y]
            self.elementos.append(self.canvas.create_polygon(points, outline=self.color, fill='', width=self.espesor_pincel.get()))
            
    def almacenarTriangulo(self, event):
        self.linea_x = event.x
        self.linea_y = event.y

    def activar_herramienta_Triangulo(self, event=None):
        self.desactivar_herramientas()
        self.current_tool = "Triangulo"
        self.canvas.config(cursor="plus")
        self.canvas.bind("<Button-1>", self.almacenarTriangulo)
        self.canvas.bind("<ButtonRelease-1>", self.CrearTriangulo)


    def desactivar_herramientas(self):
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<Button-1>')
     

    def paleta(self, event=None):
        color = colorchooser.askcolor()[1]
        if color:
            self.color = color
    
    def importar_image(self, event=None):
        self.desactivar_herramientas()
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            self.image_on_canvas = ImageTk.PhotoImage(image)
            self.elementos.append(self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_on_canvas))
        

    def guardar_dibujo(self, event=None):
        filename = filedialog.asksaveasfilename(defaultextension='.png')
        x = self.canvas.winfo_rootx() + self.ventana.winfo_rootx()
        y = self.canvas.winfo_rooty() + self.ventana.winfo_rooty()
        
        # Ajustar las coordenadas para asegurar que se captura todo el canvas
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        img = ImageGrab.grab(bbox=(x, y, x1, y1))
        img.save(filename)
        messagebox.showinfo('Guardar Dibujo', 'Imagen guardada en: ' + str(filename))

    def deshacer(self, event=None):
        if self.elementos:
            self.canvas.delete(self.elementos.pop())
           
            
    def mover(self, event):
        if self.current_tool == "Seleccionar":
            if self.selected_item:
                x = event.x - self.linea_x
                y = event.y - self.linea_y
                self.canvas.move(self.selected_item, x, y)
                self.linea_x, self.linea_y = event.x, event.y

    def posicion_mover(self, event):
        self.selected_item = self.canvas.find_closest(event.x, event.y)
        if self.selected_item:
            self.linea_x, self.linea_y = event.x, event.y
            self.elementos.append((event.x, event.y)) 

    def Activar_Herramienta_Mover(self, event=None):
        self.desactivar_herramientas()
        self.current_tool = "Seleccionar"
        self.canvas.bind("<Button-1>", self.posicion_mover)
        self.canvas.bind("<B1-Motion>", self.mover)

    def rotate_object(self, objeto, angle):
        cordenada = self.canvas.coords(objeto)

        if len(cordenada) == 4:
            cx = (cordenada[0] + cordenada[2]) / 2
            cy = (cordenada[1] + cordenada[3]) / 2
            rad = math.radians(angle)
            new_coords = self.rotar_rectangulo(cordenada, cx, cy, rad)
            self.canvas.delete(objeto)
            self.elementos.append(self.canvas.create_polygon(new_coords, outline="black", fill = "", width=self.espesor_pincel.get()))

        elif len(cordenada) == 8:
            cx = sum(cordenada[0::2]) / 4
            cy = sum(cordenada[1::2]) / 4
            rad = math.radians(angle)
            new_coords = self.rotate_polygon_coords(cordenada, cx, cy, rad)
            self.elementos.append(self.canvas.coords(objeto, new_coords))

        elif len(cordenada) == 6:
            cx = sum(cordenada[0::2]) / len(cordenada[0::2])
            cy = sum(cordenada[1::2]) / len(cordenada[1::2])
            rad = math.radians(angle)
            new_coords = self.rota_triangulo(cordenada, cx, cy, rad)
            self.elementos.append(self.canvas.coords(objeto, new_coords))
            
    
    def rotar_rectangulo(self, cordenada, cx, cy, rad):
        points = [(cordenada[0], cordenada[1]), (cordenada[2], cordenada[1]), (cordenada[2], cordenada[3]), (cordenada[0], cordenada[3])]
        new_points = []
        for x, y in points:
            x -= cx
            y -= cy
            new_x = x * math.cos(rad) - y * math.sin(rad) + cx
            new_y = x * math.sin(rad) + y * math.cos(rad) + cy
            new_points.append((new_x, new_y))
        return [coord for point in new_points for coord in point]
    
    
    def rotate_polygon_coords(self, cordenada, cx, cy, rad):
        points = [(cordenada[i], cordenada[i + 1]) for i in range(0, len(cordenada), 2)]
        new_points = []
        for x, y in points:
            x -= cx
            y -= cy
            new_x = x * math.cos(rad) - y * math.sin(rad) + cx
            new_y = x * math.sin(rad) + y * math.cos(rad) + cy
            new_points.append((new_x, new_y))
        return [coord for point in new_points for coord in point]
    
    def rota_triangulo(self, cordenada, cx, cy, rad):
        points = [(cordenada[i], cordenada[i + 1]) for i in range(0, len(cordenada), 2)]
        new_points = []
        for x, y in points:
            x -= cx
            y -= cy
            new_x = x * math.cos(rad) - y * math.sin(rad) + cx
            new_y = x * math.sin(rad) + y * math.cos(rad) + cy
            new_points.append(new_x)
            new_points.append(new_y)
        return new_points
    
    
    def on_click(self, event):
        self.linea_x = event.x
        self.linea_y = event.y
        if self.current_tool == "Rotar":
            self.current_object = self.canvas.find_closest(event.x, event.y)
            self.rotate_object(self.current_object, 15)
    
    def activar_herramienta_rotar(self, event=None):
        self.desactivar_herramientas()
        self.current_tool = "Rotar"
        self.canvas.bind("<Button-1>", self.on_click)
    
    def on_click2(self, event):
        self.linea_x = event.x
        self.linea_y = event.y
        if self.current_tool == "Rotar2":
            self.current_object = self.canvas.find_closest(event.x, event.y)
            self.rotate_object(self.current_object, -15)
        
    
    def activar_herramienta_rotar2(self, event=None):
        self.desactivar_herramientas()
        self.current_tool = "Rotar2"
        self.canvas.bind("<Button-1>", self.on_click2)
            
    def __init__(self):
        self.ventana = Tk()
        self.ventana.geometry('1100x600')  
        self.ventana.resizable(0,0)
   
        self.ventana.title('Dibujar')
        self.ventana.iconbitmap('icono\\icono_dibujo.ico')
        

        self.ventana.rowconfigure(0, weight=1)
        self.ventana.columnconfigure(0, weight=1)

        self.linea_x = 0
        self.linea_y = 0
        self.color = 'black'
        self.current_tool = None
        self.elementos = []
        self.selected_item = None
       

        self.frame = Frame(self.ventana, bg="#F2F2F2", width=1100, height=600)  
        self.frame.place(x=0, y =0, relwidth=1, relheight=1)
    
        self.canvas = Canvas(self.ventana, width=1000, height=550, bg='white')
        self.canvas.place(x=100, y=0)

        self.label = tk.Label(self.frame, text="Grosor linea", bg='white', fg='black')
        self.label.place(x=20, y=325)
        self.espesor_pincel = Scale(self.frame,  orient= HORIZONTAL, from_ = 0, to=50, length=100 ,relief=  'groove', bg='gold', width=17, sliderlength=20, highlightbackground='white',activebackground='red')
        self.espesor_pincel.set(1)
        self.espesor_pincel.place(x=0, y=340)
     

        self.ventana.bind('<Alt-s>', self.activar_herramienta_lapiz)
        self.ventana.bind('<Alt-a>', self.activar_herramienta_texto)
        self.ventana.bind('<Alt-e>', self.activar_herramienta_borrar)
        self.ventana.bind('<Alt-i>', self.activar_herramienta_linea)
        self.ventana.bind('<Alt-o>', self.activar_herramienta_rectangulo)
        self.ventana.bind('<Alt-p>', self.activar_herramienta_ovalo)
        self.ventana.bind('<Alt-c>', self.activar_herramienta_Triangulo)
        self.ventana.bind('<Alt-n>', self.importar_image)
        self.ventana.bind('<Alt-l>', self.guardar_dibujo)
        self.ventana.bind('<Alt-u>', self.paleta)
        self.ventana.bind('<Alt-z>', self.deshacer)
        self.ventana.bind('<Alt-t>', self.Activar_Herramienta_Mover)
        self.ventana.bind('<Alt-j>', self.activar_herramienta_rotar)
        self.ventana.bind('<Alt-f>', self.activar_herramienta_rotar2)

        self.canvas_colores = Canvas(self.frame, bg='#F2F2F2', width=530,  height=50)
        self.canvas_colores.place(x=0, y=560)


        id = self.canvas_colores.create_rectangle((10,10,30,30),fill ='black')
        self.canvas_colores.tag_bind(id, '<Button-1>', lambda x: self.mostrar_color('black'))

        id = self.canvas_colores.create_rectangle((40,10,60,30),fill ='gray')
        self.canvas_colores.tag_bind(id, '<Button-1>', lambda x: self.mostrar_color('gray'))

        id = self.canvas_colores.create_rectangle((70,10,90,30),fill ='yellow')
        self.canvas_colores.tag_bind(id, '<Button-1>', lambda x: self.mostrar_color('yellow'))

        id = self.canvas_colores.create_rectangle((100,10,120,30),fill ='magenta')
        self.canvas_colores.tag_bind(id, '<Button-1>', lambda x: self.mostrar_color('magenta'))

        id = self.canvas_colores.create_rectangle((130,10,150,30),fill ='blue')
        self.canvas_colores.tag_bind(id, '<Button-1>', lambda x: self.mostrar_color('blue'))

        id = self.canvas_colores.create_rectangle((160,10,180,30),fill ='orange')
        self.canvas_colores.tag_bind(id, '<Button-1>', lambda x: self.mostrar_color('orange'))

        id = self.canvas_colores.create_rectangle((190,10,210,30),fill ='salmon')
        self.canvas_colores.tag_bind(id, '<Button-1>', lambda x: self.mostrar_color('salmon'))

        id = self.canvas_colores.create_rectangle((220,10,240,30),fill ='sky blue')
        self.canvas_colores.tag_bind(id, '<Button-1>', lambda x: self.mostrar_color('sky blue'))

        id = self.canvas_colores.create_rectangle((250,10,270,30),fill ='gold')
        self.canvas_colores.tag_bind(id, '<Button-1>', lambda x: self.mostrar_color('gold'))

        id = self.canvas_colores.create_rectangle((280,10,300,30),fill ='hot pink')
        self.canvas_colores.tag_bind(id, '<Button-1>', lambda x: self.mostrar_color('hot pink'))

        id = self.canvas_colores.create_rectangle((310,10,330,30),fill ='bisque')
        self.canvas_colores.tag_bind(id, '<Button-1>', lambda x: self.mostrar_color('bisque'))

        id = self.canvas_colores.create_rectangle((340,10,360,30),fill ='brown4')
        self.canvas_colores.tag_bind(id, '<Button-1>', lambda x: self.mostrar_color('brown4'))

        id = self.canvas_colores.create_rectangle((370,10,390,30),fill ='green')
        self.canvas_colores.tag_bind(id, '<Button-1>', lambda x: self.mostrar_color('green'))

        id = self.canvas_colores.create_rectangle((400,10,420,30),fill ='purple')
        self.canvas_colores.tag_bind(id, '<Button-1>', lambda x: self.mostrar_color('purple'))

        id = self.canvas_colores.create_rectangle((430,10,450,30),fill ='green2')
        self.canvas_colores.tag_bind(id, '<Button-1>', lambda x: self.mostrar_color('green2'))

        id = self.canvas_colores.create_rectangle((460,10,480,30),fill ='dodger blue')
        self.canvas_colores.tag_bind(id, '<Button-1>', lambda x: self.mostrar_color('dodger blue'))

        id = self.canvas_colores.create_rectangle((490,10,510,30),fill ='Olive')
        self.canvas_colores.tag_bind(id, '<Button-1>', lambda x: self.mostrar_color('Olive'))

        # botones y scale de control
    

        icono_guardar = Image.open(r"icono\descargable.png")
        self.icono_guardar = icono_guardar.resize((30, 30))
        self.icono_guardar = ImageTk.PhotoImage(self.icono_guardar)
        self.boton_guardar = Button(self.frame, image=self.icono_guardar, command = self.guardar_dibujo, padx=10, pady=10)
        self.boton_guardar.place(x=55, y=235)
        Tooltip(self.boton_guardar, text = "Guardar dibujo. \Alt+l")
        
        icono_texto = Image.open(r"icono\texto.png")
        self.icono_texto = icono_texto.resize((30, 30))
        self.icono_texto = ImageTk.PhotoImage(self.icono_texto)
        self.boton_texto = Button(self.frame, image=self.icono_texto, command=self.activar_herramienta_texto, padx=10, pady=10)
        self.boton_texto.place(x=10, y=55)
        Tooltip(self.boton_texto, text = "Texto. \Alt+a")

        icono_lapiz = Image.open(r"icono\lapiz.png")
        self.icono_lapiz= icono_lapiz.resize((30, 30))
        self.icono_lapiz = ImageTk.PhotoImage(self.icono_lapiz)
        self.boton_lapiz = Button(self.frame, image=self.icono_lapiz, command=self.activar_herramienta_lapiz)
        self.boton_lapiz.place(x=10, y=10)
        Tooltip(self.boton_lapiz, text = "Lápiz. \Alt+s")
        
        icono_borrador = Image.open(r"icono\borrador.png")
        self.icono_borrador = icono_borrador.resize((30, 30))
        self.icono_borrador = ImageTk.PhotoImage(self.icono_borrador)
        self.boton_borrar = Button(self.frame, image=self.icono_borrador, command=self.activar_herramienta_borrar, padx=10, pady=10)
        self.boton_borrar.place(x=55, y=10)
        Tooltip(self.boton_borrar, text = "Borrador. \Alt+e")
        
        icono_linea = Image.open(r"icono\linea-diagonal.png")
        self.icono_linea = icono_linea.resize((30, 30))
        self.icono_linea = ImageTk.PhotoImage(self.icono_linea)
        self.boton_linea = Button(self.frame, image=self.icono_linea, command=self.activar_herramienta_linea, padx=10, pady=10)
        self.boton_linea.place(x=10, y=100)
        Tooltip(self.boton_linea, text = "Línea. \Alt+i")

        icono_rectangulo = Image.open(r"icono\cuadrado.png")
        self.icono_rectangulo = icono_rectangulo.resize((30, 30))
        self.icono_rectangulo = ImageTk.PhotoImage(self.icono_rectangulo)
        self.boton_rectangulo = Button(self.frame, image=self.icono_rectangulo, command=self.activar_herramienta_rectangulo, padx=10, pady=10)
        self.boton_rectangulo.place(x=55, y=100)
        Tooltip(self.boton_rectangulo, text = "Rectángulo. \Alt+o")
        
        icono_ovalo = Image.open(r"icono\circulo.png")
        self.icono_ovalo = icono_ovalo.resize((30, 30))
        self.icono_ovalo = ImageTk.PhotoImage(self.icono_ovalo)
        self.boton_ovalo = Button(self.frame, image=self.icono_ovalo, command=self.activar_herramienta_ovalo, padx=10, pady=10)
        self.boton_ovalo.place(x=10, y=145)
        Tooltip(self.boton_ovalo, text = "Óvalo. \Alt+p")

        icono_color = Image.open(r"icono\circulo-de-color.png")
        self.icono_color = icono_color.resize((30, 30))
        self.icono_color = ImageTk.PhotoImage(self.icono_color)
        self.boton_color = Button(self.frame, image=self.icono_color, command=self.paleta, padx=10, pady=10)
        self.boton_color.place(x=55, y=55)
        Tooltip(self.boton_color, text = "Paleta de colores. \Alt+u")

        icono_triangulo = Image.open(r"icono\triangulo.png")
        self.icono_triangulo = icono_triangulo.resize((30, 30))
        self.icono_triangulo = ImageTk.PhotoImage(self.icono_triangulo)
        self.boton_triangulo = Button(self.frame, image=self.icono_triangulo, command=self.activar_herramienta_Triangulo, padx=10, pady=10)
        self.boton_triangulo.place(x=55, y=145)
        Tooltip(self.boton_triangulo, text = "Triángulo. \Alt+c")

        icono_imagen = Image.open(r"icono\imagen.png")
        self.icono_imagen = icono_imagen.resize((30, 30))
        self.icono_imagen = ImageTk.PhotoImage(self.icono_imagen)
        self.boton_imagen = Button(self.frame, image=self.icono_imagen, command=self.importar_image, padx=10, pady=10)
        self.boton_imagen.place(x=10, y=235)
        Tooltip(self.boton_imagen, text = "Importar imágen. \Alt+n")

        icono_revertir = Image.open(r"icono\deshacer.png")
        self.icono_revertir = icono_revertir.resize((30, 30))
        self.icono_revertir = ImageTk.PhotoImage(self.icono_revertir)
        self.boton_revertir = Button(self.frame, image=self.icono_revertir, command=self.deshacer, padx=10, pady=10)
        self.boton_revertir.place(x=10, y=190)
        Tooltip(self.boton_revertir, text = "Deshacer. \Alt+z")

        icono_mover = Image.open(r"icono\moverse.png")
        self.icono_mover = icono_mover.resize((30, 30))
        self.icono_mover = ImageTk.PhotoImage(self.icono_mover)
        self.boton_mover = Button(self.frame, image=self.icono_mover, command=self.Activar_Herramienta_Mover, padx=10, pady=10)
        self.boton_mover.place(x=55, y=190)
        Tooltip(self.boton_mover, text = "Mover figura. \Alt+t")

        icono_rotar2 = Image.open(r"icono\+15.png")
        self.icono_rotar2 = icono_rotar2.resize((30, 30))
        self.icono_rotar2 = ImageTk.PhotoImage(self.icono_rotar2)
        self.boton_rotar2 = Button(self.frame, image=self.icono_rotar2, command=self.activar_herramienta_rotar2, padx=10, pady=10)
        self.boton_rotar2.place(x=10, y=280)
        Tooltip(self.boton_rotar2, text = "Rotar figura a la izquierda. \Alt+f")

        icono_rotar = Image.open(r"icono\-15.png")
        self.icono_rotar = icono_rotar.resize((30, 30))
        self.icono_rotar = ImageTk.PhotoImage(self.icono_rotar)
        self.boton_rotar = Button(self.frame, image=self.icono_rotar, command=self.activar_herramienta_rotar, padx=10, pady=10)
        self.boton_rotar.place(x=55, y=280)
        Tooltip(self.boton_rotar, text = "Rotar figura a la derecha. \Alt+j")

        self.ventana.mainloop()