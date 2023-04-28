import requests
from bs4 import BeautifulSoup
import csv
import lxml

# Hacemos una solicitud HTTP al sitio web
url = "https://argentina.as.com/resultados/futbol/inglaterra/calendario/"
response = requests.get(url)

jornadaActual = 29

# Creamos el objeto BeautifulSoup y extraemos la tabla
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.select(f'#jornada-{jornadaActual} table tbody')[0]

# Defino las cabeceras
cabeceras = ['equipoLocal', 'resultado', 'equipoVisitante']

# Abrimos el archivo CSV para escribir los datos
with open('Archivos/resultados.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    csvfile.write(','.join(cabeceras) + '\n')
    # Recorremos las filas de la tabla y extraemos los datos de cada celda
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        equipo_local = cells[0].text.strip()
        resultado = cells[1].text.strip()
        equipo_visitante = cells[2].text.strip()

        # Escribimos los datos en el archivo CSV
        writer.writerow([equipo_local, resultado, equipo_visitante])
        
# Cerramos el archivo
csvfile.close()
