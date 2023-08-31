from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connections

# Create your views here.

# ********************************Pagina principal********************************
def paginaprincipal(request):
    return render(request, 'index.html')


# *********************************Pagina perfil**********************************
def perfil(request):
    return render(request, 'perfil.html')

# *********************************Pagina alertas*********************************
def alertas(request):
    bd_alertas = connections['bd_alertas']
    cursor = bd_alertas.cursor()
    cursor.execute('SELECT id, fecha FROM videos')
    datos_alertas = cursor.fetchall()

    return render(request, 'alertas.html', {
        'datos_alertas': datos_alertas
    })

def mostraralerta(request, id_alerta):
    bd_alertas = connections['bd_alertas']
    cursor = bd_alertas.cursor()
    cursor.execute('SELECT id, fecha FROM videos')
    datos_alertas = cursor.fetchall()
    bd_alertas.commit()

    cursor.execute('SELECT fecha FROM videos WHERE id = %s', [id_alerta])
    fecha_alerta = cursor.fetchall()
    bd_alertas.commit()

    cursor.execute('SELECT nombre_video FROM videos WHERE id = %s', [id_alerta])
    video_alerta = cursor.fetchall()
    bd_alertas.commit()

    cursor.execute('SELECT nombre_captura FROM capturas WHERE id = %s', [id_alerta])
    captura_alerta = cursor.fetchall()
    bd_alertas.commit()

    fecha_alerta = fecha_alerta[0][0]
    video_alerta = video_alerta[0][0]
    captura_alerta = captura_alerta[0][0]

    video_alerta_url = f"https://capturasalertas.s3.eu-west-1.amazonaws.com/{video_alerta}"
    captura_alerta_url = f"https://capturasalertas.s3.eu-west-1.amazonaws.com/{captura_alerta}"

    return render(request, 'alerta.html', {
        'datos_alertas': datos_alertas,
        'fecha_alerta': fecha_alerta,
        'video_alerta_url': video_alerta_url,
        'captura_alerta_url': captura_alerta_url
    })


# *******************************Pagina temperatura*******************************
def temperaturas(request):
    bd_sensor = connections['bd_sensor']
    cursor = bd_sensor.cursor()
    cursor.execute('SELECT id, fecha, temperatura FROM medidas')
    datos_sensor = cursor.fetchall()

    return render(request, 'temperaturas.html', {
        'datos_sensor': datos_sensor
    })


# *********************************Pagina humedad*********************************
def humedad(request):
    bd_sensor = connections['bd_sensor']
    cursor = bd_sensor.cursor()
    cursor.execute('SELECT id, fecha, humedad FROM medidas')
    datos_sensor = cursor.fetchall()

    return render(request, 'humedad.html', {
        'datos_sensor': datos_sensor
    })


# ******************************Pagina Quienes Somos******************************
def quienessomos(request):
    return render(request, 'quienessomos.html')


# *************************Pagina politica de privacidad**************************
def privacidad(request):
    return render(request, 'privacidad.html')