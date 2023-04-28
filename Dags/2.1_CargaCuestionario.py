from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import csv
from googleapiclient.http import MediaFileUpload
import requests
from datetime import datetime, timedelta

SCOPES = "https://www.googleapis.com/auth/forms.body"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage('Archivos/token.json')
creds = None
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('Archivos/credentialsAfterGoogleDrive.json', SCOPES)
    creds = tools.run_flow(flow, store)

form_service = discovery.build('forms', 'v1', http=creds.authorize(
    Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

# Request body for creating a form
NEW_FORM = {
    "info": {
        "title": "Porras PL 22/23 - Version de prueba",
        "documentTitle": "Formulario premier"
    },
}

# Creates the initial form
result = form_service.forms().create(body=NEW_FORM).execute()

NEW_QUESTION = {
    "requests": []
}

NEW_QUESTION["requests"].insert(0, {
    "createItem": {
        "item": {
            "title": "Usuario de Discord",
            "questionItem": {
                "question": {
                    "required": True,
                    "textQuestion": {}
                }
            }
        },
        "location": {
            "index": 0
        }
    }
})

# Abrimos el archivo de los partidos
def leer_equipos(ruta_archivo):
    equipoLocal = []
    equipoVisitante = []
    with open(ruta_archivo, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            equipoLocal.append(row['equipoLocal'])
            equipoVisitante.append(row['equipoVisitante'])
    return equipoLocal, equipoVisitante

rutaArchivoJornadas = ('Archivos/jornada.csv')    
equipoLocal, equipoVisitante = leer_equipos(rutaArchivoJornadas)
    
def leer_resultados_modificados(ruta_archivoResultados):
    # Abrimos el archivo de los resultados
    with open(ruta_archivoResultados, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        golesEquipoLocal = []
        golesEquipoVisitante = []
        
        for row in reader:
            golesEquipoLocal.append(row['golesEquipoLocal'])
            golesEquipoVisitante.append(row['golesEquipoVisitante'])
    return golesEquipoLocal, golesEquipoVisitante

ruta_archivoResultados = ('Archivos/resultadosModificados.csv') 
golesEL, golesEV = leer_resultados_modificados(ruta_archivoResultados)

def puntuarResultado(equipoLocal,equipoVisitante, golesEL, golesEV):
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


respuestasCorrectas = puntuarResultado(equipoLocal, equipoVisitante, golesEL, golesEV)

# Cargo las preguntas
for i in range(10):
    question_title = equipoLocal[i] + " vs " + equipoVisitante[i]
    new_question = {
        "createItem": {
            "item": {
                "title": question_title,
                "questionItem": {
                    "question": {
                        "required": True,
                        "shortAnswerQuestion": {}
                    },
                    
                },
            },
            "location": {
                "index": i+1
            }
        } 
    }

    NEW_QUESTION["requests"].append(new_question)


idFormulario = result["formId"]
get_result = form_service.forms().get(formId=idFormulario).execute()

# Request body to add description to a Form
updateBody = {
    "requests": [{
        "updateFormInfo": {
            "info": {
                "description": "Todos a hacer las porras de la jornada 29.\n\nEl partido elegido como estrella esta fecha es el Fulham-Arsenal. Acertar el resultado exacto puede darte un empujón a la gloria.\n\nLa semana pasada solo un usuario acertó un goleador. ¿Te atreves a volver a intentarlo?\n\nEl ganador de la jornada tendrá un rol exclusivo y sumará 3 puntos para su equipo Premier League. Los cinco primeros una vez acaben la temporada también sumarán para sus clubes.\n\nEn la descripción de las preguntas tenéis cómo se puntúa en esta nueva etapa. ¡Suerte!'"
            },
            "updateMask": "description"
        }
    }]
}

# Update the form with a description
question_setting = form_service.forms().batchUpdate(
    formId=idFormulario, body=updateBody).execute()

# Agrega las preguntas
question_setting = form_service.forms().batchUpdate(
    formId=idFormulario,
    body={
        "requests": [
            NEW_QUESTION["requests"]
        ]
    }
).execute()

print(NEW_QUESTION)