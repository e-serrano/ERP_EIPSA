import psycopg2
from config import config

# Establecer la conexión a la base de datos
params = config()
# connect to the PostgreSQL server
conn = psycopg2.connect(**params)
cur = conn.cursor()

# Consultar el nombre de todas las tablas en el esquema "prueba"
query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'logging' AND table_type = 'BASE TABLE';"
cur.execute(query)

# Obtener los resultados de la consulta
rows = cur.fetchall()

# Recorrer los resultados y mostrar los nombres de las tablas
list_tables=[]
for row in rows:
    list_tables.append(row[0])
print(list_tables)

# Cerrar el cursor y la conexión
cur.close()
conn.close()