from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import csv
from googleapiclient.http import MediaFileUpload
import requests
import datetime
import gspread

SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/forms.body"]
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage('Archivos/token.json')
creds = None
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('Archivos/credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)

form_service = discovery.build('forms', 'v1', http=creds.authorize(
    Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

client = gspread.authorize(creds)
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

respuestaCorrecta = puntuarResultado(equipoLocal, equipoVisitante, golesEL, golesEV)


for i in range(10):
    question_title = equipoLocal[i] + " vs " + equipoVisitante[i]
    question_options = [
        {"value": equipoLocal[i]},
        {"value": "Empate"},
        {"value": equipoVisitante[i]}
    ]
    new_question = {
        "createItem": {
            "item": {
                "title": question_title,
                "questionItem": {
                    "question": {
                        "required": True,
                        "choiceQuestion": {
                            "type": "RADIO",
                            "options": question_options,
                            "shuffle": False,
                             "correctAnswers": [{"value": {respuestaCorrecta[i]}}] # Respuesta correcta lo elimino o dejo por defecto algo que funcione, nose o si tengo que sacarla asi se asigna despues el valor
                        },
                    }
                    }
                },
            "location": {
                "index": i+1
            }
        } 
    }
    
    NEW_QUESTION["requests"].append(new_question)


get_result = form_service.forms().get(formId=result["formId"]).execute()
linkFormulario = get_result['responderUri'] 
idFormulario = result["formId"]
print(linkFormulario)

# Request body to add description to a Form
update = {
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
    formId=result["formId"], body=update).execute()

# Agrega las preguntas
question_setting = form_service.forms().batchUpdate(
    formId=result["formId"],
    body={
        "requests": [
            NEW_QUESTION["requests"]
        ]
    }
).execute()

# preguntas[i] corresponde a NEWQUESTION campo questions osea la lista de preguntas

# Actualizamos las preguntas del formulario
for i in range(len(preguntas)):
    pregunta = preguntas[i]
    respuesta = respuestaCorrecta[i]
    question = {
        'updateItem': {
            'itemId': pregunta,
            'questionItem': {
                'question': {
                    'question': {
                        'required': True,
                        'title': pregunta,
                        'question': {
                            'choiceQuestion': {
                                'options': [
                                    {'value': respuesta},
                                    # Agrega más opciones de respuesta si es necesario
                                ]
                            }
                        }
                    }
                }
            },
            'updateMask': 'question'
        }
    }

    # Actualizamos la pregunta con la respuesta correcta
    form_service.forms().batchUpdate(formId=idFormulario, body=question).execute()

print("Respuestas correctas agregadas a las preguntas del formulario.")