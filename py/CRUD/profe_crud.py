
from tkinter import *
from tkinter import messagebox
from asyncio.windows_events import NULL # para poder manejar los NULL
import sqlite3 as sq3

'''
========================
    PARTE FUNCIONAL
========================
'''
# ********* BBDD *********
# CONECTAR
def conectar():
    global con
    global cur
    con = sq3.connect('mibd.db')
    cur = con.cursor()
    messagebox.showinfo("STATUS", "¡Conectado a la BBDD!")

# LISTAR
def listar():
    class Table():
        def __init__(self, raiz2):
            nombre_cols = ['Legajo', 'Alumno', 'Calificación', 'Email', 'Escuela', 'Localidad', 'Provincia']
            for i in range(cant_cols):
                self.e = Entry(frameppal)
                self.e.config(bg='black', fg='white')
                self.e.grid(row=0, column=i)
                self.e.insert(END,nombre_cols[i])

            for fila in range(cant_filas):
                for col in range(cant_cols):
                    self.e = Entry(frameppal)
                    self.e.grid(row=fila+1, column=col)
                    self.e.insert(END, resultado[fila][col])
                    self.e.config(state='readonly')

    # Crear la ventana y los elementos
    raiz2 = Tk()
    raiz2.title('Listado de alumnos')
    frameppal = Frame(raiz2)
    frameppal.pack(fill='both')
    framecerrar = Frame(raiz2)
    framecerrar.pack(fill='both')
    framecerrar.config(bg=color_texto_boton)
    boton_cerrar = Button(framecerrar, text='Cerrar', command=raiz2.destroy)
    boton_cerrar.config(bg=color_fondo_boton, fg=color_texto_boton, pady=10, padx=10)
    boton_cerrar.pack(fill='both')

    # Obtener los datos de la BBDD
    con = sq3.connect('mibd.db')
    cur = con.cursor()
    query1 = '''SELECT alumnos.legajo, alumnos.nombre, alumnos.nota, alumnos.email, escuelas.nombre, escuelas.localidad, escuelas.provincia FROM alumnos INNER JOIN escuelas ON alumnos.id_escuela = escuelas._id'''
    cur.execute(query1)
    resultado = cur.fetchall()
    cant_filas = len(resultado)
    cant_cols = len(resultado[0])

    tabla = Table(frameppal)
    con.close()
    raiz2.mainloop()

# SALIR
def salir():
    resp = messagebox.askquestion("CONFIRME","¿Desea salir de la aplicación?")
    if resp == 'yes':
        #con.close()
        raiz.destroy()

# ********* LIMPIAR *********
def limpiar():
    legajo.set("")
    alumno.set("")
    email.set("")
    calificacion.set("")
    escuela.set("Seleccione")
    localidad.set("")
    provincia.set("")
    legajo_input.config(state='normal')

# Mostrar Licencia
def mostrar_licencia():
    msg = '''
    Demo de un sistema CRUD en Python para gestión 
    de alumnos  Copyright (C) 2022 - Regina Noemí Molares
    Email: regina.molares@bue.edu.ar\n=======================================
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

# Mostrar AcercaDe
def mostrar_acercade():
    messagebox.showinfo("ACERCA DE...","Creado por Regina N. Molares\npara Codo a Codo 4.0 - Big Data\nNoviembre, 2022\nEmail: regina.molares@bue.edu.ar")

# ******** FUNCIONES GENERALES **************
def buscar_escuelas(actualiza):
    con = sq3.connect('mibd.db')
    cur = con.cursor()
    if actualiza:
        cur.execute('SELECT _id, localidad, provincia FROM escuelas WHERE nombre =?',(escuela.get(),))
    else: # esta opción sólo llena la lista de escuelas para el menú
        cur.execute('SELECT nombre FROM escuelas')
    
    resultado = cur.fetchall() # RECIBO LISTA DE TUPLAS con un elemento "fantasma"     
    retorno=[]
    for e in resultado:
        if actualiza:    
            localidad.set(e[1])        
            provincia.set(e[2])            
        esc = e[0]
        retorno.append(esc)        
    con.close()
    return retorno

# ************ MENU CRUD
# CREATE -> Crear
def crear():
    id_escuela = int(buscar_escuelas(True)[0]) 
    datos = id_escuela, legajo.get(), alumno.get(), calificacion.get(), email.get()
    cur.execute("INSERT INTO alumnos (id_escuela, legajo, nombre, nota, email) VALUES(?,?,?,?,?)", datos)
    con.commit()
    messagebox.showinfo("STATUS","Registro agregado")
    limpiar()

# READ -> Leer
def buscar_legajo():
    query_buscar = '''SELECT alumnos.legajo, alumnos.nombre, alumnos.nota, alumnos.email, escuelas.nombre, escuelas.localidad, escuelas.provincia FROM alumnos INNER JOIN escuelas ON alumnos.id_escuela = escuelas._id WHERE alumnos.legajo='''
    cur.execute(query_buscar + legajo.get())
    resultado = cur.fetchall()
    if resultado == []:
        messagebox.showerror("ERROR","Ese N° de legajo no existe")
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

# UPDATE -> Actualizar
def actualizar():
    id_escuela = int(buscar_escuelas(True)[0]) 
    datos = id_escuela, alumno.get(), calificacion.get(), email.get()
    cur.execute("UPDATE alumnos SET id_escuela=?, nombre =?, nota=?, email=? WHERE legajo="+legajo.get(), datos)
    con.commit()
    messagebox.showinfo("STATUS","Registro actualizado")
    limpiar()

# DELETE -> Borrar
def borrar():
    resp = messagebox.askquestion("BORRAR?", "¿Desea eliminar el registro?")
    if resp == 'yes':
        cur.execute("DELETE FROM alumnos WHERE legajo = " + legajo.get())
        con.commit()
        messagebox.showinfo("STATUS","El registro fue eliminado")
        limpiar()


'''
========================
    INTERFAZ GRÁFICA
========================
'''
# padx / pady
espaciadox = 5
espaciadoy = 5
# framebotones
fondo_framebotones = 'plum'
color_fondo_boton = 'black'
color_texto_boton = fondo_framebotones
# framecampos 
color_fondo = 'cyan'
color_letra = 'black'

raiz = Tk()
raiz.title('Python CRUD - c22611')

# --------- BARRA DEL MENÚ -------------
barramenu = Menu(raiz)
raiz.config(menu = barramenu)

# primer botón: BBDD
bbddmenu = Menu(barramenu, tearoff=0)
bbddmenu.add_command(label='Conectar', command = conectar) # sin paréntesis la llamada a la fx
bbddmenu.add_command(label='Mostrar listado de alumnos', command = listar)
bbddmenu.add_command(label='Salir', command = salir)

# 2° botón: Borrar
borrarmenu = Menu(barramenu, tearoff=0)
borrarmenu.add_command(label='Borrar', command = limpiar)

# 3er botón: Acerca de...
ayudamenu =Menu(barramenu, tearoff=0)
ayudamenu.add_command(label='Licencia', command=mostrar_licencia)
ayudamenu.add_command(label='Acerca de...', command = mostrar_acercade)


# Agrego los botones a barramenu
barramenu.add_cascade(label="BBDD",menu=bbddmenu)
barramenu.add_cascade(label='Borrar', menu=borrarmenu)
barramenu.add_cascade(label='Acerca de...', menu=ayudamenu)

# ------- FRAME CAMPOS ----------
framecampos = Frame(raiz)
framecampos.config(bg=color_fondo) # bg = color de fondo
framecampos.pack(fill='both')

# LABELS
'''
"STICKY"
     n
  nw   ne
w         e
  sw   se
     s
'''
# Apunte: posicionamiento de elemento en tkinter:https://recursospython.com/guias-y-manuales/posicionar-elementos-en-tkinter/
def config_label(mi_label, fila):
    espaciado_labels = {'column':0, 'sticky':'e','padx':espaciadox, 'pady':espaciadoy}
    colores = {'bg':color_fondo, 'fg': color_letra} # fg = foreground color
    mi_label.grid(row=fila, **espaciado_labels)
    mi_label.config(**colores)


legajolabel = Label(framecampos, text= 'Legajo:')
config_label(legajolabel, 0)
#legajolabel.grid(row=0, column=0, sticky='e',padx=10, pady=10)

alumnolabel = Label(framecampos, text= 'Alumno:')
config_label(alumnolabel, 1)
#alumnolabel.grid(row=1, column=0, sticky='e',padx=10, pady=10)

emaillabel = Label(framecampos, text= 'Email:')
config_label(emaillabel, 2)
#emaillabel.grid(row=2, column=0, sticky='e',padx=10, pady=10)

calificacionlabel = Label(framecampos, text= 'Calificación:')
config_label(calificacionlabel, 3)
#calificacionlabel.grid(row=3, column=0, sticky='e',padx=10, pady=10)

escuelalabel = Label(framecampos, text= 'Escuela:')
config_label(escuelalabel, 4)
#escuelalabel.grid(row=4, column=0, sticky='e',padx=10, pady=10)

localidadlabel = Label(framecampos, text= 'Localidad:')
config_label(localidadlabel, 5)
#localidadlabel.grid(row=5, column=0, sticky='e',padx=10, pady=10)

provincialabel = Label(framecampos, text= 'Provincia:')
config_label(provincialabel, 6)
#provincialabel.grid(row=6, column=0, sticky='e',padx=10, pady=10)

# CAMPOS DE INPUT
legajo = StringVar()
alumno = StringVar()
email = StringVar()
calificacion = DoubleVar()
escuela = StringVar()
localidad = StringVar()
provincia = StringVar()

'''
Tipos de datos TKINTER para campos Entry
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
calificacion_input.grid(row=3, column=1, padx=10, pady=10)

lista_escuelas = buscar_escuelas(False)
escuela.set('Seleccione')
escuela_option = OptionMenu(framecampos, escuela, *lista_escuelas)
escuela_option.grid(row=4, column=1, padx=10, pady=10)

#escuela_input = Entry(framecampos, textvariable = escuela)
#escuela_input.grid(row=4, column=1, padx=10, pady=10)

localidad_input = Entry(framecampos, textvariable = localidad)
localidad_input.grid(row=5, column=1, padx=10, pady=10)
localidad_input.config(state='readonly')

provincia_input = Entry(framecampos, textvariable = provincia)
provincia_input.grid(row=6, column=1, padx=10, pady=10)
provincia_input.config(state='readonly')

# FRAME DE LOS BOTONES CRUD
framebotones = Frame(raiz)
framebotones.config(bg=fondo_framebotones)
framebotones.pack(fill='both')

boton_crear = Button(framebotones, text='Crear', command=crear)
boton_crear.config(bg=color_fondo_boton, fg=color_texto_boton)
boton_crear.grid(row=0, column=0, padx=10, pady=10)

boton_leer = Button(framebotones, text = 'Leer', command=buscar_legajo)
boton_leer.config(bg=color_fondo_boton, fg=color_texto_boton)
boton_leer.grid(row=0, column=1, padx=10, pady=10)

boton_actualizar = Button(framebotones, text='Actualizar', command=actualizar)
boton_actualizar.config(bg=color_fondo_boton, fg=color_texto_boton)
boton_actualizar.grid(row=0, column=2, padx=10, pady=10)

boton_borrar = Button(framebotones, text='Borrar', command=borrar)
boton_borrar.config(bg=color_fondo_boton, fg=color_texto_boton)
boton_borrar.grid(row=0, column=3, padx=10, pady=10)

# FRAME DEL PIE
framecopy = Frame(raiz)
framecopy.config(bg='black')
framecopy.pack(fill='both')

copylabel = Label(framecopy, text = '(2022) por Regina Molares para CaC 4.0 - Big Data')
copylabel.grid(padx=10, pady=10)
copylabel.config(bg='black', fg='white')

raiz.mainloop() # ULTIMA LÍNEA
