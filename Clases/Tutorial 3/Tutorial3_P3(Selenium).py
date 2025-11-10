#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

# Tutorial de Big Data
## Tutorial 3 - Parte 3

El objetivo es conocer otro método para hacer WebScraping

"""

# Supongamos que nos interesa conseguir los precios de las gaseosas. 
# Podríamos usar lo que aprendimos la tutorial pasada sobre web scraping. Veamos

# Importo la librería requests
import requests

# Defino el url 
url = 'https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-bebidas-bebidas-sin-alcohol-gaseosas/_/N-n4l4r5'

# Extraigo el código
code = requests.get(url)
print(code)
# El error 403 nos indica que la página no nos deja extraer el código fuente. Veamos otra forma de hacerlo!

# La librería que vamos a usar se llama Selenium.
# Para poder usarla, necesitamos instalar un driver en nuestra computadora (ChromeDriver), 
# que se encuentra en este sitio: https://sites.google.com/chromium.org/driver/downloads?authuser=0

# Importamos selenium junto con algunas opciones
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# También importamos beautiful soup y pandas
from bs4 import BeautifulSoup
import pandas as pd

# Vamos a definir las opciones de selenium. 
options = Options()
# Pegamos la dirección del driver
options.add_argument(r'C:\Users\pilih\Documents\chromedriver-win64\chromedriver-win64')

# Inicializamos el driver
driver = webdriver.Chrome(options=options)

# Abrimos el sitio que querramos
driver.get(url)

# Extraemos el source code
source_code = driver.page_source

# Queremos sacar los precios de cada uno de los productos. Definimos una función
def scrape_coto(soup):
    # Definimos un diccionario para guardar los resultados
    resultados = {}
    # Buscamos todos los productos en la página
    products = soup.find_all('li', class_ = 'clearfix')
    # Iteramos sobre cada uno de uno
    for prod in products:
        # Extraemos el nombre
        name = prod.find('div', class_ = 'descrip_full')
        product_name = name.text.strip()
        # Extraemos el precio
        price = prod.find('span', class_ = 'atg_store_newPrice')
        product_price = price.text.strip()
        # Extraemos el URL
        urls = prod.find('div', class_ = 'product_info_container')
        product_url = urls.find('a', href = True)['href']
        # Guardamos en un diccionario
        resultados[product_name] = {'price': product_price, 
                                    'url' : f'www.cotodigital3.com.ar/{product_url}'}
    # El output es el diccionario con resultados
    return(resultados)
    
# Ahora vamos a automatizar el proceso.

# Comenzamos definiendo el link con las categorías que voy a buscar (en este caso, Gaseosas)
url = 'https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-bebidas-bebidas-sin-alcohol-gaseosas/_/N-n4l4r5'
    
# El sitio tiene 7 páginas con productos, por eso vamos a tener que iterar por página
page = 1
# Creamos diccionario para todos los resultados
resultados_productos = {}
# Abro el driver
driver = webdriver.Chrome(options=options)
driver.get(url)
while page >= 1:
    try:
        # Abro la página y hago click en el boton de la página para avanzar 'page'
        selector = f'//*[@id="atg_store_pagination"]/li[{page}]/a'
        driver.find_element(By.XPATH, selector).click()
        
        # Extraigo el source code y uso beautiful soup
        source_code = driver.page_source
        soup = BeautifulSoup(source_code, 'html.parser')

        # Aplico la función para extraer las características de los productos
        resultado_temp = scrape_coto(soup)

        # Lo agrego al diccionario final
        resultados_productos.update(resultado_temp)
        # Actualizo el counter de la página    
        page += 1        
    # Si hay un error (porque no hay más páginas) entonces cierra el driver y corta el while loop
    except:
        driver.quit()
        break

# Guardo los resultados en un data frame
df = pd.DataFrame.from_dict(resultados_productos, orient='index').reset_index()
# Cambio nombres de las columnas
df.columns = ['producto', 'precio', 'url']   
# Exporto como un Excel
df.to_excel('scraping_coto.xlsx', index=False)
