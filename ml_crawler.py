#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
from bs4 import BeautifulSoup
import cookielib
import networkx as nx

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
	##print len(elementos)
	for elemento in elementos:
		comprador = elemento.a.get('href').split('(')[1].split(',')[0]
		vendedor = elemento.a.get('href').split('(')[1].split(',')[1]
		item = elemento.a.get('href').split('(')[1].split(',')[3].split(')')[0]
		calificacion = elemento.div.img.get('src').split('/')[-1].split('.')[0]
		transaccion = {'comprador': comprador, 'vendedor': vendedor, 'item': item, 'calificacion': calificacion}
		##print transaccion
		
		## agrega el nodo al grafo aca, hay que ponerlo en otro lado!!!
		G.add_edge(userLinkConstructor(vendedor, 1), userLinkConstructor(comprador,1))
		
		transacciones.append(transaccion)
		lista_espera.append(comprador)
	##print 'largo de las transacciones ',len(transacciones)
	return transacciones

if __name__ == '__main__':
	
	##http://www.mercadolibre.com.ar/jm/profile?id=82640759&oper=S
	
	## usuario de origen del proceso
	usuario = '82640759'
	
	## crear objeto grafo
	G = nx.DiGraph() 
	
	## lista de espera
	lista_espera = [usuario,]
	## lista de procesados
	lista_procesados = []
	
	for ciclo in range(200):
		
		if len(lista_espera) > 0:
			candidato = lista_espera.pop()
			if candidato not in lista_procesados:
				getTransactions (candidato)
				lista_procesados.append(candidato)
		
		nx.write_graphml(G, '/home/gonza/Escritorio/grafoml.graphml')
		
		print ciclo
