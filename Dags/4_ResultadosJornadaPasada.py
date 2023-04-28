import pandas as pd
import re

# Leer el archivo resultados.csv y crear un DataFrame
df = pd.read_csv('Archivos/resultados.csv')

# Extraer los valores de golesLocal y golesVisitante de la columna "resultado"
golesLocal = df['resultado'].apply(lambda x: re.findall(r'^\d+', x)[0]).astype(int)
golesVisitante = df['resultado'].apply(lambda x: re.findall(r'\d+$', x)[0]).astype(int)

# Eliminar la columna "resultado" del DataFrame y agregar las columnas de goles
df.drop('resultado', axis=1, inplace=True)
df.insert(1, 'golesEquipoLocal', golesLocal)
df.insert(2, 'golesEquipoVisitante', golesVisitante)
df.insert(3, 'equipoVisitante', df.pop('equipoVisitante'))

# Guardar el DataFrame modificado en un nuevo archivo CSV
df.to_csv('Archivos/resultadosModificados.csv', index=False)
