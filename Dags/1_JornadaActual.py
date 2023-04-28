import requests
from bs4 import BeautifulSoup
import csv

def obtener_jornada(url: str, jornada: int) -> str:
    # Hacemos una solicitud HTTP al sitio web
    response = requests.get(url)

    # Creamos el objeto BeautifulSoup y extraemos la tabla
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.select(f'#jornada-{jornada} table tbody')[0]

    # Defino las cabeceras
    cabeceras = ['equipoLocal', 'equipoVisitante']

    # Abrimos el archivo CSV para escribir los datos
    with open('Archivos/jornada.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        csvfile.write(','.join(cabeceras) + '\n')
        # Recorremos las filas de la tabla y extraemos los datos de cada celda
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            equipo_local = cells[0].text.strip()
            equipo_visitante = cells[2].text.strip()

            # Escribimos los datos en el archivo CSV
            writer.writerow([equipo_local, equipo_visitante])

    # Cerramos el archivo
    csvfile.close()
    
    return 'Archivos/jornada.csv'

url = "https://argentina.as.com/resultados/futbol/inglaterra/calendario/"
jornada = 30
ruta_csv = obtener_jornada(url, jornada)
print(f"El archivo se guardo en {ruta_csv}")
