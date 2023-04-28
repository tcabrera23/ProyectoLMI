from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import csv
from googleapiclient.http import MediaFileUpload
import requests
import datetime
import csv
from googleapiclient.discovery import build

# Función para leer los equipos y partidos de un archivo CSV
def leer_equipos(ruta_archivo):
    equipoLocal = []
    equipoVisitante = []
    with open(ruta_archivo, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            equipoLocal.append(row['equipoLocal'])
            equipoVisitante.append(row['equipoVisitante'])
    return equipoLocal, equipoVisitante

# Función para leer los resultados modificados de un archivo CSV
def leer_resultados_modificados(ruta_archivoResultados):
    golesEquipoLocal = []
    golesEquipoVisitante = []
    with open(ruta_archivoResultados, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            golesEquipoLocal.append(row['golesEquipoLocal'])
            golesEquipoVisitante.append(row['golesEquipoVisitante'])
    return golesEquipoLocal, golesEquipoVisitante

# Función para calcular los puntos de los usuarios
def puntuarResultado(equipoLocal, equipoVisitante, golesEL, golesEV):
    resultado = []
    for i in range(10):
        if(golesEL[i] > golesEV[i]):
            resultado.append(equipoLocal[i])

        elif(golesEL[i] < golesEV[i]):
            resultado.append(equipoVisitante[i])

        elif(golesEL[i] == golesEV[i]): 
            resultado.append("Empate")
            
        else: 
            resultado.append("Partido sin disputar") 
    return resultado   

rutaArchivoJornadas = ('Archivos/jornada.csv')    
equipoLocal, equipoVisitante = leer_equipos(rutaArchivoJornadas)

ruta_archivoResultados = ('Archivos/resultadosModificados.csv') 
golesEL, golesEV = leer_resultados_modificados(ruta_archivoResultados)

respuestaCorrecta = puntuarResultado(equipoLocal, equipoVisitante, golesEL, golesEV)

SCOPES = ["https://www.googleapis.com/auth/forms.body", "https://www.googleapis.com/auth/spreadsheets"]
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage('Archivos/token.json')
creds = None
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('Archivos/credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)

# Configurar la API de Google Sheets
service = build('sheets', 'v4', credentials=creds)

# Crear una nueva hoja de cálculo en la carpeta especificada
spreadsheet_id = '1C75Q1MHYz0B0rfXhFlDdStzJhAvTPrL-CsfPU3WPbGE'
sheet_name = 'Puntajes Usuarios'

sheet_body = {
    "requests": [
        {
            "addSheet": {
                "properties": {
                    "title": sheet_name,
                    "gridProperties": {
                        "rowCount": len(respuestaCorrecta) + 1, # +1 para incluir la fila de encabezado
                        "columnCount": 2 # Dos columnas: usuario y puntosTotales
                    }
                }
            }
        }
    ]
}

sheet_response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=sheet_body).execute()
sheet_id = sheet_response['replies'][0]['addSheet']['properties']['sheetId']

# Cargar los puntajes de los usuarios en la nueva hoja de cálculo
user_column = []
points_column = []

# Obtener el nombre de usuario y los puntos totales de cada usuario
for i, resultado in enumerate(respuestaCorrecta):
    user_column.append("Usuario " + str(i+1))
    points_column.append(sum([resultado == "Empate" for resultado in respuestaCorrecta[:i+1]]))

# Agregar los datos en la hoja de cálculo
data = [
    user_column,
    points_column
]

body = {
    'values': data
}

range_name = sheet_name + '!A1:B' + str(len(respuestaCorrecta) + 1)  # +1 para incluir la fila de encabezado

# Actualizar los datos en la hoja de cálculo
result = service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id, range=range_name,
    valueInputOption='RAW', body=body).execute()
print("{0} celdas actualizadas.".format(result.get('updatedCells')))
