# -*- coding: utf-8 -*-
"""

# Tutorial de Machine Learning para Economistas
## Tutorial 3 - Parte 1

El objetivo de esta tutorial se centra en Pandas y Matplotlib y haremos mención a Numpy.

**NumPy** es una librería de cálculo numérico para Python, muchas de
las principales librerías en análisis de datos están construidas sobre
NumPy.

**Pandas** es quizás la librería que más usen en sus primeros pasos en Python, sirve para el trabajo con tablas de datos estructuradas, importar tablas de información, manipularlas y analizarlas.

**Matplolib** es una librería para graficar.

Hay mucho más para conocer sobre estas librerías de lo que se cubre en esta clase. El objetivo es que tengan el conocimiento suficiente para comenzar a usarlas y resolver las tareas más comunes.

### Introducción a Numpy

NumPy es una librería de cálculo numérico para Python, lanzada inicialmente en 1995. Está escrita en lenguajes de bajo nivel (por ejemplo, C) para permitir realizar operaciones matemáticas de manera eficiente.

Muchas librerías muy utilizadas en análisis de datos tienen a NumPy como librería base, y agregan funcionalidades adicionales por encima de ella. Algunos ejemplos son:
- Pandas: para manejo de datos tabulares
- Matplotlib: para gráficos
- SciPy: para cálculo científico
- scikit-learn: para aprendizaje automático

### Pandas

Pandas: es la librería más usada manejo de datos en tablas, tiene funciones y métodos que facilitan mucho el trabajo con este tipo de datos (dataframes). Se usa para tareas de procesamiento, análisis y visualización de datos.

Los dos tipos principales de objetos de Pandas son:
- Series (una matriz unidimensional etiquetada)
- DataFrames (una estructura de datos bidimensional etiquetada con columnas de tipos posiblemente diversos).

Ya hemos visto:
- importar/exportar y crear DataFrames
- explorar la tabla de datos

En esta clase vamos a usarla para:
- filtrar datos
- agregar columnas / filas
- unir bases (merge, join)

#### Repaso

Algunos de los métodos del paquete Pandas que vimos en la Tutorial 2 son:
- pd.read_excel(): abrir un archivo .xls o .xlsx
- pd.read_csv(): abrir un archivo .csv
- pd.read_stata(): abrir un archivo .dta
- df.head(N): ver las primeras N líneas
- df.tail(N): ver las últimas N líneas
- df.sample(N): ver una muestra de N líneas
- pd.DataFrame(columns=["AA", "BB"]): crear tabla con columnas AA y BB
- df.to_excel(): guardar una tabla en archivo .xls o .xslx
- df.to_csv(): guardar una tabla en archivo .csv
"""

import pandas as pd

"""##### Explorar datos
Vamos a usar un ejemplo con registros de grupos inventados de estudiantes
"""

# Recuerden tener el archivo en la carpeta donde están o modificar su directorio con:
import os
os.chdir(r"C:\Users\pilih\Documents\UdeSA\Teaching\Maestría Economía\Big Data\Github Big Data\Big-Data-UdeSA\Clases\Tutorial 3")

# Abrimos el archivo y vemos las primeras dos filas
df = pd.read_excel("tabla_ejemplo.xlsx")
df.head(2)

"""El 0 y 1 en el margen son los números de fila"""

df.sample(3)

"""Al importar un df, es una buena práctica imprimir algunas líneas para verificar que se haya cargado bien.
También es útil imprimir el listado de nombres de las columnas y el tipo de dato:
- df.columns: listado de nombres de columnas
- df.dtypes: tipo de dato por columna
- df.shape: cantidad de filas y columnas
- df.info: información más detallada sobre el df
"""

print('Columns:', df.columns)
print('\nTypes:\n', df.dtypes) # muestra el tipo de dato de cada columna
print('\nShape:', df.shape) # muestra cuántas filas y columnas tiene la tabla
print('\nInfo:\n', df.info)

df.info(verbose = True)# verbose imprime resumen completo

"""##### Trabajando con dataframes
A continuación vamos a ver una serie de acciones que podemos realizar con dataframes:

1. crear columnas
2. tipos de datos
3. aplicar funciones
4. seleccionar/filtrar datos
5. eliminar duplicados
6. agregar (append)
7. join/merge
8. agrupar (aggregate)

Algunas de las operaciones que podemos realizar con dataframes de pandas:
Podemos seleccionar una columna de dos maneras:
- **`df["nombre columna"]`**: esto devuelve la columna como un objeto de tipo pandas Series. Se puede usar con nombres que incluyen espacios, sirve para crear columnas y operaciones con y entre columnas existentes.
- **`df.nombre_columna`**: permite acceder a la columna, pero como un atributo del dataframe. Una limitación es que no se puede usar con nombres que incluyen espacios, ni tampoco para crear columnas nuevas. Si para operaciones con y entre columnas existentes.
"""

# Vamos a trabajarcon dataframe de ejemplo:
df = pd.read_excel("tabla_ejemplo_2.xlsx") # ejemplo2
print(df.columns)
print(df.head(3))

"""###### 1) Crear columnas"""

# Creamos una columna nueva con total de inscriptos llamada "inscriptos total"
df["inscriptos_total"] = df["inscriptos_ronda1"] + df["inscriptos_ronda2"]
print(df.head(3))

# Sumemos 2 inscriptos a cada grupo de la ronda 2 y volvamos a calcular el total
df["inscriptos_ronda2"] = df["inscriptos_ronda2"] + 2
df["inscriptos_total"] = df["inscriptos_ronda1"] + df["inscriptos_ronda2"]
print(df.head(3))

# Generemos un id concatenando area y materia, incluyamos un separador
df["area_asignatura"] = df["area"]+"_"+df["asignatura"]

# Generemos una columna que indique estado de inscripcion
df["inscripcion_estado"] = "CERRADA"

df

"""######  2) Tipo de dato
Ya vimos como podemos usar pandas para conocer el tipo de dato de cada columna, usando df.info(verbose=True).
Para ver el tipo de dato de una columna podemos usar:

`df["nombre_columna"].dtype`:
"""

df["inscriptos_total"].dtype

"""###### 3) Aplicar funciones a columnas
Las columnas son objetos iterables sobre los que podemos aplicar una función y afectará a los registros en cada uno de los elementos del array.
Podemos aplicar funciones predefinidas como también funciones propias. Veamos un ejemplo con una función predefinida:
"""

# La función round () redondea al entero más cercano
df["edad_promedio_r"] = round(df["edad_promedio"])

"""También podemos usar `df["nombre_columna"].apply(funcion x)`. Donde `apply()` inserta `df["nombre_columna"]` como parámetro en `funcion x()`.
Apply itera sobre los inputs y aplica la función sobre cada elemento.
"""

df['edad_promedio_r'] = df['edad_promedio'].apply(round)
df

"""Ahora veamos un ejemplo con una función propia:"""

# Primero definimos una función simple
def clasificar_tamano(inscriptos):
    if inscriptos < 30:
        tamano = "Chico"
    else:
        tamano = "Grande"
    return tamano

# Ahora la aplicamos
df['inscriptos_total'].apply(clasificar_tamano)
df['tamano_clase'] = df['inscriptos_total'].apply(clasificar_tamano)
df

"""###### 4) Seleccionar columnas y/o filas
Para seleccionar un sub-conjunto de filas y/o columnas (Slicing) hay distintas alternativas:
"""

# Seleccionamos una columna
df["grupo"]

# Seleccionamos varias columnas (usamos lista de nombres de columnas)
df[["grupo","asignatura","inscriptos_total"]]

# Guardamos una copia como otro dataframe
df_resumen = df[["grupo","inscriptos_total"]].copy()
df_resumen

# Para seleccionar un sub-conjunto de filas podemos usar los índices:

# Seleccionamos las filas 3 a 5
df[3:6] # el límite inferior sí se incluye pero el superior no. sería como indicar el intervalo [3, 6)

# Seleccionamos las primeras 3 filas
df[:3]

# Seleccionamos las últimas 3 filas
df[-3:]

"""Para filtrar usando condiciones:
- Si hay una condición: `df[condición]`
- Si hay más de una condición: `df[(condición1)&/|(condición2)]`

Donde la condición es booleana (evalúa a True o False), de ser 2 o más, debe estar unida por un operador lógico ("&"/"|"). Noten que los operadores lógicos que usamos son "&"/"|" y no "and"/"or". Esto es por cómo está implementado Pandas
"""

df[df["area"]!="Cs. Sociales"]

df[df["inscriptos_total"]<30]

df[(df["inscriptos_total"]<30) & (df["edad_promedio"]>40)] # muestra filas si nro. de inscriptos es menor a 30 Y edad promedio mayor a 40

# También podemos seleccionar según una condición de esta forma:
opciones = ['Física', 'Geografía']
df[df['asignatura'].isin(opciones)]

"""Para combinar filtros de filas y columas:
- **`df.loc[filas,columnas]`**: mencionamos el **nombre/etiquetas** de las columnas y filas que queremos seleccionar. A diferencia de lo que ocurre con slicing, al usar loc el límite superior SI se incluye.
- **`df.iloc[filas,columnas]`**: mencionamos las **posiciones** (como números enteros) de las columnas y filas que queremos seleccionar. En iloc el límite superior NO se incluye.

Nota: muchas veces el label e index de una fila son iguales (numéricos).
"""

# Veamos la diferencia si usamos slicing, loc o iloc
display(df[3:6]) # intervalo [3, 6)
display(df.loc[3:6]) # intervalo [3, 6]
display(df.iloc[3:6]) # intervalo [3, 6)

# En el ej. anterior cuando usamos loc usamos números para seleccionar columnas. ¿Por qué? La etiqueta de las filas eran números!
# Si nuestro df tuviera etiquetas en las filas, sería distinto, por ejemplo:

# Creamos un df con un índice
df_label = df[:3]
index_ = ['Row_1', 'Row_2', 'Row_3']
df_label.index = index_ # seteamos el índice
df_label

#display(df_label.loc[:3]) # ahora usar loc y números da error. hay que usar etiquetas!
display(df_label.loc[["Row_1", 'Row_2']])

# Seleccionando filas y columnas
df.loc[3:4,["grupo","asignatura"]]

df.iloc[3:5,[0,4]]

"""###### 5) Eliminar duplicados

Para eliminar filas y columnas podemos:
- "pisar" el dataframe con la selección de las filas/columnas que SI queremos guardado una nueva copia sobre la anterior.
- usar la función `df.drop()`.
La función `.drop()` toma como argumento una lista de labels, y puede usarse para eliminar filas o columnas. Con el parámetro "axis" definimos si eliminar filas (axis=0, valor por defecto) o columnas (axis=1).
"""

df

# Eliminamos filas
df.drop([0,3,12]) # implícitamente llama axis=0

# Eliminamos columnas
df.drop(["inscripcion_estado"], axis=1) # no guarda

# Para guardar podemos pisar (df = ...) o usar inplace=True
df.drop(["inscripcion_estado"], axis=1, inplace = True )

df_cut = df.drop([0,3,12])

"""###### 6) Agregar (append)
Python nos permite trabajar con múltiples bases al mismo tiempo. Si queremos agregar un conjunto de bases, **una debajo de la otra**, podemos usar `df_a.append(df_b)` para _appendear_ las bases df_a y df_b
"""

# Carguemos una recortada de la base
df_a = pd.read_excel("tabla_ejemplo_3a.xlsx") # exploren contenido
print(df_a.shape)

df_b = pd.read_excel("tabla_ejemplo_3b.xlsx") # exploren contenido
print(df_b.shape)

df = pd.concat([df_a, df_b])
print(df.shape)

"""Es una buena práctica inspeccionar los resultados después de hacer un append o merge. Por ejemplo, luego del append, la indexación de las filas quedó repetida ya que se preservaron los índices de las bases originales. Para arreglar esto:"""

# luego del .append ()
df = df.reset_index(drop=True) # index original es descartado

"""###### 7) Join/merge
Podemos usar las funciones `.join()` y `.merge()` para **unir horizontalmente** bases con un identificador común.
Veamos el caso de `.merge()` (join es similar, lo pueden ver en la [documentación de Pandas](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html)).

La función merge se aplica con la forma:
`df_a.merge(df_b, on=lista_columnas_id, how=tipo_join)`. Donde:
* lista_columnas_id son los nombres de la/s columna/s por los que vamos a unir las bases. Estas columnas deben encontrarse en ambos DataFrames. Si no se pasa ningún valor (y no se combinand índice, es decir que left_index y right_index son False), se deducirá que se debe hacer el merge con la intersección de las columnas en los DataFrames.
* Los tipos de joins son:
    - **left join**: preserva el 100% de las filas que tiene la tabla _de la izquierda_ del merge, y agrega las columnas del dataset _de la derecha_ con los valores (cuando hay una coincidencia) o las llena con valores nulos (cuando no hay coincidencia). Si el dataset de la derecha tiene valores para filas que no están presentes en el dataset de la izquierda, simplemente no se utilizan. El dataset resultado tiene la misma cantidad de filas que el dataset de la izquierda.
    - **right join**: es igual que el anterior, pero se preservan las filas del dataset de la derecha en lugar de las del de la izquierda.
    - **inner join**: sólo se mantienen aquellas filas que coinciden _en ambos datasets_. Si alguna fila no tiene coincidencia en uno de los dos, se descarta. El dataset final tiene igual cantidad o menos filas que el dataset más grande.
    - **outer join**: se preservan todas las filas. Si hay coincidencia, se cruzan, y si no hay coincidencia se apilan llenando con valores nulos.

El tipo de join más común que van a utilizar la mayoría de las veces es el **left join**, que se una cuando se tiene una tabla, y se quiere enriquecerla con nuevas columnas.

<img src="https://miro.medium.com/v2/resize:fit:1200/1*9eH1_7VbTZPZd9jBiGIyNA.png"
     width=400/>
"""

# Ejemplo de merge
print(df.columns)

# Abrimos otra base y vemos sus columnas
df_c = pd.read_excel("tabla_ejemplo_3c.xlsx") # exploren contenido
print(df_c.columns)

# Hacemos el merge y vemos sus columnas
df = df.merge(df_c) # exploren para ver resultado
print(df.columns)
df

# Vuelvo a descargar el c para que se duplique
df_d = pd.read_excel("tabla_ejemplo_3c.xlsx") # exploren contenido
df = df.merge(df_d) # exploren para ver resultado
print(df.columns)
df

"""Dependiendo de los datos que estemos usando, o si las bases no están bien curadas, realizar un merge puede generar duplicación de registros.
En este caso lo simulamos. Para eliminar registros duplicados:
"""

df.tail(6)
df.drop_duplicates(inplace=True)
df # cómo quedó el índice de las filas ?

df.reset_index(drop=True, inplace=True) # inplace guarda el resultado
df

"""###### 8) agrupar (aggregate)
Una operación frecuente con dataframes es agregar los datos, agrupando sobre un conjunto de variables y aplicando una función de agregación a otras. Con pandas esto se logra usando la función `.groupby()`, de la forma:
`df.groupby(by=lista_columnas_agrupamiento).agg(dict_var_func)`

Donde lista_columnas_agrupamiento es una lista con los nombres de columnas sobre las que se agrupa, y dict_var_func es un
diccionario de variable a agregar (clave) y la función con la que se agrega (valor).

Algunas de las funciones de agregación son:
- sum
- mean
- count
- first / last
- min / max
"""

# Seguimos con el mismo df ya definido
df_agg = df.groupby(by=["area","asignatura"]).agg({"inscriptos_ronda1":"sum","inscriptos_ronda2":"sum","edad_promedio":"mean"})

# Si observan el resultado verán que las variables de agrupamiento pasan a definir el índice
df_agg

# Si queremos que vuelva a ser un índice numérico hacemos:
df_agg.reset_index(inplace = True) # drop = False por default
# Vean que de esta forma, area y asignatura volvieron a ser columnas de la tabla
df_agg







