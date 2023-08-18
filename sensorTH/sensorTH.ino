#include <DHT.h>

// Declarar el tipo de sensor (DHT11)
#define DHTTYPE DHT11   // DHT 11

const int DHTPin = 8;

DHT dht(DHTPin, DHTTYPE);

void setup() {
   Serial.begin(9600);

   dht.begin();
}

void loop() {
   // Leer datos de temperatura y humedad (tarda aproximadamente 250 milisegundos)
   float t = dht.readTemperature();
   float h = dht.readHumidity();

   Serial.print("T:");
   Serial.print(t);
   Serial.print(" H:");
   Serial.print(h);
   Serial.print("\n");

   // Espera de 15 minutos
   delay(900000);
}
