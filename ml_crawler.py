#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
##
## Explorador de transacciones de mercadolibre
##
########################################################################

import urllib
import urllib2
from bs4 import BeautifulSoup
import cookielib
import networkx as nx
import time
import random
import socket, errno
import sys
import psycopg2 as pg

def connectDatabase ():
	"""
	Se conecta a la base de datos para almacenar la info
	
	Argumentos
	-------------
	
	Devuelve
	-------------
	
	"""
	
	conexion = pg.connect("dbname=base_ml user=postgres password = postgres")
	cursor = conexion.cursor()
	
	return conexion, cursor
	
def _parsePage(url):
	"""
	Toma un url y devuelve la pagina parseada como una cadena de texto
	
	Argumentos
	----------
	
	Devuelve
	----------
	
	"""

	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }


	values = {'name' : 'Gonza lo', 'location' : 'Buenos aires'}
	cj = cookielib.CookieJar()

	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

	data = urllib.urlencode(values)
	req = urllib2.Request(url, data, headers)
	response = opener.open(req)
	the_page = response.read()
	return the_page

def userLinkConstructor (user, base):
	"""
	Toma un identificador de usuario y devuelve un link para ir al perfil de ese usuario
	
	Argumentos
	----------
	user: usuario del que se quiere obtener le link
	
	Devuelve
	----------
	link al profile del usuario
	"""
	
	return 'http://www.mercadolibre.com.ar/jm/profile?id=%s&oper=S&baseLista=%d' %(user, base)

def getTransactions (usuario):
	"""
	Dado un usuario devuelve las transacciones comerciales que este realizo y una lista de los usuarios con los que comercio
	
	Argumentos
	-----------
	usuario: usuario objetivo del cual se van a registrar las transacciones
	
	Devuelve
	-----------
	transacciones: lista de diccionarios indicando las caracteristicas de transaccion {'vendedor': , 'comprador': , 'precio': , 'descripcion': , 'barrio_vendedor': , 'calificacion': }
	compradores: lista de usuarios que le compraron algo a el usuario objetivo
	
	"""
	transacciones_totales_sujeto = []
	
	## Obtego la pagina
	pagina = BeautifulSoup(_parsePage(userLinkConstructor (usuario, 1)))
	transacciones = constructTransaction (pagina)
	cont = 26
	while len(transacciones) > 0:
		transacciones_totales_sujeto.extend(transacciones)
		pagina = BeautifulSoup(_parsePage(userLinkConstructor (usuario, cont)))
		transacciones = constructTransaction (pagina)
		cont += 25
		
	return transacciones_totales_sujeto

	
def constructTransaction (page):
	"""
	Dada una lista de links filtra los que son transaccion y construye el objeto
	## modelo de objeto transaccion
	{'vendedor': , 'comprador': , 'precio': , 'descripcion': , 'barrio_vendedor': , 'calificacion': }
	"javascript:showGivenLayer(59240254,66921256,'MLA',470660567)"
	
	Argumentos:
	-------------
	links_list: lista de links de la pagina
	
	Devuelve
	-------------
	lista de interacciones para agregar al registro de transacciones
	
	"""
	
	transacciones = []
	elementos = page.find_all('div', {'id': 'content_box'})
	ubicacion_vendedor = _getUbicacionUsuario(page)
	
	## Toma la lista de usuarios que estan procesados y se fija si el acutal esta en esa lista
	
	
			
	for elemento in elementos:
		
		## el primero de la lista es el comprador, el segundo el vendedor
		comprador = _getComprador(elemento)
		vendedor = _getVendedor(elemento)
		item = _getItem(elemento)
		calificacion = _getCalificacion(elemento)
		precio = _getItemPrice(elemento)
		fecha = _getFechaTrnasaccion(elemento)
		
		transaccion = {'comprador': comprador, 'vendedor': vendedor, 'item': item, 'calificacion': calificacion, 'precio': precio, 'ubicacion_vendedor': ubicacion_vendedor, 'fecha': fecha}
		##print transaccion
		
		## se escriben los datoen en la base
		_addUser(comprador, 'pendiente')
		_addUser(vendedor, 'mapeado')
		_addTransaction(transaccion)
		
		## agrega el nodo al grafo aca, hay que ponerlo en otro lado!!!
		##G.add_edge(userLinkConstructor(vendedor, 1), userLinkConstructor(comprador,1), precio=precio, fecha=fecha)
		
		transacciones.append(transaccion)
		lista_espera.append(comprador)
	##print 'largo de las transacciones ',len(transacciones)
	return transacciones
	
def _addTransaction (transaccion):
	"""
	Agrega una transaccion a la base de datos
	"""
	
	cursor.execute(cursor.mogrify("INSERT INTO transacciones (id_comprador, id_vendedor, id_item, calificacion, fecha, comentario, monto) VALUES (%s, %s, %s, %s, %s, %s, %s)", \
					(transaccion['comprador'], transaccion['vendedor'], transaccion['item'], transaccion['calificacion'], transaccion['fecha'], 'Comentario', -999)))
	
	return None

def _addUser (id_usuario, status):
	"""
	Dadas las caracteristicas de un usuario las agrega a la tabla de usuarios
	
	Argumentos
	-----------
	
	Devuelve
	-----------
	
	"""
	
	cursor.execute(cursor.mogrify("SELECT '1' FROM usuarios WHERE id_usuario = %s", (id_usuario, )))
	existe = cursor.fetchone()
	##print existe
	if existe is not None:
		return id_usuario
		
	else:
		cursor.execute(cursor.mogrify("INSERT INTO usuarios (id_usuario, status) VALUES (%s, %s)", (id_usuario, status)))
		
		print 'El %s usuario no esta en la base y se va a agregar' %(id_usuario,)
		
		return id_usuario

def _getUbicacionUsuario (page):
	"""
	Dada una pagina web devuelve la ubicacion del usuario
	"""
	
	ubicacion = page.find('div', {'id': 'sitesince'}).text.split(':')[-1]
	
	return ubicacion

def _getListaProcesados ():
	"""
	Consulta en la DB la lista de los usuarios que ya fueron procesados
	
	Argumentos
	------------
	
	Devuelve
	------------
	
	"""
	
	cursor.execute("SELECT id_usuario FROM usuarios WHERE status = 'pendiente'")
	lista_procesados = cursor.fetchall()
	
	return lista_procesados

def _updateUserStatus (id_usuario, new_status):
	"""
	Actualiza el status del usuario
	
	Argumentos
	------------
	id_usuario: usuario al cual se le actualiza el status
	new_status: nuevo status
	
	Devuelve
	------------
	None
	"""
	
	cursor.execute(cursor.mogrify("UPDATE usuarios SET status = %s where id_usuario = %s", (new_status, id_usuario)))
	connection.commit()
	
	return None

def _getItemPrice (elemento):
	"""
	Dado un elemento completo de transaccion, devuelve el precio del objeto que se compro/vendio
	
	Argumentos
	----------
	elemento: es el objeto que devuelve bs4 cuando se filtra el div que corresponde a una transaccion completa
	
	Devuelve
	----------
	price: precio del elemento si es que hay
	"""
	
	price = elemento.find('div', {'id': 'compra_texto'}).text.split('$')[-1]
	
	return price

def getSentidoTransaccion (elemento):
	"""
	Dado un elemento de transaccion completo, devuelve el sentido en el que se realizo. 
	Si fue una compra o una venta del usuario
	
	Argumentos
	-----------
	elemento: es el objeto que devuelve bs4 cuando se filtra el div que corresponde a una transaccion completa
	
	Devuelve
	-----------
	
	"""
	
	return sentido_transaccion

def _getComprador (elemento):
	"""
	Dado un elemento de transaccion completo, devuelve el comprador. 
	Si fue una compra o una venta del usuario
	
	Argumentos
	-----------
	elemento: es el objeto que devuelve bs4 cuando se filtra el div que corresponde a una transaccion completa
	
	"""
	
	comprador = elemento.a.get('href').split('(')[1].split(',')[0]
	
	return comprador

def _getVendedor (elemento):
	"""
	Dado un elemento de transaccion completo, devuelve el vendedor. 
	Si fue una compra o una venta del usuario
	
	Argumentos
	-----------
	elemento: es el objeto que devuelve bs4 cuando se filtra el div que corresponde a una transaccion completa
	
	"""
	
	vendedor = elemento.a.get('href').split('(')[1].split(',')[1]
	return vendedor

def _getItem (elemento):
	"""
	Dado un elemento de transaccion completo, devuelve el item. 
	Si fue una compra o una venta del usuario
	
	Argumentos
	-----------
	elemento: es el objeto que devuelve bs4 cuando se filtra el div que corresponde a una transaccion completa

	"""
	
	item = elemento.a.get('href').split('(')[1].split(',')[3].split(')')[0]
	
	return item

def _getCalificacion (elemento):
	"""
	Dado un elemento de transaccion completo, devuelve la calificacion. 
	Si fue una compra o una venta del usuario
	
	Argumentos
	-----------
	elemento: es el objeto que devuelve bs4 cuando se filtra el div que corresponde a una transaccion completa
	
	"""
	
	calificacion = elemento.div.img.get('src').split('/')[-1].split('.')[0]
	
	return calificacion

def _getFechaTrnasaccion (elemento):
	"""
	Dado un elemento devuelve la fecha en la que se realizo la transaccion
	"""
	
	fecha_transaccion = elemento.find('div', {'id':'fecha'}).text.split(' ')[0]
	
	return fecha_transaccion

def _getComment ():
	"""
	Comentario que se dejo en el comentario
	"""
	
	##return comment
	return None

if __name__ == '__main__':
	
	##http://www.mercadolibre.com.ar/jm/profile?id=82640759&oper=S
	
	conexion, cursor = connectDatabase()
	
	## usuario de origen del proceso
	usuario = '82640759'
	
	## crear objeto grafo 
	##G = nx.Graph() 
	
	## lista de espera
	lista_espera = [usuario,]
	
	## lista de procesados
	##lista_procesados = _getListaProcesados()
	
	
	for ciclo in range(int(sys.argv[1])):
		
		if len(lista_espera) > 0:
			try:
				
				candidato = lista_espera.pop()
				if candidato not in _getListaProcesados():
					getTransactions (candidato)
					conexion.commit()
				else:
					print 'El candidato %s ya fue procesado' %(candidato, )
				##nx.write_graphml(G, sys.argv[2]+'.graphml')
				##time.sleep(random.randint(5, 10))
				
			except socket.error as e:
				if e.errno == errno.ECONNREFUSED:
					print 'Desconectado durmiendo por 60 segs'
					time.sleep(60)
				else:
					raise
		
		print ciclo
		
