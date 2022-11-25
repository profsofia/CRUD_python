from tkinter import *
#se encarga de crear los objetos de interfaz grafica


'''
=========================
    INTERFAZ GRÁFICA
=========================
'''

raiz = Tk()
raiz.title('Python CRUD - c22611')

# ---------BARRA DEL MENÚ------------
#le dice al papa donde va a estar ubicado el hijo barramenu
barramenu = Menu(raiz)
# Lo configura como un menu
raiz.config(menu = barramenu)

# primer boton : BBDD
bbddmenu = Menu(barramenu, tearoff=0)

bbddmenu.add_command(label='Conectar')
bbddmenu.add_command(label='Salir')
# para que se cree un boton desplegable

# 2° boton: Borrar
borrarmenu = Menu(barramenu, tearoff=0)
borrarmenu.add_command(label='Borrar')

# 3° boton : Acerca de...
ayudamenu = Menu(barramenu, tearoff=0)
ayudamenu.add_command(label='Licencia')
ayudamenu.add_command(label='Acerca de...')

# agrego los botones a barra menu
barramenu.add_cascade(label="BBDD", menu=bbddmenu)
barramenu.add_cascade(label='Borrar', menu=borrarmenu)
barramenu.add_cascade(label='Acerca de..', menu=ayudamenu)


# --------- FRAME CAMPOS -------------
framecampos = Frame(raiz)
framecampos.pack() #adaptar su tamaño a lo que tiene dentro
# Labels
'''
"STICKY"
     n
  nw   ne
w         e
  sw   se
     s
'''
#Apunte: posicionamiento de elemento en tkinter:https://recursospython.com/guias-y-manuales/posicionar-elementos-en-tkinter/

# LABELS

legajolabel = Label(framecampos, text='Legajo: ')
legajolabel.grid(row=0, column=0, sticky='e', padx=10,pady=10)

alumnolabel = Label(framecampos, text='Alumno: ')
alumnolabel.grid(row=1, column=0, sticky='e', padx=10, pady=10)

emaillabel = Label(framecampos, text='Email: ')
emaillabel.grid(row=2, column=0, sticky='e', padx=10, pady=10)

calificacionlabel = Label(framecampos, text='Calificaión: ')
calificacionlabel.grid(row=3, column=0, sticky='e', padx=10, pady=10)

escuelalabel = Label(framecampos, text='Escuela: ')
escuelalabel.grid(row=4, column=0, sticky='e', padx=10, pady=10)

localidadlabel = Label(framecampos, text='Localidad: ')
localidadlabel.grid(row=5, column=0, sticky='e', padx=10, pady=10)

provincialabel = Label(framecampos, text='Provincia: ')
provincialabel.grid(row=6, column=0, sticky='e', padx=10, pady=10)

# campos de input

legajo = StringVar()
alumno = StringVar()
email = StringVar()
calificacion = DoubleVar()
escuela = StringVar()
localidad = StringVar()
provincia = StringVar()

'''
tipos de datos TKINTER para campos Entry
entero = IntVar()  # Declara variable de tipo entera
flotante = DoubleVar()  # Declara variable de tipo flotante
cadena = StringVar()  # Declara variable de tipo cadena
booleano = BooleanVar()  # Declara variable de tipo booleana
'''

legajo_input = Entry(framecampos, textvariable = legajo)
legajo_input.grid(row=0, column=1, padx=10, pady=10)

alumno_input = Entry(framecampos, textvariable = alumno)
alumno_input.grid(row=1, column=1, padx=10, pady=10)

email_input = Entry(framecampos, textvariable = email)
email_input.grid(row=2, column=1, padx=10, pady=10)


calificacion_input = Entry(framecampos, textvariable = calificacion)
calificacion_input.grid(row=3, column=1,  padx=10, pady=10)

escuela_input = Entry(framecampos, textvariable = escuela)
escuela_input.grid(row=4, column=1, padx=10, pady=10)

localidad_input = Entry(framecampos, textvariable = localidad)
localidad_input.grid(row=5, column=1, padx=10, pady=10)


provincia_input = Entry(framecampos, textvariable = provincia)
provincia_input.grid(row=6, column=1, padx=10, pady=10)


# FRAME DE LOS BOTONES CRUD

framebotones = Frame(raiz)
framebotones.pack()

boton_crear = Button(framebotones, text='Crear')
boton_crear.grid(row = 0, column = 0, padx = 10, pady= 10)

boton_leer = Button(framebotones, text='Leer')
boton_leer.grid(row = 0, column = 1, padx = 10, pady= 10)

boton_actualizar = Button(framebotones, text='Actualizar')
boton_actualizar.grid(row = 0, column = 2, padx = 10, pady= 10)

boton_borrar = Button(framebotones, text='Borrar')
boton_borrar.grid(row = 0, column = 3, padx = 10, pady= 10)

# FRAME DEL PIE

framecopy = Frame(raiz)
framecopy.pack()

copylabel = Label(framecopy, text = '(2022) por Sofia Schenone para CaC 4.0- Big Data')
copylabel.grid(padx=10, pady=10)

# esta a la espera de que le demos la instruccion de cerrado
raiz.mainloop()