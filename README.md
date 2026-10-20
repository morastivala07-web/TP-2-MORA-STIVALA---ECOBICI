# TP-2-MORA-STIVALA---ECOBICI
Reporte de entradas, salidas y balances por estación a partir de viajes de bicicletas.
# Reporte operativo de movimientos de Ecobici

# Problema: Quien revisa la operación de una red de bicicletas necesita conocer las salidas y llegadas por estación durante un período. Los viajes incompletos, duplicados o inconsistentes pueden alterar esos conteos.

# Solución: Aplicación de consola en Python que importa viajes desde CSV o JSON, valida los registros y genera un reporte por estación con entradas, salidas y balance neto. El usuario elige un período. Se seleccionan los viajes por su fecha de inicio y se contabilizan ambos extremos de cada viaje seleccionado. El balance se calcula como llegadas menos salidas.

# Datos: Se utilizarán al menos 50 viajes simulados y reproducibles. Cada registro tendrá identificador, inicio, fin, estación de origen y estación de destino. No serán datos reales del servicio Ecobici.

# Resultados
# - Reporte CSV por estación con salidas, llegadas y balance.
# - Archivo de viajes rechazados con sus motivos.

# Alcance y limitaciones: Se controlarán fechas inválidas, fin anterior al inicio, estaciones faltantes e identificadores duplicados. La suma de los balances de todas las estaciones debe ser cero. El balance no representa bicicletas disponibles: no incluye inventario inicial ni reposiciones. La aplicación funcionará por consola, sin conexión en tiempo real.