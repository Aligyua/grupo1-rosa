from tkinter import Frame, messagebox, mainloop,ttk, StringVar, Spinbox, IntVar
from tkinter import Tk, Label, Button, Entry
import sqlite3
import datetime
import re
from PIL import Image, ImageTk


class Login:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.geometry("800x600")
        self.ventana.title("Inicia Sesion en Bloom Music")

        fondo = "#fff8ff"


        #---------------------------------------------
        #----------------SQL PART---------------------
        #---------------------------------------------

        self.conn = sqlite3.connect("Database_Bloom_Music.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''   
            CREATE TABLE IF NOT EXISTS Usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_Usuario VARCHAR(15) NOT NULL,
                email VARCHAR(15) NOT NULL,
                contraseña VARCHAR(15) NOT NULL,
                Fecha_registro DATE,
                genero VARCHAR(15) NOT NULL
            )
        ''') #CREA LA TABLA POR SI NO EXISTE
        self.conn.commit()
        


        #---------------------------------------------
        #----------------FRAMES-----------------------
        #---------------------------------------------
        
        self.frame_superior = Frame(self.ventana)
        self.frame_superior.configure(bg=fondo)
        self.frame_superior.pack(fill="both",expand=True)
        
        self.frame_inferior = Frame(self.ventana)
        self.frame_inferior.configure(bg=fondo)
        self.frame_inferior.pack(fill="both",expand=True)
        
        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)
        
        #-------------------------------------------------------------
        #-----------------------PARTE DE TITULO-----------------------
        #----------------------IMAGEN Y LOGO Lg-----------------------
        
        self.img = Image.open("LogoLogin.png")
        self.img = self.img.resize((200,200))
        self.render = ImageTk.PhotoImage(self.img)
        self.fondo = Label(self.frame_superior, image = self.render, bg = fondo)
        self.fondo.pack(expand=True, fill="both", side="top")
        
        

        #-------------------------------------------------------------
        #-----------------------PARTE DE TITULO-----------------------
        #-------------------------------------------------------------
        
        self.titulo = Label (self.frame_superior,
                             text= "Inicia Sesión en Bloom Music",
                             font=("Calista MT", 20, "bold"),
                             bg=fondo
                             )
        self.titulo.pack(side="top", pady=20)
        
        
        
        #-------------------------------------------------------------
        #-----------------------PARTE DE DATOS-----------------------
        #-------------------------------------------------------------
        
        self.label_usuario = Label (self.frame_inferior,
                                    text="Usuario/Correo",
                                    font=("Arial",18),
                                    bg= fondo,
                                    fg= "black"
                                    )
        self.label_usuario.grid(row=0, column=0, padx=10, sticky="e") 
        #el sticky seria que cada vez q se utilice se vaya hacia el ESTE "e" sin importar su resolucion
        
        self.entry_usuario = Entry(self.frame_inferior,
                                   text="Usuario/Correo",
                                   font=("Arial",18),
                                   bg=fondo,
                                   fg="black")
        
        self.entry_usuario.grid(row=0, column=1, columnspan=3, padx=5, sticky="w")
        
        
        
        
        
        self.label_passw = Label (self.frame_inferior,
                                    text="Contraseña",
                                    font=("Arial",18),
                                    bg= fondo,
                                    fg= "black"
                                    )
        self.label_passw.grid(row=1, column=0, padx=10, sticky="e")
        
        
        
        self.entry_passw = Entry(self.frame_inferior,
                                   text="Contraseña",
                                   font=("Arial",18),
                                   bg=fondo,
                                   fg="black",
                                   show="*"
                                   ) #Lo que va a ver el usuario sin importar el input
        self.entry_passw.grid(row=1, column=1, columnspan=3, padx=5, sticky= "w")
        

        #-------------------------------------------------------------
        #-----------------------PARTE DE BOTONES----------------------
        #-------------------------------------------------------------


        self.boton_ingresar = Button (self.frame_inferior,
                                     text="Iniciar Sesión",
                                     width=16,
                                     font=("Arial",12),
                                     command=self.entrar)
        self.boton_ingresar.grid(row=2, column=0, columnspan=2, pady=35)

        
        self.boton_registro = Button (self.frame_inferior,
                                     text="Registrarse",
                                     width=16,
                                     font=("Arial",12),
                                     command=self.irARegistroI
                                     )
        self.boton_registro.grid(row=3, column=0, columnspan=2, pady=0)


        mainloop()


    def entrar(self):
        nombre = self.entry_usuario.get()
        contra = self.entry_passw.get()

        self.cursor.execute("SELECT * FROM usuario WHERE nombre_Usuario = ? AND contraseña = ?", (nombre, contra))
        usuario = self.cursor.fetchone()

        if usuario:
            messagebox.showinfo("Bloom Music", "¡Bienvenido!")
            self.ventana.destroy() # Cierra la ventana de login al iniciar sesión correctamente.
        else:
            messagebox.showerror("Bloom Music", "Nombre de usuario o contraseña incorrectos.")

        self.conn.close() # Cierra la conexión a la base de datos
        #La primera parte es el titulo, el segundo el mensaje 

    def irARegistroI(self):
        self.ventana.destroy()
        RegistroI()

datos_usuario = {}
class GestorDeUsuarios:
    def __init__(self):
        self.conn = sqlite3.connect('Database_Bloom_Music.db')
        self.cursor = self.conn.cursor()
    def guardar_usuario(self, datos):
        try:
            fecha_nacimiento = datos['fecha_nacimiento']
            self.cursor.execute("INSERT INTO Usuario (nombre_Usuario, email, contraseña, fecha_registro,genero) VALUES (?, ?, ?, ?,?)",
                                (datos['nombre'], datos['email'], datos['contraseña'], fecha_nacimiento, datos['genero']))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El nombre de usuario o correo electrónico ya existe.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
        finally:
            if self.conn:
                self.conn.close()


class RegistroI:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.geometry("800x600")
        self.ventana.title("Registrate en Bloom Music")

        fondo = "#fff8ff"

        #---------------------------------------------
        #----------------FRAMES-----------------------
        #---------------------------------------------
        
        self.frame_superior = Frame(self.ventana)
        self.frame_superior.configure(bg=fondo)
        self.frame_superior.pack(fill="both",expand=True)
        
        self.frame_inferior = Frame(self.ventana)
        self.frame_inferior.configure(bg=fondo)
        self.frame_inferior.pack(fill="both",expand=True)
        
        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)
        
        #-------------------------------------------------------------
        #-----------------------PARTE DE TITULO-----------------------
        #----------------------IMAGEN Y LOGO Lg-----------------------
        
        self.img = Image.open("LogoLogin.png")
        self.img = self.img.resize((200,200))
        self.render = ImageTk.PhotoImage(self.img)
        self.fondo = Label(self.frame_superior, image = self.render, bg = fondo)
        self.fondo.pack(expand=True, fill="both", side="top")
        
        

        #-------------------------------------------------------------
        #-----------------------PARTE DE TITULO-----------------------
        #-------------------------------------------------------------
        
        self.titulo = Label (self.frame_superior,
                             text= "Registrate para empezar a escuchar contenido",
                             font=("Calista MT", 20, "bold"),
                             bg=fondo
                             )
        self.titulo.pack(side="top", pady=20)
        
        
        
        #-------------------------------------------------------------
        #-----------------------PARTE DE DATOS-----------------------
        #-------------------------------------------------------------
        
        self.label_correo = Label (self.frame_inferior,
                                    text="Correo",
                                    font=("Arial",18),
                                    bg= fondo,
                                    fg= "black"
                                    )
        self.label_correo.grid(row=0, column=0, padx=10, sticky="e") 
        #el sticky seria que cada vez q se utilice se vaya hacia el ESTE "e" sin importar su resolucion
        
        self.entry_correo = Entry(self.frame_inferior,
                                   text="Correo",
                                   font=("Arial",18),
                                   bg=fondo,
                                   fg="black")
        
        self.entry_correo.grid(row=0, column=1, columnspan=3, padx=5, sticky="w")
        
        
        
        
    

        #-------------------------------------------------------------
        #-----------------------PARTE DE BOTONES----------------------
        #-------------------------------------------------------------


        self.boton_ingresar = Button (self.frame_inferior,
                                     text="Siguiente",
                                     width=16,
                                     font=("Arial",12),
                                     command=self.irARegistroII
                                     )
        self.boton_ingresar.grid(row=2, column=0, columnspan=2, pady=35)

        
        self.boton_registro = Button (self.frame_inferior,
                                     text="Volver",
                                     width=16,
                                     font=("Arial",12),
                                     command=self.volverLogin
                                     )
        self.boton_registro.grid(row=3, column=0, columnspan=2, pady=0)


        mainloop()

    def volverLogin(self):
        self.ventana.destroy()
        Login()

    def irARegistroII(self):
        email = self.entry_correo.get()
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email): # Validación básica de correo
            messagebox.showerror("Error", "Por favor, ingrese un correo electrónico válido.")
            return
        datos_usuario['email'] = email
        self.ventana.destroy()
        RegistroII()






class RegistroII:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.geometry("800x600")
        self.ventana.title("Registrate en Bloom Music")

        fondo = "#fff8ff"

        #---------------------------------------------
        #----------------FRAMES-----------------------
        #---------------------------------------------
        
        self.frame_superior = Frame(self.ventana)
        self.frame_superior.configure(bg=fondo)
        self.frame_superior.pack(fill="both",expand=True)
        
        self.frame_inferior = Frame(self.ventana)
        self.frame_inferior.configure(bg=fondo)
        self.frame_inferior.pack(fill="both",expand=True)
        
        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)
        
        #-------------------------------------------------------------
        #-----------------------PARTE DE TITULO-----------------------
        #----------------------IMAGEN Y LOGO Lg-----------------------
        
        self.img = Image.open("LogoLogin.png")
        self.img = self.img.resize((200,200))
        self.render = ImageTk.PhotoImage(self.img)
        self.fondo = Label(self.frame_superior, image = self.render, bg = fondo)
        self.fondo.pack(expand=True, fill="both", side="top")
        
        

        #-------------------------------------------------------------
        #-----------------------PARTE DE TITULO-----------------------
        #-------------------------------------------------------------
        
        self.titulo = Label (self.frame_superior,
                             text= "Paso 1 de 3",
                             font=("Calista MT", 20),
                             fg="#a6a6a6",
                             bg=fondo
                             )
        self.titulo = Label (self.frame_superior,
                             text= "Crea una contraseña",
                             font=("Calista MT", 20, "bold"),
                             bg=fondo
                             )
        self.titulo.pack(side="top", pady=20)
        
        
        
        #-------------------------------------------------------------
        #-----------------------PARTE DE DATOS-----------------------
        #-------------------------------------------------------------
        
        self.label_contra = Label (self.frame_inferior,
                                    text="Contraseña",
                                    font=("Arial",18),
                                    bg= fondo,
                                    fg= "black"
                                    )
        self.label_contra.grid(row=0, column=0, padx=10, sticky="e") 
        #el sticky seria que cada vez q se utilice se vaya hacia el ESTE "e" sin importar su resolucion
        
        self.entry_contra = Entry(self.frame_inferior,
                                   text="Contraseña",
                                   font=("Arial",18),
                                   bg=fondo,
                                   fg="black")
        
        self.entry_contra.grid(row=0, column=1, columnspan=3, padx=5, sticky="w")
        


        #-------------------------------------------------------------
        #-----------------------PARTE DE TEXTO DEBAJO-----------------------
        #-------------------------------------------------------------
        
        self.texto = Label (self.frame_superior,
                             text= "Tu contraseña debe contener al menos:",
                             font=("Calista MT", 12),
                             fg="#a6a6a6",
                             bg=fondo
                             )
        self.texto1 = Label (self.frame_superior,
                             text= "1 caracter especial",
                             font=("Calista MT", 12),
                             fg="#a6a6a6",
                             bg=fondo
                             )
        self.texto.pack(side="bottom", pady=0)
        self.texto1.pack(side="bottom", pady=0)
        
        
        
        
    

        #-------------------------------------------------------------
        #-----------------------PARTE DE BOTONES----------------------
        #-------------------------------------------------------------


        self.boton_siguiente = Button (self.frame_inferior,
                                     text="Siguiente",
                                     width=16,
                                     font=("Arial",12),
                                     command=self.siguienteRegistro
                                     )
        self.boton_siguiente.grid(row=2, column=0, columnspan=2, pady=35)

        
        self.boton_volver = Button (self.frame_inferior,
                                     text="Volver",
                                     width=16,
                                     font=("Arial",12),
                                     command=self.volverRegistro
                                     )
        self.boton_volver.grid(row=3, column=0, columnspan=2, pady=0)


        mainloop()

    def volverRegistro(self):
        self.ventana.destroy()
        RegistroI()

    def siguienteRegistro(self):
        contra = self.entry_contra.get()
        if not contra:
            messagebox.showerror("Error", "Por favor, ingrese una contraseña.")
            return
        datos_usuario['contraseña'] = contra
        self.ventana.destroy()
        RegistroIII()

class RegistroIII:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.geometry("800x600")
        self.ventana.title("Registrate en Bloom Music")

        fondo = "#fff8ff"

        #---------------------------------------------
        #----------------SQL PART---------------------
        #---------------------------------------------

        self.conn = sqlite3.connect("Database_Bloom_Music")
        self.cursor = self.conn.cursor()

        #---------------------------------------------
        #----------------FRAMES-----------------------
        #---------------------------------------------

        self.frame_superior = Frame(self.ventana)
        self.frame_superior.configure(bg=fondo)
        self.frame_superior.pack(fill="both",expand=True)

        self.frame_inferior = Frame(self.ventana)
        self.frame_inferior.configure(bg=fondo)
        self.frame_inferior.pack(fill="both",expand=True)

        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)

        #-------------------------------------------------------------
        #-----------------------PARTE DE TITULO-----------------------
        #----------------------IMAGEN Y LOGO Lg-----------------------

        self.img = Image.open("LogoLogin.png")
        self.img = self.img.resize((200,200))
        self.render = ImageTk.PhotoImage(self.img)
        self.fondo = Label(self.frame_superior, image = self.render, bg = fondo)
        self.fondo.pack(expand=True, fill="both", side="top")


        #-------------------------------------------------------------
        #-----------------------PARTE DE TITULO-----------------------
        #-------------------------------------------------------------

        self.titulo = Label (self.frame_superior,
                             text= "Paso 1 de 3",
                             font=("Calista MT", 20),
                             fg="#a6a6a6",
                             bg=fondo
                             )
        self.titulo = Label (self.frame_superior,
                             text= "Crea tu usuario",
                             font=("Calista MT", 20, "bold"),
                             bg=fondo
                             )
        self.titulo.pack(side="top", pady=20)



        #-------------------------------------------------------------
        #-----------------------PARTE DE DATOS-----------------------
        #-------------------------------------------------------------

        self.label_usuario = Label (self.frame_inferior,
                                    text="Nombre de Usuario",
                                    font=("Arial",12),
                                    bg= fondo,
                                    fg= "black"
                                    )
        self.label_usuario.grid(row=0, column=0, padx=10, sticky="e")
        #el sticky seria que cada vez q se utilice se vaya hacia el ESTE "e" sin importar su resolucion

        self.entry_usuario = Entry(self.frame_inferior,
                                   text="Nombre de Usuario",
                                   font=("Arial",12),
                                   bg=fondo,
                                   fg="black")

        self.entry_usuario.grid(row=0, column=1, columnspan=3, padx=5, sticky="w")



        #-------------------------------------------------------------
        #-----------------------PARTE DE TEXTO DEBAJO-----------------------
        #-------------------------------------------------------------

        self.texto = Label (self.frame_superior,
                             text= "Apareceras con este nombre:",
                             font=("Calista MT", 12),
                             fg="#a6a6a6",
                             bg=fondo
                             )

        self.texto.pack(side="top", pady=0)


        










        # ----------------------------------FECHA NACIMIENTO
        self.frame_fecha = Frame(self.frame_inferior, bg=fondo)
        self.frame_fecha.grid(row=2, column=0, columnspan=3, sticky="ew", pady=10) # Expande horizontalmente
        self.frame_fecha.rowconfigure(1, weight=1)
        self.frame_fecha.columnconfigure(1, weight=1) # Permite que los elementos se expandan
        self.frame_fecha.columnconfigure(2, weight=1)
        self.frame_fecha.columnconfigure(3, weight=1)

        self.etiqueta1 = Label(self.frame_fecha, text="Fecha de Nacimiento", bg=fondo,fg="Black")
        

        self.fecha_nacimiento_dia = IntVar()
        self.fecha_nacimiento_mes = StringVar()
        self.fecha_nacimiento_year = IntVar()

        self.spin_fecha_nacimiento_dia = Spinbox(self.frame_fecha,
                                                 textvariable=self.fecha_nacimiento_dia,
                                                 from_=1,  # Día mínimo 1
                                                 to=31,
                                                 increment=1,
                                                 width=5)

        self.lista = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre","Diciembre"]

        self.opciones_fecha_nacimiento_mes = ttk.Combobox(self.frame_fecha, textvariable=self.fecha_nacimiento_mes, values=self.lista, width=15)
        self.fecha_nacimiento_mes.set("Seleccione su Mes de Nac....")
        


        self.spin_fecha_nacimiento_year = Spinbox(self.frame_fecha,
                                                 textvariable=self.fecha_nacimiento_year,
                                                 from_=1900,
                                                 to=2025,
                                                 increment=1,
                                                 width=5)
        self.etiqueta1.grid(row=0, column=1,sticky="ew",padx=5)
        self.spin_fecha_nacimiento_dia.grid(row=0, column=2, padx=5, sticky="ew")
        self.opciones_fecha_nacimiento_mes.grid(row=0, column=3, padx=5, sticky="ew")
        self.spin_fecha_nacimiento_year.grid(row=0, column=4, padx=5, sticky="ew")
        
        
        #GENERO SECCION

        self.frame_genero = Frame(self.frame_inferior, bg=fondo)
        self.frame_genero.grid(row=3, column=0, columnspan=3, sticky="ew", pady=10) # Expande horizontalmente
        self.frame_genero.rowconfigure(1, weight=1)
        self.frame_genero.columnconfigure(1, weight=1) # Permite que los elementos se expandan
        self.frame_genero.columnconfigure(2, weight=1)
        self.frame_genero.columnconfigure(3, weight=1)

        self.etiqueta_resultado = Frame(self.frame_genero)
        self.genero_seleccionado = StringVar()
        self.seleccion = self.genero_seleccionado.get()
        


        
        self.genero_seleccionado.set("Masculino")  # Valor por defecto

# Grupo de botones de opción (Radiobuttons)
        self.radio_masculino = ttk.Radiobutton(self.frame_genero, text="Masculino", variable=self.genero_seleccionado, value="Masculino")
        self.radio_masculino.grid(row=3, column=1, padx=5)

        self.radio_femenino = ttk.Radiobutton(self.frame_genero, text="Femenino", variable=self.genero_seleccionado, value="Femenino")
        self.radio_femenino.grid(row=3, column=2, padx=5)

        self.radio_otro = ttk.Radiobutton(self.frame_genero, text="Otro", variable=self.genero_seleccionado, value="Otro")
        self.radio_otro.grid(row=3, column=3, padx=5)

        #-------------------------------------------------------------
        #-----------------------PARTE DE BOTONES----------------------
        #-------------------------------------------------------------
        

        self.boton_siguiente = Button (self.frame_inferior,
                                     text="Siguiente",
                                     width=16,
                                     font=("Arial",12),
                                     command=self.GuardarBDD
                                     )
        self.boton_siguiente.grid(row=5, column=0, columnspan=2, pady=35)


        self.boton_registro = Button (self.frame_inferior,
                                     text="Volver",
                                     width=16,
                                     font=("Arial",12),
                                     command=self.volverRegistro
                                     )
        self.boton_registro.grid(row=5, column=1, columnspan=2, pady=0)
        mainloop()

    def volverRegistro(self):
        self.ventana.destroy()
        RegistroII()
    
    
    def obtener_numero_mes(self, mes):
        meses = {"Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
                 "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12}
        return meses[mes]
   


    def GuardarBDD(self):


        nombre = self.entry_usuario.get()
        genero= self.genero_seleccionado.get()
        try:
            dia = int(self.spin_fecha_nacimiento_dia.get())
            mes = self.obtener_numero_mes(self.opciones_fecha_nacimiento_mes.get())
            year = int(self.spin_fecha_nacimiento_year.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese una fecha de nacimiento válida.")
            return
        if not nombre or dia == 0 or mes is None or year == 0:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return
        

        try:
            fecha_nacimiento = datetime.date(year, mes, dia)
            datos_usuario['nombre'] = nombre
            datos_usuario['genero'] = genero
            datos_usuario['fecha_nacimiento'] = fecha_nacimiento
            gestor = GestorDeUsuarios()
            if gestor.guardar_usuario(datos_usuario):
                messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
                self.ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo registrar el usuario.  Intenta de nuevo.")
        except ValueError as e:
            messagebox.showerror("Error", f"Fecha inválida: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

         # Cierra la conexión a la base de datos
        #La primera parte es el titulo, el segundo el mensaje 







RegistroIII()