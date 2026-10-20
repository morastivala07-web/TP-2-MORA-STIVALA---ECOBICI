# Reporte de movimientos de Ecobici
Mora Stivala
## Problema y solución

Una persona que revisa una red de bicicletas necesita conocer las salidas y llegadas por estación. Contarlas a mano puede llevar tiempo y dar errores si los viajes están repetidos o incompletos.
Este programa permite leer viajes desde CSV o JSON, elegir un período y generar un reporte por estación con salidas, llegadas y balance.

## Instalación y uso

Se necesita Python 3.10 o superior. Hay que descargar el proyecto, extraer el ZIP y abrir la carpeta en Visual Studio Code. No se necesitan bibliotecas externas.
Desde la terminal, en la carpeta principal, ejecutar:
`python src/main.py`

El programa pide el formato (`csv` o `json`) y las fechas inicial y final. Para probarlo, usar `2026-10-01` y `2026-10-07`.
Se seleccionan los viajes por su inicio, incluyendo ambos días, y se cuentan tanto su salida como su llegada, aunque terminen fuera del período.

## Datos

Se usan 50 viajes válidos y 4 registros incorrectos, todos simulados. Cada registro tiene identificador, inicio, fin, origen y destino.
Para volver a generarlos:
`python src/generar_datos.py`
Este comando reemplaza los datos anteriores y siempre genera el mismo conjunto. La procedencia, las variables y las condiciones de uso CC0 1.0 se explican en `data/README.md`.

## Limpieza y validación

Se quitan espacios sobrantes y se registran los cambios. Se rechazan campos faltantes o vacíos, fechas inválidas, identificadores repetidos y viajes cuyo fin no sea posterior al inicio. Se conserva la primera aparición válida de cada identificador.
Una expresión regular comprueba el formato de fecha y datetime verifica que exista. No se inventan valores para completar datos faltantes. Los nombres de estaciones deben coincidir exactamente después de quitar espacios.

## Resultados

En la carpeta outputs se guardan:
- `reporte_estaciones.csv`: salidas, llegadas y balance.
- `rechazos.csv`: registros incorrectos y sus motivos.
- `limpieza.csv`: campos corregidos de los viajes aceptados.

El reporte corresponde al período elegido; los rechazos, a todo el archivo. Las salidas se reemplazan en cada ejecución completada.

Con las fechas del ejemplo se seleccionan 50 viajes:
| Estación | Salidas | Llegadas | Balance |
|---|---:|---:|---:|
| A | 13 | 12 | -1 |
| B | 13 | 13 | 0 |
| C | 12 | 13 | 1 |
| D | 12 | 12 | 0 |

El balance es llegadas menos salidas. La suma de los balances debe ser cero. Si no hay viajes en el período, se informa y se guarda el reporte solo con encabezados.

## Organización del código

- `src/main.py`: recibe las opciones y coordina el programa.
- `src/fuentes.py`: clase base FuenteDatos y lectores CSV y JSON.
- `src/modelos.py`: clase BalanceEstacion, que registra movimientos y calcula el balance.
- `src/pipeline.py`: funciones de validación, limpieza, selección y cálculo.
- `src/exportacion.py`: guarda los resultados.
- `src/generar_datos.py`: genera los datos.
- `tests/test_ecobici.py`: pruebas automáticas.

Los lectores devuelven la misma estructura para que los cálculos funcionen con ambos formatos. Las funciones separan las tareas del programa.

## Pruebas

Desde la carpeta principal, ejecutar:
`python -m unittest discover -s tests -v`
Las pruebas revisan casos normales, entradas inválidas, limpieza, períodos vacíos, selección por inicio y viajes a la misma estación. También comprueban la equivalencia entre CSV y JSON y la conservación de salidas, llegadas y balances.
Si la terminal está dentro de src, los comandos son:
- `python main.py`
- `python generar_datos.py`
- `python -m unittest discover -s ../tests -v`

## Limitaciones

Los datos son ficticios y no describen la operación real de Ecobici. Los horarios se interpretan como locales de Buenos Aires, sin convertir zonas horarias.
El balance no indica bicicletas disponibles: faltan el inventario inicial y las reposiciones. El programa no tiene interfaz web ni conexión en tiempo real.
