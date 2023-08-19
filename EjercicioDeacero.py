# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 17:52:02 2023

@author: josev
"""
#%%
##conseguir datos de api##

import requests
import json
import pandas as pd
Response_API_LineasAereas = requests.get('https://analytics.deacero.com/api/teenus/get-data/fed214f3-332d-522c-97ac-da395a066dba?format=json')

#%% Transformar a tabla
Data_LineasAereas = Response_API_LineasAereas.text
#print(Data_LineasAereas)
LineasAereas_dict = json.loads(Data_LineasAereas)

#transformar en tabla
df_LineasAereas= pd.DataFrame(LineasAereas_dict)

#%%confirmar que jala la tabla
print(df_LineasAereas)

#%%
#repetir#
Response_API_Pasajeros2016 = requests.get('https://analytics.deacero.com/api/teenus/get-data/3689da48-d557-5e5f-8347-006ced354939?format=json')
Response_API_Pasajeros2017 = requests.get('https://analytics.deacero.com/api/teenus/get-data/2a323bb8-0a6d-5bd5-8366-90041c4f1c8c?format=json')
Response_API_Vuelos2016 = requests.get('https://analytics.deacero.com/api/teenus/get-data/2743ebad-f1e2-5eff-8c4d-f8c5191d1775?format=json')
Response_API_Vuelos2017 = requests.get('https://analytics.deacero.com/api/teenus/get-data/a6960833-d5a3-56dc-b125-da9e4e1fce69?format=json')


Data_Pasajeros2016 = Response_API_Pasajeros2016.text
Data_Pasajeros2017 = Response_API_Pasajeros2017.text
Data_Vuelos2016 = Response_API_Vuelos2016.text
Data_Vuelos2017 = Response_API_Vuelos2017.text

#print(Data_Pasajeros2016)
#print(Data_Pasajeros2017)
#print(Data_Vuelos2016)
#print(Data_Vuelos2017)

Pasajeros2016_dict = json.loads(Data_Pasajeros2016)

df_Pasajeros2016 = pd.DataFrame(Pasajeros2016_dict)
print(df_Pasajeros2016)

Pasajeros2017_dict = json.loads(Data_Pasajeros2017)

df_Pasajeros2017 = pd.DataFrame(Pasajeros2017_dict)
print(df_Pasajeros2017)

Vuelos2016_dict = json.loads(Data_Vuelos2016)

df_Vuelos2016 = pd.DataFrame(Vuelos2016_dict)
print(df_Vuelos2016)

Vuelos2017_dict = json.loads(Data_Vuelos2017)

df_Vuelos2017 = pd.DataFrame(Vuelos2017_dict)
print(df_Vuelos2017)

#%% posibles problemas despues de ver
#claramente 1 cliente tiene varios viajes ya que hay 100 clientes para cada año y 200 vuelos, esto no es necesariamente un problema pero se debe mantener en mente
#1 que el id pasajero se repita dentro de la tabla para cada año
#2 que el id pasajero se repita al unir ambos años
#3 la relacion entre tablas se puede hacer con el cve_cliente y el ID Pasajero, esto puede ser un problema si se repite el id pasajero al relacionar las tablas


#%% revisar primero las tablas y ver si se repite el id_Pasajero

df_Pasajeros2016["ID_Pasajero"].nunique()
#df_Pasajeros2016["ID_Pasajero"].nunique()
#Out[71]: 100
#los 100 de 2016 son unique

df_Pasajeros2017["ID_Pasajero"].nunique()
df_Pasajeros2017["Pasajero"].nunique()
df_Pasajeros2017["Edad"].nunique()


#2017 33 son unique 
#por alguna razon 38 nombres son unique y 33 ids son unique
df_Pasajeros2017['ClaveUnica'] = df_Pasajeros2017['ID_Pasajero'].astype(str)+ ' ' + df_Pasajeros2017['Pasajero'].astype(str)+ ' ' + df_Pasajeros2017['Edad'].astype(str)
df_Pasajeros2017['ClaveUnica'].nunique()
df_Pasajeros2017['ClaveUnica'].unique()
print(df_Pasajeros2017.to_string())

print(df_Pasajeros2017['ClaveUnica'])

#estoy confirmando con la clave unica que solo hay 38 pasajeros unicos
#voy a borras los duplicados para quedarme con una tabla de (38,3)


df_Vuelos2016["Cve_Cliente"].nunique()
#86 unique de 200
df_Vuelos2017["Cve_Cliente"].nunique()
#31 unique de 200

#%% soluciones

#quitar duplicados de pasajeros ya que puede resultar en problemas al unir con los vuelos
df_Pasajerosdroptest = df_Pasajeros2017.drop_duplicates(keep='first',subset=["ClaveUnica"])

df_Pasajerosdroptest
df_Pasajerosdroptest["ID_Pasajero"].unique()
df_Pasajerosdroptest["ClaveUnica"].nunique()

df_Pasajeros2017['ClaveUnica'].nunique()
#Hay clientes diferentes con el mismo id pasajero, esto va a ser un problema en el futuro pero primero quiero ver como se comporta
#voy a concatenar las dos tablas de pasajeros para ver que no se repitan aun mas ids
df_Pasajeros2017revisado= df_Pasajeros2017.drop_duplicates(keep='first',subset=["ClaveUnica"])


#%% concatenar 1 tablas 100,3 y una 38,4
#tengo que hacer drop de la columna clave unica
df_Pasajeros2017revisado = df_Pasajeros2017revisado.drop(['ClaveUnica'],axis=1)
#resultado final debe ser una tabla 138,3
framesPasajeros =[df_Pasajeros2016,df_Pasajeros2017revisado]
df_Pasajeros20162017 = pd.concat(framesPasajeros)
print(df_Pasajeros20162017)
#si no comparten datos entre tablas entonces los uniques deben ser 133
df_Pasajeros20162017["ID_Pasajero"].nunique()
#son 133, lo cual significa que se mantiene el problema orignial de los duplicados en el 2017, por el momento no lo voy a cambiar ya que debo entender los vuelos primero para identificar cual de los pasajeros quitar
#quiero generar una variable de id_pasajero+nombre para tener un identificador unico, sin embargo esto no ayuda ya que no se tiene el nombre del cliente en los datos de vuelos. Lo que puedo ver es el año

#%%
#mismo proceso con vuelos, en este caso no creo tener problemas pero de igual manera debo revisar

print(df_Vuelos2016)
print(df_Vuelos2017)

#problemas que pudiera tener, la misma clave en la misma ruta en la misma fecha ya que no creo que sea posible en un caso real
#vuelvo a realizar una clave unica para ver si es el caso

df_Vuelos2016['Cve_Cliente'].nunique()
#######SUPER IMPORTANTE REVISAR EN QUE FECHAS CAEN LOS VUELOS PARA REVISAR TENDENCIAS############

df_Vuelos2016['ClaveUnica'] = df_Vuelos2016['Cve_LA'].astype(str)+ ' ' + df_Vuelos2016['Viaje'].astype(str)+ ' ' + df_Vuelos2016['Clase'].astype(str) + ' ' + df_Vuelos2016['Precio'].astype(str) + ' ' + df_Vuelos2016['Ruta'].astype(str) + ' ' + df_Vuelos2016['Cve_Cliente'].astype(str)

df_Vuelos2016['ClaveUnica'].nunique()

#200 vuelos unicos

#realizar lo mismo para 2017

df_Vuelos2017['Cve_Cliente'].nunique()
df_Vuelos2017['ClaveUnica'] = df_Vuelos2017['Cve_LA'].astype(str)+ ' ' + df_Vuelos2017['Viaje'].astype(str)+ ' ' + df_Vuelos2017['Clase'].astype(str) + ' ' + df_Vuelos2017['Precio'].astype(str) + ' ' + df_Vuelos2017['Ruta'].astype(str) + ' ' + df_Vuelos2017['Cve_Cliente'].astype(str)
df_Vuelos2017['ClaveUnica'].nunique()

#200 vuelos unicos

#%%concatenar  2 tablas de 200,7 debo tener una tabla de 400,7 al final
framesVuelos=[df_Vuelos2016,df_Vuelos2017]
df_Vuelos20162017=pd.concat(framesVuelos)

print(df_Vuelos20162017)
#confirmo tener 400 rows y 7 columnas


#%% RELACIONAR LAS TABLAS
#LA VARIABLE A UTILIZAR ES Cve_Cliente en la tabla de vuelos y ID_Pasajero en tabla de pasajeros
#se que hay 5 ids que no son unique, hasta donde se, no tengo forma de determinar quien es el correcto y quien no. No se puede resolver mediante año ya que los problemas son el mismo año. Quiza tengo que ver los casos individuales.

#identificar claves problema
print(df_Pasajeros20162017.duplicated(subset=["ID_Pasajero"]).to_string())
print(df_Pasajeros20162017.to_string())
# los problemas son 742 717 570 582 562
# los pasajeros problema no son similares en edad o nombre, lo cual indica que de verdad son personas diferentes

df_Pasajeros20162017["Pasajero"].nunique()
#todos los nombres son unicos, por lo cual no se puede hacer espacio para uno de los pasajeros. Tambien significa que el error en ids repetidos no se debe a alguien registrandose en ambos años y de alguna forma causando un error en el segundo año. Voy a tener que hacer un drop aleatoreo de los IDs repetidos

df_Pasajeros20162017revisado = df_Pasajeros20162017.drop_duplicates(keep='first',subset=["ID_Pasajero"])

#revisar que todos son unique
df_Pasajeros20162017revisado
df_Pasajeros20162017revisado["ID_Pasajero"].nunique()

#133 rows de ID_Pasajero y los 133 son unique

#revisar que tengan mismo numero de ids, o minimo que la tabla de vuelos tenga mas

df_Vuelos20162017["Cve_Cliente"].nunique()
df_Pasajeros20162017revisado["ID_Pasajero"].nunique()

#es extraño pero no es problema aun.

#el merge va a ser many to one, es decir, el cliente tiene muplitples viajes con su Cve_Cliente, pero en la tabla de pasajeros solo tiene un ID y una edad
#ponerle el mismo nombre a la variable de ID para que el merge sea atuomatico
df_Pasajeros20162017revisado["Cve_Cliente"] = df_Pasajeros20162017revisado["ID_Pasajero"]

print(df_Pasajeros20162017revisado)

df_Pasajeros20162017revisado = df_Pasajeros20162017revisado.drop(["ID_Pasajero"],axis=1)

print(df_Vuelos20162017)

df_Vuelos20162017
left_df = df_Vuelos20162017
right_df = df_Pasajeros20162017revisado
df_testmerge = left_df.merge(right_df, on="Cve_Cliente", how="left")

df_testmerge.shape

#acabo con una lista de 400 vuelos y 9 columnas. Esto significa que el merge si se hizo como yo lo quería, basandose en la tabla de vuelos

print(df_testmerge)

#%% Como producto final se pida una tabla con las siguientes columnas
# Fecha del viaje-Clase-Precio-Ruta-Edad-Línea Aérea
df_testmerge["Fecha del Viaje"] = df_testmerge["Viaje"]
df_testmerge = df_testmerge.drop(["Viaje"],axis=1)

df_testmerge = df_testmerge.drop(["Pasajero"],axis=1)
print(df_testmerge)
# me gustaría hacer un analisis de los clientes pero eso no es lo que se pide en este caso entonces voy a dropear la Cve Cliente
df_testmerge = df_testmerge.drop(["Cve_Cliente"],axis=1)
df_testmerge = df_testmerge.drop(["ClaveUnica"],axis=1)
#Ya tengo las 6 columnas, Ahora solo tengo que cambial la Linea Aerea
df_testmerge["Code"] = df_testmerge["Cve_LA"]
df_testmerge = df_testmerge.drop(["Cve_LA"],axis=1)

#Lo unico que falta es cambiar el nombre de la Linea Aerea

linea_key = df_LineasAereas

mergelinea = df_testmerge.merge(linea_key,on= "Code", how="left")
mergelinea = mergelinea.fillna("Otra")
mergelinea = mergelinea.drop(["Code"],axis=1)


#%%% Sacar datos adicionales requeridos
#Piden datos trimestrales, entonces voy a cambiar la fecha a formato date time
mergelineatest = mergelinea
mergelineatest["Fecha del Viaje"]=pd.to_datetime(mergelineatest["Fecha del Viaje"])
mergelineatest['half_year'] = mergelineatest['Fecha del Viaje'].dt.month.apply(lambda x: 'Jan-Jun' if x <= 6 else 'Jul-Dec')
mergelineatest["year"] = mergelineatest["Fecha del Viaje"].dt.year



groupedyear= mergelineatest.groupby(["year","half_year"])["Precio"]
precioyear = groupedyear.mean()
print(precioyear)

groupedclase= mergelineatest.groupby(["Clase","half_year"])["Precio"]
precioclase = groupedclase.mean()
print(precioclase)

groupedruta= mergelineatest.groupby(["Ruta","half_year"])["Precio"]
precioruta = groupedruta.mean()
print(precioruta)

groupedlinea= mergelineatest.groupby(["Linea_Aerea","half_year"])["Precio"]
preciolinea = groupedlinea.mean()
print(preciolinea)


