# Por cada nuevo formulario, nueva hoja de calculo

from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import csv
from googleapiclient.http import MediaFileUpload
import requests
import google.auth
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import random
import string

DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
SCOPES = ["https://www.googleapis.com/auth/forms.body", "https://www.googleapis.com/auth/spreadsheets"]

store = file.Storage('Archivos/token.json')
creds = None
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('Archivos/credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)

form_service = discovery.build('forms', 'v1', http=creds.authorize(
    Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)
service = build('sheets', 'v4', credentials=creds)


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
with open('Archivos/jornada.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    equipoLocal = []
    equipoVisitante = []
    for row in reader:
        equipoLocal.append(row['equipoLocal'])
        equipoVisitante.append(row['equipoVisitante'])

# Funcion que carga las preguntas del forms

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
                            "shuffle": False
                        },
                    }
                },
            },
            "location": {
                "index": i+1
            }
        } 
    }
    


    NEW_QUESTION["requests"].append(new_question)


get_result = form_service.forms().get(formId=result["formId"]).execute()
linkFormulario = get_result['responderUri'] 
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

# Print the result to see it now has a description
getresult = form_service.forms().get(formId=result["formId"]).execute()
#print(getresult)

idFormulario = result["formId"]

# Agrega las preguntas
question_setting = form_service.forms().batchUpdate(
    formId=result["formId"],
    body={
        "requests": [
            NEW_QUESTION["requests"]
        ]
    }
).execute()


# Obtener el ID de la hoja de cálculo existente
spreadsheet_id = '1C75Q1MHYz0B0rfXhFlDdStzJhAvTPrL-CsfPU3WPbGE'  # Reemplaza esto con el ID de tu hoja de cálculo existente

# Crear un nombre aleatorio para la nueva hoja
new_sheet_name = "Fecha i+1"

# Crear la nueva hoja de cálculo
request_body = {
    'requests': [{
        'addSheet': {
            'properties': {
                'title': new_sheet_name
            }
        }
    }]
}
response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body).execute()

# Obtener el ID de la nueva hoja de cálculo
new_sheet_id = response['replies'][0]['addSheet']['properties']['sheetId']

print(f'Se ha creado una nueva hoja de cálculo con ID: {new_sheet_id} y se ha agregado a la hoja de cálculo existente.')
