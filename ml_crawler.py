#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
from bs4 import BeautifulSoup as bs

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

def getTramsactions (usuario):
	"""
	Dado un usuario devuelve las transacciones comerciales que este realizo y una lista de los usuarios con los que comercio
	
	## modelo de objeto transaccion
	{'vendedor': , 'comprador': , 'precio': , 'descripcion': , 'barrio_vendedor': , 'calificacion': }
	"javascript:showGivenLayer(59240254,66921256,'MLA',470660567)"
	Argumentos
	-----------
	usuario: usuario objetivo del cual se van a registrar las transacciones
	
	Devuelve
	-----------
	transacciones: lista de diccionarios indicando las caracteristicas de transaccion {'vendedor': , 'comprador': , 'precio': , 'descripcion': , 'barrio_vendedor': , 'calificacion': }
	compradores: lista de usuarios que le compraron algo a el usuario objetivo
	
	"""
	url = 'http://'+usuario
	pagina = _parsePage(url)
	
	
	
def crawl ():
	"""
	
	"""
	


if __name__ == '__main__':
	## usuario de origen del proceso
	usuario = ''
	
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
				
			
			
