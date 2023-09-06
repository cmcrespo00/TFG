import serial
import time
import pymysql

# Abrir el puerto serie al que esta conectado el arduino
ser = serial.Serial("/dev/ttyACM0",9600)

# Detalles de la conexión a la base de datos (Amazon RDS)
host = 'medidasclimaticas.ctpm25au8ifw.eu-west-1.rds.amazonaws.com'
port = 3306  		# El puerto de Mysql es 3306
user = 'admin'
password = '12345678'
database = 'datos_sensor'

# Conectarse a la base de datos
conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
cursor = conn.cursor()

# Crear una tabla en la base de datos
cursor.execute('''
	CREATE TABLE IF NOT EXISTS medidas (
		id INTEGER PRIMARY KEY AUTO_INCREMENT,
		fecha TIMESTAMP,
		temperatura REAL,
		humedad REAL
	)
''')
conn.commit()

try:
	while True:
		# Obtener valores de temperatura y humedad
		datos = ser.readline().decode('utf-8').strip()
		
		if datos.startswith("T:") and "H:" in datos:
			fecha = time.strftime("%Y-%m-%d_%H:%M:%S")
			
			temperatura_comienzo = datos.index("T:") + 2
			humedad_comienzo = datos.index("H:") + 2
				
			temperatura = float(datos[temperatura_comienzo:datos.index(" ", temperatura_comienzo)])
			humedad = float(datos[humedad_comienzo:])
			
			
			print("%s" % fecha)
			print("   La temperatura es de %sº" % temperatura)
			print("   y la humedad es de %s%%." % humedad)
			
			# Insertar los datos en la base de datos
			cursor.execute("INSERT INTO medidas (fecha, temperatura, humedad) VALUES (%s, %s, %s)", (fecha, temperatura, humedad))
			conn.commit()
			
		# Tiempo de espera entre medidas
		time.sleep(900)
		
except KeyboardInterrupt:
	print("Lectura del sensor finalizada.")
	conn.close()
