#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
from bs4 import BeautifulSoup
import cookielib

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
	url = usuario
	pagina = _parsePage(url)
	
	psd_page = BeautifulSoup(pagina)
	links = psd_page.find_all('a')
	
	for link in links:
		print link.get('href')

def userLinkConstructor (user):
	"""
	Toma un identificador de usuario y devuelve un link para ir al perfil de ese usuario
	
	Argumentos
	----------
	user: usuario del que se quiere obtener le link
	
	Devuelve
	----------
	link al profile del usuario
	"""
	
	return 'http://www.mercadolibre.com.ar/jm/profile?id=%s&oper=S' %(user,)

def constructTransaction (link_list):
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
	
def getNumeroPaginas (soup_object):
	"""
	toma el numero de interacciones totales y lo divide por 25 lo que da el numero de veces que hay que paginar
	"""
	
	return page_number

if __name__ == '__main__':

	##http://www.mercadolibre.com.ar/jm/profile?id=82640759&oper=S
	
	## usuario de origen del proceso
	usuario = '82640759'
	
	getTransactions(userLinkConstructor(usuario))
	
	## lista de espera
	lista_espera = [usuario,]
	## lista de procesados
	lista_procesados = []
	
	for ciclo in range(10):
		if len(lista_espera) > 0:
			candidato = lista_espera.pop()
			
			if candidato not in lista_procesados:
				getTransactions()
				lista_espera.extend(compradores)
				lista_procesados.extend(candidato)
				
			
			
