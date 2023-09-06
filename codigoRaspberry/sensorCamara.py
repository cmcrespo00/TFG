import RPi.GPIO as GPIO
from picamera import PiCamera
import time
import pymysql
from io import BytesIO
import boto3
from botocore.exceptions import NoCredentialsError
import ffmpeg

#Definir el pin GPIO al que se ha conectado el sensor de movimiento PIR
pin_sensor_movimiento = 11

#Configuración de los pines de la Raspberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_sensor_movimiento, GPIO.IN)

#Inicializar la cámara
camera = PiCamera()

# Detalles de la conexión a la base de datos (Amazon RDS)
host = 'medidasclimaticas.ctpm25au8ifw.eu-west-1.rds.amazonaws.com'
port = 3306  		# El puerto de Mysql es 3306
user = 'admin'
password = '12345678'
database = 'datos_alertas'

# Conectarse a la base de datos
conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
cursor = conn.cursor()

# Crear una tabla en la base de datos para los videos
cursor.execute('''
	CREATE TABLE IF NOT EXISTS videos (
		id INTEGER PRIMARY KEY AUTO_INCREMENT,
		fecha TIMESTAMP,
		nombre_video TEXT
	)
''')
conn.commit()

# Crear una tabla en la base de datos para las capturas (id_video 
# corresponde al identificador del video al que van asociadas las
# capturas)
cursor.execute('''
	CREATE TABLE IF NOT EXISTS capturas (
		id INTEGER PRIMARY KEY AUTO_INCREMENT,
		fecha TIMESTAMP,
		nombre_captura TEXT,
		id_video INTEGER
	)
''')
conn.commit()


# Credenciales de acceso de AWS
aws_access_key_id = '******************'
aws_secret_access_key = '******************'

# Crear una instancia para S3
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Bucket y rutas de archivo
nombre_bucket = 'capturasalertas'
carpeta_capturas = 'capturas/'   #Ruta donde se almacenarán las capturas
carpeta_videos = 'videos/'       #Ruta donde se almacenarán los videos

try:
	while True:
		if GPIO.input(pin_sensor_movimiento):
			print("Movimiento detectado!")
			fecha = time.strftime("%Y-%m-%d_%H:%M:%S")
			
			nombre_video_input = fecha + '.h264'
			ruta_video_input= carpeta_videos + nombre_video_input
			
			nombre_video_output = fecha + '.mp4'
			ruta_video_output = carpeta_videos + nombre_video_output
			
			nombre_captura = fecha + '.jpg'
			ruta_captura = carpeta_capturas + nombre_captura
			
			#Tomar captura cuando haya movimiento
			camera.capture(ruta_captura)
			
			#Iniciar la grabación y guardar el vídeo en un archivo
			camera.start_recording(ruta_video_input)
			stream = BytesIO()

			# Grabar 10 segundos o hasta que el movimiento termine
			start_time = time.time()
			while time.time()-start_time < 10 and GPIO.input(pin_sensor_movimiento):
				camera.capture(stream, format='jpeg')
				stream.seek(0)
				time.sleep(10)

			#Detener la grabación
			camera.stop_recording()
			
			#Convertir vídeo de formato .h264 a .mp4
			ffmpeg.input(ruta_video_input).output(ruta_video_output).run()
			
			# Subir la captura y el video al servicio S3 de amazon
			s3.upload_file(ruta_captura, nombre_bucket, ruta_captura)
			
			s3.upload_file(ruta_video_output, nombre_bucket, ruta_video_output)
			
			# Insertar los datos en la base de datos
			cursor.execute("INSERT INTO videos (fecha, nombre_video) VALUES (%s, %s)", (fecha, ruta_video_output))
			conn.commit()
			
			# Obtener el último valor de ID guardado
			id_video = cursor.lastrowid
			cursor.execute("INSERT INTO capturas (fecha, nombre_captura, id_video) VALUES (%s, %s, %s)", (fecha, ruta_captura, id_video))
			conn.commit()
		
			print("     %s" % fecha)
			print("     Video y captura guardados")
		else:
			print("No se ha detectado movimiento.")
			
		#Espera 10 segundo.
		time.sleep(10)
			
except KeyboardInterrupt:
	print("Programa interrumpido.")

except NoCredentialsError:
	print("Credenciales no disponibles")

except Exception as e:
	print("Error: ", e)

finally:
	conn.close()
	GPIO.cleanup()
