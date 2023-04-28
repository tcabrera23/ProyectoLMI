import csv

# Crear una funcion que mea lea el archivo en CargaForms
# Voy a tener que definir las listas 

# Abrimos el archivo de los resultados
with open('Archivos/resultadosModificados.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    golesEquipoLocal = []
    golesEquipoVisitante = []
    equipoLocal = []
    equipoVisitante = []
    for row in reader:
        golesEquipoLocal.append(row['golesEquipoLocal'])
        golesEquipoVisitante.append(row['golesEquipoVisitante'])
        equipoLocal.append(row['equipoLocal'])
        equipoVisitante.append(row['equipoVisitante'])


def puntuarResultado(equipoLocal, golesEquipoLocal, equipoVisitante, golesEquipoVisitante):
    resultado = []
    for i in range(10):
        if(golesEquipoLocal[i] > golesEquipoVisitante[i]):
            resultado.append(equipoLocal[i])

        elif(golesEquipoLocal[i] < golesEquipoVisitante[i]):
            resultado.append(equipoVisitante[i])

        elif(golesEquipoLocal[i] == golesEquipoVisitante[i]): 
            resultado.append("Empate")
            
        else: 
            resultado.append("Partido sin disputar") 
    return resultado   


viendoResultados = puntuarResultado(equipoLocal, golesEquipoLocal, equipoVisitante, golesEquipoVisitante)
print(viendoResultados)


  
# Extraer el google sheet y ordenar lista de usuarios por campo puntos en orden descendente
# Este proceso se tiene que hacer 3 dias despues de la creacion del cuestionario