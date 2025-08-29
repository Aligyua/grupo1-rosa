#PARA ACTIVAR EN WINDOWS .venv es ".venv\Scripts\Activate" mientras que para
# desactivarlo solo escribir deactivate
#Para linux es "source .venv/bin/activate" idem windows
#para las librerias ejecutar "pip install" con los siguientes: "requests"; "pygame"

from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
import pygame
import os, sys, time
import requests

root = Tk()




#Ventana Tkinter
root.title("Bloom's Music Player")
root.geometry("800x600")

#Funciones del MENU


#sub-menu IMPORTAR
def Importar_Musica(): #Importa un archivo wav/mp3 y la hace global para poder reproducirla
    global filename
    filename = filedialog.askopenfilename()


def Importar_Carpeta():
    filename = filedialog.askopenfilename()
    print(filename)



#sub-menu NOSOTROS
def bloom_submenubar():
    tkinter.messagebox.showinfo('Sobre Bloom','!Somos una empresa indie amantes de la musica como vos!. programado por mati je')
    

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

#Menu Bar
menubar = Menu(root)
root.config(menu=menubar) #Lo prepara para los submenus que se le pueden agregar con add_cascade y tambien mantiene este menu arriba de todo

#Sub-menus
subMenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Inicio',menu=subMenu) #Esta dentro del Menu y categorizado como un sub-menu

subMenu.add_command(label='Ir a...') #Esta dentro del sub menu llamado "subMenu"
subMenu.add_command(label='Cerrar',command=root.destroy) #Esta dentro del sub menu llamado "subMenu" ejecuta el comando root.destroy para cerrar la app

subMenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Importar',menu=subMenu) #Esta dentro del Menu y categorizado como un sub-menu
subMenu.add_command(label='Carpeta', command=Importar_Carpeta) #Esta dentro del sub menu llamado "subMenu" y ejecuta el comando para buscar carpetas con mp3/wav
subMenu.add_command(label='Musica',command=Importar_Musica) #Esta dentro del sub menu llamado "subMenu" importa musica wav/mp3 en tu dispositivo

subMenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Bloom',menu=subMenu) #Esta dentro del Menu y categorizado como un sub-menu

subMenu.add_command(label='Nosotros', command=bloom_submenubar) #Esta dentro del sub menu llamado "subMenu" presentacion/info de bloom al usuario dentro de la app
subMenu.add_command(label='Ayuda') #Esta dentro del sub menu llamado "subMenu"

#FRAMES

#frame medio
frame_medio = Frame(root, relief=RAISED, borderwidth=1)
frame_medio.pack()

#Bienvenida Texto
texto = Label(root, text = 'Bienvenido a el Reproductor mas Copado')
texto.pack()

#Imagenes para los botones Bloom
reproducir_photo = PhotoImage(file='imagenes/boton_reproducir64px.png')
parar_photo = PhotoImage(file='imagenes/boton_parar64px.png')
pausar_photo = PhotoImage(file='imagenes/boton_pausa64px.png')
atras_photo = PhotoImage(file='imagenes/boton_atras64px.png')

#Boton de retroceder musica
boton_retroceder_musica = Button(frame_medio, image=atras_photo, command=retroceder_musica)
boton_retroceder_musica.pack(side=LEFT, padx=10)

#Boton de reproducir musica
boton_reproducir_musica = Button(frame_medio, image=reproducir_photo, command=reproducir_musica)
boton_reproducir_musica.pack(side=LEFT, padx=10)


#Boton de parar musica
boton_parar_musica = Button(frame_medio, image=parar_photo, command=parar_musica)
boton_parar_musica.pack(side=LEFT, padx=10)

#Boton de PAUSAR musica
boton_pausa_musica = Button(frame_medio, image=pausar_photo, command=pausar_musica)
boton_pausa_musica.pack(side=LEFT, padx=10)


#Escala de volumen
escala_volumetrica = Scale (root, from_=0, to=100, orient=HORIZONTAL, command=ajustar_volumen)
escala_volumetrica.set(50)
pygame.mixer.music.set_volume(0.50)
escala_volumetrica.pack()


#barra de estado (bienvenida/reproduccion/pausa)
barra_estado = Label(root,text='Bienvenido a Bloom', relief= SUNKEN, anchor=W)
barra_estado.pack(side=BOTTOM, fill=X)

root.mainloop()