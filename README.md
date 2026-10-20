# Datos del proyecto

## De dónde salen los datos

Nombre: [Tu nombre y apellido]  
Fecha: 20 de octubre de 2026.
Para este trabajo usé datos simulados, creados con el archivo `src/generar_datos.py`. No son viajes reales de Ecobici.
Hay 54 registros: 50 viajes válidos y 4 registros con errores puestos a propósito para comprobar que el programa los detecte.

## Cómo volver a generarlos

Desde la carpeta principal del proyecto se ejecuta:
`python src/generar_datos.py`
El programa siempre genera los mismos datos, sin usar números aleatorios. Al ejecutarlo, reemplaza los archivos `viajes.csv` y `viajes.json` de la carpeta `data`.

## Qué representa cada registro

Cada registro representa un viaje y tiene estos campos:
- `id_viaje`: identificador del viaje.
- `inicio`: fecha y hora de inicio.
- `fin`: fecha y hora de finalización.
- `origen`: estación de salida.
- `destino`: estación de llegada.

Las fechas tienen el formato `AAAA-MM-DD HH:MM` y se interpretan como horarios locales de Buenos Aires, sin conversiones de zona horaria.
CSV y JSON contienen la misma información, en el mismo orden. Todos los campos están guardados como texto.

## Cómo se armaron los viajes

Se usaron cuatro estaciones ficticias: A, B, C y D.
El primer viaje empieza el 1 de octubre de 2026 a las 08:00. Los siguientes comienzan cada tres horas y duran entre 15 y 44 minutos.
También se agregaron estos errores:
- Un viaje repetido.
- Una fecha que no existe.
- Un viaje que termina antes de empezar.
- Un viaje sin estación de destino.
Además, el origen del primer viaje tiene espacios de más para probar la limpieza.

## Qué hace el programa con los errores

El programa quita los espacios al principio y al final de los campos. Los cambios de los viajes aceptados quedan en `outputs/limpieza.csv`.
Los registros rechazados se guardan en `outputs/rechazos.csv`, con sus datos originales y el motivo. El número de registro empieza en 1; no indica necesariamente la línea del archivo.
Si se repite un identificador, se conserva el primer viaje válido y se rechazan las apariciones posteriores con ese identificador. No se inventan fechas ni estaciones para completar datos faltantes.

## Uso de los datos

Los datos simulados se ofrecen bajo CC0 1.0:  
https://creativecommons.org/publicdomain/zero/1.0/
Esto se aplica a los datos generados para el trabajo. El proyecto no está vinculado con el servicio Ecobici.

## Limitaciones

Estos datos sirven para probar el programa. Como los viajes y las estaciones son ficticios y siguen un patrón fijo, no permiten sacar conclusiones sobre el uso real de Ecobici.
No se incluyen datos personales.