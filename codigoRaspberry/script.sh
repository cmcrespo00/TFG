#!/bin/bash

#Ejecutar el programa para obtener los datos de Temperatura y Humedad
python sensorTH.py &

#Ejecutar el programa para obtener los datos de la camara
python sensorCamara.py &

echo "Ejecutando programas"
