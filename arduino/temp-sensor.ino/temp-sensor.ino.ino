#include <TinyDHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  int8_t hum = dht.readHumidity();
  float temp = dht.readTemperature();
  if (!isnan(temp) && !isnan(hum)) {
    String text = "Temperature: " + String(temp, 2) + "°C   " +
    "Humidity: " + String(hum) + "%";
    Serial.println(text);
  }
  delay(1000);
}
