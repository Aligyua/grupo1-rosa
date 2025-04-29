# punto 1
class Sombrero:
  Ravenclaw = 0
  Griffindor = 0
  Slytherin = 0
  Hufflepuff = 0
  def __init__(self, diccionario):
    self.diccionario = diccionario

  def preguntas(self):
    diccionario= self.diccionario.keys()

  def sumarPuntos(self):
    for elem in self.diccionario:
      print (elem)
      respuesta = input("Ingresar el número de respuesta: ")
      if respuesta == 1 :
        Ravenclaw= self.Ravenclaw + 5
      if respuesta == 2 :
        Griffindor= self.Griffindor + 1
      if respuesta == 3 :
        Slytherin= self.Slytherin + 3
      if respuesta == 4 :
        Hufflepuff= self.Hufflepuff + 2

  def decirCasa(self):
    if self.Ravenclaw > self.Griffindor and self.Ravenclaw > self.Slytherin and self.Ravenclaw > self.Hufflepuff:
      print("La casa es Ravenclaw")
    if self.Griffindor > self.Ravenclaw and self.Griffindor > self.Slytherin and self.Griffindor > self.Hufflepuff:
      print("La casa es Griffindor")
    if self.Slytherin > self.Ravenclaw and self.Slytherin > self.Griffindor and self.Slytherin > self.Hufflepuff:
      print("La casa es Slytherin")
    if self.Hufflepuff > self.Ravenclaw and self.Hufflepuff > self.Griffindor and self.Hufflepuff > self.Slytherin:
      print("La casa es Hufflepuff")

sombrero= Sombrero({"Que mascota preferis":[0,1,2,3]})

sombrero.sumarPuntos() # lo intentamos :)

# punto 2

class Partida:
  jugador1 = 0
  jugador2 = 0
  empate = 0
  def __init__(self, diccionario):
    self.diccionario = diccionario
    
  def rondas(self):
    diccionario= self.diccionario.keys()

  def sumarPuntos(self):
    jugador1 = input("Ingresar el valor: ")
    jugador2 = input("Ingresar el valor: ")
    if jugador1 == "piedra" and jugador2 == "papel":
      jugador2 = self.jugador2 + 1
    if jugador1 == "piedra" and jugador2 == "tijera":
      jugador1 = self.jugador1 + 1
    if jugador1 == "piedra" and jugador2 == "spock":
      jugador2 = self.jugador2 + 1
    if jugador1 == "piedra" and jugador2 == "lagarto":
      jugador1 = self.jugador1 + 1

    if jugador1 == "papel" and jugador2 == "spock":
      jugador1 = self.jugador1 + 1
    if jugador1 == "papel" and jugador2 == "piedra":
      jugador1 = self.jugador1 + 1
    if jugador1 == "papel" and jugador2 == "tijera":
      jugador2 = self.jugador2 + 1
    if jugador1 == "papel" and jugador2 == "lagarto":
      jugador2 = self.jugador2 + 1

    if jugador1 == "spock" and jugador2 == "piedra":
      jugador2 = self.jugador2 + 1
    if jugador1 == "spock" and jugador2 == "tijera":
      jugador1 = self.jugador1 + 1
    if jugador1 == "spock" and jugador2 == "papel":
      jugador2 = self.jugador2 + 1
    if jugador1 == "spock" and jugador2 == "lagarto":
      jugador2 = self.jugador2 + 1

    if jugador1 == "tijera" and jugador2 == "lagarto":
      jugador1 = self.jugador1 + 1
    if jugador1 == "tijera" and jugador2 == "piedra":
      jugador2 = self.jugador2 + 1
    if jugador1 == "tijera" and jugador2 == "spock":
      jugador2 = self.jugador2 + 1
    if jugador1 == "tijera" and jugador2 == "papel":
      jugador1 = self.jugador1 + 1

    if jugador1 == "lagarto" and jugador2 == "spock":
      jugador1 = self.jugador1 + 1
    if jugador1 == "lagarto" and jugador2 == "piedra":
      jugador2 = self.jugador2 + 1
    if jugador1 == "lagarto" and jugador2 == "papel":
      jugador1 = self.jugador1 + 1
    if jugador1 == "lagarto" and jugador2 == "tijera":
      jugador2 = self.jugador2 + 1
    
    if jugador1 == jugador2:
      empate = self.empate + 1

# punto 3
class Tennis:
  jugador1 = 0
  jugador2 = 0

  def __init__(self, secuencia):
    self.secuencia = secuencia

  def juego(self):
    secuencia= self.secuencia.keys()

  def sumarPuntos(self):
    puntos= [input("Ingresar la secuencia de puntos, separado por comas: ")]
    while True:
      for elem in puntos:
        if elem=="P1":
          jugador1 = self.jugador1 + 1
        
        if elem=="P2":
          jugador2= self.jugador2 + 1

        if jugador2>=3 and jugador1>=3:
          if elem=="P1":
            jugador1 = self.jugador1 + 1

          if elem=="P2":
            jugador2= self.jugador2 + 1
            
          if jugador2>jugador1+1:
            print("Gana el jugador 2")
            break
          if jugador1>jugador2+1:
            print("Gana el jugador 1")
            break
      break

# punto 4

juegos= {"Ocarina of time": 1998, "Majora's Mask": 2000, "Four Swords": 2003, "The Wind Waker": 2003, "The Minish Cap" : 2004, "Twilight Princess": 2006, "Phantom Hourglass": 2007,"Spirit Tracks" : 2009, "Skyward Sword": 2011, "A Link to the Past": 2013, " Tri Force Heroes" : 2015, "Breath of the Wild": 2017, "Tears of the Kingdom": 2019, "Link's Awakening" : 2019, "Echoes of Wisdom" : 2024}

print (juegos)
juego1= input("Ingresar el nombre del juego: ")
juego2= input("Ingresar el nombre del juego: ")
  
cuenta = abs(juegos[juego1] - juegos[juego2])
print("La diferencia de años entre los juegos es: ", cuenta)
