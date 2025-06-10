from tkinter import Frame, messagebox, mainloop,ttk, StringVar, Spinbox, IntVar
from tkinter import Tk, Label, Button, Entry
from PIL import Image, ImageTk
import sqlite3

class Login:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.geometry("800x600")
        self.ventana.title("Inicia Sesion en Bloom Music")

        fondo = "#fff8ff"


        #---------------------------------------------
        #----------------SQL PART---------------------
        #---------------------------------------------

        self.conn = sqlite3.connect("Database_Bloom_Music")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''   
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_Usuario VARCHAR(15) NOT NULL,
                email VARCHAR(15) NOT NULL,
                contraseña VARCHAR(15) NOT NULL,
                Fecha_registro DATE
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
        
        self.label_usuario = Label (self.frame_inferior,
                                    text="Contraseña",
                                    font=("Arial",18),
                                    bg= fondo,
                                    fg= "black"
                                    )
        self.label_usuario.grid(row=0, column=0, padx=10, sticky="e") 
        #el sticky seria que cada vez q se utilice se vaya hacia el ESTE "e" sin importar su resolucion
        
        self.entry_usuario = Entry(self.frame_inferior,
                                   text="Contraseña",
                                   font=("Arial",18),
                                   bg=fondo,
                                   fg="black")
        
        self.entry_usuario.grid(row=0, column=1, columnspan=3, padx=5, sticky="w")
        


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
        self.ventana.destroy()
        RegistroIII()

class RegistroIII:
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
                             text= "Crea tu usuario",
                             font=("Calista MT", 20, "bold"),
                             bg=fondo
                             )
        self.titulo.pack(side="top", pady=20)



        #-------------------------------------------------------------
        #-----------------------PARTE DE DATOS-----------------------
        #-------------------------------------------------------------

        self.label_usuario = Label (self.frame_inferior,
                                    text="Nombre",
                                    font=("Arial",18),
                                    bg= fondo,
                                    fg= "black"
                                    )
        self.label_usuario.grid(row=0, column=0, padx=10, sticky="e")
        #el sticky seria que cada vez q se utilice se vaya hacia el ESTE "e" sin importar su resolucion

        self.entry_usuario = Entry(self.frame_inferior,
                                   text="Nombre",
                                   font=("Arial",18),
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
        #self.opciones_fecha_nacimiento_mes.configure(width=40,
                                                     #activebackground="gray",
                                                     #bd=0,
                                                     #cursor="hand2")
        #self.fecha_nacimiento_mes.set("Seleccione su Mes de Nac....")


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
        
        



        #-------------------------------------------------------------
        #-----------------------PARTE DE BOTONES----------------------
        #-------------------------------------------------------------


        self.boton_ingresar = Button (self.frame_inferior,
                                     text="Siguiente",
                                     width=16,
                                     font=("Arial",12),
                                     #command=self.pasaRegistro2
                                     )
        self.boton_ingresar.grid(row=5, column=0, columnspan=2, pady=35)


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
    
    


Login()