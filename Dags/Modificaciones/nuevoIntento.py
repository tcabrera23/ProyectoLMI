# Importar las librerías necesarias
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

import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Definir las credenciales de API
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

cliente = gspread.authorize(creds)

# Abrir la hoja de cálculo de Google Sheets
# Reemplaza 'Nombre de la hoja de cálculo' con el nombre de tu hoja de cálculo de Google Sheets
hoja_calculo = cliente.open('Nombre de la hoja de cálculo').sheet1

formulario = []

# Crear una lista de preguntas de opción múltiple con sus opciones y respuestas correctas
preguntas = ["¿Cuál es tu color favorito?",
             "¿Cuál es tu animal favorito?",
             "¿Cuál es tu comida favorita?",
             "¿Cuál es tu película favorita?",
             "¿Cuál es tu deporte favorito?",
             "¿Cuál es tu pasatiempo favorito?",
             "¿Cuál es tu música favorita?",
             "¿Cuál es tu destino de viaje favorito?",
             "¿Cuál es tu estación del año favorita?",
             "¿Cuál es tu libro favorito?"]

opciones = [["Rojo", "Azul", "Verde"],
            ["Perro", "Gato", "Elefante"],
            ["Pizza", "Sushi", "Hamburguesa"],
            ["Star Wars", "El Padrino", "El Señor de los Anillos"],
            ["Fútbol", "Baloncesto", "Tenis"],
            ["Leer", "Cocinar", "Hacer ejercicio"],
            ["Pop", "Rock", "Hip hop"],
            ["París", "Nueva York", "Tokio"],
            ["Primavera", "Verano", "Otoño"],
            ["Orgullo y prejuicio", "1984", "Cien años de soledad"]]

respuestas_correctas = ["Rojo", "Gato", "Pizza", "Star Wars", "Fútbol", "Leer", "Pop", "París", "Primavera", "Orgullo y prejuicio"]

# Cargar las preguntas y respuestas al formulario
for i in range(len(preguntas)):
    pregunta = preguntas[i]
    opciones_pregunta = opciones[i]
    # Crear la pregunta
    formulario.append_row([pregunta])
    # Crear las opciones de respuesta
    formulario.append_row(opciones_pregunta)

print("Preguntas y respuestas cargadas exitosamente en el formulario de Google.")