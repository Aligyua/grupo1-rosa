class Plato:
  def __init__(self, nombreP, tipo, peso):
   self.nombreP = nombreP
   self.tipo = tipo
   self.peso = peso

class Equipos(Plato):

  def __init__(self, nombre, platosFuertes,colorEquipo,puntajeCocinero,cantIntegrantes):
    self.nombre = nombre
    self.platosFuertes = []
    self.colorEquipo = colorEquipo
    self.puntajeCocinero = puntajeCocinero
    self.cantIntegrantes = cantIntegrantes



class Hellskitchen(Equipos,Plato):
  contadorAzul=0
  contadorRojo=0
  
  def __init__(self,equipoRojo, equipoAzul):
    
    self.equipoRojo = equipoRojo
    self.equipoAzul = equipoAzul

  def equipoGanador(self, equipoRojo, equipoAzul):
    if self.contadorRojo<self.contadorAzul:
      print("El equipo ganador es el equipo Azul")
    if self.contadorRojo>self.contadorAzul:
      print("El equipo ganador es el equipo Rojo")
    

    
      
    
  def eliminacion(self, equipoRojo, equipoAzul):
    contadorPerdedor=10
    nombreEliminado=0
    if self.contadorRojo<self.contadorAzul:
      for elem in self.equipoRojo.puntajeCocinero.keys():
        if contadorPerdedor<elem:
          contadorPerdedor=elem
          nombreEliminado=elem.value
      print("El eliminado", equipoRojo,"es", nombreEliminado, "con un puntaje de", contadorPerdedor)

    
    else:
      for elem in self.equipoRojo.puntajeCocinero.keys():
        if contadorPerdedor<elem:
          contadorPerdedor=elem
          nombreEliminado=elem.value
      print("El eliminado del equipo",equipoAzul,"es", nombreEliminado, "con un puntaje de", contadorPerdedor)
    

  def PruebaPastelero (self, equipoRojo, equipoAzul):
    contadorRojoPastel=0
    contadorAzulPastel=0
    for x in equipoAzul.self.platosFuertes:
      if x.self.tipo == "Reposteria":
        contadorAzulPastel= contadorAzulPastel+1
    for x in equipoRojo.self.platosFuertes:
      if x.self.tipo == "Reposteria":
        contadorRojoPastel= contadorRojoPastel+1
    if contadorRojoPastel>contadorAzulPastel:
      print("El equipo", equipoRojo, "es el ganador")
      equipoAzul.eliminacion()
      
    else:
      print("El equipo", equipoAzul, "es el ganador")
      equipoRojo.eliminacion()
    
  def PruebaDeLaCarne (self, equipoRojo, equipoAzul):
    contadorRojoCarne=0
    contadorAzulCarne=0
    for x in equipoAzul.self.platosFuertes:
      if x.self.tipo == "Carne":
        contadorAzulCarne= contadorAzulCarne+1
    for x in equipoRojo.self.platosFuertes:
      if x.self.tipo == "Carne":
        contadorRojoCarne= contadorRojoCarne+1
    if contadorRojoCarne>contadorAzulCarne:
      print("El equipo", equipoRojo, "es el ganador")
      equipoAzul.eliminacion()

  def PruebaDePrejuicios (self, equipoRojo, equipoAzul):
    contadorCocinerosRojo=0
    contadorCocinerosAzul=0
  
    for elem in self.equipoRojo.puntajeCocinero.keys():
      contadorCocinerosRojo = contadorCocinerosRojo + elem
    if contadorCocinerosRojo>contadorCocinerosAzul:
      print("El contador ganador es el rojo con ", contadorCocinerosRojo)

    for elem in self.equipoAzul.puntajeCocinero.keys():
      contadorCocinerosAzul = contadorCocinerosAzul + elem
    else:
       print("El contador ganador es el azul con ", contadorCocinerosAzul)

#Platos
Milanesa=Plato("Milanesa", "Carne", "500")
Magdalena=Plato("Magdalena", "Reposteria", "200")
Torta=Plato("Torta", "Reposteria", "300")


#Equipos
equipoAzul=Equipos("Azulado",[Torta,Magdalena], "Azul", {1:10, 2:5, 3:8, 4:7}, 4)

equipoRojo=Equipos("Rojizo",[Milanesa,Torta], "Rojo", {1:10, 2:5, 3:8, 4:7, 5:9}, 5)


#Hellskitchen
equipos=Hellskitchen(equipoRojo, equipoAzul)