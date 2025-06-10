#1
class Dia:
  calendario = {1:"premio1", 2:"premio2", 3:"premio3", 4:"premio4", 5:"premio5", 6:"premio6", 7:"premio7", 8:"premio8", 9:"premio9", 10: "premio10", 11:"premio11", 12:"premio12", 13:"premio13", 14:"premio14", 15:"premio15", 16:"premio16", 17:"premio17", 18:"premio18", 19:"premio19", 20:"premio20", 21:"premio21", 22:"premio22", 23:"premio23", 24:"premio24", 25:"premio25"}
  
  def __init__(self, dia, mes, ano):
    self.dia = dia
    self.mes = mes
    self.ano = ano
    

  def RegaloDelDia(self):
    
    if self.mes == 12 and self.ano == 24:
      print(self.calendario[self.dia])
    else:
      print("No hay regalo para hoy")
    hora= int(input("Ingrese la hora: "))
    if hora< 24:
      hora= 24- hora
      print("Faltan", hora, "para abrir el regalo")

  def FechaAnterior(self):
    fechames=0
    fechaño=0
    
    if self.mes != 12 and self.mes < 12:
      fechames= 12- self.mes
      
    if self.ano != 24 and self.ano < 24:
      fechaño= 24- self.ano
    
    print("Faltan", fechames, "meses y ", fechaño ," para el regalo")

  def FechaPosterior(self):
    fechames=0
    fechaño=0

    if self.mes != 12 and self.mes < 12:
      fechames=self.mes

    if self.ano != 24 and self.ano > 24:
      fechaño= 24- self.ano

    print("Pasaron", fechames, "mes(es) y ", fechaño ,"año(s) para el regalo")

hoy=Dia(1,12,24)
hoy.RegaloDelDia()

#2
class Handle:
  Hashtag= 0
  Estudiante=0
  usuario=0
  def __init__(self, url):
    self.url= url

  def ContarHandles(self):
    for i in self.url:
      if i == "#":
        self.Hashtag+=1
      if i == "$":
        self.Estudiante+=1
      if i == "@ ":
        self.usuario+=1

    print("Hashtags: ", self.Hashtag, "Estudiantes: ", self.Estudiante, "Usuarios: ", self.usuario)

#3
class Persona:
  def __init__(self, nombre, edad, altura):
    self.nombre= nombre
    self.edad= edad
    self.altura= altura

class TrucoTrato:
  susto= 0
  dulces= 0


  
  def Truco(self, Persona):
    nombre= Persona.nombre
    edad= Persona.edad
    altura= Persona.altura
    contadorsustos=self.susto

    #nombre
    contadornombre=len(Persona.nombre)
    if contadornombre >= 2:
      contadorsustos = contadornombre/2 
    
    #edad
    paredad=edad.split()
    for x in paredad:
      if x%2 ==0:
        contadorsustos= contadorsustos+1
        
    #altura
    if altura%100>=1:
      contadorsustos= (altura%100)*3
    
    print("La cantidad de sustos que vas a tener son de ", contadorsustos, "🎃 👻 💀 🕷 🕸 🦇")

  def Dulce(self, Persona):
    nombre= Persona.nombre
    edad= Persona.edad
    altura= Persona.altura
    contadordulces=self.dulces
    
    #nombre
    contadornombre=len(Persona.nombre)
    contadordulces = contadornombre

    #edad
    if Persona.edad/3 < 3:
      contadordulces= contadordulces * Persona.edad/3
    else: 
      contadordulces= contadordulces + 3

    #altura
    if Persona.altura < 150:
      contadordulces= contadordulces * Persona.Altura/50
    else: 
       contadordulces= contadordulces + 6

damian= Persona("Damian", 18, 175)