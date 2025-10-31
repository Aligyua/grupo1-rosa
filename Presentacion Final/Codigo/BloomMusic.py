# BloomMusic.py - VERSIÓN OPTIMIZADA Y MODULAR
"""
BLOOM MUSIC - REPRODUCTOR DE MÚSICA
====================================
Versión optimizada con sistema modular de navegación
"""

import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

import pygame
from mutagen.mp3 import MP3

import os, sys, time
import datetime
import re
import random
import json

# Importar módulos personalizados
try:
    from config_persistente import GestorBaseDatosPersistente
    from GestorVentanas import GestorVentanas
    from PaginaEditarPerfil import abrir_editar_perfil
    from radioBloom import RadioModule
except ImportError as e:
    print(f"⚠️ Error importando módulos: {e}")
    print("Asegúrate de que todos los archivos estén en la misma carpeta")
    sys.exit(1)


def resource_path(relative_path):
    """
    Obtiene la ruta absoluta de un recurso, funciona tanto en desarrollo
    como cuando está empaquetado con PyInstaller.
    
    Args:
        relative_path: Ruta relativa al recurso (ej: 'LogoLogin.png')
    
    Returns:
        Ruta absoluta al recurso
    """
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Si no existe _MEIPASS, estamos en desarrollo normal
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Inicializar Pygame
pygame.mixer.init()

# Variable global para datos de registro
datos_usuario = {}

# ==============================================================================
# RESPONSIVE MANAGER (Heredado del código original)
# ==============================================================================

class ResponsiveManager:
    def __init__(self, root):
        self.root = root
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        
        self.base_width = min(1200, int(self.screen_width * 0.8))
        self.base_height = min(800, int(self.screen_height * 0.8))
        
        self.scale_factor = min(self.screen_width / 1920, self.screen_height / 1080)
        self.scale_factor = max(0.85, min(1.3, self.scale_factor))
        
    def get_window_geometry(self):
        x = (self.screen_width - self.base_width) // 2
        y = (self.screen_height - self.base_height) // 2
        return f"{self.base_width}x{self.base_height}+{x}+{y}"
    
    def scale_font(self, base_size):
        return max(8, int(base_size * self.scale_factor))
    
    def scale_dimension(self, base_dimension):
        return max(1, int(base_dimension * self.scale_factor))
    
    def get_sidebar_width(self):
        if self.base_width < 800:
            return 180
        elif self.base_width < 1000:
            return 220
        else:
            return 250

# ==============================================================================
# LOGIN (Heredado con mejoras mínimas)
# ==============================================================================

class Login:
    def __init__(self):
        self.ventana = Tk()
        self.responsive = ResponsiveManager(self.ventana)
        
        self.ventana.geometry(self.responsive.get_window_geometry())
        self.ventana.title("Bloom Music - Iniciar Sesión")
        self.ventana.minsize(600, 500)
        
        self.gestor_bd = GestorBaseDatosPersistente()
        fondo = "#fff8ff"
        self.ventana.configure(bg=fondo)
        
        # Frame con scroll
        canvas = tk.Canvas(self.ventana, bg=fondo, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.ventana, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas, bg=fondo)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        def configure_canvas(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind('<Configure>', configure_canvas)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        main_container = Frame(self.scrollable_frame, bg=fondo)
        main_container.pack(expand=True, pady=20)
        
        # Logo
        logo_size = self.responsive.scale_dimension(200)
        try:
            logo_path = resource_path("LogoLogin.png")  # ✅ USAR resource_path()
            img = Image.open(logo_path).resize((logo_size, logo_size), Image.LANCZOS)
            render = ImageTk.PhotoImage(img)
            logo_label = Label(main_container, image=render, bg=fondo)
            logo_label.image = render
            logo_label.pack(pady=(0, 20))
        except:
            pass
        
        Label(main_container, text="Inicia Sesión en Bloom Music",
              font=("Helvetica", self.responsive.scale_font(20), "bold"), 
              bg=fondo).pack(pady=(0, 30))
        
        # Campos
        campos_frame = Frame(main_container, bg=fondo)
        campos_frame.pack(pady=20)
        campos_frame.grid_columnconfigure(1, weight=1)
        
        Label(campos_frame, text="USUARIO", 
              font=("Helvetica", self.responsive.scale_font(14)), 
              bg=fondo).grid(row=0, column=0, sticky="e", padx=(0, 15), pady=15)
        
        entry_width = max(25, self.responsive.scale_dimension(30))
        self.entry_usuario = Entry(campos_frame, 
                                   font=("Helvetica", self.responsive.scale_font(14)), 
                                   width=entry_width)
        self.entry_usuario.grid(row=0, column=1, pady=15, sticky="ew")
        
        Label(campos_frame, text="CONTRASEÑA", 
              font=("Helvetica", self.responsive.scale_font(14)), 
              bg=fondo).grid(row=1, column=0, sticky="e", padx=(0, 15), pady=15)
        
        password_frame = Frame(campos_frame, bg=fondo)
        password_frame.grid(row=1, column=1, pady=15, sticky="ew")
        
        self.entry_passw = Entry(password_frame, 
                                font=("Helvetica", self.responsive.scale_font(14)), 
                                width=max(23, self.responsive.scale_dimension(27)), 
                                show="*")
        self.entry_passw.pack(side="left", fill="x", expand=True)
        self.entry_passw.bind('<Return>', lambda e: self.entrar())
        
        self.show_password = False
        self.btn_toggle_password = Button(password_frame, text="👁", 
                                          font=("Helvetica", self.responsive.scale_font(12)),
                                          bg=fondo, relief="flat", cursor="hand2",
                                          command=self.toggle_password_visibility)
        self.btn_toggle_password.pack(side="left", padx=5)
        
        # Botones
        botones_frame = Frame(main_container, bg=fondo)
        botones_frame.pack(pady=30)
        
        btn_width = max(15, self.responsive.scale_dimension(20))
        Button(botones_frame, text="Iniciar Sesión", width=btn_width,
               font=("Helvetica", self.responsive.scale_font(12), "bold"), 
               bg="#cf0a8d", fg="#ffffff", cursor="hand2",
               command=self.entrar).pack(pady=10)
        
        Button(botones_frame, text="Registrarse", width=btn_width,
               font=("Helvetica", self.responsive.scale_font(12), "bold"), 
               bg="#cf0a8d", fg="#ffffff", cursor="hand2",
               command=self.ir_registro).pack(pady=10)
        
        self.ventana.mainloop()
    
    def entrar(self):
        nombre = self.entry_usuario.get()
        contra = self.entry_passw.get()
        
        if not nombre or not contra:
            messagebox.showerror("Error", "Complete todos los campos")
            return
        
        usuario = self.gestor_bd.validar_login(nombre, contra)
        
        if usuario:
            messagebox.showinfo("Bloom Music", f"¡Bienvenido {usuario['nombre']}!")
            self.ventana.destroy()
            ReproductorBloom(usuario, self.gestor_bd)
        else:
            self.entry_passw.delete(0, END)
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    
    def toggle_password_visibility(self):
        if self.show_password:
            self.entry_passw.config(show="*")
            self.btn_toggle_password.config(text="👁")
            self.show_password = False
        else:
            self.entry_passw.config(show="")
            self.btn_toggle_password.config(text="🔒")
            self.show_password = True
    
    def ir_registro(self):
        self.ventana.destroy()
        RegistroI(self.gestor_bd)

# ==============================================================================
# REGISTRO (Heredado - versiones compactas)
# ==============================================================================

class RegistroI:
    def __init__(self, gestor_bd):
        self.gestor_bd = gestor_bd
        self.ventana = Tk()
        self.responsive = ResponsiveManager(self.ventana)
        
        self.ventana.geometry(self.responsive.get_window_geometry())
        self.ventana.title("Registrate en Bloom Music")
        self.ventana.minsize(600, 500)
        
        fondo = "#fff8ff"
        self.ventana.configure(bg=fondo)
        
        # Interface simplificada
        main_container = Frame(self.ventana, bg=fondo)
        main_container.pack(expand=True, pady=50)
        
        Label(main_container, text="Registrate para empezar a escuchar contenido",
              font=("Helvetica", self.responsive.scale_font(18), "bold"), 
              bg=fondo).pack(pady=(0, 30))
        
        campos_frame = Frame(main_container, bg=fondo)
        campos_frame.pack(pady=20)
        
        Label(campos_frame, text="Correo Electrónico", 
              font=("Helvetica", self.responsive.scale_font(14)), 
              bg=fondo).grid(row=0, column=0, sticky="e", padx=(0, 10), pady=10)
        
        entry_width = max(20, self.responsive.scale_dimension(25))
        self.entry_correo = Entry(campos_frame, 
                                 font=("Helvetica", self.responsive.scale_font(14)), 
                                 width=entry_width)
        self.entry_correo.grid(row=0, column=1, pady=10)
        self.entry_correo.bind('<Return>', lambda e: self.irARegistroII())
        
        botones_frame = Frame(main_container, bg=fondo)
        botones_frame.pack(pady=30)
        
        btn_width = max(15, self.responsive.scale_dimension(20))
        Button(botones_frame, text="Siguiente", width=btn_width,
               font=("Helvetica", self.responsive.scale_font(12), "bold"), 
               bg="#cf0a8d", fg="#ffffff", cursor="hand2",
               command=self.irARegistroII).pack(pady=10)
        
        Button(botones_frame, text="Volver", width=btn_width,
               font=("Helvetica", self.responsive.scale_font(12), "bold"), 
               bg="#cf0a8d", fg="#ffffff", cursor="hand2",
               command=self.volverLogin).pack(pady=10)
        
        self.ventana.mainloop()
    
    def volverLogin(self):
        self.ventana.destroy()
        Login()
    
    def irARegistroII(self):
        email = self.entry_correo.get()
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Por favor, ingrese un correo electrónico válido.")
            return
        datos_usuario['email'] = email
        self.ventana.destroy()
        RegistroII(self.gestor_bd)

# Clases RegistroII y RegistroIII heredadas del código original (omitidas por brevedad)
# NOTA: Usa las mismas del código original sin cambios significativos

# ==============================================================================
# REGISTRO PASO 2 - CONTRASEÑA (RESPONSIVO)
# ==============================================================================

class RegistroII:
    def __init__(self, gestor_bd):
        self.gestor_bd = gestor_bd
        self.ventana = Tk()
        self.responsive = ResponsiveManager(self.ventana)
        
        self.ventana.geometry(self.responsive.get_window_geometry())
        self.ventana.title("Registrate en Bloom Music")
        self.ventana.minsize(600, 500)

        fondo = "#fff8ff"
        self.ventana.configure(bg=fondo)

        # Frame con scroll
        canvas = tk.Canvas(self.ventana, bg=fondo, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.ventana, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas, bg=fondo)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        def configure_canvas(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind('<Configure>', configure_canvas)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        main_container = Frame(self.scrollable_frame, bg=fondo)
        main_container.pack(expand=True, pady=20)
        
        # Logo
        logo_size = self.responsive.scale_dimension(180)
        try:
            logo_path = resource_path("LogoLogin.png")  # ✅ USAR resource_path()
            img = Image.open(logo_path).resize((logo_size, logo_size), Image.LANCZOS)
            render = ImageTk.PhotoImage(img)
            logo_label = Label(main_container, image=render, bg=fondo)
            logo_label.image = render
            logo_label.pack(pady=(0, 10))
        except:
            pass
        
        Label(main_container, 
              text="Paso 1 de 3",
              font=("Helvetica", self.responsive.scale_font(14)), 
              fg="#a6a6a6",
              bg=fondo).pack()
        
        Label(main_container, 
              text="Crea una contraseña",
              font=("Helvetica", self.responsive.scale_font(18), "bold"), 
              bg=fondo).pack(pady=(5, 20))
        
        campos_frame = Frame(main_container, bg=fondo)
        campos_frame.pack(pady=15)
        
        label_font = self.responsive.scale_font(14)
        entry_width = max(25, self.responsive.scale_dimension(30))
        
        Label(campos_frame, text="Contraseña", 
              font=("Helvetica", label_font), bg=fondo).grid(row=0, column=0, sticky="e", padx=(0, 15), pady=12)
        
        self.entry_contra = Entry(campos_frame, font=("Helvetica", label_font), width=entry_width, show="•")
        self.entry_contra.grid(row=0, column=1, pady=12, sticky="ew")
        
        Label(campos_frame, text="Repita Contraseña", 
              font=("Helvetica", label_font), bg=fondo).grid(row=1, column=0, sticky="e", padx=(0, 15), pady=12)
        
        self.entry_contra2 = Entry(campos_frame, font=("Helvetica", label_font), width=entry_width, show="•")
        self.entry_contra2.grid(row=1, column=1, pady=12, sticky="ew")
        self.entry_contra2.bind('<Return>', lambda e: self.siguienteRegistro())
        
        requisitos_frame = Frame(main_container, bg=fondo)
        requisitos_frame.pack(pady=10)
        
        Label(requisitos_frame, 
              text="Tu contraseña debe contener al menos:",
              font=("Helvetica", self.responsive.scale_font(10)), 
              fg="#a6a6a6",
              bg=fondo).pack()
        
        req_text = "• 8 caracteres   • 1 mayúscula   • 1 minúscula   • 1 número   • 1 carácter especial"
        Label(requisitos_frame, 
              text=req_text,
              font=("Helvetica", self.responsive.scale_font(9)), 
              fg="#a6a6a6",
              bg=fondo).pack()
        
        botones_frame = Frame(main_container, bg=fondo)
        botones_frame.pack(pady=20)
        
        btn_width = max(15, self.responsive.scale_dimension(20))
        btn_font = self.responsive.scale_font(12)
        
        Button(botones_frame, 
               text="Siguiente", 
               width=btn_width,
               font=("Helvetica", btn_font, "bold"), 
               bg="#cf0a8d", 
               fg="#ffffff",
               cursor="hand2",
               command=self.siguienteRegistro).pack(pady=8)
        
        Button(botones_frame, 
               text="Volver", 
               width=btn_width,
               font=("Helvetica", btn_font, "bold"), 
               bg="#cf0a8d", 
               fg="#ffffff",
               cursor="hand2",
               command=self.volverRegistro).pack(pady=8)

        self.ventana.mainloop()
    
    def mayusculascontra(self, contra):
        return any(c.isupper() for c in contra)
    
    def minusculascontra(self, contra):
        return any(c.islower() for c in contra)
    
    def caractespecialcontra(self, contra):
        return bool(re.search(r'[^a-zA-Z0-9]', contra))
    
    def numeroscontra(self, contra):
        return any(c.isdigit() for c in contra)
    
    def validarcontra(self, contra, contrarep):
        if len(contra) < 8:
            messagebox.showwarning("Error: Contraseña Inválida", "La contraseña debe tener al menos 8 CARACTERES")
            return False
        
        if not self.mayusculascontra(contra):
            messagebox.showwarning("Error: Contraseña Inválida", "La contraseña debe tener al menos 1 caracter en mayúscula")
            return False

        if not self.minusculascontra(contra):
            messagebox.showwarning("Error: Contraseña Inválida", "La contraseña debe tener al menos 1 caracter en minúscula")
            return False
        
        if not self.caractespecialcontra(contra):
            messagebox.showwarning("Error: Contraseña Inválida", "La contraseña debe tener al menos 1 caracter especial")
            return False
        
        if not self.numeroscontra(contra):
            messagebox.showwarning("Error: Contraseña Inválida", "La contraseña debe tener al menos 1 caracter numérico")
            return False
        
        if contra != contrarep:
            messagebox.showwarning("Error", "Las contraseñas no coinciden.")
            return False
        
        return True

    def volverRegistro(self):
        self.ventana.destroy()
        RegistroI(self.gestor_bd)

    def siguienteRegistro(self):
        contra = self.entry_contra.get()
        contrarep = self.entry_contra2.get()
        
        if self.validarcontra(contra, contrarep):
            datos_usuario['contraseña'] = contra
            self.ventana.destroy()
            RegistroIII(self.gestor_bd)
        else:
            self.entry_contra.delete(0, END)
            self.entry_contra2.delete(0, END)

# ==============================================================================
# REGISTRO PASO 3 - DATOS PERSONALES (RESPONSIVO)
# ==============================================================================

class RegistroIII:
    def __init__(self, gestor_bd):
        self.gestor_bd = gestor_bd
        self.ventana = Tk()
        self.responsive = ResponsiveManager(self.ventana)
        
        self.ventana.geometry(self.responsive.get_window_geometry())
        self.ventana.title("Registrate en Bloom Music")
        self.ventana.minsize(600, 600)

        fondo = "#fff8ff"
        self.ventana.configure(bg=fondo)

        # Frame con scroll
        canvas = tk.Canvas(self.ventana, bg=fondo, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.ventana, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=fondo)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((400, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        main_container = Frame(scrollable_frame, bg=fondo)
        main_container.pack(pady=20)
        
        # Logo
        logo_size = self.responsive.scale_dimension(150)
        try:
            logo_path = resource_path("LogoLogin.png")  # ✅ USAR resource_path()
            img = Image.open(logo_path).resize((logo_size, logo_size), Image.LANCZOS)
            render = ImageTk.PhotoImage(img)
            logo_label = Label(main_container, image=render, bg=fondo)
            logo_label.image = render
            logo_label.pack(pady=(0, 10))
        except:
            pass
        
        Label(main_container, 
              text="Paso 2 de 3",
              font=("Helvetica", self.responsive.scale_font(14)), 
              fg="#a6a6a6",
              bg=fondo).pack()
        
        Label(main_container, 
              text="Crea tu usuario",
              font=("Helvetica", self.responsive.scale_font(18), "bold"), 
              bg=fondo).pack(pady=(5, 15))
        
        campos_frame = Frame(main_container, bg=fondo)
        campos_frame.pack(pady=10)
        
        # Configurar expansión de columnas para alineación
        campos_frame.grid_columnconfigure(1, weight=1)
        
        label_font = self.responsive.scale_font(12)
        entry_width = max(28, self.responsive.scale_dimension(35))
        
        Label(campos_frame, text="Nombre de Usuario", 
              font=("Helvetica", label_font), bg=fondo).grid(row=0, column=0, sticky="e", padx=(0, 15), pady=12)
        
        self.entry_usuario = Entry(campos_frame, font=("Helvetica", label_font), width=entry_width)
        self.entry_usuario.grid(row=0, column=1, pady=12, sticky="ew")
        
        Label(main_container, 
              text="Aparecerás con este nombre en Bloom Music",
              font=("Helvetica", self.responsive.scale_font(9)), 
              fg="#a6a6a6",
              bg=fondo).pack(pady=(0, 15))
        
        # Fecha de Nacimiento
        fecha_frame = Frame(main_container, bg=fondo)
        fecha_frame.pack(pady=10)
        
        Label(fecha_frame, text="Fecha de Nacimiento", 
              font=("Helvetica", label_font, "bold"), bg=fondo).pack(pady=(0, 8))
        
        fecha_inputs = Frame(fecha_frame, bg=fondo)
        fecha_inputs.pack()
        
        self.fecha_nacimiento_dia = IntVar(value=1)
        self.fecha_nacimiento_mes = StringVar(value="Enero")
        self.fecha_nacimiento_year = IntVar(value=2000)

        spin_font = self.responsive.scale_font(11)
        spin_width = max(6, self.responsive.scale_dimension(8))
        
        Label(fecha_inputs, text="Día", font=("Helvetica", self.responsive.scale_font(9)), bg=fondo).grid(row=0, column=0, padx=5)
        self.spin_dia = Spinbox(fecha_inputs, textvariable=self.fecha_nacimiento_dia,
                                from_=1, to=31, width=spin_width, font=("Helvetica", spin_font))
        self.spin_dia.grid(row=1, column=0, padx=5)
        
        Label(fecha_inputs, text="Mes", font=("Helvetica", self.responsive.scale_font(9)), bg=fondo).grid(row=0, column=1, padx=5)
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        combo_width = max(10, self.responsive.scale_dimension(12))
        self.combo_mes = ttk.Combobox(fecha_inputs, textvariable=self.fecha_nacimiento_mes,
                                      values=meses, width=combo_width, font=("Helvetica", spin_font), state="readonly")
        self.combo_mes.grid(row=1, column=1, padx=5)
        
        Label(fecha_inputs, text="Año", font=("Helvetica", self.responsive.scale_font(9)), bg=fondo).grid(row=0, column=2, padx=5)
        self.spin_year = Spinbox(fecha_inputs, textvariable=self.fecha_nacimiento_year,
                                from_=1950, to=2010, width=spin_width, font=("Helvetica", spin_font))
        self.spin_year.grid(row=1, column=2, padx=5)
        
        # Género
        genero_frame = Frame(main_container, bg=fondo)
        genero_frame.pack(pady=15)
        
        Label(genero_frame, text="Género", 
              font=("Helvetica", label_font, "bold"), bg=fondo).pack(pady=(0, 8))
        
        self.genero_seleccionado = StringVar(value="Masculino")
        
        botones_genero = Frame(genero_frame, bg=fondo)
        botones_genero.pack()
        
        radio_padx = self.responsive.scale_dimension(15)
        
        ttk.Radiobutton(botones_genero, text="Masculino", 
                       variable=self.genero_seleccionado, value="Masculino").pack(side=LEFT, padx=radio_padx)
        ttk.Radiobutton(botones_genero, text="Femenino", 
                       variable=self.genero_seleccionado, value="Femenino").pack(side=LEFT, padx=radio_padx)
        ttk.Radiobutton(botones_genero, text="Otro", 
                       variable=self.genero_seleccionado, value="Otro").pack(side=LEFT, padx=radio_padx)
        
        # Botones
        botones_frame = Frame(main_container, bg=fondo)
        botones_frame.pack(pady=25)
        
        btn_width = max(15, self.responsive.scale_dimension(20))
        btn_font = self.responsive.scale_font(12)
        
        Button(botones_frame, 
               text="Registrarse", 
               width=btn_width,
               font=("Helvetica", btn_font, "bold"), 
               bg="#cf0a8d", 
               fg="#ffffff",
               cursor="hand2",
               command=self.GuardarBDD).pack(pady=8)
        
        Button(botones_frame, 
               text="Volver", 
               width=btn_width,
               font=("Helvetica", btn_font, "bold"), 
               bg="#cf0a8d", 
               fg="#ffffff",
               cursor="hand2",
               command=self.volverRegistro).pack(pady=8)

        self.ventana.mainloop()

    def volverRegistro(self):
        self.ventana.destroy()
        RegistroII(self.gestor_bd)
    
    def obtener_numero_mes(self, mes):
        meses = {"Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
                 "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12}
        return meses.get(mes, 1)
   
    def GuardarBDD(self):
        nombre = self.entry_usuario.get()
        genero = self.genero_seleccionado.get()
        
        if not nombre:
            messagebox.showerror("Error", "Por favor, ingrese un nombre de usuario.")
            return
        
        try:
            dia = int(self.fecha_nacimiento_dia.get())
            mes = self.obtener_numero_mes(self.fecha_nacimiento_mes.get())
            year = int(self.fecha_nacimiento_year.get())
            
            fecha_nacimiento = datetime.date(year, mes, dia)
            
            hoy = datetime.date.today()
            edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            
            if edad < 13:
                messagebox.showerror("Error", "Debes tener al menos 13 años para registrarte.")
                return
            
        except ValueError as e:
            messagebox.showerror("Error", f"Fecha inválida: {e}")
            return
        
        datos_usuario['nombre'] = nombre
        datos_usuario['genero'] = genero
        datos_usuario['fecha_nacimiento'] = fecha_nacimiento
        
        if self.gestor_bd.registrar_usuario(datos_usuario):
            messagebox.showinfo("¡Éxito!", 
                              f"¡Bienvenido a Bloom Music, {nombre}!\n\n"
                              "Tu cuenta ha sido creada correctamente.")
            self.ventana.destroy()
            Login()
        else:
            messagebox.showerror("Error", 
                               "El nombre de usuario o correo electrónico ya existe.\n"
                               "Por favor, intenta con otros datos.")
            self.ventana.destroy()
            RegistroI(self.gestor_bd)

# ==============================================================================
# REPRODUCTOR OPTIMIZADO - VERSIÓN MODULAR
# ==============================================================================
class ReproductorBloom:
    def __init__(self, usuario_datos, gestor_bd):
        self.usuario = usuario_datos
        self.gestor_bd = gestor_bd
        
        self.root = Tk()
        self.responsive = ResponsiveManager(self.root)
        
        # Aplicar geometría responsiva
        self.root.geometry(self.responsive.get_window_geometry())
        self.root.title(f"Bloom Music - {self.usuario['nombre']}")
        self.root.minsize(800, 600)
        self.root.configure(bg="white")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Bind para detectar cambios de tamaño
        self.root.bind('<Configure>', self.on_resize)
        self.resize_timer = None
        
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill="both", expand=True)
        
        self.radio_module = None
        self.current_view = "home"
        
        # Variables del reproductor
        self.pausa = FALSE
        self.en_reproduccion = FALSE
        self.playlist = []
        self.duracion_total = 0
        self.aleatorio_activado = FALSE
        self.loop_mode = 0
        self.timer_id = None
        self.slider_moving = False
        self.current_position_s = 0.0
        self.play_start_position = 0.0
        self.play_start_time = 0.0
        self.last_volume = 0.70
        self.is_muted = False
        
        self.barra_estado = tk.Label(self.root, 
                                     text=f'Bienvenido {self.usuario["nombre"]}',
                                     bd=1,
                                     relief=SUNKEN,
                                     anchor=W)
        self.barra_estado.pack(side=BOTTOM, fill=X)
        
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        
        self.create_widgets()
        self.cargar_configuraciones_usuario()
        
        self.root.mainloop()
    
    def on_resize(self, event):
        """Maneja el redimensionamiento de la ventana"""
        if event.widget == self.root:
            # Cancelar timer anterior
            if self.resize_timer:
                self.root.after_cancel(self.resize_timer)
            
            # Esperar 200ms antes de recalcular (evita múltiples llamadas)
            self.resize_timer = self.root.after(200, self.adjust_layout)
    
    def adjust_layout(self):
        """Ajusta el layout basado en el tamaño actual de la ventana"""
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # Si la ventana es muy pequeña, ocultar sidebar
        if width < 900 and hasattr(self, 'sidebar_frame'):
            self.sidebar_frame.pack_forget()
        elif hasattr(self, 'sidebar_frame'):
            sidebar_width = self.responsive.get_sidebar_width()
            self.sidebar_frame.config(width=sidebar_width)
            self.sidebar_frame.pack(side="left", fill="y", padx=10, pady=10, before=self.top_bar_frame)
    
    def create_widgets(self):
        # Menú
        subMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Archivo', menu=subMenu)
        subMenu.add_command(label='Cerrar Sesión', command=self.on_closing)
        
        subMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Importar', menu=subMenu)
        subMenu.add_command(label='Carpeta', command=self.Importar_Carpeta)
        subMenu.add_command(label='Música', command=self.Importar_Musica)
        
        # Top Bar con altura responsiva
        top_bar_height = self.responsive.scale_dimension(70)
        self.top_bar_frame = tk.Frame(self.main_frame, bg="white", height=top_bar_height)
        self.top_bar_frame.pack(side="top", fill="x", pady=(0, 10))
        self.top_bar_frame.pack_propagate(False)
        
        # Controles de reproducción
        self.playback_controls_frame = tk.Frame(self.top_bar_frame, bg="white")
        self.playback_controls_frame.pack(side="left", padx=10, pady=10)
        
        btn_font_size = self.responsive.scale_font(14)
        
        self.aleatorio_button2 = tk.Button(self.playback_controls_frame, text="🔀",
                                          font=("Helvetica", btn_font_size), bg="white", relief="flat",
                                          command=self.toggle_aleatorio)
        self.aleatorio_button2.pack(side="left", padx=5)
        
        tk.Button(self.playback_controls_frame, text="⏮", font=("Helvetica", btn_font_size),
                 bg="white", relief="flat", command=self.prev_song).pack(side="left", padx=5)
        
        tk.Button(self.playback_controls_frame, text="▶", font=("Helvetica", btn_font_size),
                 bg="white", relief="flat", command=self.reproducir_musica).pack(side="left", padx=5)
        
        tk.Button(self.playback_controls_frame, text="⏸️", font=("Helvetica", btn_font_size),
                 bg="white", relief="flat", command=self.pausar_musica).pack(side="left", padx=5)
        
        tk.Button(self.playback_controls_frame, text="⏭", font=("Helvetica", btn_font_size),
                 bg="white", relief="flat", command=self.next_song).pack(side="left", padx=5)
        
        self.bucle_button2 = tk.Button(self.playback_controls_frame, text="🔂",
                                       font=("Helvetica", btn_font_size), bg="white", relief="flat",
                                       command=self.toggle_loop)
        self.bucle_button2.pack(side="left", padx=5)
        
        # Display de canción actual con imagen responsiva
        self.current_song_frame = tk.Frame(self.top_bar_frame, bg="white")
        self.current_song_frame.pack(side="left", expand=True, fill="both", padx=10, pady=5)
        
        # Imagen de álbum pequeña (responsiva)
        album_size = self.responsive.scale_dimension(40)
        try:
            self.original_image_small = Image.open(resource_path("emiliaMP3Foto.png"))
            self.resized_image_small = self.original_image_small.resize((album_size, album_size), Image.LANCZOS)
            self.album_cover_small = ImageTk.PhotoImage(self.resized_image_small)
            self.album_label_small = tk.Label(self.current_song_frame, image=self.album_cover_small, bg="white")
            self.album_label_small.pack(side="left", padx=5)
        except:
            pass
        
        # Info de canción
        self.song_info_frame = tk.Frame(self.current_song_frame, bg="white")
        self.song_info_frame.pack(side="left", padx=5, fill="both", expand=True)
        
        info_font_title = self.responsive.scale_font(10)
        info_font_artist = self.responsive.scale_font(8)
        
        self.song_title_top = tk.Label(self.song_info_frame, 
                               text="Ninguna canción seleccionada", 
                               font=("Helvetica", info_font_title, "bold"), 
                               bg="white", 
                               anchor="w")
        self.song_title_top.pack(fill="x")
        
        self.artist_top = tk.Label(self.song_info_frame, 
                           text=f"{self.usuario['nombre']} - Bloom Music", 
                           font=("Helvetica", info_font_artist), 
                           bg="white", 
                           anchor="w")
        self.artist_top.pack(fill="x")
        
        # Barra de progreso con mejor visualización
        self.progress_frame = tk.Frame(self.song_info_frame, bg="white")
        self.progress_frame.pack(fill="x", expand=True)
        
        time_font = self.responsive.scale_font(9)
        
        self.current_time_label = tk.Label(self.progress_frame, 
                                          font=("Helvetica", time_font),
                                          bg="white", 
                                          text="00:00",
                                          width=5)
        self.current_time_label.pack(side="left", padx=(0, 5))
        
        # Slider mejorado con mejor visibilidad
        progress_length = max(300, self.responsive.scale_dimension(400))
        
        # Configurar estilo del slider
        style = ttk.Style()
        style.configure("Custom.Horizontal.TScale", 
                       background="white",
                       troughcolor="#e0e0e0",
                       bordercolor="white",
                       lightcolor="#CF0A8D",
                       darkcolor="#CF0A8D")
        
        self.progress_bar = ttk.Scale(self.progress_frame, 
                                     from_=0, 
                                     to=100,
                                     orient="horizontal", 
                                     length=progress_length,
                                     style="Custom.Horizontal.TScale",
                                     command=self.slider_drag)
        self.progress_bar.set(0)
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=5)
        self.progress_bar.bind("<ButtonPress-1>", self.slider_press)
        self.progress_bar.bind("<ButtonRelease-1>", self.slider_release)
        
        self.total_time_label = tk.Label(self.progress_frame, 
                                        font=("Helvetica", time_font),
                                        bg="white", 
                                        text="00:00",
                                        width=5)
        self.total_time_label.pack(side="left", padx=(5, 0))
        
        # Control de volumen
        self.right_controls_frame = tk.Frame(self.top_bar_frame, bg="white")
        self.right_controls_frame.pack(side="right", padx=10, pady=10)
        
        self.volume_label = tk.Label(self.right_controls_frame, text="🔊",
                                     font=("Helvetica", btn_font_size), bg="white", cursor="hand2")
        self.volume_label.pack(side="left", padx=5)
        self.volume_label.bind("<Button-1>", self.toggle_mute)
        
        volume_length = self.responsive.scale_dimension(80)
        self.volume_scale = ttk.Scale(self.right_controls_frame, from_=0, to=100,
                                      orient="horizontal", length=volume_length,
                                      command=lambda s: self.ajustar_volumen(float(s)))
        self.volume_scale.set(70)
        pygame.mixer.music.set_volume(0.70)
        self.volume_scale.pack(side="left", padx=5)
        
        # Sidebar con ancho responsivo
        sidebar_width = self.responsive.get_sidebar_width()
        self.sidebar_frame = tk.Frame(self.main_frame, bg="white", width=sidebar_width)
        self.sidebar_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.sidebar_frame.pack_propagate(False)
        
        # Content frame
        self.content_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Header del sidebar
        self.header_frame = tk.Frame(self.sidebar_frame, bg="white")
        self.header_frame.pack(fill="x", pady=(0, 10))
        
        # Logo del sidebar (responsivo)
        logo_sidebar_size = self.responsive.scale_dimension(80)
        try:
            logo_path = resource_path("LogoLogin.png")  # ✅ USAR resource_path()
            img = Image.open(logo_path).resize((logo_sidebar_size, logo_sidebar_size), Image.LANCZOS)
            render = ImageTk.PhotoImage(img)
            label = tk.Label(self.header_frame, image=render, bg="white")
            label.image = render
            label.pack(side="top", padx=5, pady=5)
        except:
            pass
        
        # Botones del header
        btn_size = self.responsive.scale_font(12)
        
        self.tres_puntos_button = tk.Button(self.header_frame, 
                                    text="⋯", 
                                    bg="white", 
                                    relief="sunken", 
                                    font=("Helvetica", btn_size, "bold"),
                                    cursor="hand2",
                                    command=self.mostrar_menu_usuario)
        self.tres_puntos_button.place(relx=0.85, y=15)
        
        self.atras_button = tk.Button(self.header_frame, 
                              text="⬅️", 
                              bg="white", 
                              relief="sunken", 
                              font=("Helvetica", btn_size, "bold"),
                              cursor="hand2",
                              command=self.on_closing)
        self.atras_button.place(x=10, y=15)
        
        # Barra de búsqueda
        search_font = self.responsive.scale_font(10)
        self.search_entry = ttk.Entry(self.sidebar_frame, font=("Helvetica", search_font))
        self.search_entry.insert(0, "Buscar")
        self.search_entry.pack(fill="x", padx=10, pady=5)
        self.search_entry.bind("<FocusIn>", self.on_search_focus_in)
        self.search_entry.bind("<FocusOut>", self.on_search_focus_out)
        self.search_entry.config(foreground="gray")
        
        # Botones del sidebar (responsivos)
        sidebar_btn_font = self.responsive.scale_font(12)
        
        self.home_button = tk.Button(self.sidebar_frame, text="🏠 Home",
                                    font=("Helvetica", sidebar_btn_font), bg="#e0e0e0", relief="flat",
                                    anchor="w", padx=20, command=self.show_home_view)
        self.home_button.pack(fill="x", pady=5)
        
        tk.Button(self.sidebar_frame, text="✨ Nuevo", font=("Helvetica", sidebar_btn_font),
         bg="white", relief="flat", anchor="w", padx=20, command=lambda: self.show_dev_view("Nuevo")).pack(fill="x", pady=5)
        
        self.radio_button = tk.Button(self.sidebar_frame, text="📻 Radio",
                                      font=("Helvetica", sidebar_btn_font), bg="white", relief="flat",
                                      anchor="w", padx=20, command=self.show_radio_view)
        self.radio_button.pack(fill="x", pady=5)
        
        label_font = self.responsive.scale_font(10)
        tk.Label(self.sidebar_frame, text="Librería", font=("Helvetica", label_font, "bold"),
                bg="white", anchor="w").pack(fill="x", padx=10, pady=(15, 5))
        
        tk.Button(self.sidebar_frame, text="➕ Añadidos recientemente",
         font=("Helvetica", sidebar_btn_font), bg="white", relief="flat",
         anchor="w", padx=20,
         command=lambda: self.show_dev_view("Añadidos Recientemente")).pack(fill="x", pady=5)

        
        tk.Button(self.sidebar_frame, text="🧑‍🎤 Artistas", font=("Helvetica", sidebar_btn_font),
         bg="white", relief="flat", anchor="w", padx=20,
         command=lambda: self.show_dev_view("Artistas")).pack(fill="x", pady=5)
        
        tk.Button(self.sidebar_frame, text="💿 Álbumes", font=("Helvetica", sidebar_btn_font),
                 bg="white", relief="flat", anchor="w", padx=20,
                 command=lambda: self.show_dev_view("Álbumes")).pack(fill="x", pady=5)

        tk.Button(self.sidebar_frame, text="🎵 Canciones", font=("Helvetica", sidebar_btn_font),
         bg="white", relief="flat", anchor="w", padx=20,
         command=lambda: self.show_dev_view("Canciones")).pack(fill="x", pady=5)
        
        # ÁREA DE CONTENIDO PRINCIPAL
        # Imagen del álbum (responsiva)
        album_display_size = self.responsive.scale_dimension(200)
        try:
            img = Image.open(resource_path("emiliaMP3Foto.png")).resize((album_display_size), Image.LANCZOS)
            render = ImageTk.PhotoImage(img)
            label = tk.Label(self.content_frame, image=render, bg="#f0f0f0")
            label.image = render
            label.pack(pady=20)
        except:
            tk.Label(self.content_frame, text="[Album Cover]",
                    font=("Helvetica", self.responsive.scale_font(14)),
                    bg="#f0f0f0").pack(pady=20)
        
        # Título de canción
        title_font = self.responsive.scale_font(18)
        self.song_title = tk.Label(self.content_frame, text="Selecciona una canción",
                                   font=("Helvetica", title_font, "bold"), bg="#f0f0f0")
        self.song_title.pack()
        
        subtitle_font = self.responsive.scale_font(12)
        tk.Label(self.content_frame, text="Bloom Music Player",
                font=("Helvetica", subtitle_font), bg="#f0f0f0").pack()
        
        # Controles inferiores
        self.player_controls_bottom_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        self.player_controls_bottom_frame.pack(pady=10)
        
        bottom_btn_font = self.responsive.scale_font(12)
        bottom_btn_padx = self.responsive.scale_dimension(20)
        bottom_btn_pady = self.responsive.scale_dimension(5)
        
        tk.Button(self.player_controls_bottom_frame, text="▶ Play",
                 font=("Helvetica", bottom_btn_font, "bold"), bg="#CF0A8D", fg="white",
                 relief="flat", padx=bottom_btn_padx, pady=bottom_btn_pady,
                 command=self.reproducir_musica).pack(side="left", padx=5)
        
        self.aleatorio_button_bottom = tk.Button(self.player_controls_bottom_frame,
                                                 text="🔀 Aleatorio",
                                                 font=("Helvetica", bottom_btn_font, "bold"),
                                                 bg="#e0e0e0", relief="flat",
                                                 padx=bottom_btn_padx, pady=bottom_btn_pady,
                                                 command=self.toggle_aleatorio)
        self.aleatorio_button_bottom.pack(side="left", padx=5)
        
        self.loop_button_right = tk.Button(self.player_controls_bottom_frame,
                                          text="🔂", font=("Helvetica", self.responsive.scale_font(14)),
                                          bg="#f0f0f0", relief="flat",
                                          command=self.toggle_loop)
        self.loop_button_right.pack(side="left", padx=5)
        
        # PLAYLIST CON SCROLL
        self.playlist_frame = tk.Frame(self.content_frame, bg="white")
        self.playlist_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        # Frame para listbox con scrollbar
        listbox_container = Frame(self.playlist_frame, bg="white")
        listbox_container.pack(fill="both", expand=True, pady=5, padx=5)
        
        scrollbar = Scrollbar(listbox_container)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        playlist_font = self.responsive.scale_font(10)
        self.playlistbox = Listbox(listbox_container, bg="white",
                                   font=("Helvetica", playlist_font),
                                   selectbackground="#adaaaa",
                                   yscrollcommand=scrollbar.set)
        self.playlistbox.pack(side=LEFT, fill="both", expand=True)
        scrollbar.config(command=self.playlistbox.yview)
        
        # Botones de playlist
        self.playlist_buttons_frame = Frame(self.playlist_frame, bg="white")
        self.playlist_buttons_frame.pack(fill="x", pady=5)
        
        playlist_btn_font = self.responsive.scale_font(11)
        playlist_btn_padx = self.responsive.scale_dimension(15)
        
        tk.Button(self.playlist_buttons_frame, text="🎵 Añadir Canción",
                 font=("Helvetica", playlist_btn_font), bg="white", relief="flat",
                 anchor="w", padx=playlist_btn_padx,
                 command=self.Importar_Musica).pack(side=LEFT, fill="x", expand=True)
        
        tk.Button(self.playlist_buttons_frame, text="📁 Añadir Carpeta",
                 font=("Helvetica", playlist_btn_font), bg="white", relief="flat",
                 anchor="w", padx=playlist_btn_padx,
                 command=self.Importar_Carpeta).pack(side=LEFT, fill="x", expand=True)
        
        tk.Button(self.playlist_buttons_frame, text="❌ Eliminar",
                 font=("Helvetica", playlist_btn_font), bg="white", relief="flat",
                 anchor="w", padx=playlist_btn_padx,
                 command=self.del_from_playlist).pack(side=LEFT, fill="x", expand=True)
    
    # ===== MÉTODOS DE LA INTERFAZ =====
    
    

    def on_search_focus_in(self, event):
        if self.search_entry.get() == "Buscar":
            self.search_entry.delete(0, END)
            self.search_entry.config(foreground="black")

    def on_search_focus_out(self, event):
        if self.search_entry.get() == "":
            self.search_entry.insert(0, "Buscar")
            self.search_entry.config(foreground="gray")

    def mostrar_menu_usuario(self):
        menu = Menu(self.root, tearoff=0)
        menu.add_command(label=f"👤 {self.usuario['nombre']}", state="disabled")
        menu.add_separator()
        menu.add_command(label="⚙️ Editar Perfil", command=self.abrir_configuracion)
        menu.add_command(label="ℹ️ Acerca de Bloom", command=self.bloom_submenubar)
        menu.add_separator()
        menu.add_command(label="🚪 Cerrar Sesión", command=self.on_closing)
        
        # Posicionar menú
        menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())
    
    def abrir_configuracion(self):
        """Abre la ventana de editar perfil"""
        def actualizar_datos(nuevos_datos):
            self.usuario = nuevos_datos
            self.barra_estado.config(text=f'🏠 {self.usuario["nombre"]}')
        
        abrir_editar_perfil(self.root, self.usuario, self.gestor_bd, actualizar_datos)

    def bloom_submenubar(self):
        messagebox.showinfo('Sobre Bloom',
                       '¡Somos una empresa indie amantes de la música como vos!\n\n'
                       'Programado por mati je\n'
                       f'\nUsuario: {self.usuario["nombre"]}\n'
                       f'Email: {self.usuario["email"]}')
    
    # ===== MÉTODOS DE IMPORTACIÓN =====
    
    def Importar_Musica(self):
        filename = filedialog.askopenfilename(
            defaultextension=".mp3",
            filetypes=[("Archivos de Audio", "*.mp3 *.wav"), ("Todos", "*.*")]
        )
        if filename:
            self.add_to_playlist(filename)
    
    def Importar_Carpeta(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            for file in os.listdir(folder_path):
                full_path = os.path.join(folder_path, file)
                if os.path.isfile(full_path) and full_path.lower().endswith(('.mp3', '.wav')):
                    self.add_to_playlist(full_path)
    
    def add_to_playlist(self, full_path):
        if not full_path or full_path in self.playlist:
            return
        
        file_name = os.path.basename(full_path)
        nombre_limpio = file_name.replace('.mp3', '').replace('.wav', '')
        self.playlistbox.insert('end', nombre_limpio)
        self.playlist.append(full_path)
    
    def del_from_playlist(self):
        try:
            seleccion = self.playlistbox.curselection()
            if not seleccion:
                return
            
            index = int(seleccion[0])
            self.playlistbox.delete(index)
            
            if index < len(self.playlist):
                del self.playlist[index]
        except:
            pass
    
    # ===== CONTROL DE SLIDER =====
    
    def slider_press(self, event):
        self.slider_moving = True
        self._cancelar_timer()
    
    def slider_drag(self, value):
        if self.slider_moving:
            tiempo = float(value)
            mins, secs = divmod(tiempo, 60)
            self.current_time_label.config(text=f'{int(mins):02d}:{int(secs):02d}')
    
    def slider_release(self, event):
        tiempo_deseado = float(self.progress_bar.get())
        seleccion = self.playlistbox.curselection()
        
        if seleccion:
            idx = int(seleccion[0])
            cancion = self.playlist[idx]
            
            self._cancelar_timer()
            pygame.mixer.music.stop()
            pygame.mixer.music.load(cancion)
            
            # Evitar seek a tiempo 0
            seek_time = max(0.1, tiempo_deseado)
            
            pygame.mixer.music.play(start=0)
            pygame.mixer.music.set_pos(seek_time)
            
            self.current_position_s = tiempo_deseado
            self.play_start_position = tiempo_deseado
            self.play_start_time = time.time()
            self.en_reproduccion = TRUE
            self.pausa = FALSE
            
            self.duracion_total = self.obtener_datos_cancion(cancion)
            self.progress_bar.config(to=self.duracion_total)
            
            self._iniciar_timer()
        
        self.slider_moving = False
        
        # Devolver el foco a la ventana principal
        self.root.focus_set()
    
    # ===== TIMER =====
    
    def _cancelar_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
    
    def _iniciar_timer(self):
        self._cancelar_timer()
        self._actualizar_tiempo()
    
    def _actualizar_tiempo(self):
        if not pygame.mixer.music.get_busy() and not self.pausa:
            self.next_song()
            return
        
        if not self.slider_moving:
            if self.en_reproduccion and not self.pausa:
                elapsed = time.time() - self.play_start_time
                self.current_position_s = self.play_start_position + elapsed
            
            if self.current_position_s >= self.duracion_total - 0.5 and self.duracion_total > 0:
                self._cancelar_timer()
                self.next_song()
                return
            
            mins, secs = divmod(self.current_position_s, 60)
            self.current_time_label.config(text=f'{int(mins):02d}:{int(secs):02d}')
            self.progress_bar.set(self.current_position_s)
        
        self.timer_id = self.root.after(100, self._actualizar_tiempo)
    
    # ===== CONTROLES DE REPRODUCCIÓN =====
    
    def reproducir_musica(self):
        try:
            seleccion = self.playlistbox.curselection()
            if not seleccion:
                if self.playlist:
                    self.playlistbox.activate(0)
                    self.playlistbox.selection_set(0)
                    seleccion = self.playlistbox.curselection()
                else:
                    messagebox.showerror('Error', 'Selecciona una canción')
                    return
            
            idx = int(seleccion[0])
            cancion = self.playlist[idx]
            nombre = os.path.basename(cancion)
            nombre_limpio = nombre.replace('.mp3', '').replace('.wav', '')
            self.song_title_top.config(text=f'🎵 {nombre_limpio}')
            
            if self.pausa:
                pygame.mixer.music.unpause()
                self.play_start_position = self.current_position_s
                self.play_start_time = time.time()
                self.pausa = FALSE
                self.en_reproduccion = TRUE
                self._iniciar_timer()
                self.barra_estado.config(text=f'Reproduciendo: {nombre_limpio}')
            else:
                self._cancelar_timer()
                pygame.mixer.music.stop()
                pygame.mixer.music.load(cancion)
                pygame.mixer.music.play(start=0)
                
                self.en_reproduccion = TRUE
                self.pausa = FALSE
                self.current_position_s = 0.0
                self.play_start_position = 0.0
                self.play_start_time = time.time()
                
                self.duracion_total = self.obtener_datos_cancion(cancion)
                self.progress_bar.config(to=self.duracion_total)
                self.song_title.config(text=nombre_limpio)
                self.barra_estado.config(text=f'Reproduciendo: {nombre_limpio}')
                
                try:
                    if cancion.lower().endswith('.mp3'):
                        from mutagen.id3 import ID3
                        tags = ID3(cancion)
                        artista = tags.get('TPE1', [f"{self.usuario['nombre']}"])[0]
                        album = tags.get('TALB', ['Bloom Music'])[0]
                        self.artist_top.config(text=f'{artista} - {album}')
                    else:
                        self.artist_top.config(text=f'{self.usuario["nombre"]} - Bloom Music')
                except:
                    self.artist_top.config(text=f'{self.usuario["nombre"]} - Bloom Music')
                
                mins, secs = divmod(self.duracion_total, 60)
                self.total_time_label.config(text=f'{int(mins):02d}:{int(secs):02d}')
                
                self._iniciar_timer()
                
        except Exception as e:
            messagebox.showerror('Error', f'No se pudo reproducir: {e}')
    
    def pausar_musica(self):
        if self.en_reproduccion:
            elapsed = time.time() - self.play_start_time
            self.current_position_s = self.play_start_position + elapsed
            
            self.pausa = TRUE
            self.en_reproduccion = FALSE
            pygame.mixer.music.pause()
            self._cancelar_timer()
            self.barra_estado.config(text='En Pausa...')
    
    def parar_musica(self):
        pygame.mixer.music.stop()
        self.en_reproduccion = FALSE
        self.pausa = FALSE
        self.current_position_s = 0.0
        self.play_start_position = 0.0
        self.play_start_time = 0.0
        
        self.progress_bar.set(0)
        self.current_time_label.config(text="00:00")
        self._cancelar_timer()
        self.barra_estado.config(text='Música Detenida')
    
    def next_song(self):
        if not self.playlist:
            return
        
        seleccion = self.playlistbox.curselection()
        actual_idx = int(seleccion[0]) if seleccion else -1
        
        if self.loop_mode == 2:
            proximo_idx = actual_idx
        elif self.aleatorio_activado:
            proximo_idx = actual_idx
            if len(self.playlist) > 1:
                while proximo_idx == actual_idx:
                    proximo_idx = random.randint(0, len(self.playlist) - 1)
        else:
            if actual_idx < len(self.playlist) - 1:
                proximo_idx = actual_idx + 1
            else:
                if self.loop_mode == 1:
                    proximo_idx = 0
                else:
                    self.parar_musica()
                    return
        
        self.playlistbox.selection_clear(0, END)
        self.playlistbox.activate(proximo_idx)
        self.playlistbox.selection_set(proximo_idx)
        self.reproducir_musica()
    
    def prev_song(self):
        if not self.playlist:
            return
        
        seleccion = self.playlistbox.curselection()
        if not seleccion:
            return
        
        actual_idx = int(seleccion[0])
        
        if self.current_position_s > 3.0:
            self.reproducir_musica()
            return
        
        previo_idx = actual_idx - 1 if actual_idx > 0 else 0
        
        self.playlistbox.selection_clear(0, END)
        self.playlistbox.activate(previo_idx)
        self.playlistbox.selection_set(previo_idx)
        self.reproducir_musica()
    
    def toggle_aleatorio(self):
        if self.aleatorio_activado:
            self.aleatorio_activado = FALSE
            self.aleatorio_button2.config(bg="white", fg="black", relief="flat")
            self.aleatorio_button_bottom.config(bg="#e0e0e0", fg="black", relief="flat")
        else:
            self.aleatorio_activado = TRUE
            self.aleatorio_button2.config(bg="#CF0A8D", fg="white", relief="raised")
            self.aleatorio_button_bottom.config(bg="#CF0A8D", fg="white", relief="raised")
    
    def toggle_loop(self):
        self.loop_mode = (self.loop_mode + 1) % 3
        
        self.bucle_button2.config(bg="white", fg="black", relief="flat", text="🔂")
        self.loop_button_right.config(bg="#f0f0f0", fg="black", relief="flat", text="🔂")
        
        if self.loop_mode == 1:
            self.bucle_button2.config(bg="#CF0A8D", fg="white", relief="raised")
            self.loop_button_right.config(bg="#CF0A8D", fg="white", relief="raised")
        elif self.loop_mode == 2:
            self.bucle_button2.config(bg="#CF0A8D", fg="black", relief="raised", text="🔂¹")
            self.loop_button_right.config(bg="#CF0A8D", fg="black", relief="raised", text="🔂¹")
    
    def toggle_mute(self, event=None):
        if self.is_muted:
            pygame.mixer.music.set_volume(self.last_volume)
            self.volume_scale.set(self.last_volume * 100)
            self.volume_label.config(text="🔊")
            self.is_muted = False
        else:
            current_vol = pygame.mixer.music.get_volume()
            if current_vol > 0.01:
                self.last_volume = current_vol
            pygame.mixer.music.set_volume(0.0)
            self.volume_scale.set(0)
            self.volume_label.config(text="🔇")
            self.is_muted = True
    
    def ajustar_volumen(self, valor):
        volumen = float(valor) / 100
        pygame.mixer.music.set_volume(volumen)
        
        if volumen > 0 and self.is_muted:
            self.is_muted = False
            self.last_volume = volumen
            self.volume_label.config(text="🔊")
        elif volumen == 0 and not self.is_muted:
            self.is_muted = True
            self.volume_label.config(text="🔇")
        elif volumen > 0:
            self.last_volume = volumen
    
    def obtener_datos_cancion(self, cancion):
        try:
            if cancion.lower().endswith('.mp3'):
                audio = MP3(cancion)
                return audio.info.length
            else:
                audio = pygame.mixer.Sound(cancion)
                return audio.get_length()
        except:
            return 0
    
    # ===== RADIO =====
    
    def show_radio_view(self):
        if self.current_view == "radio":
            return
        if hasattr(self, 'dev_content_frame'):
            self.dev_content_frame.pack_forget()
    
        self.content_frame.pack_forget()
        self.home_button.config(bg="white")
        self.radio_button.config(bg="#e0e0e0")
        
        if not hasattr(self, 'radio_content_frame'):
            self.radio_content_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        
        if self.radio_module:
            self.radio_module.destroy()
        
        self.radio_module = RadioModule(self.radio_content_frame, self)
        self.radio_content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.current_view = "radio"
        self.barra_estado.config(text='📻 Vista de Radio')
    
    def show_home_view(self):
        if self.current_view == "home":
            return
        
        if self.radio_module and self.radio_module.radio_playing:
            self.radio_module.stop_radio()
        
        if hasattr(self, 'radio_content_frame'):
            self.radio_content_frame.pack_forget()
        
        if hasattr(self, 'dev_content_frame'):
            self.dev_content_frame.pack_forget()
        
        self.home_button.config(bg="#e0e0e0")
        self.radio_button.config(bg="white")
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.current_view = "home"
        self.barra_estado.config(text=f'Bienvenido {self.usuario["nombre"]}')
    
    def show_dev_view(self, nombre_vista):
        """Muestra mensaje de desarrollo sin romper otras vistas"""
        if self.current_view == nombre_vista:
            return
    
        # Ocultar vista actual
        if self.current_view == "home":
            self.content_frame.pack_forget()
        elif self.current_view == "radio" and hasattr(self, 'radio_content_frame'):
            self.radio_content_frame.pack_forget()
        elif hasattr(self, 'dev_content_frame'):
            self.dev_content_frame.pack_forget()
    
        # Actualizar botones del sidebar
        self.home_button.config(bg="white")
        self.radio_button.config(bg="white")
    
        # Crear/mostrar frame de desarrollo
        if not hasattr(self, 'dev_content_frame'):
            self.dev_content_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
    
        # Limpiar contenido anterior
        for widget in self.dev_content_frame.winfo_children():
            widget.destroy()
    
        # Contenido del mensaje
        tk.Label(self.dev_content_frame, 
             text="🚧",
             font=("Helvetica", self.responsive.scale_font(60)),
             bg="#f0f0f0").pack(pady=30)
    
        tk.Label(self.dev_content_frame, 
             text=f"Sección: {nombre_vista}",
             font=("Helvetica", self.responsive.scale_font(24), "bold"),
             bg="#f0f0f0").pack(pady=10)
    
        tk.Label(self.dev_content_frame, 
             text="Esta funcionalidad está en desarrollo",
             font=("Helvetica", self.responsive.scale_font(16)),
             fg="gray",
             bg="#f0f0f0").pack(pady=5)
    
        tk.Label(self.dev_content_frame, 
             text="¡Pronto estará disponible!",
             font=("Helvetica", self.responsive.scale_font(14)),
             fg="gray",
             bg="#f0f0f0").pack(pady=5)
    
        # Botón para volver
        tk.Button(self.dev_content_frame,
             text="⬅️ Volver al Inicio",
             font=("Helvetica", self.responsive.scale_font(12), "bold"),
             bg="#CF0A8D",
             fg="white",
             relief="flat",
             padx=20,
             pady=10,
             cursor="hand2",
             command=self.show_home_view).pack(pady=30)
    
        # Mostrar frame
        self.dev_content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    
        self.current_view = nombre_vista
        self.barra_estado.config(text=f'🚧 {nombre_vista} - En Desarrollo')
    # ===== CONFIGURACIONES =====
    
    def cargar_configuraciones_usuario(self):
        config = self.gestor_bd.cargar_configuraciones(self.usuario['id'])
        
        if config:
            print(f"✓ Cargando configuraciones de {self.usuario['nombre']}")
            
            volumen = config['volumen']
            self.last_volume = volumen
            pygame.mixer.music.set_volume(volumen)
            self.volume_scale.set(volumen * 100)
            
            if config['modo_aleatorio']:
                self.toggle_aleatorio()
            
            for _ in range(config['modo_bucle']):
                self.toggle_loop()
            
            if config['playlist']:
                for cancion in config['playlist']:
                    if os.path.exists(cancion):
                        self.add_to_playlist(cancion)
                print(f"✓ {len(config['playlist'])} canciones restauradas")
            
            self.barra_estado.config(text=f"✓ Configuraciones cargadas - {self.usuario['nombre']}")
    
    def guardar_configuraciones_usuario(self):
        config = {
            'volumen': pygame.mixer.music.get_volume(),
            'modo_aleatorio': self.aleatorio_activado,
            'modo_bucle': self.loop_mode,
            'playlist': self.playlist
        }
        
        if self.gestor_bd.guardar_configuraciones(self.usuario['id'], config):
            print(f"✓ Configuraciones guardadas")
    
    def on_closing(self):
        self.guardar_configuraciones_usuario()
        
        if self.en_reproduccion:
            self.parar_musica()
        
        if self.radio_module and self.radio_module.radio_playing:
            self.radio_module.stop_radio()
        
        respuesta = messagebox.askyesno("Cerrar Sesión", 
                                        "¿Deseas cerrar sesión?\n\nTus configuraciones han sido guardadas.")
        
        if respuesta:
            self.root.destroy()
            

# ==============================================================================
# INICIO DE LA APLICACIÓN
# ==============================================================================

if __name__ == "__main__":
    print("="*60)
    print("🎵 BLOOM MUSIC - Sistema Responsivo")
    print("="*60)
    print("✓ Inicializando base de datos...")
    
    
    print("✓ Base de datos lista")
    print("✓ Iniciando sistema de login...")
    print("="*60)
    
    Login()
    
    # ===== CONFIGURACIONES =====
    
    def cargar_configuraciones_usuario(self):
        config = self.gestor_bd.cargar_configuraciones(self.usuario['id'])
        
        if config:
            print(f"✓ Cargando configuraciones de {self.usuario['nombre']}")
            
            volumen = config['volumen']
            self.last_volume = volumen
            pygame.mixer.music.set_volume(volumen)
            self.volume_scale.set(volumen * 100)
            
            if config['modo_aleatorio']:
                self.toggle_aleatorio()
            
            for _ in range(config['modo_bucle']):
                self.toggle_loop()
            
            if config['playlist']:
                for cancion in config['playlist']:
                    if os.path.exists(cancion):
                        self.add_to_playlist(cancion)
                print(f"✓ {len(config['playlist'])} canciones restauradas")
            
            self.barra_estado.config(text=f"✓ Configuraciones cargadas - {self.usuario['nombre']}")
    
    def guardar_configuraciones_usuario(self):
        config = {
            'volumen': pygame.mixer.music.get_volume(),
            'modo_aleatorio': self.aleatorio_activado,
            'modo_bucle': self.loop_mode,
            'playlist': self.playlist
        }
        
        if self.gestor_bd.guardar_configuraciones(self.usuario['id'], config):
            print(f"✓ Configuraciones guardadas")
    
    def on_closing(self):
        self.guardar_configuraciones_usuario()
        
        if self.en_reproduccion:
            self.parar_musica()
        
        if self.radio_module and hasattr(self.radio_module, 'radio_playing') and self.radio_module.radio_playing:
            self.radio_module.stop_radio()
        
        respuesta = messagebox.askyesno("Cerrar Sesión", 
                                        "¿Deseas cerrar sesión?\n\nTus configuraciones han sido guardadas.")
        
        if respuesta:
            self.root.destroy()
            
# ==============================================================================
# INICIO DE LA APLICACIÓN
# ==============================================================================

if __name__ == "__main__":
    print("="*60)
    print("🎵 BLOOM MUSIC - Sistema Modular y Persistente")
    print("="*60)
    print("✓ Inicializando base de datos...")
    
    Login()
