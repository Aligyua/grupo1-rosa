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
        
        #ESTADO PAUSA Y DEMAS
        self.pausa = FALSE
        self.en_reproduccion = FALSE
        self.playlist = []

        #barra de estado (bienvenida/reproduccion/pausa)
        self.barra_estado = tk.Label(root,text='Bienvenido a Bloom', relief= SUNKEN)
        self.barra_estado.pack(side=BOTTOM, fill=X)
        #MENU CREAR TOOLBAR
        
        
        #Menu Bar
        self.menubar = menubar = Menu(root)
        self.root.config(menu=menubar) #Lo prepara para los submenus que se le pueden agregar con add_cascade y tambien mantiene este menu arriba de todo

        self.create_widgets()
    #Funciones del MENU

    

#sub-menu IMPORTAR
    def Importar_Musica(self): #Importa un archivo wav/mp3 y la hace global para poder reproducirla
        global filename
        filename = filedialog.askopenfilename()
        self.add_to_playlist(filename)


    def Importar_Carpeta(self):
        filename = filedialog.askopenfilename()
        print(filename)

    def add_to_playlist(self,file):
        
        file = os.path.basename(file)
        if file == "":
             tkinter.messagebox.showerror('Archivo no encontrado','Bloom no pudo encontrar su archivo. Intentalo de nuevo')
        index = 0 #es el valor que va a tener dentro de la lista cuando agregue la cancion
        self.playlistbox.insert(index, file)
        self.playlist.insert(index,filename)
        index += 1
           
    
    def del_from_playlist(self):
        cancion_seleccionada = self.playlistbox.curselection()
        cancion_seleccionada = int(cancion_seleccionada[0])
        self.playlistbox.delete(cancion_seleccionada)
    #Pygame
    pygame.mixer.init() #Inicializar el reproductor

    def slider_barra_progreso_cancion(self,event):
        valor_actual_slider = self.progress_bar.get()
        pygame.mixer.music.seek_to(valor_actual_slider)



    def cancion_actual_reproduciendose(self,cancion):
        datos_archivo = os.path.splitext(cancion)
        if datos_archivo[1] == '.mp3':
            audio = MP3(cancion)
            duracion_total = audio.info.length
        else:
            audio = pygame.mixer.Sound(cancion)
            duracion_total = audio.get_length()
        
        #TITULO MAIN
        self.song_title ['text'] = os.path.basename(cancion)
#Representacion en minutos/segundos del total
        mins, secs = divmod(duracion_total, 60)
        mins= round(mins)
        secs= round(secs)
        formato_tiempo = '{:02d}:{:02d}'.format(mins,secs)
        self.total_time_label['text'] = formato_tiempo

        tiempothreading = threading.Thread(target=self.comenzar_temporizador, args=(duracion_total,))
        tiempothreading.start()

    def retroceder_musica(self):
        try:
            pygame.mixer.music.load(filename)
            #utiliza la variable filename para reproducir la musica que se importo (por ahora)
            pygame.mixer.music.play()
            self.barra_estado['text'] = 'Reproduciendo Musica' + '   -   ' + os.path.basename(filename)  #barra de estado para mostrar al usuario que se esta ejecutando
        except:
                tkinter.messagebox.showerror('Archivo no encontrado','Bloom no pudo encontrar su archivo. Intentalo de nuevo')
        self.barra_estado['text'] = 'Rewinded...' + '   -   ' + os.path.basename(filename)

    pausa = FALSE #comienza con pausa como FALSO para reiniciarlo

    #------------------------------------
#------------DATOS DE CANCION
#------------------------------------
    def mostrar_datos_musica(self,cancion):
        self.song_title_top['text'] = 'Reproduciendo' + ' - ' + os.path.basename(cancion)

        datos_archivo = os.path.splitext(cancion)

        if datos_archivo[1] == '.mp3':
            audio = MP3(cancion)
            duracion_total = audio.info.length
        else:
            audio = pygame.mixer.Sound(cancion)
            duracion_total = audio.get_length()
        
        #TITULO MAIN
        self.song_title ['text'] = os.path.basename(cancion)
#Representacion en minutos/segundos del total
        mins, secs = divmod(duracion_total, 60)
        mins= round(mins)
        secs= round(secs)
        formato_tiempo = '{:02d}:{:02d}'.format(mins,secs)
        self.total_time_label['text'] = formato_tiempo

        tiempothreading = threading.Thread(target=self.comenzar_temporizador, args=(duracion_total,))
        tiempothreading.start()

    def comenzar_temporizador(self,tiempo):
        contador_musica_actual = 0
    # pygame.mixer.music.get_busy() da resultado FALSE cuando paramos la musica
        while contador_musica_actual <= tiempo and pygame.mixer.music.get_busy():
            if self.pausa:
                continue
            else:
                mins, secs = divmod(contador_musica_actual, 60)
                mins= round(mins)
                secs= round(secs)
                formato_tiempo = '{:02d}:{:02d}'.format(mins,secs)
                time.sleep(1)
                contador_musica_actual +=1
                self.current_time_label['text'] = formato_tiempo



    def pausar_musica(self):
        if self.en_reproduccion == TRUE:
            self.pausa = TRUE
            self.en_reproduccion = FALSE
            pygame.mixer.music.pause()
            self.barra_estado['text'] = 'En Pausa...' + '   -   ' + os.path.basename(filename)
    def parar_musica(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.get_busy()
    
        

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------- EN PROCESO PARA CREAR UNA OPCION DE PAUSA REPRODUCIR EN UN SOLO BOTON-----------
#----------------------------------------------------------------------------------------------------------------------------------
    def toggleplaypause(self):
        if self.pausa:
            pygame.mixer.music.unpause()
            self.barra_estado['text'] = 'Reproduciendo Musica' + '   -   ' + os.path.basename(filename)
            self.en_reproduccion = TRUE
            self.pausa = FALSE
            try:
                pygame.mixer.music.load(filename)
                #utiliza la variable filename para reproducir la musica que se importo (por ahora)
                pygame.mixer.music.play()
                self.en_reproduccion = TRUE
                self.barra_estado['text'] = 'Reproduciendo Musica' + '   -   ' + os.path.basename(filename)  #barra de estado para mostrar al usuario que se esta ejecutando
            except:
                tkinter.messagebox.showerror('Archivo no encontrado','Bloom no pudo encontrar su archivo. Intentalo de nuevo')
        else:
            self.pausar_musica()
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------

    def reproducir_musica(self):
        if self.pausa:
            pygame.mixer.music.unpause()
            self.barra_estado['text'] = 'Reproduciendo Musica' + '   -   ' + os.path.basename(filename)
            self.en_reproduccion = TRUE
            self.pausa = FALSE
        else:
            
            try:
                self.parar_musica()
                #para la playlist esta parte
                cancion_seleccionada = self.playlistbox.curselection()
                cancion_seleccionada = int(cancion_seleccionada[0]) # te da el numero de la lista en int
                reproducir_cancion = self.playlist[cancion_seleccionada] # Te trae la direccion de la cancion
                pygame.mixer.music.load(reproducir_cancion)
                #utiliza la variable filename para reproducir la musica que se importo (por ahora)
                pygame.mixer.music.play()
                self.en_reproduccion = TRUE
                self.barra_estado['text'] = 'Reproduciendo Musica' + '   -   ' + os.path.basename(reproducir_cancion)
                self.mostrar_datos_musica(reproducir_cancion)  #barra de estado para mostrar al usuario que se esta ejecutando
                self.cancion_actual_reproduciendose(reproducir_cancion)
            except:
                tkinter.messagebox.showerror('Archivo no encontrado','Bloom no pudo encontrar su archivo. Intentalo de nuevo')
        


    def parar_musica(self):
        pygame.mixer.music.stop()
        self.barra_estado['text'] = 'Musica Frenada' + '   -   ' + os.path.basename(filename) #barra de estado para mostrar al usuario que se esta ejecutando
        print('Deteniendo la Musica...')

    def ajustar_volumen(self,valor):

        volumen = int(valor)/100
        pygame.mixer.music.set_volume(volumen) #toma el valor desde 0 a 1 (0.01;0.2;0.9;1)

    #sub-menu NOSOTROS
    def bloom_submenubar(self):
        tkinter.messagebox.showinfo('Sobre Bloom','!Somos una empresa indie amantes de la musica como vos!. programado por mati je')
  


    
    




    def create_widgets(self):
        #Sub-menus
        subMenu = Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='Inicio',menu=subMenu) #Esta dentro del Menu y categorizado como un sub-menu

        subMenu.add_command(label='Ir a...') #Esta dentro del sub menu llamado "subMenu"
        subMenu.add_command(label='Cerrar',command=self.root.destroy) #Esta dentro del sub menu llamado "subMenu" ejecuta el comando root.destroy para cerrar la app

        subMenu = Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='Importar',menu=subMenu) #Esta dentro del Menu y categorizado como un sub-menu
        subMenu.add_command(label='Carpeta', command=self.Importar_Carpeta) #Esta dentro del sub menu llamado "subMenu" y ejecuta el comando para buscar carpetas con mp3/wav
        subMenu.add_command(label='Musica',command=self.Importar_Musica) #Esta dentro del sub menu llamado "subMenu" importa musica wav/mp3 en tu dispositivo

        subMenu = Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='Bloom',menu=subMenu) #Esta dentro del Menu y categorizado como un sub-menu

        subMenu.add_command(label='Nosotros', command=self.bloom_submenubar) #Esta dentro del sub menu llamado "subMenu" presentacion/info de bloom al usuario dentro de la app
        subMenu.add_command(label='Ayuda') #Esta dentro del sub menu llamado "subMenu"

        # --- TOP CONTROL BAR ---
        self.top_bar_frame = tk.Frame(self.main_frame, bg="white", height=70)
        self.top_bar_frame.pack(side="top", fill="x", pady=(0, 10))
        self.top_bar_frame.pack_propagate(False)

        # Left section of top bar (Playback controls)
        self.playback_controls_frame = tk.Frame(self.top_bar_frame, bg="white")
        self.playback_controls_frame.pack(side="left", padx=10, pady=10)

        self.aleatorio_button2 = tk.Button(self.playback_controls_frame, text="🔀", font=("Helvetica", 14), bg="white", relief="flat")
        self.aleatorio_button2.pack(side="left", padx=5)
        
        self.prev_button = tk.Button(self.playback_controls_frame, text="⏮", font=("Helvetica", 14), bg="white", relief="flat", command=self.retroceder_musica)
        self.prev_button.pack(side="left", padx=5)

        self.play_button = tk.Button(self.playback_controls_frame, text="▶", font=("Helvetica", 14), bg="white", relief="flat", command=self.reproducir_musica)
        self.play_button.pack(side="left", padx=5)

        self.pause_button = tk.Button(self.playback_controls_frame, text="⏸️", font=("Helvetica", 14), bg="white", relief="flat", command=self.pausar_musica)
        self.pause_button.pack(side="left", padx=5)

        self.next_button = tk.Button(self.playback_controls_frame, text="⏭", font=("Helvetica", 14), bg="white", relief="flat")
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
            print("Small album cover image not found. Please provide a valid path.")
            
        self.song_info_frame = tk.Frame(self.current_song_frame, bg="white")
        self.song_info_frame.pack(side="left", padx=5)

        self.song_title_top = tk.Label(self.song_info_frame, text="Beautiful Stranger", font=("Helvetica", 10, "bold"), bg="white", anchor="w")
        self.song_title_top.pack(fill="x")
        
        self.artist_top = tk.Label(self.song_info_frame, text="Laufey - Everything I Know About Love", font=("Helvetica", 8), bg="white", anchor="w")
        self.artist_top.pack(fill="x")

        self.progress_frame = tk.Frame(self.current_song_frame, bg="white")
        self.progress_frame.pack(side="left", fill="x", expand=True, padx=10)

        self.current_time_label = tk.Label(self.progress_frame, font=("Helvetica", 8), bg="white")
        self.current_time_label.pack(side="left")

        self.progress_bar = ttk.Scale(self.progress_frame, from_=0, to=100, orient="horizontal", length=200, command=lambda s: self.cancion_actual_reproduciendose(float(s)))
        self.progress_bar.set(25)
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=5)

        self.total_time_label = tk.Label(self.progress_frame, font=("Helvetica", 8), bg="white")
        self.total_time_label.pack(side="left")

        # Right section of top bar (Volume, Queue, Settings)
        self.right_controls_frame = tk.Frame(self.top_bar_frame, bg="white")
        self.right_controls_frame.pack(side="right", padx=10, pady=10)

        self.volume_label = tk.Label(self.right_controls_frame, text="🔊", font=("Helvetica", 14), bg="white")
        self.volume_label.pack(side="left", padx=5)
        
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
            print("Main album cover image not found. Please provide a valid path.")
            self.album_label_main = tk.Label(self.content_frame, text="[Album Cover]")
            self.album_label_main.pack(pady=20)
        
        #TITULO MUSICA EN REPRODUCCION
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
        
        #-------------------------------------------------------------
        #-------------------PLAYLISTBOX------------------------------
        #------------------------------------------------------------
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
        self.del_song_button = tk.Button(self.playlist_buttons_frame, text="X Eliminar Canción", font=("Helvetica", 12), bg="white", relief="flat", anchor="w", padx=20, command=self.del_from_playlist)
        self.del_song_button.pack(side= LEFT,fill="x")

        songs = [
            ("Fragile", "3:00"), 
            ("Beautiful Stranger", "3:00"), 
            ("Valentina", "3:00"), 
            ("Above the Chinese Restaurant", "3:00"), 
            ("Dear Soulmate", "3:00"),
            ("What Love Will Do To You", "3:00"),
            ("I've Never Been in Love Before", "3:00"),
            ("Just Like Chet", "3:00"),
            ("Everything I Know About Love", "3:00")
        ]
        for i, (song, duration) in enumerate(songs):
            song_frame = tk.Frame(self.playlist_frame, bg="white")
            if song == "Beautiful Stranger":
                song_frame.configure(bg="#e0e0e0")
            song_frame.pack(fill="x", pady=2)
            
            song_num = tk.Label(song_frame, text=f"{i+1}", font=("Helvetica", 10), bg=song_frame.cget("bg"), width=3, anchor="e")
            song_num.pack(side="left", padx=10)
            
            song_name = tk.Label(song_frame, text=song, font=("Helvetica", 10), bg=song_frame.cget("bg"), anchor="w")
            song_name.pack(side="left", fill="x", expand=True)
            
            song_duration = tk.Label(song_frame, text=duration, font=("Helvetica", 10), bg=song_frame.cget("bg"), width=5, anchor="e")
            song_duration.pack(side="right", padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = Pagina_Principal(root)
    root.mainloop()