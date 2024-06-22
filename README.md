
# Log Processor for IIS to SQLite

## Descripción

Este script está diseñado para procesar archivos de registro (logs) del Servidor de Información de Internet de Microsoft (IIS) y almacenar los datos extraídos en una base de datos SQLite. Esto es útil para análisis posteriores y para mantener un almacenamiento centralizado y fácilmente accesible de los registros de actividad del servidor web.

## Características

- **Lectura de archivos `.log`**: Procesa archivos con la extensión `.log`, típicamente generados por IIS.
- **Extracción de datos**: Analiza cada línea del archivo de log para extraer datos relevantes basados en la estructura predefinida del log de IIS.
- **Almacenamiento en SQLite**: Inserta los registros en una base de datos SQLite, permitiendo consultas y análisis adicionales.
- **Manejo de codificaciones**: Soporta la lectura de archivos en diferentes codificaciones, ajustándose a variaciones comunes en los archivos de log.

## Requisitos

- Python 3.x
- Bibliotecas de Python:
  - `sqlite3`: para la gestión de la base de datos SQLite.
  - `tqdm`: para mostrar barras de progreso durante el procesamiento.

Para instalar las dependencias necesarias, puedes usar el siguiente comando:

\```bash
pip install tqdm
\```

## Uso

1. **Coloca el script en tu directorio de trabajo**: Asegúrate de que el script `script.py` esté en el directorio desde donde deseas ejecutarlo.

2. **Prepara tus archivos de log**: Coloca los archivos de log de IIS con la extensión `.log` en un directorio accesible.

3. **Ejecuta el script**: Utiliza la línea de comandos para ejecutar el script con los siguientes parámetros:

\```bash
python script.py <ruta_carpeta_logs> <ruta_base_datos>
\```

- `<ruta_carpeta_logs>`: La ruta completa al directorio que contiene los archivos `.log`.
- `<ruta_base_datos>`: La ruta donde deseas que se cree el archivo de la base de datos SQLite.

### Ejemplo de Uso

\```bash
python script.py C:\Logs C:\Database\logs.db
\```

## Estructura de la Base de Datos

La base de datos SQLite contiene una tabla llamada `logs` con las siguientes columnas:

- `date`: Fecha del registro.
- `time`: Hora del registro.
- `s_ip`: IP del servidor.
- `cs_method`: Método HTTP utilizado (GET, POST, etc.).
- `cs_uri_stem`: El recurso que fue accedido.
- `cs_uri_query`: La consulta realizada.
- `s_port`: Puerto del servidor.
- `cs_username`: Nombre de usuario que realizó la solicitud.
- `c_ip`: IP del cliente.
- `cs_user_agent`: Agente de usuario del cliente.
- `cs_referer`: Referente de la solicitud.
- `sc_status`: Código de estado HTTP de la respuesta.
- `sc_substatus`: Subcódigo de estado.
- `sc_win32_status`: Código de estado de Windows.
- `time_taken`: Tiempo tomado para completar la operación en milisegundos.

## Contribuciones

Las contribuciones al proyecto son bienvenidas. Si deseas mejorar el script o agregar nuevas funcionalidades, considera clonar el repositorio y realizar tus propuestas a través de pull requests.

## Licencia

Este proyecto es de dominio público. Siéntete libre de usarlo, modificarlo y distribuirlo como desees.
