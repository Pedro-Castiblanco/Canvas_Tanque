
# Requerimientos básicos:
# Realizar la simulación de la variación interactiva del volumen de un tanque de agua. 
# Hay que visualizar el tanque y su volumen actual. 
# Además, en una gráfica, visualizar el histórico de los volúmenes.


import tkinter as tk
import time
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as pyplot 
from matplotlib.animation import FuncAnimation 
# # Constantes
# ## Dimensiones del Canvas
width=600
height=600


# # Ventana y componentes con tkinter
master = tk.Tk()
deslizador = tk.Scale(master, from_=0, to=10, length=600,tickinterval=1, orient=tk.HORIZONTAL)
deslizador.pack()
deslizador1 = tk.Scale(master, from_=-10, to=0, length=600,tickinterval=1, orient=tk.HORIZONTAL)
deslizador1.pack()
canvas = tk.Canvas(master, width=width, height=height)
canvas.pack()
img = tk.PhotoImage(file="planta.gif")
canvas.create_image(0, 0, anchor=tk.NW, image=img)

# ############### INICIO TANQUE
# # Este bloque agrupa la funcionalidad del tanque
# # es candidato para ser convertido en una clase en la siguiente versión 

class Tanque1():
  def __init__(self,capacidad_total,capacidad_actual,izquierda,abajo, derecha, arriba):
    self.capacidad_total=capacidad_total
    self.capacidad_actual=capacidad_actual
    self.izquierda=izquierda
    self.abajo=abajo
    self.derecha=derecha
    self.arriba=arriba
    # #Dimensiones del tanque
      # #Ubicación en 
      # #Calcula los pixeles del borde del liquido
    alto = abajo - arriba
    altura_liquido = int(alto * capacidad_actual/capacidad_total)

      #Define los rectangulos que representan el aire y el líquido
    self.aire = canvas.create_rectangle(
          izquierda, arriba,
          derecha, abajo - altura_liquido,
          fill='white',
        )
    self.liquido = canvas.create_rectangle(
            izquierda, abajo - altura_liquido,
          derecha, abajo,
          fill='blue',
        )

  def deja_salir(self,t,S2):
            '''
            Entradas
            --------
            t:float; indica el tiempo en segundos transcurrido
            S2:float; indica el area de la válvula que permite el paso del caudal

            Salidas
            -------
            volumen:float; indica el volumen de agua que salió o entro en ese tiempo 

            Descripción 
            ----------
            En caso que el valor de la válvula negativo sale el líquido usando el modelo físico correspondiente 
            En caso que el valor sea positivo entra liquido proporciona a la apertura y al tiempo

            '''
            S1=11 # Área superior del tanque
            H=self.capacidad_actual/S1 # Altura del líquido

            # según http://www.sc.ehu.es/sbweb/fisica3/fluidos/vaciado/vaciado.html
            #h=(sqrt(H)-S2*sqrt(2*9.8/(S1^2-S2^2))*t/2).^2;
            h=(math.sqrt(H)-S2*math.sqrt(2*9.8/(S1**2-S2**2))*t/2)**2
            volumen=(H-h)*S1

            if (self.capacidad_actual-volumen)<0:
                    volumen=self.capacidad_actual
            return volumen
            
  def actualiza_nivel(self):
                alto = self.abajo - self.arriba
                altura_liquido = int(alto * self.capacidad_actual / 100)
                # Dibuja un rectángulo para representar la parte ocupada 
                # y otro para el resto
                canvas.coords(
                    self.aire,
                    self.izquierda,self.arriba,
                    self.derecha, self.abajo - altura_liquido,
                )
                canvas.coords(
                    self.liquido,
                    self.izquierda, self.abajo - altura_liquido,
                    self.derecha, self.abajo,
                )
  '''
            Entradas
            --------
            izquierda, derecha, arriba, abajo: Ubicacion de los rectangulos de aire y liquido dentro del tanque

            Salidas
            -------
            Aire:objeto; crea un cuadro con el nivel de aire que hay en el tanque
            Liquido:objeto; crea un cuadro con el nivel de liquido que hay en el tanque  

            Descripción 
            ----------
           Funciona como una rutina que dibuja los nuevos rectangulos tanto del liquido como del aire, esto lo hace cada que se actualiza el nivel de agua en el tanque 

            '''

    # #################### FIN TANQUE

tanque=Tanque1(100,30,155, 300, 325, 200)
label_volumen = tk.Label(canvas,text=tanque.capacidad_actual)
label_volumen.place(x=0, y=200)
tiempo_global= time.time()
label_tiempo = tk.Label(canvas, text=tiempo_global)
label_tiempo.place(x=0, y=0)
def actualizacion_periodica():
        global tiempo_global
        label_tiempo.after(100, actualizacion_periodica) #= tk.Label(text=time.time())
        tiempo_actual = time.time()
        label_tiempo['text'] =  str(tiempo_actual)
        tiempo = tiempo_actual - tiempo_global
        tiempo_global = tiempo_actual
        # 

        S2=deslizador.get()
        S3=deslizador1.get()
        if S3<0:
            tanque.capacidad_actual += tanque.deja_salir(tiempo,S3)
            if  tanque.capacidad_actual >100:
             tanque.capacidad_actual =100
        elif S2>0 and tanque.capacidad_actual <100:
            tanque.capacidad_actual += tiempo*S2*1 
        label_volumen['text']=str(tanque.capacidad_actual)
        tanque.actualiza_nivel()
        

label_tiempo.after(100, actualizacion_periodica)


tk.mainloop()

# #Recomendaciones
# # No se puede usar el mismo deslizador para el líquido que entra y el que sale 
# #    Un deslizador para el líquido que entra
# #    Otro deslizador para el líquido que sale
# # El volumen del líquido no puede superar el volumen del tanque
# # Comentar la rutina que le falta el comentario
# # Crear una clase (`class`) para el tanque
# # Además, en una gráfica, visualizar el histórico de los volúmenes. 

#Intento de trazar la grafica 
'''
x=[]
y=[]
figure =pyplot.figure()
line= pyplot.plot_date(x,y,'-')
def grafica(frame):
  x.append(time.time())
  y.append(volumen)
  line.setdata(x,y)
  figure.gca().relim()
  figure.gca().autoscale_view()
  return line
animation1= FuncAnimation(figure,grafica,interval=1000)
pyplot.show()
'''