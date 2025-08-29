import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
import pygame
import os, sys, time
import requests

#Funciones del MENU


#sub-menu IMPORTAR
def Importar_Musica(): #Importa un archivo wav/mp3 y la hace global para poder reproducirla
    global filename
    filename = filedialog.askopenfilename()


def Importar_Carpeta():
    filename = filedialog.askopenfilename()
    print(filename)


#Pygame
pygame.mixer.init() #Inicializar el reproductor

def retroceder_musica():
    reproducir_musica()
    barra_estado['text'] = 'Rewinded...' + '   -   ' + os.path.basename(filename)

pausa = FALSE #comienza con pausa como FALSO para reiniciarlo

def pausar_musica():
    global pausa
    pausa = TRUE
    pygame.mixer.music.pause()
    barra_estado['text'] = 'En Pausa...' + '   -   ' + os.path.basename(filename)

def reproducir_musica():
    global pausa
    if pausa:
        pygame.mixer.music.unpause()
        barra_estado['text'] = 'Reproduciendo Musica' + '   -   ' + os.path.basename(filename)
        pausa = FALSE
    else:
        try:
            pygame.mixer.music.load(filename)
            #utiliza la variable filename para reproducir la musica que se importo (por ahora)
            pygame.mixer.music.play()
            barra_estado['text'] = 'Reproduciendo Musica' + '   -   ' + os.path.basename(filename)  #barra de estado para mostrar al usuario que se esta ejecutando
        except:
            tkinter.messagebox.showerror('Archivo no encontrado','Bloom no pudo encontrar su archivo. Intentalo de nuevo')
        


def parar_musica():
    pygame.mixer.music.stop()
    barra_estado['text'] = 'Musica Frenada' + '   -   ' + os.path.basename(filename) #barra de estado para mostrar al usuario que se esta ejecutando
    print('Deteniendo la Musica...')

def ajustar_volumen(valor):
    volumen = int(valor)/100
    pygame.mixer.music.set_volume(volumen) #toma el valor desde 0 a 1 (0.01;0.2;0.9;1)

#barra de estado (bienvenida/reproduccion/pausa)
barra_estado = Label(root,text='Bienvenido a Bloom', relief= SUNKEN, anchor=W)
barra_estado.pack(side=BOTTOM, fill=X)

class Pagina_Principal:
    def __init__(self, root):
        self.root = root
        self.root.title("Bloom Music")
        self.root.geometry("1200x800")
        self.root.configure(bg="white")

        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill="both", expand=True)

        self.create_widgets()
    
    



    def create_widgets(self):
        # --- TOP CONTROL BAR ---
        top_bar_frame = tk.Frame(self.main_frame, bg="white", height=70)
        top_bar_frame.pack(side="top", fill="x", pady=(0, 10))
        top_bar_frame.pack_propagate(False)

        # Left section of top bar (Playback controls)
        playback_controls_frame = tk.Frame(top_bar_frame, bg="white")
        playback_controls_frame.pack(side="left", padx=10, pady=10)

        aleatorio_button2 = tk.Button(playback_controls_frame, text="🔀", font=("Helvetica", 14), bg="white", relief="flat")
        aleatorio_button2.pack(side="left", padx=5)
        
        prev_button = tk.Button(playback_controls_frame, text="⏮", font=("Helvetica", 14), bg="white", relief="flat")
        prev_button.pack(side="left", padx=5)

        play_pause_button = tk.Button(playback_controls_frame, text="▶", font=("Helvetica", 14), bg="white", relief="flat",command=pausar_musica)
        play_pause_button.pack(side="left", padx=5)

        next_button = tk.Button(playback_controls_frame, text="⏭", font=("Helvetica", 14), bg="white", relief="flat")
        next_button.pack(side="left", padx=5)
        
        bucle_button2 = tk.Button(playback_controls_frame, text="🔃​", font=("Helvetica", 14), bg="white", relief="flat")
        bucle_button2.pack(side="left", padx=5)

        # Middle section of top bar (Current Song Display & Progress)
        current_song_frame = tk.Frame(top_bar_frame, bg="white")
        current_song_frame.pack(side="left", expand=True, padx=20, pady=10)

        try:
            album_cover_small_path = "path/to/your/album_cover.png"
            original_image_small = Image.open(album_cover_small_path)
            resized_image_small = original_image_small.resize((40, 40), Image.LANCZOS)
            self.album_cover_small = ImageTk.PhotoImage(resized_image_small)
            album_label_small = tk.Label(current_song_frame, image=self.album_cover_small, bg="white")
            album_label_small.pack(side="left", padx=5)
        except FileNotFoundError:
            print("Small album cover image not found. Please provide a valid path.")
            
        song_info_frame = tk.Frame(current_song_frame, bg="white")
        song_info_frame.pack(side="left", padx=5)

        song_title_top = tk.Label(song_info_frame, text="Beautiful Stranger", font=("Helvetica", 10, "bold"), bg="white", anchor="w")
        song_title_top.pack(fill="x")
        
        artist_top = tk.Label(song_info_frame, text="Laufey - Everything I Know About Love", font=("Helvetica", 8), bg="white", anchor="w")
        artist_top.pack(fill="x")

        progress_frame = tk.Frame(current_song_frame, bg="white")
        progress_frame.pack(side="left", fill="x", expand=True, padx=10)

        current_time_label = tk.Label(progress_frame, text="0:30", font=("Helvetica", 8), bg="white")
        current_time_label.pack(side="left")

        progress_bar = ttk.Scale(progress_frame, from_=0, to=100, orient="horizontal", length=200)
        progress_bar.set(25)
        progress_bar.pack(side="left", fill="x", expand=True, padx=5)

        total_time_label = tk.Label(progress_frame, text="3:00", font=("Helvetica", 8), bg="white")
        total_time_label.pack(side="left")

        # Right section of top bar (Volume, Queue, Settings)
        right_controls_frame = tk.Frame(top_bar_frame, bg="white")
        right_controls_frame.pack(side="right", padx=10, pady=10)

        volume_label = tk.Label(right_controls_frame, text="🔊", font=("Helvetica", 14), bg="white")
        volume_label.pack(side="left", padx=5)
        
        volume_scale = ttk.Scale(right_controls_frame, from_=0, to=100, orient="horizontal", length=80)
        volume_scale.set(70)
        volume_scale.pack(side="left", padx=5)

        queue_button = tk.Button(right_controls_frame, text="☰", font=("Helvetica", 14), bg="white", relief="flat")
        queue_button.pack(side="left", padx=5)

        settings_button = tk.Button(right_controls_frame, text="⚙️", font=("Helvetica", 14), bg="white", relief="flat")
        settings_button.pack(side="left", padx=5)

        # --- Rest of the UI (Sidebar and Main Content) ---
        sidebar_frame = tk.Frame(self.main_frame, bg="white", width=250)
        sidebar_frame.pack(side="left", fill="y", padx=10, pady=10)
        sidebar_frame.pack_propagate(False)

        content_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        header_frame = tk.Frame(sidebar_frame, bg="white")
        header_frame.pack(fill="x", pady=(0, 10))

        bloom_label = tk.Label(header_frame, text="Bloom Music", font=("Helvetica", 14, "bold"), bg="white")
        bloom_label.pack(side="left", padx=10, pady=10)

        search_entry = ttk.Entry(sidebar_frame, width=30)
        search_entry.insert(0, "Buscar")
        search_entry.pack(fill="x", padx=10, pady=5)
        
        home_button = tk.Button(sidebar_frame, text="🏠 Home", font=("Helvetica", 12), bg="#e0e0e0", relief="flat", anchor="w", padx=20)
        home_button.pack(fill="x", pady=5)
        
        new_button = tk.Button(sidebar_frame, text="✨ Nuevo", font=("Helvetica", 12), bg="white", relief="flat", anchor="w", padx=20)
        new_button.pack(fill="x", pady=5)
        
        radio_button = tk.Button(sidebar_frame, text="📻 Radio", font=("Helvetica", 12), bg="white", relief="flat", anchor="w", padx=20)
        radio_button.pack(fill="x", pady=5)

        library_label = tk.Label(sidebar_frame, text="Librería", font=("Helvetica", 10, "bold"), bg="white", anchor="w")
        library_label.pack(fill="x", padx=10, pady=(15, 5))

        recently_added_button = tk.Button(sidebar_frame, text="➕ Añadidos recientemente", font=("Helvetica", 12), bg="white", relief="flat", anchor="w", padx=20)
        recently_added_button.pack(fill="x", pady=5)

        artists_button = tk.Button(sidebar_frame, text="🧑‍🎤 Artistas", font=("Helvetica", 12), bg="white", relief="flat", anchor="w", padx=20)
        artists_button.pack(fill="x", pady=5)

        albums_button = tk.Button(sidebar_frame, text="💿 Álbumes", font=("Helvetica", 12), bg="white", relief="flat", anchor="w", padx=20)
        albums_button.pack(fill="x", pady=5)

        songs_button = tk.Button(sidebar_frame, text="🎵 Canciones", font=("Helvetica", 12), bg="white", relief="flat", anchor="w", padx=20)
        songs_button.pack(fill="x", pady=5)

        playlists_label = tk.Label(sidebar_frame, text="Playlist", font=("Helvetica", 10, "bold"), bg="white", anchor="w")
        playlists_label.pack(fill="x", padx=10, pady=(15, 5))

        try:
            album_cover_path_main = "path/to/your/album_cover.png"
            original_image_main = Image.open(album_cover_path_main)
            resized_image_main = original_image_main.resize((300, 300), Image.LANCZOS)
            self.album_cover_main = ImageTk.PhotoImage(resized_image_main)
            album_label_main = tk.Label(content_frame, image=self.album_cover_main)
            album_label_main.pack(pady=20)
        except FileNotFoundError:
            print("Main album cover image not found. Please provide a valid path.")
            album_label_main = tk.Label(content_frame, text="[Album Cover]")
            album_label_main.pack(pady=20)
            
        song_title = tk.Label(content_frame, text="Everything I Know About Love", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        song_title.pack()
        
        artist_label = tk.Label(content_frame, text="Laufey - 2022", font=("Helvetica", 12), bg="#f0f0f0")
        artist_label.pack()

        player_controls_bottom_frame = tk.Frame(content_frame, bg="white")
        player_controls_bottom_frame.pack(pady=10)
        
        play_button_bottom = tk.Button(player_controls_bottom_frame, text="▶ Play", font=("Helvetica", 12, "bold"), bg="#FF69B4", fg="white", relief="flat", padx=20, pady=5)
        play_button_bottom.pack(side="left", padx=5)
        
        aleatorio_button2 = tk.Button(player_controls_bottom_frame, text="🔀 Aleatorio", font=("Helvetica", 12, "bold"), bg="#e0e0e0", relief="flat", padx=20, pady=5)
        aleatorio_button2.pack(side="left", padx=5)
        
        playlist_frame = tk.Frame(content_frame, bg="white")
        playlist_frame.pack(fill="both", expand=True, pady=(20, 0))
        
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
            song_frame = tk.Frame(playlist_frame, bg="white")
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