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
import time

# Importamos para que espere entre páginas
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Vamos a definir las opciones de selenium. 
options = Options()
# Pegamos la dirección del driver
options.add_argument(r'C:\Users\pilih\Documents\chromedriver-win64\chromedriver-win64\chromedriver.exe')

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
    products = soup.select("div.producto-card")
    # Iteramos sobre cada uno de uno
    for prod in products:
        # Extraemos el nombre
        name = prod.select_one("h3.nombre-producto")
        product_name = name.get_text(strip=True) if name else None
        # Extraemos el precio
        price = prod.select_one("h4.card-title")
        product_price = price.get_text(strip=True) if price else None
        # Extraemos el URL
        ur = prod.select_one("a[href]")
        product_url = ur["href"].strip() if ur and ur.has_attr("href") else None
        if product_url and product_url.startswith("/"):
            product_url = "https://www.cotodigital3.com.ar" + product_url
        if product_name:  # guardamos sólo si hay nombre
            resultados[product_name] = {"price": product_price, "url": product_url}
    # El output es el diccionario con resultados
    return(resultados)
    
# Ahora vamos a automatizar el proceso.

# Comenzamos definiendo el link con las categorías que voy a buscar (en este caso, Gaseosas)
url = 'https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-bebidas-bebidas-sin-alcohol-gaseosas/_/N-n4l4r5'
    
# El sitio tiene 7 páginas con productos, por eso vamos a tener que iterar por página
# Creamos diccionario para todos los resultados
resultados_productos = {}
# Abro el driver
driver = webdriver.Chrome(options=options)
driver.get(url)

page = 1
while True:
    # Espero a que carguen los datos antes de seguir
    wait = WebDriverWait(driver, 15)
    
    # Esperar a que carguen los productos antes de extraer el código
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.producto-card")))
    
    # Extraigo el source code y uso beautiful soup
    source_code = driver.page_source
    
    soup = BeautifulSoup(source_code, 'html.parser')

    # Aplico la función para extraer las características de los productos
    resultado_temp = scrape_coto(soup)
    
    # Lo agrego al diccionario final
    resultados_productos.update(resultado_temp)
    print(f"Página {page} scrapeada. Total productos: {len(resultados_productos)}")

    # Intentar hacer clic en el botón "Siguiente"
    try:
        # Referencia para detectar que la página cambió
        ref_item = driver.find_elements(By.CSS_SELECTOR, "div.producto-card")[0]
    
        # Botón "Siguiente" según tu DOM (a.page-link.page-back-next)
        next_button = driver.find_element(
            By.XPATH,
            "//li[not(contains(@class,'disabled'))]"
            "/a[contains(@class,'page-back-next') and contains(normalize-space(.),'Siguiente')]"
        )
    
        # Asegurar visibilidad y forzar el click con JS
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", next_button)
        driver.execute_script("arguments[0].click();", next_button)
    
        # Esperar que realmente se refresque la grilla
        wait.until(EC.staleness_of(ref_item))
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.producto-card")))
        page += 1
        time.sleep(1.0)
    
    except Exception:
        print("No hay más páginas disponibles.")
        driver.quit()
        break
    
# Guardo los resultados en un data frame
df = pd.DataFrame.from_dict(resultados_productos, orient='index').reset_index()
# Cambio nombres de las columnas
df.columns = ['producto', 'precio', 'url']   
# Exporto como un Excel
df.to_excel('scraping_coto.xlsx', index=False)
