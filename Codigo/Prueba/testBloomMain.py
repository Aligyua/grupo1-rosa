import tkinter as tk
from tkinter import *
from tkinter import filedialog, PhotoImage
import tkinter.messagebox
from tkinter import ttk
import threading
from PIL import Image, ImageTk

import pygame
from mutagen.mp3 import MP3

import os, sys, time
import requests

#------------------------------------------------------------
#---------------TOOLBAR MENU-----------------

class Pagina_Principal:
    def __init__(self, root):
        self.root = root
        self.root.title("Bloom Music")
        self.root.geometry("1200x800")
        self.root.configure(bg="white")

        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill="both", expand=True)

        #---------------------------------------------
        #----------------SQL PART---------------------
        #---------------------------------------------
        
        # ESTADO Y VARIABLES DE CONTROL
        self.pausa = FALSE
        self.en_reproduccion = FALSE
        self.playlist = [] # Rutas completas
        self.duracion_total = 0 # Duración de la canción actual en segundos
        
        global filename 
        filename = "" 
        
        # BANDERA DE CONTROL DE HILO
        self.stop_timer_flag = threading.Event() 
        # BANDERA PARA CONTROLAR EL MOVIMIENTO DEL SLIDER
        self.slider_moving = False 
        # Variable para mantener la posición actual cuando la música está pausada o detenida
        self.current_position_s = 0.0
        
        # Variable para almacenar la posición de inicio al dar Play/Reanudar
        self.play_start_position = 0.0
        
        # ⭐️ VARIABLES DE CONTROL DE VOLUMEN/MUTE ⭐️
        self.last_volume = 0.70 
        self.is_muted = False

        #barra de estado (bienvenida/reproduccion/pausa)
        self.barra_estado = tk.Label(root,text='Bienvenido a Bloom', relief= SUNKEN)
        self.barra_estado.pack(side=BOTTOM, fill=X)
        
        # Menu Bar
        self.menubar = menubar = Menu(root)
        self.root.config(menu=menubar)

        self.create_widgets()
    
    #Funciones del MENU

    #sub-menu IMPORTAR
    def Importar_Musica(self): 
        global filename
        filename = filedialog.askopenfilename(defaultextension=".mp3", 
                                              filetypes=[("Archivos de Audio", "*.mp3 *.wav"), 
                                                         ("Todos los archivos", "*.*")])
        if filename:
            self.add_to_playlist(filename)


    def Importar_Carpeta(self):
        global folder_path
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.select_folder(folder_path)

    def select_folder(self, folder):
        index = self.playlistbox.size() 
        
        if folder: 
            self.playlistbox.delete(0, END)
            self.playlist.clear() 
            
            try:
                for file in os.listdir(folder):
                    full_path = os.path.join(folder, file) 
                    
                    if os.path.isfile(full_path) and full_path.lower().endswith(('.mp3', '.wav')):
                        
                        self.playlistbox.insert(index, file) 
                        self.playlist.append(full_path)
                        
                        index += 1
                        
            except FileNotFoundError:
                tkinter.messagebox.showerror('Directorio no encontrado','Bloom no pudo encontrar su directorio. Intentalo de nuevo')

    def add_to_playlist(self, full_path):
        
        if not full_path:
             tkinter.messagebox.showerror('Archivo no encontrado','Bloom no pudo encontrar su archivo. Intentalo de nuevo')
             return
             
        file_name = os.path.basename(full_path) 
        
        self.playlistbox.insert('end', file_name) 
        self.playlist.append(full_path)

    
    def del_from_playlist(self):
        try:
            cancion_seleccionada = self.playlistbox.curselection()
            if not cancion_seleccionada:
                return 
                
            index = int(cancion_seleccionada[0])
            
            self.playlistbox.delete(index)
            
            if index < len(self.playlist):
                del self.playlist[index]
                
        except Exception as e:
            tkinter.messagebox.showerror('Error', 'No se pudo eliminar la canción seleccionada.')
            
    # Pygame
    pygame.mixer.init()

    # --- FUNCIONES PARA CONTROLAR EL SLIDER ---
    def slider_press(self, event):
        self.slider_moving = True

    def slider_move(self, event):
        if self.slider_moving:
            tiempo_deseado = self.progress_bar.get()
            self.current_position_s = tiempo_deseado
            
            mins, secs = divmod(tiempo_deseado, 60)
            formato_tiempo = '{:02d}:{:02d}'.format(int(mins), int(secs))
            self.current_time_label.config(text=formato_tiempo) 
    
    def slider_release(self, event):
        tiempo_deseado = self.progress_bar.get()
        
        if pygame.mixer.music.get_busy() or self.pausa:
             pygame.mixer.music.set_pos(tiempo_deseado) 
             
             self.current_position_s = tiempo_deseado
             self.play_start_position = tiempo_deseado
        
        self.slider_moving = False
    # --- FIN DE LAS FUNCIONES DEL SLIDER ---


    # ⭐️ FUNCIÓN TOGGLE MUTE ⭐️
    def toggle_mute(self, event=None):
        if self.is_muted:
            # DESILENCIAR
            volumen_a_restaurar = self.last_volume 
            pygame.mixer.music.set_volume(volumen_a_restaurar)
            self.volume_scale.set(volumen_a_restaurar * 100)
            self.volume_label.config(text="🔊") 
            self.is_muted = False
        else:
            # SILENCIAR
            current_vol = pygame.mixer.music.get_volume()
            
            if current_vol > 0.01:
                self.last_volume = current_vol 
                
            pygame.mixer.music.set_volume(0.0)
            self.volume_scale.set(0)
            self.volume_label.config(text="🔇")
            self.is_muted = True
            
    # ⭐️ FUNCIÓN CANCIÓN SIGUIENTE ⭐️
    def next_song(self):
        cancion_seleccionada = self.playlistbox.curselection()
        
        if not self.playlist:
            return
            
        if not cancion_seleccionada:
            # Si no hay nada seleccionado, empezamos en la primera
            proximo_idx = 0
        else:
            actual_idx = int(cancion_seleccionada[0])
            
            # Si no es la última, avanzamos
            if actual_idx < len(self.playlist) - 1:
                proximo_idx = actual_idx + 1
            else:
                # Volver a la primera canción si estamos en la última (bucle)
                proximo_idx = 0

        # 1. Deseleccionar, activar y seleccionar la próxima
        self.playlistbox.selection_clear(0, END)
        self.playlistbox.activate(proximo_idx)
        self.playlistbox.selection_set(proximo_idx)
        
        # 2. Reproducir la nueva canción
        self.reproducir_musica()

    # ⭐️ FUNCIÓN CANCIÓN ANTERIOR ⭐️
    def prev_song(self):
        cancion_seleccionada = self.playlistbox.curselection()
        
        if not self.playlist:
            return
            
        if not cancion_seleccionada:
            # Si no hay nada seleccionado, no hacemos nada
            return
            
        actual_idx = int(cancion_seleccionada[0])
        
        # Calcular el índice de la canción anterior
        if actual_idx > 0:
            previo_idx = actual_idx - 1
        else:
            # Si ya está en la primera (índice 0), se queda en la misma (límite)
            previo_idx = 0

        # 1. Deseleccionar, activar y seleccionar la previa
        self.playlistbox.selection_clear(0, END)
        self.playlistbox.activate(previo_idx)
        self.playlistbox.selection_set(previo_idx)
        
        # 2. Reproducir la nueva canción (la misma si previo_idx es 0 y ya estaba ahí)
        self.reproducir_musica()


    def obtener_datos_cancion(self, cancion):
        try:
            datos_archivo = os.path.splitext(cancion)
            if datos_archivo[1].lower() == '.mp3':
                audio = MP3(cancion)
                duracion_total = audio.info.length
            else:
                audio = pygame.mixer.Sound(cancion)
                duracion_total = audio.get_length()
        except Exception:
             duracion_total = 0 
        
        return duracion_total

    def cancion_actual_reproduciendose(self, cancion):
        
        self.duracion_total = self.obtener_datos_cancion(cancion)
             
        # Configurar el slider con la duración total
        self.progress_bar.config(to=self.duracion_total)
        self.progress_bar.set(0)
        self.current_position_s = 0.0 # Reiniciar la posición al cargar una nueva canción
        self.play_start_position = 0.0 # Reiniciar posición de inicio

        # TITULO MAIN
        self.song_title ['text'] = os.path.basename(cancion)
        
        mins, secs = divmod(self.duracion_total, 60)
        mins= round(mins)
        secs= round(secs)
        formato_tiempo = '{:02d}:{:02d}'.format(mins,secs)
        self.total_time_label['text'] = formato_tiempo

        tiempothreading = threading.Thread(target=self.comenzar_temporizador, args=(self.duracion_total,))
        tiempothreading.start()

    #------------------------------------
    #------------DATOS DE CANCION
    #------------------------------------
    def mostrar_datos_musica(self, cancion):
        self.song_title_top['text'] = 'Reproduciendo' + ' - ' + os.path.basename(cancion)
        self.song_title ['text'] = os.path.basename(cancion)
        
        duracion = self.obtener_datos_cancion(cancion)
        mins, secs = divmod(duracion, 60)
        mins= round(mins)
        secs= round(secs)
        formato_tiempo = '{:02d}:{:02d}'.format(mins,secs)
        self.total_time_label['text'] = formato_tiempo


    def comenzar_temporizador(self, tiempo):
        
        while pygame.mixer.music.get_busy() or self.pausa: 
            
            if self.stop_timer_flag.is_set():
                 break 
            
            # Solo actualizamos el slider si el usuario NO lo está moviendo
            if not self.slider_moving:
                
                # Si está en reproducción y no pausada:
                if pygame.mixer.music.get_busy() and not self.pausa:
                    tiempo_transcurrido_relativo = pygame.mixer.music.get_pos() / 1000
                    
                    self.current_position_s = self.play_start_position + tiempo_transcurrido_relativo
                
                # Formatear y actualizar el tiempo
                mins, secs = divmod(self.current_position_s, 60)
                formato_tiempo = '{:02d}:{:02d}'.format(int(mins), int(secs))
                
                # Actualizaciones seguras de la interfaz
                self.current_time_label.after(0, lambda t=formato_tiempo: self.current_time_label.config(text=t))
                self.progress_bar.after(0, lambda val=self.current_position_s: self.progress_bar.set(val))

            # Si el tiempo actual supera la duración total, salimos 
            if self.current_position_s >= tiempo:
                break
            
            # Pausa de tiempo para refrescar el hilo 
            self.stop_timer_flag.wait(0.1) 
        
        # Limpiar al finalizar 
        self.current_position_s = 0.0
        self.play_start_position = 0.0
        self.current_time_label.after(0, lambda: self.current_time_label.config(text="00:00")) 
        self.progress_bar.after(0, lambda: self.progress_bar.set(0)) 


    def pausar_musica(self):
        if self.en_reproduccion == TRUE:
            tiempo_transcurrido_relativo = pygame.mixer.music.get_pos() / 1000 
            self.current_position_s = self.play_start_position + tiempo_transcurrido_relativo
            
            self.pausa = TRUE
            self.en_reproduccion = FALSE
            pygame.mixer.music.pause()
            
            try:
                cancion_seleccionada_idx = self.playlistbox.curselection()
                song_name = os.path.basename(self.playlist[int(cancion_seleccionada_idx[0])]) if cancion_seleccionada_idx else "..."
            except:
                song_name = "..."
                
            self.barra_estado['text'] = 'En Pausa...' + '   -   ' + song_name
            
    def parar_musica(self):
        pygame.mixer.music.stop()
        self.en_reproduccion = FALSE
        self.pausa = FALSE 
        self.current_position_s = 0.0
        self.play_start_position = 0.0
        
        self.stop_timer_flag.set()
        self.stop_timer_flag.clear()

        try:
            cancion_seleccionada_idx = self.playlistbox.curselection()
            song_name = os.path.basename(self.playlist[int(cancion_seleccionada_idx[0])]) if cancion_seleccionada_idx else "..."
        except:
            song_name = "..."
            
        self.barra_estado['text'] = 'Musica Frenada' + '   -   ' + song_name
        
        
    def reproducir_musica(self):
        global filename
        
        try:
            cancion_seleccionada = self.playlistbox.curselection()
            if not cancion_seleccionada:
                # Intenta usar la primera canción si no hay selección pero hay playlist
                if self.playlist:
                    self.playlistbox.activate(0)
                    self.playlistbox.selection_set(0)
                    cancion_seleccionada = self.playlistbox.curselection()
                else:
                    tkinter.messagebox.showerror('Error', 'Por favor, selecciona una canción de la lista.')
                    return

            cancion_seleccionada_idx = int(cancion_seleccionada[0]) 
            reproducir_cancion = self.playlist[cancion_seleccionada_idx] 
            song_name = os.path.basename(reproducir_cancion)
            
            # Caso 1: Si está en pausa, reanudar
            if self.pausa:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(reproducir_cancion)
                pygame.mixer.music.play(start=self.current_position_s) 
                self.play_start_position = self.current_position_s
                self.pausa = FALSE
            
            # Caso 2: Iniciar una nueva reproducción (o reiniciar si no estaba pausada)
            else:
                # 1. DETENER HILO ANTERIOR y Pygame
                self.stop_timer_flag.set() 
                pygame.mixer.music.stop()
                self.stop_timer_flag.clear() 

                # 2. Cargar y Reproducir (desde el inicio o desde el punto del slider si se movió)
                pygame.mixer.music.load(reproducir_cancion)
                
                # Usar self.current_position_s que fue actualizado por el slider_release
                # Si no se movió el slider, current_position_s será 0.0
                start_pos = self.current_position_s 
                pygame.mixer.music.play(start=start_pos)
                
                self.en_reproduccion = TRUE
                self.pausa = FALSE
                self.progress_bar.set(start_pos) 
                self.play_start_position = start_pos 
                
                # Actualizar la interfaz e iniciar el nuevo hilo si no estaba corriendo
                self.mostrar_datos_musica(reproducir_cancion)
                self.cancion_actual_reproduciendose(reproducir_cancion)

            self.en_reproduccion = TRUE
            self.barra_estado['text'] = 'Reproduciendo Musica' + '   -   ' + song_name
                
        except IndexError:
            tkinter.messagebox.showerror('Error', 'Selección no válida. Asegúrate de que la canción existe en la lista.')
        except pygame.error as e:
            tkinter.messagebox.showerror('Error de Pygame', f"No se pudo cargar el archivo. Error: {e}")
        except Exception as e:
            tkinter.messagebox.showerror('Error Desconocido', f"Sucedió un error al intentar reproducir: {e}")


    def ajustar_volumen(self, valor):
        volumen = float(valor)/100
        pygame.mixer.music.set_volume(volumen) 
        
        # Sincronización con el mute
        if volumen > 0 and self.is_muted:
            self.is_muted = False
            self.last_volume = volumen
            self.volume_label.config(text="🔊")
        
        elif volumen == 0 and not self.is_muted:
            self.is_muted = True
            self.volume_label.config(text="🔇")
        elif volumen > 0 and not self.is_muted:
            self.last_volume = volumen # Guardar el último volumen real

    def bloom_submenubar(self):
        tkinter.messagebox.showinfo('Sobre Bloom','!Somos una empresa indie amantes de la musica como vos!. programado por mati je')
 

# --- WIDGETS ---
    def create_widgets(self):
        # Sub-menus (Omitidos por brevedad, son los mismos)
        subMenu = Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='Inicio',menu=subMenu) 
        subMenu.add_command(label='Ir a...')
        subMenu.add_command(label='Cerrar',command=self.root.destroy) 

        subMenu = Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='Importar',menu=subMenu) 
        subMenu.add_command(label='Carpeta', command=self.Importar_Carpeta) 
        subMenu.add_command(label='Musica',command=self.Importar_Musica) 

        subMenu = Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='Bloom',menu=subMenu) 

        subMenu.add_command(label='Nosotros', command=self.bloom_submenubar)
        subMenu.add_command(label='Ayuda')

        # --- TOP CONTROL BAR ---
        self.top_bar_frame = tk.Frame(self.main_frame, bg="white", height=70)
        self.top_bar_frame.pack(side="top", fill="x", pady=(0, 10))
        self.top_bar_frame.pack_propagate(False)

        # Left section of top bar (Playback controls)
        self.playback_controls_frame = tk.Frame(self.top_bar_frame, bg="white")
        self.playback_controls_frame.pack(side="left", padx=10, pady=10)

        self.aleatorio_button2 = tk.Button(self.playback_controls_frame, text="🔀", font=("Helvetica", 14), bg="white", relief="flat")
        self.aleatorio_button2.pack(side="left", padx=5)
        
        # ⭐️ BOTÓN PREVIO ASIGNADO ⭐️
        self.prev_button = tk.Button(self.playback_controls_frame, text="⏮", font=("Helvetica", 14), bg="white", relief="flat", command=self.prev_song)
        self.prev_button.pack(side="left", padx=5)

        self.play_button = tk.Button(self.playback_controls_frame, text="▶", font=("Helvetica", 14), bg="white", relief="flat", command=self.reproducir_musica)
        self.play_button.pack(side="left", padx=5)

        self.pause_button = tk.Button(self.playback_controls_frame, text="⏸️", font=("Helvetica", 14), bg="white", relief="flat", command=self.pausar_musica)
        self.pause_button.pack(side="left", padx=5)

        # ⭐️ BOTÓN SIGUIENTE ASIGNADO ⭐️
        self.next_button = tk.Button(self.playback_controls_frame, text="⏭", font=("Helvetica", 14), bg="white", relief="flat", command=self.next_song)
        self.next_button.pack(side="left", padx=5)
        
        self.bucle_button2 = tk.Button(self.playback_controls_frame, text="🔃​", font=("Helvetica", 14), bg="white", relief="flat")
        self.bucle_button2.pack(side="left", padx=5)

        # Middle section of top bar (Current Song Display & Progress)
        self.current_song_frame = tk.Frame(self.top_bar_frame, bg="white")
        self.current_song_frame.pack(side="left", expand=True, padx=10, pady=10)

        try:
            self.album_cover_small_path = "emiliaMP3Foto.png"
            self.original_image_small = Image.open(self.album_cover_small_path)
            self.resized_image_small = self.original_image_small.resize((40, 40), Image.LANCZOS)
            self.album_cover_small = ImageTk.PhotoImage(self.resized_image_small)
            self.album_label_small = tk.Label(self.current_song_frame, image=self.album_cover_small, bg="white")
            self.album_label_small.pack(side="left", padx=5)
        except FileNotFoundError:
            pass 
            
        self.song_info_frame = tk.Frame(self.current_song_frame, bg="white")
        self.song_info_frame.pack(side="left", padx=5)

        self.song_title_top = tk.Label(self.song_info_frame, text="Beautiful Stranger", font=("Helvetica", 10, "bold"), bg="white", anchor="w")
        self.song_title_top.pack(fill="x")
        
        self.artist_top = tk.Label(self.song_info_frame, text="Laufey - Everything I Know About Love", font=("Helvetica", 8), bg="white", anchor="w")
        self.artist_top.pack(fill="x")

        self.progress_frame = tk.Frame(self.current_song_frame, bg="white")
        self.progress_frame.pack(side="left", fill="x", expand=True, padx=10)

        self.current_time_label = tk.Label(self.progress_frame, font=("Helvetica", 8), bg="white", text="00:00")
        self.current_time_label.pack(side="left")

        # Configuración del Slider
        self.progress_bar = ttk.Scale(self.progress_frame, from_=0, to=100, orient="horizontal", length=200)
        self.progress_bar.set(0) 
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=5)

        # ENLACES DE EVENTOS PARA CONTROL PRECISO DEL SLIDER
        self.progress_bar.bind("<ButtonPress-1>", self.slider_press) 
        self.progress_bar.bind("<Motion>", self.slider_move) 
        self.progress_bar.bind("<ButtonRelease-1>", self.slider_release) 

        self.total_time_label = tk.Label(self.progress_frame, font=("Helvetica", 8), bg="white", text="00:00")
        self.total_time_label.pack(side="left")

        # Right section of top bar (Volume, Queue, Settings)
        self.right_controls_frame = tk.Frame(self.top_bar_frame, bg="white")
        self.right_controls_frame.pack(side="right", padx=10, pady=10)

        self.volume_label = tk.Label(self.right_controls_frame, text="🔊", font=("Helvetica", 14), bg="white")
        self.volume_label.pack(side="left", padx=5)
        # CONEXIÓN DEL LABEL PARA MUTE
        self.volume_label.bind("<Button-1>", self.toggle_mute)
        
        self.volume_scale = ttk.Scale(self.right_controls_frame, from_=0, to=100, orient="horizontal", length=80 ,command=lambda s: self.ajustar_volumen(float(s)))
        self.volume_scale.set(70)
        pygame.mixer.music.set_volume(0.70)
        self.volume_scale.pack(side="left", padx=10)

        self.queue_button = tk.Button(self.right_controls_frame, text="☰", font=("Helvetica", 14), bg="white", relief="flat")
        self.queue_button.pack(side="left", padx=5)

        self.settings_button = tk.Button(self.right_controls_frame, text="⚙️", font=("Helvetica", 14), bg="white", relief="flat")
        self.settings_button.pack(side="left", padx=5)

        # --- Rest of the UI (Sidebar and Main Content) ---
        self.sidebar_frame = tk.Frame(self.main_frame, bg="white", width=250)
        self.sidebar_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.sidebar_frame.pack_propagate(False)

        self.content_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.header_frame = tk.Frame(self.sidebar_frame, bg="white")
        self.header_frame.pack(fill="x", pady=(0, 10))

        self.bloom_label = tk.Label(self.header_frame, text="Bloom Music", font=("Helvetica", 14, "bold"), bg="white")
        self.bloom_label.pack(side="left", padx=10, pady=10)

        self.search_entry = ttk.Entry(self.sidebar_frame, width=30)
        self.search_entry.insert(0, "Buscar")
        self.search_entry.pack(fill="x", padx=10, pady=5)
        
        self.home_button = tk.Button(self.sidebar_frame, text="🏠 Home", font=("Helvetica", 12), bg="#e0e0e0", relief="flat", anchor="w", padx=20)
        self.home_button.pack(fill="x", pady=5)
        
        self.new_button = tk.Button(self.sidebar_frame, text="✨ Nuevo", font=("Helvetica", 12), bg="white", relief="flat", anchor="w", padx=20)
        self.new_button.pack(fill="x", pady=5)
        
        self.radio_button = tk.Button(self.sidebar_frame, text="📻 Radio", font=("Helvetica", 12), bg="white", relief="flat", anchor="w", padx=20)
        self.radio_button.pack(fill="x", pady=5)

        self.library_label = tk.Label(self.sidebar_frame, text="Librería", font=("Helvetica", 10, "bold"), bg="white", anchor="w")
        self.library_label.pack(fill="x", padx=10, pady=(15, 5))

        self.recently_added_button = tk.Button(self.sidebar_frame, text="➕ Añadidos recientemente", font=("Helvetica", 12), bg="white", relief="flat", anchor="w", padx=20)
        self.recently_added_button.pack(fill="x", pady=5)

        self.artists_button = tk.Button(self.sidebar_frame, text="🧑‍🎤 Artistas", font=("Helvetica", 12), bg="white", relief="flat", anchor="w", padx=20)
        self.artists_button.pack(fill="x", pady=5)

        self.albums_button = tk.Button(self.sidebar_frame, text="💿 Álbumes", font=("Helvetica", 12), bg="white", relief="flat", anchor="w", padx=20)
        self.albums_button.pack(fill="x", pady=5)

        self.songs_button = tk.Button(self.sidebar_frame, text="🎵 Canciones", font=("Helvetica", 12), bg="white", relief="flat", anchor="w", padx=20)
        self.songs_button.pack(fill="x", pady=5)

        self.playlists_label = tk.Label(self.sidebar_frame, text="Playlist", font=("Helvetica", 10, "bold"), bg="white", anchor="w")
        self.playlists_label.pack(fill="x", padx=10, pady=(15, 5))

        
        try:
            self.album_cover_path_main = "emiliaMP3Foto.png"
            self.original_image_main = Image.open(self.album_cover_path_main)
            self.resized_image_main = self.original_image_main.resize((200, 200), Image.LANCZOS)
            self.album_cover_main = ImageTk.PhotoImage(self.resized_image_main)
            self.album_label_main = tk.Label(self.content_frame, image=self.album_cover_main)
            self.album_label_main.pack(pady=20)
        except FileNotFoundError:
            self.album_label_main = tk.Label(self.content_frame, text="[Album Cover]", bg="#f0f0f0")
            self.album_label_main.pack(pady=20)
        
        self.song_title = tk.Label(self.content_frame, text="Everything I Know About Love", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        self.song_title.pack()
        
        self.artist_label = tk.Label(self.content_frame, text="Laufey - 2022", font=("Helvetica", 12), bg="#f0f0f0")
        self.artist_label.pack()

        self.player_controls_bottom_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        self.player_controls_bottom_frame.pack(pady=10)
        
        self.play_button_bottom = tk.Button(self.player_controls_bottom_frame, text="▶ Play", font=("Helvetica", 12, "bold"), bg="#CF0A8D", fg="white", relief="flat", padx=20, pady=5, command=self.reproducir_musica)
        self.play_button_bottom.pack(side="left", padx=5)
        
        self.aleatorio_button2 = tk.Button(self.player_controls_bottom_frame, text="🔀 Aleatorio", font=("Helvetica", 12, "bold"), bg="#e0e0e0", relief="flat", padx=20, pady=5)
        self.aleatorio_button2.pack(side="left", padx=5)
        
        self.playlist_frame = tk.Frame(self.content_frame, bg="white")
        self.playlist_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        self.playlistbox = Listbox(self.playlist_frame, 
                                   bg="white", 
                                   font=("Helvetica", 10), 
                                   selectbackground="#adaaaa",
                                   )
        self.playlistbox.pack(fill="both", anchor="w", pady=5)
        
        self.playlist_buttons_frame = Frame(self.playlist_frame)
        self.playlist_buttons_frame.pack()
        
        self.add_song_button = tk.Button(self.playlist_buttons_frame, text="🎵 Añadir Canción", font=("Helvetica", 12), bg="white", relief="flat", anchor="w", padx=20, command=self.Importar_Musica)
        self.add_song_button.pack(side= LEFT, fill="x")
        
        self.add_playlist_button = tk.Button(self.playlist_buttons_frame, text="🎵 Añadir Playlist", font=("Helvetica", 12), bg="white", relief="flat", anchor="w", padx=20, command=self.Importar_Carpeta)
        self.add_playlist_button.pack(side= LEFT, fill="x")
        
        self.del_song_button = tk.Button(self.playlist_buttons_frame, text="X Eliminar Canción", font=("Helvetica", 12), bg="white", relief="flat", anchor="w", padx=20, command=self.del_from_playlist)
        self.del_song_button.pack(side= LEFT,fill="x")


if __name__ == "__main__":
    root = tk.Tk()
    app = Pagina_Principal(root)
    root.mainloop()