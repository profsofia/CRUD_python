from tkinter import *
#se encarga de crear los objetos de interfaz grafica
from asyncio.windows_events import NULL # para poder manejar los NULL
import sqlite3 as sq3
from tkinter import messagebox
#from tkinter import messagebox

'''
=========================
PARTE FUNCIONAL
=========================
'''

#### BBDD >>>>>>>>>>>>>>>>>

# CONECTAR


def conectar():
  global con
  global cur
  con = sq3.connect('mibd.db')
  cur = con.cursor()
  messagebox.showinfo('STATUS', 'Conectado a la BBDD!')

## LISTAR >>>>>>
def listar():
  class Table():
    #método constructor
    def __init__(self, raiz2):
      nombre_cols = ['Legajo', 'Alumno', 'Calificación', 'Email', 'Escuela', 'Localidad', 'Provincia']
      for col in range(cant_columnas):
        ## entry dentro del frame principal para la lista nombre_cols
        self.e = Entry(frameprincipal)
        self.e.config(bg='black', fg='white')
        self.e.grid(row=0, column=col)
        self.e.insert(END, nombre_cols[col])
      for fila in range(cant_filas):
        for columna in range(cant_columnas):
          self.e = Entry(frameprincipal)
          self.e.grid(row=fila+1, column=columna)
          self.e.insert(END, result[fila][columna])
          self.e.config(state='readonly')
  ## CREA LA VENTANA
  raiz2 = Tk()
  raiz2.title('Listado de alumnos')
  # donde se va a encontrar la tabla
  frameprincipal = Frame(raiz2)
  frameprincipal.pack(fill='both')
  # boton para cerrar la tabla
  framecerrar = Frame(raiz2)
  framecerrar.pack(fill='both')
  framecerrar.config(bg = color_texto_boton)

  boton_cerrar = Button(framecerrar, text='Cerrar', command=raiz2.destroy)
  boton_cerrar.config(bg=color_fondo_boton, fg=color_texto_boton, pady=espaciadoy, padx=espaciadox)
  boton_cerrar.pack(fill='both')
  ##### FIN DE CREAR LA VENTANA

  ### CONEXIÓN A LA BBDD
  con = sq3.connect('mibd.db')
  cur = con.cursor()
  query1= '''SELECT alumnos.legajo, alumnos.nombre, alumnos.nota, alumnos.email, escuelas.nombre, escuelas.localidad, escuelas.provincia FROM alumnos INNER JOIN escuelas ON alumnos.id_escuela = escuelas._id'''
  cur.execute(query1)
  result = cur.fetchall()
  cant_filas = len(result)
  cant_columnas = len(result[0])


  tabla = Table(frameprincipal)
  con.close()
  raiz2.mainloop()


# SALIR

def salir():
  resp = messagebox.askquestion("CONFIRME", "¿Desea salir de la aplicación?")
  if resp == 'yes':
    #con.close()
    raiz.destroy()



# limpiar
def limpiar():
    legajo.set("")
    alumno.set("")
    email.set("")
    calificacion.set("")
    escuela.set("Seleccione")
    localidad.set("")
    provincia.set("")
    legajo_input.config(state='normal')

## MOSTRAR ACERCA DE >>>>>>>>
def mostrar_acercade():
  messagebox.showinfo("ACERCA DE...", "Creado por Sofía Schenone \npara CaC 4.0 - Big Data\nNoviembre, 2022\nEmail: sofiainesschenone@gmail.com")

# Licencia >>>>>>>>>
def mostrar_licencia():
  msg = '''
    Sistema CRUD en Python
    Copyright (C) 2022 - Sofia Schenone
    Email: sofiainesschenone@gmail.com\n=======================================
    This program is free software: you can redistribute it 
    and/or modify it under the terms of the GNU General Public 
    License as published by the Free Software Foundation, 
    either version 3 of the License, or (at your option) any 
    later version.
    This program is distributed in the hope that it will be 
    useful, but WITHOUT ANY WARRANTY; without even the 
    implied warranty of MERCHANTABILITY or FITNESS FOR A 
    PARTICULAR PURPOSE.  See the GNU General Public License 
    for more details.
    You should have received a copy of the GNU General Public 
    License along with this program.  
    If not, see <https://www.gnu.org/licenses/>.'''
  messagebox.showinfo("LICENCIA", msg)


##### FUNCIONES GENERALES >>>>>>>>>>>>>>

def buscar_escuelas(actualiza):
  con = sq3.connect('mibd.db')
  cur = con.cursor()
  if actualiza:
    # se pone coma en el get por el elemento fantasma, se recibe una tupla de un solo elemento, no es un string
     cur.execute('SELECT _id, localidad, provincia FROM escuelas WHERE nombre=?', (escuela.get(), ))
      #necesito todos los datos de una escuela
  else:
    cur.execute('SELECT nombre FROM escuelas')
    
  resultado = cur.fetchall() # Recibe una lista con tuplas
  retorno = []
  #print(resultado)
  for e in resultado:
    if actualiza:
      localidad.set(e[1])
      provincia.set(e[2])
    esc = e[0]
    retorno.append(esc)


    # solo necesito una lista con todas las escuelas
  con.close()
  return retorno


####################### Menú CRUD >>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# CREATE
def crear():
    id_escuela = int(buscar_escuelas(True)[0]) 
    datos = id_escuela, legajo.get(), alumno.get(), calificacion.get(), email.get()
    cur.execute("INSERT INTO alumnos (id_escuela, legajo, nombre, nota, email) VALUES(?,?,?,?,?)", datos)
    con.commit()
    messagebox.showinfo("STATUS","Registro agregado")
    limpiar()

# UPDATE
def actualizar():
   id_escuela = int(buscar_escuelas(True)[0]) 
   datos = id_escuela, alumno.get(), calificacion.get(), email.get()
   cur.execute("UPDATE alumnos SET id_escuela=?, nombre=?, nota=?, email=? WHERE legajo="+legajo.get(), datos)
   con.commit()
   messagebox.showinfo("STATUS","Registro actualizado")
   limpiar()
# DELETE
def borrar():
  resp= messagebox.askquestion("BORRAR?", "¿Desea eliminar el registro?")
  if resp == 'yes':
    cur.execute("DELETE FROM alumnos WHERE legajo ="+ legajo.get())
    con.commit()
    messagebox.showinfo("STATUS", "El registro fué eliminado")
    limpiar()

# READ
def buscar_legajo():
  query_buscar = '''SELECT alumnos.legajo, alumnos.nombre, alumnos.nota, alumnos.email, escuelas.nombre, escuelas.localidad, escuelas.provincia FROM alumnos INNER JOIN escuelas ON alumnos.id_escuela = escuelas._id WHERE alumnos.legajo='''
  cur.execute(query_buscar + legajo.get())
  resultado = cur.fetchall()
  if resultado ==[]:
    messagebox.showerror("ERROR", "Ese N° de legajo no existe")
    legajo.set("")
  else:
    for campo in resultado:
      alumno.set(campo[1])
      calificacion.set(campo[2])
      email.set(campo[3])
      escuela.set(campo[4])
      localidad.set(campo[5])
      provincia.set(campo[6])
      legajo_input.config(state='disabled')
######### FIN CRUD >>>>>>>>>>>>>>>>>>>>>>>>>>>
'''
=========================
    INTERFAZ GRÁFICA
=========================
'''

# padx / pady
espaciadox = 10
espaciadoy = 10

# Colores
fondo_framebotones = 'gray5'
color_fondo_boton = 'DarkOrange2'
color_texto_boton = 'AntiqueWhite1'
# framecampos
color_fondo = 'gray5'
color_letra = 'AntiqueWhite1'

raiz = Tk()
raiz.title('Python CRUD - c22611')

# ---------BARRA DEL MENÚ------------
#le dice al papa donde va a estar ubicado el hijo barramenu
barramenu = Menu(raiz)
# Lo configura como un menu
raiz.config(menu = barramenu)

# primer boton : BBDD
bbddmenu = Menu(barramenu, tearoff=0)

bbddmenu.add_command(label='Conectar', command=conectar) # sin paréntesis, para que lo ejecute cuando se aprieta el botón.
bbddmenu.add_command(label="Mostrar listado de alumnos", command= listar)
bbddmenu.add_command(label='Salir', command=salir)
# para que se cree un boton desplegable

# 2° boton: Borrar
borrarmenu = Menu(barramenu, tearoff=0)
borrarmenu.add_command(label='Borrar', command=limpiar)

# 3° boton : Acerca de...
ayudamenu = Menu(barramenu, tearoff=0)
ayudamenu.add_command(label='Licencia', command=mostrar_licencia)
ayudamenu.add_command(label='Acerca de...', command=mostrar_acercade)


# agrego los botones a barra menu
barramenu.add_cascade(label="BBDD", menu=bbddmenu)
barramenu.add_cascade(label='Borrar', menu=borrarmenu)
barramenu.add_cascade(label='Acerca de..', menu=ayudamenu)


# --------- FRAME CAMPOS -------------
framecampos = Frame(raiz)
framecampos.config(bg=color_fondo)
framecampos.pack(fill = 'both') #adaptar su tamaño a lo que tiene dentro
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

def config_label(mi_label, fila):
  espaciado_labels = {
    'column':0,
    'sticky':'e',
    'padx':espaciadox,
    'pady':espaciadoy
  }
  colores = {
    'bg':color_fondo,
    'fg': color_letra
  }
  mi_label.grid(row=fila, **espaciado_labels)
  mi_label.config(**colores)

# LABELS

legajolabel = Label(framecampos, text='Legajo: ')
config_label(legajolabel, 0)
#legajolabel.grid(row=0, column=0, sticky='e', padx=10,pady=10)

alumnolabel = Label(framecampos, text='Alumno: ')
config_label(alumnolabel, 1)

emaillabel = Label(framecampos, text='Email: ')
config_label(emaillabel, 2)

calificacionlabel = Label(framecampos, text='Calificaión: ')
config_label(calificacionlabel, 3)

escuelalabel = Label(framecampos, text='Escuela: ')
config_label(escuelalabel, 4)

localidadlabel = Label(framecampos, text='Localidad: ')
config_label(localidadlabel, 5)

provincialabel = Label(framecampos, text='Provincia: ')
config_label(provincialabel, 6)


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

#escuela_input = Entry(framecampos, textvariable = escuela)
#escuela_input.grid(row=4, column=1, padx=10, pady=10)
lista_escuelas = buscar_escuelas(False)
escuela.set('Seleccione')
escuela_option =OptionMenu(framecampos, escuela, *lista_escuelas)
escuela_option.grid(row=4, column=1, padx=10, pady=10)

localidad_input = Entry(framecampos, textvariable = localidad)
localidad_input.grid(row=5, column=1, padx=10, pady=10)
localidad_input.config(state='readonly')
provincia_input = Entry(framecampos, textvariable = provincia)
provincia_input.grid(row=6, column=1, padx=10, pady=10)
provincia_input.config(state='readonly')

# FRAME DE LOS BOTONES CRUD

def config_botones(mi_boton, columna):
  espaciado_botones = {
    'row':0,
    'sticky':'e',
    'padx':espaciadox,
    'pady':espaciadoy
  }
  colores = {
    'bg':color_fondo_boton,
    'fg': color_letra
  }
  mi_boton.grid(column=columna, **espaciado_botones)
  mi_boton.config(**colores)

framebotones = Frame(raiz)
framebotones.config(bg=color_fondo)
framebotones.pack(fill = 'both')

boton_crear = Button(framebotones, text='Crear', command=crear)
config_botones(boton_crear,0)
#boton_crear.grid(row = 0, column = 0, padx = 10, pady= 10)

boton_leer = Button(framebotones, text='Leer', command=buscar_legajo)
config_botones(boton_leer,1)

#boton_leer.grid(row = 0, column = 1, padx = 10, pady= 10)

boton_actualizar = Button(framebotones, text='Actualizar', command=actualizar)
config_botones(boton_actualizar,2)
#boton_actualizar.grid(row = 0, column = 2, padx = 10, pady= 10)

boton_borrar = Button(framebotones, text='Borrar', command=borrar)
config_botones(boton_borrar,3)
#boton_borrar.grid(row = 0, column = 3, padx = 10, pady= 10)

# FRAME DEL PIE

framecopy = Frame(raiz)
framecopy.config(bg=color_fondo)
framecopy.pack(fill = 'both')

copylabel = Label(framecopy, text = '(2022) por Sofia Schenone para CaC 4.0- Big Data')
copylabel.config(bg=color_fondo, fg = 'white')
copylabel.grid(padx=10, pady=10)

# esta a la espera de que le demos la instruccion de cerrado
raiz.mainloop()