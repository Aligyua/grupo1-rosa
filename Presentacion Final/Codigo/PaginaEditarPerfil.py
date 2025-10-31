# PaginaEditarPerfil.py
"""
BLOOM MUSIC - EDITAR PERFIL
============================
Ventana para editar datos del usuario
"""

import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk


class VentanaEditarPerfil:
    """Ventana modal para editar perfil del usuario"""
    
    def __init__(self, parent, usuario_datos, gestor_bd, callback_actualizar=None):
        self.parent = parent
        self.usuario = usuario_datos.copy()
        self.gestor_bd = gestor_bd
        self.callback_actualizar = callback_actualizar
        
        # Crear ventana modal
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Editar Perfil - Bloom Music")
        self.ventana.geometry("600x500")
        self.ventana.configure(bg="white")
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        # Centrar ventana
        self.ventana.update_idletasks()
        x = (self.ventana.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (500 // 2)
        self.ventana.geometry(f"600x500+{x}+{y}")
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de edición de perfil"""
        # Header
        header = tk.Frame(self.ventana, bg="#FDA5E0", height=70)
        header.pack(side=TOP, fill=X)
        
        tk.Label(header, text="⚙️ Configuración de Usuario",
                font=("Helvetica", 18, "bold"), bg="#FDA5E0").pack(pady=20)
        
        # Frame principal con scroll
        main_canvas = tk.Canvas(self.ventana, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.ventana, orient="vertical", command=main_canvas.yview)
        scrollable_frame = Frame(main_canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # Título
        tk.Label(scrollable_frame, text="Datos del Usuario",
                font=("Helvetica", 16, "bold"), bg="white").pack(pady=(10, 20))
        
        # NOMBRE DE USUARIO
        nombre_frame = tk.Frame(scrollable_frame, bg="white")
        nombre_frame.pack(fill="x", pady=10)
        
        tk.Label(nombre_frame, text="Nombre de Usuario",
                font=("Helvetica", 12, "bold"), bg="white").pack(side=LEFT, padx=10)
        
        self.entry_nombre = tk.Entry(nombre_frame, font=("Helvetica", 12), bg="white", width=25)
        self.entry_nombre.insert(0, self.usuario.get('nombre', ''))
        self.entry_nombre.pack(side=LEFT, padx=10)
        
        # EMAIL
        email_frame = tk.Frame(scrollable_frame, bg="white")
        email_frame.pack(fill="x", pady=10)
        
        tk.Label(email_frame, text="Email",
                font=("Helvetica", 12, "bold"), bg="white").pack(side=LEFT, padx=10)
        
        self.entry_email = tk.Entry(email_frame, font=("Helvetica", 12), bg="white", width=30)
        self.entry_email.insert(0, self.usuario.get('email', ''))
        self.entry_email.pack(side=LEFT, padx=10)
        
        # GÉNERO
        genero_frame = tk.Frame(scrollable_frame, bg="white")
        genero_frame.pack(fill="x", pady=10)
        
        tk.Label(genero_frame, text="Género",
                font=("Helvetica", 12, "bold"), bg="white").pack(side=LEFT, padx=10)
        
        self.combo_genero = ttk.Combobox(genero_frame, 
                                         values=["Masculino", "Femenino", "Otro"],
                                         font=("Helvetica", 12), width=20, state="readonly")
        genero_actual = self.usuario.get('genero', 'Masculino')
        self.combo_genero.set(genero_actual if genero_actual else "Masculino")
        self.combo_genero.pack(side=LEFT, padx=10)
        
        # CONTRASEÑA
        contraseña_frame = tk.Frame(scrollable_frame, bg="white")
        contraseña_frame.pack(fill="x", pady=10)
        
        tk.Label(contraseña_frame, text="Nueva Contraseña",
                font=("Helvetica", 12, "bold"), bg="white").pack(side=LEFT, padx=10)
        
        self.entry_contraseña = tk.Entry(contraseña_frame, font=("Helvetica", 12),
                                         bg="white", width=25, show="*")
        self.entry_contraseña.pack(side=LEFT, padx=10)
        
        # Botón mostrar/ocultar contraseña
        self.mostrar_contra = False
        
        def toggle_contraseña():
            if self.mostrar_contra:
                self.entry_contraseña.config(show="*")
                btn_toggle.config(text="👁")
                self.mostrar_contra = False
            else:
                self.entry_contraseña.config(show="")
                btn_toggle.config(text="🙈")
                self.mostrar_contra = True
        
        btn_toggle = tk.Button(contraseña_frame, text="👁", font=("Helvetica", 12),
                               bg="white", relief="flat", command=toggle_contraseña)
        btn_toggle.pack(side=LEFT, padx=5)
        
        tk.Label(scrollable_frame, text="(Dejar en blanco para no cambiar)",
                font=("Helvetica", 9), fg="gray", bg="white").pack()
        
        # Separador
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=20)
        
        # BOTONES
        botones_frame = tk.Frame(scrollable_frame, bg="white")
        botones_frame.pack(pady=20)
        
        tk.Button(botones_frame, text="💾 Guardar Cambios",
                 font=("Helvetica", 14, "bold"), bg="#00c853", fg="white",
                 relief="flat", padx=20, pady=10,
                 command=self.guardar_cambios).pack(side=LEFT, padx=10)
        
        tk.Button(botones_frame, text="❌ Cancelar",
                 font=("Helvetica", 14, "bold"), bg="#757575", fg="white",
                 relief="flat", padx=20, pady=10,
                 command=self.ventana.destroy).pack(side=LEFT, padx=10)
        
        # Separador
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=20)
        
        # ZONA PELIGROSA
        danger_frame = tk.Frame(scrollable_frame, bg="#ffebee", relief="solid", bd=1)
        danger_frame.pack(fill="x", pady=10, padx=20)
        
        tk.Label(danger_frame, text="⚠️ Zona Peligrosa",
                font=("Helvetica", 12, "bold"), bg="#ffebee", fg="#c62828").pack(pady=10)
        
        tk.Label(danger_frame, 
                text="Eliminar tu cuenta es permanente y no se puede deshacer.\n"
                     "Se perderán todas tus playlists y configuraciones.",
                font=("Helvetica", 9), bg="#ffebee", fg="#666").pack(pady=5)
        
        tk.Button(danger_frame, text="🗑️ Eliminar Cuenta",
                 font=("Helvetica", 12, "bold"), bg="#d32f2f", fg="white",
                 relief="flat", padx=20, pady=8,
                 command=self.confirmar_eliminar_cuenta).pack(pady=10)
    
    def guardar_cambios(self):
        """Guarda los cambios del perfil"""
        nuevo_nombre = self.entry_nombre.get().strip()
        nuevo_email = self.entry_email.get().strip()
        nuevo_genero = self.combo_genero.get()
        nueva_contraseña = self.entry_contraseña.get().strip()
        
        if not nuevo_nombre or not nuevo_email:
            messagebox.showerror("Error", "El nombre y email son obligatorios")
            return
        
        # Validar email
        import re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", nuevo_email):
            messagebox.showerror("Error", "Email inválido")
            return
        
        # Preparar datos
        datos = {
            'nombre': nuevo_nombre,
            'email': nuevo_email,
            'genero': nuevo_genero,
            'contraseña': nueva_contraseña
        }
        
        # Actualizar en la base de datos
        if self.gestor_bd.actualizar_usuario(self.usuario['id'], datos):
            messagebox.showinfo("Bloom Music", 
                              f"✅ Datos actualizados correctamente!\n\n"
                              f"Usuario: {nuevo_nombre}\n"
                              f"Email: {nuevo_email}")
            
            # Actualizar datos locales
            self.usuario['nombre'] = nuevo_nombre
            self.usuario['email'] = nuevo_email
            self.usuario['genero'] = nuevo_genero
            
            # Llamar callback si existe
            if self.callback_actualizar:
                self.callback_actualizar(self.usuario)
            
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", 
                               "No se pudieron guardar los cambios.\n"
                               "El nombre de usuario o email ya existe.")
    
    def confirmar_eliminar_cuenta(self):
        """Confirma la eliminación de la cuenta"""
        respuesta = messagebox.askyesno(
            "⚠️ Confirmar Eliminación",
            "¿Estás COMPLETAMENTE SEGURO de que deseas eliminar tu cuenta?\n\n"
            "Esta acción:\n"
            "• NO se puede deshacer\n"
            "• Eliminará todas tus playlists\n"
            "• Borrará todas tus configuraciones\n"
            "• Cerrará la aplicación\n\n"
            "¿Deseas continuar?",
            icon='warning'
        )
        
        if not respuesta:
            return
        
        # Segunda confirmación
        respuesta2 = messagebox.askyesno(
            "⚠️ Última Confirmación",
            f"Por favor confirma escribiendo tu nombre de usuario:\n\n"
            f"Escribe '{self.usuario['nombre']}' para confirmar",
            icon='warning'
        )
        
        if not respuesta2:
            return
        
        # Solicitar confirmación escrita
        from tkinter import simpledialog
        confirmacion = simpledialog.askstring(
            "Confirmar Eliminación",
            f"Escribe '{self.usuario['nombre']}' para confirmar:",
            parent=self.ventana
        )
        
        if confirmacion != self.usuario['nombre']:
            messagebox.showinfo("Cancelado", "Eliminación cancelada.")
            return
        
        # Eliminar cuenta
        if self.gestor_bd.eliminar_usuario(self.usuario['id']):
            messagebox.showinfo("Bloom Music",
                              "Tu cuenta ha sido eliminada correctamente.\n"
                              "La aplicación se cerrará.")
            self.ventana.destroy()
            self.parent.quit()
        else:
            messagebox.showerror("Error", "No se pudo eliminar la cuenta.")


def abrir_editar_perfil(parent, usuario_datos, gestor_bd, callback=None):
    """Función auxiliar para abrir la ventana de editar perfil"""
    VentanaEditarPerfil(parent, usuario_datos, gestor_bd, callback)