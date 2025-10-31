# GestorVentanas.py
"""
BLOOM MUSIC - GESTOR DE VENTANAS
=================================
Sistema modular para gestionar las diferentes vistas sin perder datos
"""

import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os

class GestorVentanas:
    """Gestiona la navegación entre ventanas sin perder estado"""
    
    def __init__(self, main_frame, reproductor_instance, responsive_manager):
        self.main_frame = main_frame
        self.reproductor = reproductor_instance
        self.responsive = responsive_manager
        
        # Diccionario para almacenar las vistas
        self.vistas = {}
        self.vista_actual = None
        
        # Referencias a frames persistentes
        self.content_frames = {}
        
    def crear_sidebar(self, parent_frame):
        """Crea el sidebar común para todas las vistas"""
        sidebar_width = self.responsive.get_sidebar_width()
        sidebar_frame = tk.Frame(parent_frame, bg="white", width=sidebar_width)
        sidebar_frame.pack(side="left", fill="y", padx=10, pady=10)
        sidebar_frame.pack_propagate(False)
        
        # Header del sidebar
        header_frame = tk.Frame(sidebar_frame, bg="white")
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Logo
        logo_size = self.responsive.scale_dimension(80)
        try:
            img = Image.open("LogoLogin.png").resize((logo_size, logo_size), Image.LANCZOS)
            render = ImageTk.PhotoImage(img)
            label = tk.Label(header_frame, image=render, bg="white")
            label.image = render
            label.pack(side="top", padx=5, pady=5)
        except:
            pass
        
        # Botones del header
        btn_size = self.responsive.scale_font(12)
        
        tres_puntos = tk.Button(header_frame, text="⋯", bg="white", 
                               relief="sunken", font=("Helvetica", btn_size, "bold"),
                               cursor="hand2", command=self.reproductor.mostrar_menu_usuario)
        tres_puntos.place(relx=0.85, y=15)
        
        atras = tk.Button(header_frame, text="⬅️", bg="white",
                         relief="sunken", font=("Helvetica", btn_size, "bold"),
                         cursor="hand2", command=self.reproductor.on_closing)
        atras.place(x=10, y=15)
        
        # Barra de búsqueda
        search_font = self.responsive.scale_font(10)
        search_entry = ttk.Entry(sidebar_frame, font=("Helvetica", search_font))
        search_entry.insert(0, "Buscar")
        search_entry.pack(fill="x", padx=10, pady=5)
        search_entry.bind("<FocusIn>", self.reproductor.on_search_focus_in)
        search_entry.bind("<FocusOut>", self.reproductor.on_search_focus_out)
        search_entry.config(foreground="gray")
        
        # Botones de navegación
        sidebar_btn_font = self.responsive.scale_font(12)
        
        self.home_button = tk.Button(sidebar_frame, text="🏠 Home",
                                     font=("Helvetica", sidebar_btn_font), bg="white",
                                     relief="flat", anchor="w", padx=20,
                                     command=lambda: self.cambiar_vista("home"))
        self.home_button.pack(fill="x", pady=5)
        
        self.new_button = tk.Button(sidebar_frame, text="✨ Nuevo",
                                    font=("Helvetica", sidebar_btn_font), bg="white",
                                    relief="flat", anchor="w", padx=20,
                                    command=lambda: self.cambiar_vista("nuevo"))
        self.new_button.pack(fill="x", pady=5)
        
        self.radio_button = tk.Button(sidebar_frame, text="📻 Radio",
                                      font=("Helvetica", sidebar_btn_font), bg="white",
                                      relief="flat", anchor="w", padx=20,
                                      command=lambda: self.cambiar_vista("radio"))
        self.radio_button.pack(fill="x", pady=5)
        
        # Sección Librería
        label_font = self.responsive.scale_font(10)
        tk.Label(sidebar_frame, text="Librería", font=("Helvetica", label_font, "bold"),
                bg="white", anchor="w").pack(fill="x", padx=10, pady=(15, 5))
        
        self.recently_button = tk.Button(sidebar_frame, text="➕ Añadidos recientemente",
                                        font=("Helvetica", sidebar_btn_font), bg="white",
                                        relief="flat", anchor="w", padx=20,
                                        command=lambda: self.cambiar_vista("recientes"))
        self.recently_button.pack(fill="x", pady=5)
        
        self.artists_button = tk.Button(sidebar_frame, text="🧑‍🎤 Artistas",
                                        font=("Helvetica", sidebar_btn_font), bg="white",
                                        relief="flat", anchor="w", padx=20,
                                        command=lambda: self.cambiar_vista("artistas"))
        self.artists_button.pack(fill="x", pady=5)
        
        self.albums_button = tk.Button(sidebar_frame, text="💿 Álbums",
                                       font=("Helvetica", sidebar_btn_font), bg="white",
                                       relief="flat", anchor="w", padx=20,
                                       command=lambda: self.cambiar_vista("albums"))
        self.albums_button.pack(fill="x", pady=5)
        
        self.songs_button = tk.Button(sidebar_frame, text="🎵 Canciones",
                                      font=("Helvetica", sidebar_btn_font), bg="white",
                                      relief="flat", anchor="w", padx=20,
                                      command=lambda: self.cambiar_vista("canciones"))
        self.songs_button.pack(fill="x", pady=5)
        
        # Sección Playlists
        tk.Label(sidebar_frame, text="Playlists", font=("Helvetica", label_font, "bold"),
                bg="white", anchor="w").pack(fill="x", padx=10, pady=(15, 5))
        
        self.crear_playlist_button = tk.Button(sidebar_frame, text="➕ Crear Playlist",
                                               font=("Helvetica", sidebar_btn_font), 
                                               bg="white", relief="flat", anchor="w", padx=20,
                                               command=lambda: self.cambiar_vista("crear_playlist"))
        self.crear_playlist_button.pack(fill="x", pady=5)
        
        # Almacenar referencias a botones
        self.botones_navegacion = {
            'home': self.home_button,
            'nuevo': self.new_button,
            'radio': self.radio_button,
            'recientes': self.recently_button,
            'artistas': self.artists_button,
            'albums': self.albums_button,
            'canciones': self.songs_button,
            'crear_playlist': self.crear_playlist_button
        }
        
        return sidebar_frame
    
    def cambiar_vista(self, nombre_vista):
        """Cambia entre vistas sin perder datos"""
        # Si ya estamos en esta vista, no hacer nada
        if self.vista_actual == nombre_vista:
            return
        
        # Actualizar botones del sidebar
        for nombre, boton in self.botones_navegacion.items():
            if nombre == nombre_vista:
                boton.config(bg="#e0e0e0")
            else:
                boton.config(bg="white")
        
        # Ocultar vista actual
        if self.vista_actual and self.vista_actual in self.content_frames:
            self.content_frames[self.vista_actual].pack_forget()
        
        # Mostrar nueva vista
        if nombre_vista not in self.content_frames:
            self._crear_vista(nombre_vista)
        
        self.content_frames[nombre_vista].pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.vista_actual = nombre_vista
        
        # Actualizar barra de estado
        nombres_vistas = {
            'home': f'🏠 Inicio - {self.reproductor.usuario["nombre"]}',
            'nuevo': '✨ Explorar Nuevo',
            'radio': '📻 Vista de Radio',
            'recientes': '➕ Añadidos Recientemente',
            'artistas': '🧑‍🎤 Artistas',
            'albums': '💿 Álbums',
            'canciones': '🎵 Canciones',
            'crear_playlist': '➕ Crear Playlist'
        }
        self.reproductor.barra_estado.config(text=nombres_vistas.get(nombre_vista, ''))
    
    def _crear_vista(self, nombre_vista):
        """Crea el frame de contenido para cada vista"""
        frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.content_frames[nombre_vista] = frame
        
        if nombre_vista == "home":
            self._crear_vista_home(frame)
        elif nombre_vista == "canciones":
            self._crear_vista_canciones(frame)
        elif nombre_vista == "recientes":
            self._crear_vista_recientes(frame)
        elif nombre_vista == "crear_playlist":
            self._crear_vista_crear_playlist(frame)
        elif nombre_vista == "nuevo":
            self._crear_vista_nuevo(frame)
        elif nombre_vista == "albums":
            self._crear_vista_albums(frame)
        else:
            # Vista placeholder
            tk.Label(frame, text=f"Vista: {nombre_vista}\n(En desarrollo)",
                    font=("Helvetica", 20), bg="#f0f0f0").pack(expand=True)
    
    def _crear_vista_home(self, parent):
        """Vista principal del reproductor"""
        # Imagen del álbum
        album_display_size = self.responsive.scale_dimension(200)
        try:
            img = Image.open("emiliaMP3Foto.png").resize((album_display_size, album_display_size), Image.LANCZOS)
            render = ImageTk.PhotoImage(img)
            label = tk.Label(parent, image=render, bg="#f0f0f0")
            label.image = render
            label.pack(pady=20)
        except:
            tk.Label(parent, text="[Album Cover]",
                    font=("Helvetica", self.responsive.scale_font(14)),
                    bg="#f0f0f0").pack(pady=20)
        
        # Título de canción
        title_font = self.responsive.scale_font(18)
        self.reproductor.song_title = tk.Label(parent, text="Selecciona una canción",
                                               font=("Helvetica", title_font, "bold"), bg="#f0f0f0")
        self.reproductor.song_title.pack()
        
        subtitle_font = self.responsive.scale_font(12)
        tk.Label(parent, text="Bloom Music Player",
                font=("Helvetica", subtitle_font), bg="#f0f0f0").pack()
        
        # Controles inferiores
        player_controls_bottom_frame = tk.Frame(parent, bg="#f0f0f0")
        player_controls_bottom_frame.pack(pady=10)
        
        bottom_btn_font = self.responsive.scale_font(12)
        bottom_btn_padx = self.responsive.scale_dimension(20)
        bottom_btn_pady = self.responsive.scale_dimension(5)
        
        tk.Button(player_controls_bottom_frame, text="▶ Play",
                 font=("Helvetica", bottom_btn_font, "bold"), bg="#CF0A8D", fg="white",
                 relief="flat", padx=bottom_btn_padx, pady=bottom_btn_pady,
                 command=self.reproductor.reproducir_musica).pack(side="left", padx=5)
        
        self.reproductor.aleatorio_button_bottom = tk.Button(player_controls_bottom_frame,
                                                             text="🔀 Aleatorio",
                                                             font=("Helvetica", bottom_btn_font, "bold"),
                                                             bg="#e0e0e0", relief="flat",
                                                             padx=bottom_btn_padx, pady=bottom_btn_pady,
                                                             command=self.reproductor.toggle_aleatorio)
        self.reproductor.aleatorio_button_bottom.pack(side="left", padx=5)
        
        self.reproductor.loop_button_right = tk.Button(player_controls_bottom_frame,
                                                       text="🔂", font=("Helvetica", self.responsive.scale_font(14)),
                                                       bg="#f0f0f0", relief="flat",
                                                       command=self.reproductor.toggle_loop)
        self.reproductor.loop_button_right.pack(side="left", padx=5)
        
        # PLAYLIST CON SCROLL
        playlist_frame = tk.Frame(parent, bg="white")
        playlist_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        listbox_container = Frame(playlist_frame, bg="white")
        listbox_container.pack(fill="both", expand=True, pady=5, padx=5)
        
        scrollbar = Scrollbar(listbox_container)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        playlist_font = self.responsive.scale_font(10)
        self.reproductor.playlistbox = Listbox(listbox_container, bg="white",
                                               font=("Helvetica", playlist_font),
                                               selectbackground="#adaaaa",
                                               yscrollcommand=scrollbar.set)
        self.reproductor.playlistbox.pack(side=LEFT, fill="both", expand=True)
        scrollbar.config(command=self.reproductor.playlistbox.yview)
        
        # Restaurar playlist si existe
        for cancion in self.reproductor.playlist:
            nombre_limpio = os.path.basename(cancion).replace('.mp3', '').replace('.wav', '')
            self.reproductor.playlistbox.insert('end', nombre_limpio)
        
        # Botones de playlist
        playlist_buttons_frame = Frame(playlist_frame, bg="white")
        playlist_buttons_frame.pack(fill="x", pady=5)
        
        playlist_btn_font = self.responsive.scale_font(11)
        playlist_btn_padx = self.responsive.scale_dimension(15)
        
        tk.Button(playlist_buttons_frame, text="🎵 Añadir Canción",
                 font=("Helvetica", playlist_btn_font), bg="white", relief="flat",
                 anchor="w", padx=playlist_btn_padx,
                 command=self.reproductor.Importar_Musica).pack(side=LEFT, fill="x", expand=True)
        
        tk.Button(playlist_buttons_frame, text="📁 Añadir Carpeta",
                 font=("Helvetica", playlist_btn_font), bg="white", relief="flat",
                 anchor="w", padx=playlist_btn_padx,
                 command=self.reproductor.Importar_Carpeta).pack(side=LEFT, fill="x", expand=True)
        
        tk.Button(playlist_buttons_frame, text="❌ Eliminar",
                 font=("Helvetica", playlist_btn_font), bg="white", relief="flat",
                 anchor="w", padx=playlist_btn_padx,
                 command=self.reproductor.del_from_playlist).pack(side=LEFT, fill="x", expand=True)
    
    def _crear_vista_canciones(self, parent):
        """Vista de todas las canciones"""
        # Header
        header = tk.Frame(parent, bg="#FDA5E0", height=70)
        header.pack(side="top", fill=X)
        tk.Label(header, bg="#FDA5E0", text="🎵 Canciones",
                font=("Helvetica", self.responsive.scale_font(20))).pack()
        
        # Botón aleatorio
        aleatorio_frame = tk.Frame(parent, bg="white")
        aleatorio_frame.pack(fill="x", side="top", pady=(20, 0))
        
        tk.Button(aleatorio_frame, text="🔀", font=("Helvetica", 20, "bold"),
                 bg="#FDA5E0", relief="flat",
                 command=self.reproductor.toggle_aleatorio).pack(padx=5, side="right")
        
        # Lista de canciones
        playlist_frame = tk.Frame(parent, bg="white")
        playlist_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        scrollbar = Scrollbar(playlist_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        listbox = Listbox(playlist_frame, bg="white",
                         font=("Helvetica", self.responsive.scale_font(10)),
                         selectbackground="#adaaaa", relief=FLAT,
                         yscrollcommand=scrollbar.set)
        listbox.pack(fill="both", expand=True, anchor="w", pady=5)
        scrollbar.config(command=listbox.yview)
        
        # Llenar con canciones de la playlist
        for cancion in self.reproductor.playlist:
            nombre = os.path.basename(cancion).replace('.mp3', '').replace('.wav', '')
            listbox.insert('end', nombre)
        
        # Vincular doble clic para reproducir
        def reproducir_seleccionada(event):
            if listbox.curselection():
                idx = int(listbox.curselection()[0])
                if idx < len(self.reproductor.playlist):
                    # Actualizar selección en playlistbox principal
                    self.reproductor.playlistbox.selection_clear(0, END)
                    self.reproductor.playlistbox.activate(idx)
                    self.reproductor.playlistbox.selection_set(idx)
                    self.reproductor.reproducir_musica()
        
        listbox.bind('<Double-Button-1>', reproducir_seleccionada)
    
    def _crear_vista_recientes(self, parent):
        """Vista de añadidos recientemente"""
        # Header
        header = tk.Frame(parent, bg="#FDA5E0", height=70)
        header.pack(side="top", fill=X)
        tk.Label(header, bg="#FDA5E0", text="➕ Añadidos Recientemente",
                font=("Helvetica", self.responsive.scale_font(20))).pack()
        
        # Lista de canciones recientes (últimas 20)
        playlist_frame = tk.Frame(parent, bg="white")
        playlist_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        scrollbar = Scrollbar(playlist_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        listbox = Listbox(playlist_frame, bg="white",
                         font=("Helvetica", self.responsive.scale_font(10)),
                         selectbackground="#adaaaa", relief=FLAT,
                         yscrollcommand=scrollbar.set)
        listbox.pack(fill="both", expand=True, pady=5)
        scrollbar.config(command=listbox.yview)
        
        # Mostrar últimas 20 canciones
        canciones_recientes = self.reproductor.playlist[-20:] if len(self.reproductor.playlist) > 20 else self.reproductor.playlist
        for cancion in reversed(canciones_recientes):
            nombre = os.path.basename(cancion).replace('.mp3', '').replace('.wav', '')
            listbox.insert('end', f"🎵 {nombre}")
        
        if not canciones_recientes:
            tk.Label(playlist_frame, text="No hay canciones añadidas aún",
                    font=("Helvetica", self.responsive.scale_font(12)),
                    bg="white", fg="gray").pack(expand=True)
    
    def _crear_vista_crear_playlist(self, parent):
        """Vista para crear playlists"""
        # Header
        header = tk.Frame(parent, bg="#FFCBFC", height=70)
        header.pack(side="top", fill=X)
        tk.Label(header, bg="#FFCBFC", text="➕ Crear Playlist",
                font=("Helvetica", self.responsive.scale_font(20))).pack()
        
        # Frame de datos
        datos_frame = tk.Frame(parent, bg="#FFDAFD")
        datos_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Nombre de playlist
        nombre_frame = tk.Frame(datos_frame, bg="#FFDAFD")
        nombre_frame.pack(fill="x", side="top", pady=(20, 0))
        
        tk.Label(nombre_frame, text="Poné nombre a tu playlist",
                font=("Helvetica", self.responsive.scale_font(20)),
                bg="#FFDAFD").pack(side="top", fill="x")
        
        entry_nombre = tk.Entry(nombre_frame, highlightthickness=3,
                               highlightcolor="#000000", bg="#FFDAFD",
                               width=40, relief="flat",
                               font=("Helvetica", self.responsive.scale_font(12)))
        entry_nombre.pack(side="top", pady=10)
        
        # Elegir color
        color_label_frame = tk.Frame(datos_frame, bg="#FFDAFD")
        color_label_frame.pack(fill="x", side="top", pady=20)
        
        tk.Label(color_label_frame, text="Elegí un color para tu portada",
                font=("Helvetica", self.responsive.scale_font(20)),
                bg="#FFDAFD").pack(side=TOP, fill="x")
        
        # Botones de colores
        color_frame = tk.Frame(datos_frame, bg="#FFDAFD")
        color_frame.pack(fill="x", side="top", pady=20)
        
        colores = ["#B349FF", "#7247FF", "#60FEF1", "#99FF93", "#FFFC55", "#FF5D5D"]
        color_seleccionado = [colores[0]]  # Lista mutable para almacenar selección
        
        def seleccionar_color(color):
            color_seleccionado[0] = color
        
        for color in colores:
            btn = tk.Button(color_frame, bg=color, relief="flat",
                           width=15, height=8,
                           command=lambda c=color: seleccionar_color(c))
            btn.pack(side=LEFT, padx=10)
        
        # Botón confirmar
        confirmar_frame = tk.Frame(datos_frame, bg="#FFDAFD")
        confirmar_frame.pack(fill="x", side="top", pady=20)
        
        def confirmar_playlist():
            nombre = entry_nombre.get()
            if nombre.strip():
                from tkinter import messagebox
                messagebox.showinfo("Playlist Creada",
                                  f"Playlist '{nombre}' creada con éxito!\n"
                                  f"Color: {color_seleccionado[0]}")
                entry_nombre.delete(0, END)
            else:
                from tkinter import messagebox
                messagebox.showwarning("Error", "Por favor ingresa un nombre para la playlist")
        
        tk.Button(confirmar_frame, text="Confirmar", fg="#ffffff",
                 font=("Helvetica", self.responsive.scale_font(20), "bold"),
                 bg="#cf0a8d", relief="flat", width=20,
                 command=confirmar_playlist).pack(side=BOTTOM)
    
    def _crear_vista_nuevo(self, parent):
        """Vista de exploración de géneros"""
        # Header
        header = tk.Frame(parent, bg="#FDA5E0", height=70)
        header.pack(side="top", fill=X)
        tk.Label(header, bg="#FDA5E0", text="✨ Descubrí Algo Nuevo",
                font=("Helvetica", self.responsive.scale_font(20))).pack()
        
        # Géneros musicales
        generos_frame1 = tk.Frame(parent, bg="white")
        generos_frame1.pack(fill="x", side="top", pady=(20, 0))
        
        generos_frame2 = tk.Frame(parent, bg="white")
        generos_frame2.pack(fill="x", side="top", pady=(20, 0))
        
        generos = [
            ("POP", "#3cfd23"),
            ("Cumbia", "#d67a02"),
            ("Hip Hop", "#1feefd"),
            ("Tendencia", "#c905b8"),
        ]
        
        generos2 = [
            ("Rock", "#2d06db"),
            ("Salsa", "#a023f3"),
            ("Jazz", "#e00a0a"),
            ("Latina", "#efff0c")
        ]
        
        btn_width = max(10, self.responsive.scale_dimension(12))
        btn_height = max(5, self.responsive.scale_dimension(6))
        
        for nombre, color in generos:
            tk.Button(generos_frame1, text=nombre,
                     font=("Helvetica", self.responsive.scale_font(20), "bold"),
                     bg=color, relief="flat", width=btn_width, height=btn_height
                     ).pack(padx=20, side="left")
        
        for nombre, color in generos2:
            tk.Button(generos_frame2, text=nombre,
                     font=("Helvetica", self.responsive.scale_font(20), "bold"),
                     bg=color, relief="flat", width=btn_width, height=btn_height
                     ).pack(padx=20, side="left")
    
    def _crear_vista_albums(self, parent):
        """Vista de álbums"""
        # Header
        header = tk.Frame(parent, bg="#FDA5E0", height=70)
        header.pack(side="top", fill=X)
        tk.Label(header, bg="#FDA5E0", text="💿 Álbums",
                font=("Helvetica", self.responsive.scale_font(20))).pack()
        
        # Grid de álbums (placeholder)
        albums_frame1 = tk.Frame(parent, bg="white")
        albums_frame1.pack(fill="x", side="top", pady=(20, 0))
        
        albums_frame2 = tk.Frame(parent, bg="white")
        albums_frame2.pack(fill="x", side="top", pady=(20, 0))
        
        # Crear 8 placeholders de álbums
        for i in range(4):
            frame = tk.Frame(albums_frame1, bg="white")
            frame.pack(padx=20, side="left")
            
            tk.Button(frame, text="", bg="#3cfd23", relief="flat",
                     width=10, height=5).pack()
            tk.Label(frame, text=f"Artista {i+1} | Álbum",
                    bg="white", font=("Helvetica", 10, "bold")).pack(side=BOTTOM)
        
        for i in range(4, 8):
            frame = tk.Frame(albums_frame2, bg="white")
            frame.pack(padx=20, side="left")
            
            tk.Button(frame, text="", bg="#3cfd23", relief="flat",
                     width=10, height=5).pack()
            tk.Label(frame, text=f"Artista {i+1} | Álbum",
                    bg="white", font=("Helvetica", 10, "bold")).pack(side=BOTTOM)