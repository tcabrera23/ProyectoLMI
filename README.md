Actualmente me encuentro trabajando en un proyecto que siempre tuve muchas ganas de hacer, debido a que involucra a la comunidad de La Media Inglesa. 

Para estar en contexto: 

El año pasado en nuestro servidor de discord, los seguidores del canal, participábamos en "Las porras de la jornada" que constaba en entrar a un formulario de Google y tratar de predecir por cada fecha, los resultados en la Premier League. Luego, el responsable compartía un Excel con la clasificación de los participantes. Para divertirse estaba muy bien, pero el proceso tenía sus lagunas, ya que solo se encargaba una o pocas personas y lo hacían de forma manual. Además, si ocurría alguna anomalía, como por ejemplo la suspensión de partidos por la muerte de la Reina Isabel, luego podría resultar ser muy tedioso el volver a revisar que votó cada uno y actualizarlo en Excel (teniendo en cuenta que pueden pasar varios meses para jugar el partido pendiente). A los meses quienes se encargaban lo dejaron de hacer. Actualmente hay otra persona a cargo, pero la clasificación se reinició y sigue sin ser óptimo. 

Es por esto que pensé en diseñar un sistema que funcione de forma automatizada y sea capaz de: 
- Crear el formulario de Google con los partidos a disputarse de la nueva jornada y guardar las elecciones de los usuarios en un archivo csv.
- Una vez pasada la jornada, recolectar de internet los resultados y guardarlos en otro archivo csv.
- A partir del sistema de puntajes definido por la comunidad, comparar los resultados de la jornada con las votaciones de los usuarios y obtener la clasificación en orden descendente por puntos totales.

Las tecnologías que serán utilizadas son:
- Python (Procesos ETL y Chatbot conectado a Discord).
- Excel (Almacenamiento de datos. En caso de que la cantidad de participantes aumente significativamente, se migrará a SQL).
- Airflow (Ejecutará el programa por su propia cuenta en una fecha determinada).

# Pendiente:

- Establecer las respuestas correctas del formulario y obtener los puntos de los usuarios en una hoja de calcúlo (La API de Google Forms no me permite utilizar un cuestionario, posiblemente tendré que hacer el proceso del formulario con Django)
- Optimizar el código con funciones y modúlos
- Definir los DAG y sus dependencias
- Ejecutar en el servidor de Apache Airflow
- Chatbot conectado a Discord