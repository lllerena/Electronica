#-*- coding: utf-8 -*-
# =====================================================================
# ====================   Usando libreria grafica   ====================
# =====================================================================
# Autor :  Luis Llerena Alarcon
# Fecha :  28 febrero 2020 01:00pm
# 

# font : standar
# link : http://patorjk.com/software/taag/#p=display&h=0&v=0&f=Standard&t=main


from __future__ import print_function
from Tkinter import *         # Importa la libreria Tkinter (Maneja Graficos)
from PIL import Image, ImageTk
from time import sleep
import time,serial,csv
import paho.mqtt.client as mqtt    # import the client1
from numpy import linspace, pi, sin
import csv
import ttk
#import LLL_module		# modulo de funciones basicas
# broker_address = "192.168.1.23"		# IP del broker MQTT (Miraflores - Lima)
# broker_address = "120.120.121.23"		# IP del broker MQTT (Cuzco)
broker_address = "192.168.1.23"			# IP del broker MQTT (Mosquitto en Raspberry Pi)

NODE_EN = [0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
nodo_nombre_corto = ["abc"]*121	#Cantidad de nombres cortos
nodo_nombre_largo = ["abcdef"]*121
NODE_Q = 100			# Numero de nodos maximo por pantalla
node = 0
MAPAS = 6				# Cantidad de mapas
iconta = 0				# 

# ESTABLECER VALORES DE LA INTERFAZ

sts_mapa = 1                        # mapa actual ???
cambios = True
IMA_ALM_UBIX = [0]*(NODE_Q*MAPAS+1)				# CREACION DE LISTAS DEL TAMANO A UTILIZAR = NODOS*PANTALLA
IMA_ALM_UBIY = [0]*(NODE_Q*MAPAS+1)	

NODE_STS     = [0]*(NODE_Q+1)*6			# 0 = sin humo  1 =con humo
NODE_STS_ANT = [0]*(NODE_Q+1)*6			# usado para hacer cambios
THR_node = [0,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56,4.56]
LL_node  = [0]*(NODE_Q+1)
IMA_ALARMA = [0]*(NODE_Q*MAPAS + 1)		# lista de imagenes
acumulador = [0]*(NODE_Q + 1)
				
PANTALLA1 = range(1,NODE_Q + 1)				## desde 1 - hasta la cantidad de nodos+1
#PANTALLA1 = range(1,6)						# MODO PRUEBA
PANTALLA2 = range((NODE_Q*1)+1,((NODE_Q)*2)+1)
PANTALLA3 = range((NODE_Q*2)+1,((NODE_Q)*3)+1)
PANTALLA4 = range((NODE_Q*3)+1,((NODE_Q)*4)+1)
PANTALLA5 = range((NODE_Q*4)+1,((NODE_Q)*5)+1)
PANTALLA6 = range((NODE_Q*5)+1,((NODE_Q)*6)+1)

sirena_activa=0

PRT_485 = serial.Serial(
	port='/dev/ttyS0',             # /ttyS0
	baudrate = 9600,               # 9600
	parity=serial.PARITY_NONE,     # "N"
	bytesize=serial.EIGHTBITS,     # "8"
	stopbits=serial.STOPBITS_ONE,  # "1"
	timeout=1                      #
	)

##############################
###    FUNCIONES USADAS    ###
##############################

def ubix_ubiy_nodoxpant():
	global IMA_ALM_UBIX,IMA_ALM_UBIY
	global NODE_Q,MAPAS
	# LECTURA DE ARCHIVO DE UBICACION X - Y
	posicion = 1
	posicionx=1
	posiciony=1

	with open('POS_CIRC.csv') as archivo: 
		reader = archivo.read().splitlines()
		for k in reader :			# LECTURA LINEA POR LINEA			
			reader = k.split(',')
			#print(reader)
			#print reader 
			for m in reader:		# Lectura de los elementos de la fila			
				if ((posicion-1)/100)%2==0:
					IMA_ALM_UBIX[posicionx] = int(m)
					#print("X%d   ==>  %d" % (posicionx,IMA_ALM_UBIX[posicionx])) 
					posicion += 1
					posicionx += 1
				else:	
					IMA_ALM_UBIY[posiciony] = int(m)
					posicion += 1 	
					posiciony += 1
		#print IMA_ALM_UBIX
		#print len(IMA_ALM_UBIX)
		#print IMA_ALM_UBIY
	archivo.close()

	#IMA_ALM_UBIX = [0,368,347,200,300,559,522,200,300,100,100,200,300,100,100,200,300]
	#IMA_ALM_UBIY = [0,257,294,100,300,209,286,100,300,100,100,200,300,100,100,200,300]
					  #PANTALLA1      #PANTALLA2 	  #PANTALLA3

	NODE_XPANTALLA = [1]*(NODE_Q+1)

def node_en_read():               # LECTURA DE ARCHIVO DE ENABLE
	posicion = 0
	with open("NODE_EN.csv") as archivo:  
		print ('===============================')	
		print ('Leyendo CSV : NODE_EN.csv')
		reader = archivo.read().splitlines()    # Lectura linea por linea (registro por registro)
		for row in reader :
			#print (type(row[10]),end="" )
			if ((posicion>=1)&(posicion<10)): 
				print ("Pos: %d  "%posicion,end="")  	
				#print ("Row : %s"%row,end="")
				#print ("Row[10] : %s"%row[10])
				NODE_EN[posicion] = (int)(row[10])
				print ("Value: %d  "%NODE_EN[posicion])			
			if (posicion>=1): 
				NODE_EN[posicion] = (int)(row[10])
			posicion+=1  				# Contador para insertar valores a NODE_EN
	print ('Cerrando    : NODE_EN.csv')
	
	archivo.close()	
	
def node_en_write():               # ESCRITURA DE ARCHIVO DE ENABLE
	posicion = 0
	with open("Borra.csv", "w") as csvfile:
		print ("Writing CSV : ")
		escribidor=csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for x in range(0,106):
			escribidor.writerow([NODE_EN[x],])
		escribidor.writerow(['Spam'] * 5 + ['Baked Beans'])
	csvfile.close()
	
def node_nombre_read():     # carga el nombre de cada nodo
	global nodo_nombre_corto,nodo_nombre_largo
	print("==============================")
	print("abriendo archivo de nombres")
	with open('NODE_NAME.csv') as file:
		reader = csv.reader(file)
		count = 0
		for row in reader:
			nodo_nombre_corto[count]=row[1]
			nodo_nombre_largo[count]=row[2]
			#print (row[1])
			if count>120: 
				break
			count += 1
	print("Total nombres leidos : ",end='')
	print(count)
	file.close()

def revisa_nodo():      # Actualiza cuando hay cambio de pantalla
	global NODE_STS_ANT,NODE_STS,NODE_XPANTALLA
	global PANTALLA1, PANTALLA2, PANTALLA3
	#global NODOS
	# if sts_mapa == 1:
	# 	for revisar in PANTALLA1 : 						
	# 		print NODE_STS[revisar]
	# 		print NODE_XPANTALLA[revisar]
	# 		if NODE_STS[revisar] == 1 and NODE_XPANTALLA[revisar] != 0 :
	# 			acumulador [conteo] = revisar
	# 			conteo += 1
	# 	for revisar in acumulador
	# 		if NODE_STS[revisar] == 1 and NODE_XPANTALLA[revisar] != 0 :
	# 			print("PANTALLA1")
	# 			on_ima1(revisar)				
	# 		#elif NODE_STS [revisar] == 0 :
	# 			# print("TODO CORRECTO")
	# 			# off_ima(revisar)
	# 		#else:
	# 			#print("Falla :/")

	if sts_mapa == 1:
		print ("Mapa 1")
		for revisar in range(1,101):
			if IMA_ALM_UBIX[revisar] !=0 and NODE_STS[revisar] == 1: # and NODE_XPANTALLA[revisar] != 0 :
				#print("prendiendo nodo en PANTALLA 1")
				on_ima1(revisar)
				#print("prendiendo sirena")
				sirena_activa=1              # Activa la sirena auditiva
			elif NODE_STS [revisar] == 0 and NODE_STS_ANT[revisar] == 1 and IMA_ALM_UBIX[revisar]== 0:
				#print("TODO CORRECTO APAGANDO")
				off_ima(revisar)
			NODE_STS_ANT[revisar] = NODE_STS[revisar]
	elif sts_mapa == 2:
		print("Mapa 2")
		for revisar in PANTALLA2:    #(101,201)
			#print revisar-NODOS
			#print NODE_STS[revisar-NODOS]
			if IMA_ALM_UBIX[revisar] !=0 and NODE_STS[revisar-(NODE_Q*1)] == 1 : #and NODE_XPANTALLA[revisar-(NODE_Q*1)] != 0
				on_ima2(revisar)
			elif NODE_STS [revisar-(NODE_Q*1)] == 0 and NODE_STS_ANT[revisar-(NODE_Q*1)] :
				#print("TODO CORRECTO")
				off_ima(revisar)
			NODE_STS_ANT[revisar] = NODE_STS[revisar]
	elif sts_mapa == 3:
		print("Mapa 3")
		for revisar in PANTALLA3 :
			if IMA_ALM_UBIX[revisar] !=0 and NODE_STS[revisar-(NODE_Q*2)] == 1: #and NODE_XPANTALLA[revisar-(NODE_Q*2)] != 0 :
					#print revisar
				print("PANTALLA 3")
				print(IMA_ALM_UBIX[revisar])
				print(IMA_ALM_UBIY[revisar])
				on_ima3(revisar)
			elif NODE_STS [revisar-(NODE_Q*2)] == 0 and NODE_STS_ANT[revisar-(NODE_Q*2)] == 1 and IMA_ALM_UBIX[revisar] == 0:
				#print("TODO CORRECTO")
				off_ima(revisar)
			NODE_STS_ANT[revisar] = NODE_STS[revisar]
	elif sts_mapa == 4:
		for revisar in PANTALLA4 : 						
			if IMA_ALM_UBIX[revisar] !=0 and NODE_STS[revisar-(NODE_Q*3)] == 1: # and NODE_XPANTALLA[revisar-(NODE_Q*3)] != 0 :
				print("PANTALLA 4")
				on_ima4(revisar)
			elif NODE_STS [revisar-(NODE_Q*3)] == 0 and NODE_STS_ANT[revisar-(NODE_Q*3)] == 1 and  IMA_ALM_UBIX[revisar] == 0:
				off_ima(revisar)
			NODE_STS_ANT[revisar] = NODE_STS[revisar]			
	elif sts_mapa == 5:
		for revisar in PANTALLA5 : 						
			if IMA_ALM_UBIX[revisar] !=0 and NODE_STS[revisar-(NODE_Q*4)] == 1: # and NODE_XPANTALLA[revisar-(NODE_Q*4)] != 0 :
				print("PANTALLA 5")
				on_ima5(revisar)
			elif NODE_STS [revisar-(NODE_Q*4)] == 0 and NODE_STS_ANT[revisar-(NODE_Q*4)] == 1 and IMA_ALM_UBIX[revisar] == 0:
				off_ima(revisar)
			NODE_STS_ANT[revisar] = NODE_STS[revisar]			
	elif sts_mapa == 6:
		for revisar in PANTALLA6 :
			if IMA_ALM_UBIX[revisar] !=0 and NODE_STS[revisar-(NODE_Q*5)] == 1: # and NODE_XPANTALLA[revisar-(NODE_Q*5)] != 0 :
				print("PANTALLA 6")
				on_ima6(revisar)
			elif NODE_STS [revisar-(NODE_Q*5)] == 0 and NODE_STS_ANT[revisar-(NODE_Q*5)] == 1 and IMA_ALM_UBIX[revisar] == 0:
				off_ima(revisar)
			NODE_STS_ANT[revisar] = NODE_STS[revisar]			
	print ("Revisando nodos...")

# ===================     Cuando llega un mensaje    ====================
def on_message(client, userdata, message):
	global LL_node,NODE_EN,NODE_last
	global acumulador,cambios
	global flag_escritura		#Variable para escribir en txt
	global msg_rec
	global node
	msg_rec = str(message.payload.decode("utf-8"))
	print("msg rec. %s"%msg_rec)    # N0048:04:0:0016:V001
	if message.topic=="syl_mqtt":   # Solo si el topico es el correcto
		node = int(msg_rec[1:5],10)       # Obtiene el valor del nodo
		fc_final = int(msg_rec[6:8],10)   # Obtiene el FC (function code)
		ind = int(msg_rec[9:10],10)       # Obtiene indicador de humo
		txs = int(msg_rec[11:15],10)      # Obtiene cantidad de transmisiones
		volt=int(msg_rec[17:20],10)       # Obtiene el valor del voltaje
		#volt = 372
		print(" Nodo  : %d"%node)
		print(" FC    : %d"%fc_final)
		print(" humo? : %d"%ind)
		print(" txs   : %d"%txs)
		print(" Volts : %d"%volt)
		print(" En    : %d"%NODE_EN[node])
		if (fc_final==4)&(NODE_EN[node]==1)&(ind==1):    # detecta si el nodo esta en alarma
			NODE_STS[node]=ind		# 0=sin humo  1=con humo
			NODE_last = node
			#print NODE_STS[node]
			flag_escritura = 1		#Activa escritura en disco
		if (fc_final==4)&(NODE_EN[node]==1)&(ind==0):    # detecta si el nodo esta en alarma
			NODE_STS[node]=ind		# 0=sin humo  1=con humo
			NODE_last = -1
			flag_escritura = 1		#Activa escritura en disco
		cambios=True

def on_ima1(pon):
	IMA_ALARMA[pon] = Image.open("img/16_25.png")   						# DEBEN PASAR BUCLE PRINCIPAL AMBAS LINEAS
	IMA_ALARMA[pon] = ImageTk.PhotoImage(IMA_ALARMA[pon])
	canvas.create_image(IMA_ALM_UBIX[pon],IMA_ALM_UBIY[pon], image = IMA_ALARMA[pon])

def on_ima2(pon):
	IMA_ALARMA[pon] = Image.open("img/16_50.png")   
	IMA_ALARMA[pon] = ImageTk.PhotoImage(IMA_ALARMA[pon])
	canvas.create_image(IMA_ALM_UBIX[pon],IMA_ALM_UBIY[pon], image = IMA_ALARMA[pon])

def on_ima3(pon):
	IMA_ALARMA[pon] = Image.open("img/16_50.png")   
	IMA_ALARMA[pon] = ImageTk.PhotoImage(IMA_ALARMA[pon])
	canvas.create_image(IMA_ALM_UBIX[pon],IMA_ALM_UBIY[pon], image = IMA_ALARMA[pon])

def on_ima4(pon):
	IMA_ALARMA[pon] = Image.open("img/16_50.png")   
	IMA_ALARMA[pon] = ImageTk.PhotoImage(IMA_ALARMA[pon])
	canvas.create_image(IMA_ALM_UBIX[pon],IMA_ALM_UBIY[pon], image = IMA_ALARMA[pon])

def on_ima5(pon):
	IMA_ALARMA[pon] = Image.open("img/16_50.png")   
	IMA_ALARMA[pon] = ImageTk.PhotoImage(IMA_ALARMA[pon])
	canvas.create_image(IMA_ALM_UBIX[pon],IMA_ALM_UBIY[pon], image = IMA_ALARMA[pon])

def on_ima6(pon):
	IMA_ALARMA[pon] = Image.open("img/16_50.png")   
	IMA_ALARMA[pon] = ImageTk.PhotoImage(IMA_ALARMA[pon])
	canvas.create_image(IMA_ALM_UBIX[pon],IMA_ALM_UBIY[pon], image = IMA_ALARMA[pon])

def off_ima(poff):						
	IMA_ALARMA[poff] = Image.open("img/14.png")   					#Foto vacia para el Reset
	IMA_ALARMA[poff] = ImageTk.PhotoImage(IMA_ALARMA[poff])
	canvas.create_image(IMA_ALM_UBIX[poff],IMA_ALM_UBIY[poff], image = IMA_ALARMA[poff])


# ===============================          CAMBIO DE MAPA      ==========================
def cambio_mapa(num_map):
	global sts_mapa
	global canvas
	canvas.destroy()
	canvas = Canvas(raiz, width=930, height=600,bg="#F2E9C0") #930
	canvas.grid(row=0,column=0,columnspan=3,rowspan=4)
	if num_map==1:
		canvas.create_image(0,0, image = photo_img_mapa1, anchor = 'nw')
	elif num_map==2:
		canvas.create_image(0,0, image = photo_img_mapa2, anchor = 'nw')
	elif num_map==3:
		canvas.create_image(0,0, image = photo_img_mapa3, anchor = 'nw')
	elif num_map==4:
		canvas.create_image(0,0, image = photo_img_mapa4, anchor = 'nw')
	elif num_map==5:
		canvas.create_image(0,0, image = photo_img_mapa5, anchor = 'nw')
	elif num_map==6:
		canvas.create_image(0,0, image = photo_img_mapa6, anchor = 'nw')
	sts_mapa = num_map     #Mapa en en que se encuentra actualmente
	revisa_nodo()

def cambio_mp1():
	cambio_mapa(1)

def cambio_mp2():
	cambio_mapa(2)

def cambio_mp3():
	cambio_mapa(3)

def cambio_mp4():
	cambio_mapa(4)

def cambio_mp5():
	cambio_mapa(5)

def cambio_mp6():
	cambio_mapa(6)

def cerrar_todo():
	global raiz
	#guardar variables en archivos *.txt y *csv
	print(" Cerrando . . . ")
	raiz.destroy()
	print("     ya cerro. ")	

def todos():     #activa todas las alarmas
	for k in range(1,100):
		if (IMA_ALM_UBIX[k] !=0 and NODE_EN[k]==1):
			NODE_STS[k]=1
	cambios=True
	revisa_nodo()

	'''
	#if sts_mapa == 1:
	#	for k in PANTALLA1:
	#		if (IMA_ALM_UBIX[k] !=0 and NODE_EN[k]==1):
	#			NODE_STS[k]=1
	#			# on_ima1(k)
	#	cambios=True
	#	revisa_nodo()
		
	if sts_mapa == 2:
		for k in PANTALLA2:
			if IMA_ALM_UBIX[k] !=0 :
				on_ima2(k)
	elif sts_mapa == 3:
		for k in PANTALLA3:
			if IMA_ALM_UBIX[k] !=0 :
				on_ima2(k)
	elif sts_mapa == 4:	
		for k in PANTALLA4:
			if IMA_ALM_UBIX[k] !=0 :
				on_ima2(k)
	elif sts_mapa == 5:	
		for k in PANTALLA5:
			if IMA_ALM_UBIX[k] !=0 :
				on_ima2(k)
	elif sts_mapa == 6:	
		for k in PANTALLA6:
			if IMA_ALM_UBIX[k] !=0 :
				on_ima2(k)
	'''
def silenciar():
	sirena_activa=0

def alm_reset():
	global sts_mapa
	for k in PANTALLA1:
			if (IMA_ALM_UBIX[k] !=0 and NODE_EN[k]==1):
				NODE_STS[k]=0
				NODE_STS_ANT[k]=0

				#falta desdibujar todo
	revisa_nodo()
	sirena_activa=0
	cambio_mapa(sts_mapa)

def cada_segundo():
	global contadorSeg
	global counter
	global flag_escritura
	global node
	global cont 	#Cuenta el posible nodo a transmitir
	global NODE_Q
	cont = 1	#Cuenta el posible nodo a transmitir
	contadorSeg=1
	counter=0
	tx=0		#Cantidad de transmiciones por 10 segundos
	#print(iconta)

	if ((counter+1)%200==0):	# aprox. cada 10 segundo
		while(1):
			#print("\nEstoy probando: ")
			#print(cont)

			if tx == 10:
				print("Final TX lapso largo")
				break
			if NODE_EN[cont]==1:
				#print("Voy a transmitir el nodo:")
				#
				sendserial(cont)
				tx += 1
			# El master que transmite
			cont +=1
			if cont>NODE_Q:
				cont=0

			
	if ((counter+1)%20==0):		# aprox. cada 1  segundo
		ult_nodo=68	# cambiar por variable "nodo"
		M1_1="M1"		# El master que transmite
		M1_2="04"		# tipo de transmision (FC a transmitir)
		M1_3=("R00%s" % ult_nodo)   # Nodo   
		M1_41="1"		# Nodo habilitado      falta
		M1_42=NODE_STS[ult_nodo]
		M1_43="1"		# si tiene reporte semanal
		M1_44="0"		# bateria OK
		syl_buf="%s:%s:%s:%s%s%s%s\n"%(M1_1,M1_2,M1_3,M1_41,M1_42,M1_43,M1_44)
		PRT_485.write(syl_buf)   # Salida hacia tablero TAB_200
		#print(syl_buf)           # Salida hacia monitor
		time.sleep(0.1)
		contadorSeg += 1

	if (flag_escritura == 1):		# Verifica que Llega un Mensaje 
		writetxt()			# Añade una linea al archivo .txt  
		sendserial(node)	# Envia por serial 485
		flag_escritura = 0	# entra solo una vez
		
		"""
		M01_3="R0069" # Nodo 
		M01__2=NODE_STS[69]
		syl_buf="%s:%s:%s:%s%s%s%s\n"%(M01_1,M01_2,M01_3,M01__1,M01__2,M01__3,M01__4)
		#PRT_485.write("%s:%s:%s:%s%s%s%s\n"%(M01_1,M01_2,M01_3,M01__1,M01__2,M01__3,M01__4))
		PRT_485.write(syl_buf)
		#print("%s:%s:%s:%s%s%s%s\n"%(M01_1,M01_2,M01_3,M01__1,M01__2,M01__3,M01__4)) #Muestra en Pantalla
		print(syl_buf)
		time.sleep(.01)
		#PRT_485.write('M01:04:N0068:0:1:1:0')    # Indica que esta transmitiendo por RS485
		"""
	counter += 1
		
	if (counter>=32000):
		counter=0

	time.sleep(.01)
	

	#label_conta = Label(miFrame6, text=iconta)
	#label_conta.pack()

def writetxt():			# Añade una linea al archivo .txt  
	#global msg_rec
	print(time.strftime("%y/%m/%d %H:%M:%S"),"===>",msg_rec)
	ym= time.strftime("./Logs/%Y_%m.txt")
	archivo =open(ym,"a")		#Crea un .txt con ese nombre (Año y mes)
	fh = time.strftime("%y/%m/%d %H:%M:%S")
	cad_esc = "%s ===> %s\n"%(fh,msg_rec)
	archivo.write(cad_esc)		#Escribe en el archivo .txt 
	archivo.close()


def sendserial(nodo_local):	# Envia por serial 485
	M1_1="M1"		# El master que transmite
	M1_2="04"		# tipo de transmision (FC a transmitir)
	M1_3=("R00%s" % nodo_local)		# Node number
	M1_41="%s" % NODE_EN[nodo_local]	# Node enabled?
	M1_42=NODE_STS[nodo_local]
	M1_43="1"		# si tiene reporte semanal
	M1_44="0"		# bateria OK
	syl_buf="%s:%s:%s:%s%s%s%s\n"%(M1_1,M1_2,M1_3,M1_41,M1_42,M1_43,M1_44)
	PRT_485.write(syl_buf)		# Salida hacia tablero TAB_200
	print("Data a Transmitir 485 : ")
	print(syl_buf)				# Salida hacia monitor
	time.sleep(0.1)

#######################################
###   VENTANA DE CONFIGURACION #2   ###
#######################################

def ventana2():
	global win2
	global NODE_EN
	node_nombre_read()
	win2=Toplevel()
	win2.title("Configuración 01..60")		# Titulo de la venta
	win2.geometry("900x520+20+5")
	miFrame1=Frame(win2,width=850, height=500)
	miFrame1.grid(columnspan=23,rowspan=23)


	for x in range(1,61):
		chkV[x]=IntVar()
		chkV[x].set(NODE_EN[x])			### Asignacion de Checkbox
		lc[x]=StringVar()				### Definicion de Label Nombre Corto como cadena
		ll[x]=StringVar()				### Definicion de Label Nombre Largo como cadena
		lc[x].set(nodo_nombre_corto[x])	### Asignacion de Label Nombre Corto
		ll[x].set(nodo_nombre_largo[x])	### Asignacion de Label Nombre Largo

	###   Creacion de palomitas
	for h in range(1,10):
		mis= "nodo 00%d"%h
		chkExample = Checkbutton(miFrame1,text=mis,var=chkV[h])
		chkExample.grid(row=h+1,column=1)
	for h in range(10,21):
		mis= "nodo 0%d"%h
		chkExample = Checkbutton(miFrame1,text=mis,var=chkV[h])
		chkExample.grid(row=h+1,column=1)
	for h in range(21,41):		# 21 hasta 40
		mis= "nodo 0%d"%h
		chkExample = Checkbutton(miFrame1,text=mis,var=chkV[h])
		chkExample.grid(row=h-19,column=9)
	for h in range(41,61):		# 21 hasta 60
		mis= "nodo 0%d"%h
		chkExample = Checkbutton(miFrame1,text=mis,var=chkV[h])
		chkExample.grid(row=h-39,column=17)


	##############################
	###   Nombre de columnas  ####
	##############################
	
	lblF1_1=Label(miFrame1,text="Enable ",font=("Helvetica", 12))
	lblF1_1.grid(row=1, column=1)
	lblF1_3=Label(miFrame1,text="N corto",font=("Helvetica", 12))
	lblF1_3.grid(row=1, column=3)
	lblF1_5=Label(miFrame1,text="N Largo",font=("Helvetica", 12))
	lblF1_5.grid(row=1, column=5)

	lblF1_9=Label(miFrame1,text="Enable ",font=("Helvetica", 12))
	lblF1_9.grid(row=1, column=9)
	lblF1_11=Label(miFrame1,text="N corto",font=("Helvetica", 12))
	lblF1_11.grid(row=1, column=11)
	lblF1_13=Label(miFrame1,text="N Largo",font=("Helvetica", 12))
	lblF1_13.grid(row=1, column=13)

	lblF1_17=Label(miFrame1,text="Enable ",font=("Helvetica", 12))
	lblF1_17.grid(row=1, column=17)
	lblF1_19=Label(miFrame1,text="N corto",font=("Helvetica", 12))
	lblF1_19.grid(row=1, column=19)
	lblF1_21=Label(miFrame1,text="N Largo",font=("Helvetica", 12))
	lblF1_21.grid(row=1, column=21)
	

	###   lineas Verticales   ###
	
	ttk.Separator(miFrame1,orient=VERTICAL).grid(column=2,row=2, rowspan=20,sticky="ns")
	ttk.Separator(miFrame1,orient=VERTICAL).grid(column=4,row=2, rowspan=20,sticky="ns")
	ttk.Separator(miFrame1,orient=VERTICAL).grid(column=6,row=1, rowspan=21,sticky="ns")

	ttk.Separator(miFrame1,orient=VERTICAL).grid(column=10,row=2, rowspan=20,sticky="ns")
	ttk.Separator(miFrame1,orient=VERTICAL).grid(column=12,row=2, rowspan=20,sticky="ns")
	ttk.Separator(miFrame1,orient=VERTICAL).grid(column=14,row=1, rowspan=21,sticky="ns")

	ttk.Separator(miFrame1,orient=VERTICAL).grid(column=18,row=2, rowspan=20,sticky="ns")
	ttk.Separator(miFrame1,orient=VERTICAL).grid(column=20,row=2, rowspan=20,sticky="ns")
	ttk.Separator(miFrame1,orient=VERTICAL).grid(column=22,row=1, rowspan=21,sticky="ns")


	 ###  creacion de nombre corto / nombre largo
	
	for x in range (1,21):
		Label01=Label(miFrame1,textvariable=lc[x])
		Label01.grid(row=1+x,column=3)
		Label01=Label(miFrame1,textvariable=ll[x])
		Label01.grid(row=1+x,column=5)

	for x in range (21,41):
		Label01=Label(miFrame1,textvariable=lc[x])
		Label01.grid(row=x-19,column=11)
		Label01=Label(miFrame1,textvariable=ll[x])
		Label01.grid(row=x-19,column=13)

	for x in range (41,61):
		Label01=Label(miFrame1,textvariable=lc[x])
		Label01.grid(row=x-39,column=19)
		Label01=Label(miFrame1,textvariable=ll[x])
		Label01.grid(row=x-39,column=21)

	# Crea espacios para que se vean los botones
	Labelalgo=Label(miFrame1,text=" ")
	Labelalgo.grid(row=22,column=20)
	Labelalgo=Label(miFrame1,text=" ")
	Labelalgo.grid(row=23,column=21)
	Labelalgo=Label(miFrame1,text=" ")
	Labelalgo.grid(row=24,column=22)
	Labelalgo=Label(miFrame1,text=" ")
	Labelalgo.grid(row=25,column=23)

	#--------------------- Botons ------------------------

	#boton2=Button(miFrame1,text="Voltaje",width=5, command=ventana3)
	#boton2.grid(row=21,column=8)
	#boton2.config(cursor="hand2")




	#---------------------------------------------------------------------------------------------
	#=============================Ventana 3==============================================
	#------------------------------------------------------------------------------------
	def ventana3():
		global NODE_EN
		global nodo_nombre_corto
		global nodo_nombre_largo
		global win3

		def Regresa2():
			global win3
			ventana2()
			win3.destroy()

		
		win3=Toplevel()
		win3.title("Configuración 61..120")		# Titulo de la venta
		win3.geometry("900x520+20+5")
		
		#label = Label(window, text="This is window #%s" % self.count)
		#label.pack(side="top", fill="both", expand=True, padx=40, pady=40);
		miFrame3=Frame(win3,width=850, height=500)
		miFrame3.grid(columnspan=23,rowspan=23)

		
		for x in range(61,121):
			#print(x,end="")
			chkV[x].set(NODE_EN[x])			### Asignacion de Checkbox
			lc[x]=StringVar()				### Definicion de Label Nombre Corto como cadena
			ll[x]=StringVar()				### Definicion de Label Nombre Largo como cadena
			lc[x].set(nodo_nombre_corto[x])	### Asignacion de Label Nombre Corto
			ll[x].set(nodo_nombre_largo[x])	### Asignacion de Label Nombre Largo
		


		'''
		
		chkV061P2.set(NODE_EN[61])
		chkV062P2.set(NODE_EN[62])
		chkV063P2.set(NODE_EN[63])
		
		
		'''

		###   Creacion de palomitas
		for x in range(61,81):		# 61 hasta 80
			mis= "nodo 0%d"%x
			chkExample = Checkbutton(miFrame3,text=mis,var=chkV[x])
			chkExample.grid(row=x-59,column=1)
		for x in range(81,100):		# 81 hasta 99
			mis= "nodo 0%d"%x
			chkExample = Checkbutton(miFrame3,text=mis,var=chkV[x])
			chkExample.grid(row=x-79,column=9)
		x=100	
		mis= "nodo %d"%x
		chkExample = Checkbutton(miFrame3,text=mis,var=chkV[x])
		chkExample.grid(row=x-79,column=9)
		for x in range(101,121):	# 101 hasta 120
			mis= "nodo %d"%x
			chkExample = Checkbutton(miFrame3,text=mis,var=chkV[x])
			chkExample.grid(row=x-99,column=17)



		##############################
		###   Nombre de columnas  ####
		##############################
		
		lblF2_1=Label(miFrame3,text="Enable ",font=("Helvetica", 12))
		lblF2_1.grid(row=1, column=1)
		lblF2_3=Label(miFrame3,text="N corto",font=("Helvetica", 12))
		lblF2_3.grid(row=1, column=3)
		lblF2_5=Label(miFrame3,text="N Largo",font=("Helvetica", 12))
		lblF2_5.grid(row=1, column=5)

		lblF2_9=Label(miFrame3,text="Enable ",font=("Helvetica", 12))
		lblF2_9.grid(row=1, column=9)
		lblF2_11=Label(miFrame3,text="N corto",font=("Helvetica", 12))
		lblF2_11.grid(row=1, column=11)
		lblF2_13=Label(miFrame3,text="N Largo",font=("Helvetica", 12))
		lblF2_13.grid(row=1, column=13)

		lblF2_17=Label(miFrame3,text="Enable ",font=("Helvetica", 12))
		lblF2_17.grid(row=1, column=17)
		lblF2_19=Label(miFrame3,text="N corto",font=("Helvetica", 12))
		lblF2_19.grid(row=1, column=19)
		lblF2_21=Label(miFrame3,text="N Largo",font=("Helvetica", 12))
		lblF2_21.grid(row=1, column=21)


		###   lineas Verticales   ###
		
		ttk.Separator(miFrame3,orient=VERTICAL).grid(column=2,row=2, rowspan=20,sticky="ns")
		ttk.Separator(miFrame3,orient=VERTICAL).grid(column=4,row=2, rowspan=20,sticky="ns")
		ttk.Separator(miFrame3,orient=VERTICAL).grid(column=6,row=1, rowspan=21,sticky="ns")

		ttk.Separator(miFrame3,orient=VERTICAL).grid(column=10,row=2, rowspan=20,sticky="ns")
		ttk.Separator(miFrame3,orient=VERTICAL).grid(column=12,row=2, rowspan=20,sticky="ns")
		ttk.Separator(miFrame3,orient=VERTICAL).grid(column=14,row=1, rowspan=21,sticky="ns")

		ttk.Separator(miFrame3,orient=VERTICAL).grid(column=18,row=2, rowspan=20,sticky="ns")
		ttk.Separator(miFrame3,orient=VERTICAL).grid(column=20,row=2, rowspan=20,sticky="ns")
		ttk.Separator(miFrame3,orient=VERTICAL).grid(column=22,row=1, rowspan=21,sticky="ns")

		 ###  creacion de nombre corto / nombre largo
		
		for x in range (61,81):
			Label01=Label(miFrame3,textvariable=lc[x])
			Label01.grid(row=x-59,column=3)
			Label01=Label(miFrame3,textvariable=ll[x])
			Label01.grid(row=x-59,column=5)

		for x in range (81,101):
			Label01=Label(miFrame3,textvariable=lc[x])
			Label01.grid(row=x-79,column=11)
			Label01=Label(miFrame3,textvariable=ll[x])
			Label01.grid(row=x-79,column=13)

		for x in range (101,121):
			Label01=Label(miFrame3,textvariable=lc[x])
			Label01.grid(row=x-99,column=19)
			Label01=Label(miFrame3,textvariable=ll[x])
			Label01.grid(row=x-99,column=21)

		# Crea espacios para que se vean los botones
		Labelalgo=Label(miFrame3,text="        ")
		Labelalgo.grid(row=22,column=20)
		Labelalgo=Label(miFrame3,text="        ")
		Labelalgo.grid(row=23,column=21)
		Labelalgo=Label(miFrame3,text="        ")
		Labelalgo.grid(row=24,column=22)
		Labelalgo=Label(miFrame3,text="                     ")
		Labelalgo.grid(row=25,column=23)

		
		boton5=Button(miFrame3,text="<-Back", command=Regresa2,width=7,height=2)
		boton5.place(x=800,y=450)  
		boton5.config(cursor="hand2")
		boton6=Button(miFrame3,text="Cerrar", command=win3.destroy,width=7,height=2)
		boton6.place(x=700,y=450)  
		boton6.config(cursor="hand2")
		
	def cerrando2():
		print("Enable3 antes   : %d"%NODE_EN[3])
		NODE_EN[3]=chkV[3].get()
		print("Enable3 despues : %d"%NODE_EN[3])
		win2.destroy()
		
		
	def next3():
		global win2
		ventana3()
		win2.destroy()
		
	
	btn_v3a=Button(miFrame1,text="Next->", command=next3,width=7,height=2)
	btn_v3a.place(x=800,y=450)  
	btn_v3a.config(cursor="hand2")
	btn_v3b=Button(miFrame1,text="Cerrar", command=cerrando2,width=7,height=2)
	btn_v3b.place(x=700,y=450)  
	btn_v3b.config(cursor="hand2")
	

#####################################################################################
#                       _   _                                             _         
#     ___    ___     __| | (_)   __ _    ___          _ __ ___     __ _  (_)  _ __  
#    / __|  / _ \   / _` | | |  / _` |  / _ \        | '_ ` _ \   / _` | | | | '_ \ 
#   | (__  | (_) | | (_| | | | | (_| | | (_) |       | | | | | | | (_| | | | | | | |
#    \___|  \___/   \__,_| |_|  \__, |  \___/        |_| |_| |_|  \__,_| |_| |_| |_|
#                               |___/                                               
#  
#####################################################################################


client = mqtt.Client("P1")        #create new instance
client.on_message = on_message    #attach function to callback

client.connect(broker_address)    #connect to broker
client.loop_start()               #start the loop
client.subscribe("syl_mqtt")
client.publish("syl_Urubamba","Pantalla entrando - humo_v52A")
# ===================               NODOS ACTIVOS              ====================
node_en_read()
#node_en_write()
# ===================     Posiciones de circulinas por frame   ====================
ubix_ubiy_nodoxpant()
# ===================             carga imagenes               ====================
# =================================================================================

#####  Inicio de loop grafico

raiz=Tk()                     #! Raiz de la ventana
raiz.title("Sol y Luna - Sistema de Monitoreo de Humo")   # Titulo de la venta
raiz.resizable(False, False)                              # No se podra cambiar tamaño
raiz.geometry("1024x600+0-25")   #-15 para evitar el marco superior
#raiz.wm_attributes('-alpha', 0.7)
chkV=[]
lc=[]
ll=[]
for j in range(1,125):
	chkV.append(8)		# agrega el integer "8"
	lc.append("Hola")	# agrega el string  "Hola"
	ll.append("Holaaa")	# agrega el string  "Holaaa"


for x in range(1,123):
	chkV[x] = IntVar()

img_mapa1=Image.open("img/MapaSyL_01_General.png")             		# 926x578     
photo_img_mapa1= ImageTk.PhotoImage(img_mapa1)
img_mapa2=Image.open("img/MapaSyL_02.png")            				# 926x578      
photo_img_mapa2= ImageTk.PhotoImage(img_mapa2)
img_mapa3=Image.open("img/MapaSyL_03.png")            				# 926x578      
photo_img_mapa3= ImageTk.PhotoImage(img_mapa3)
img_mapa4=Image.open("img/MapaSyL_04.png")          				# 926x578      
photo_img_mapa4= ImageTk.PhotoImage(img_mapa4)
img_mapa5=Image.open("img/MapaSyL_05_Zona_Oprtv.png")               # 926x578      
photo_img_mapa5= ImageTk.PhotoImage(img_mapa5)
img_mapa6=Image.open("img/MapaSyL_06_Wayra.png")            		# 926x578      
photo_img_mapa6= ImageTk.PhotoImage(img_mapa6)

img_mp1_ledon=Image.open("img/x.gif")  # Carga imagen led ON_12x12
photo_img_mp1_ledon= ImageTk.PhotoImage(img_mp1_ledon)

	
# =================================================================================
# =======================================          FRAMES          ================
# =================================================================================
canvas = Canvas(raiz, width=930, height=600,bg="#F2E9C0")
canvas.grid(row=0,column=0,columnspan=4,rowspan=4)

#miFrame1=Frame(raiz, width=945, height=500, relief="groove",bg="blue")  # Frame inferior (texto) ,bg="green"
#miFrame1.grid(row=0,column=0,rowspan=3,columnspan=1)   #,rowspan=2

miFrame2=Frame(raiz, width=600, height=20, bg="blue")  # Frame inferior (texto) ,bg="green"
miFrame2.grid(row=4,column=0)   #,rowspan=2

miFrame6=Frame(raiz, width=96, height=130, bg="green")  # Frame de leyenda superior ,bg="green"
miFrame6.grid(column=4,row=0)

miFrame7=Frame(raiz, width=96, height=370, bg="blue")  # Frame de leyenda inderior,bg="green"
miFrame7.grid(column=4,row=1)

miFrame9=Frame(raiz, width=96, height=110, bg="green")  # Frame de Boton  ,bg="blue" , bd=1, relief="solid"
miFrame9.grid(column=4,row=2)


#time.sleep(1) # wait
#Imagen de Leyenda (logo Sol y Luna)

img_logo=Image.open("img/log2.png")      # 63x63
logo= ImageTk.PhotoImage(img_logo)
labellogo=Label(miFrame6, image=logo)
labellogo.place(x=14,y=8)	##Ubicacion del logo (Esquina superior Derecha)

# ===============================          BOTONES PRINCIPALES     ==========================

#config = PhotoImage(file="img/config_01.png")
#botonEnvio=Button(miFrame9, image= config  , command=ventana2, width=60,height=30)
#botonEnvio.place(x=14,y=26)
#botonEnvio.config(cursor="hand2")
#botonEnvio.pack(side=LEFT)

cambio_mapa(1)				#Muestra el mapa en el comienzo del programa

botonReset=Button(miFrame6, text="Reset", command=alm_reset,width=7,height=2)
botonReset.place(x=4,y=80)
botonReset.config(cursor="hand2")

botonReset=Button(miFrame6, text=".", command=todos,width=1,height=1)
botonReset.place(x=30,y=40)
botonReset.config(cursor="hand2")

botonConfig=Button(miFrame9, text="Config", command=ventana2,width=2,height=1)
botonConfig.place(x=25,y=5)
botonConfig.config(cursor="hand2")
#botonCerrar.pack(side= RIGHT)

botonSilence=Button(miFrame9, text="Silenciar", command=silenciar,width=7,height=1)
botonSilence.place(x=4,y=37)
botonSilence.config(cursor="hand2")

botonCerrar=Button(miFrame9, text="Cerrar", command=cerrar_todo,width=7,height=1)   #.pack()
botonCerrar.place(x=4,y=68)
botonCerrar.config(cursor="hand2")
#botonCerrar.pack(side= RIGHT)

# =======================      BOTONES EN LEYENDAS (cambio de mapas)     ==================

boton_mp1=Button(miFrame7, text="Principal", command=cambio_mp1,width=7,height=3)
boton_mp1.place(x=4,y=4)
boton_mp1.config(cursor="hand2")
#boton_mp1.pack(side= RIGHT)

boton_mp2=Button(miFrame7, text="Mapa 2", command=cambio_mp2,width=7,height=3)
boton_mp2.place(x=4,y=63)
boton_mp2.config(cursor="hand2")
#boton_mp1.pack(side= RIGHT)

boton_mp3=Button(miFrame7, text="Mapa 3", command=cambio_mp3,width=7,height=3)
boton_mp3.place(x=4,y=123)
boton_mp3.config(cursor="hand2")
#botonCerrar.pack(side= RIGHT)

boton_mp4=Button(miFrame7, text="Mapa 4", command=cambio_mp4,width=7,height=3)
boton_mp4.place(x=4,y=183)
boton_mp4.config(cursor="hand2")

boton_mp5=Button(miFrame7, text="Mapa 5", command=cambio_mp5,width=7,height=3)
boton_mp5.place(x=4,y=243)
boton_mp5.config(cursor="hand2")

boton_mp6=Button(miFrame7, text="Mapa 6", command=cambio_mp6,width=7,height=3)
boton_mp6.place(x=4,y=303)
boton_mp6.config(cursor="hand2")

#boton_mp4=Button(miFrame8, text="Mapa 6", command=cambio_mp6,width=5)
#boton_mp4.place(x=12,y=510)
#boton_mp4.config(cursor="hand2")
flag_escritura=0
while 1:
	cada_segundo()
	raiz.update_idletasks()
	raiz.update()
	time.sleep(0.05)
	iconta+=1
	if cambios:
		revisa_nodo()
		cambios=False
raiz.mainloop()                                 # Metodo Loop bucle infinito


