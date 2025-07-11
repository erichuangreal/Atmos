#include <TinyDHT.h>

const int SAMPLING_RATE = 1; // Define the sampling rate (in sec)
const int NUM_SAMPLES = 5; // Define the number of samples taken for smoothing

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

float tempSamples[NUM_SAMPLES] = {};
float humSamples[NUM_SAMPLES] = {};
int index = 0;
int count = 0;

// Smoothing function
float getSmoothedAvg(float newSample, float samples[], int size) {
  samples[index] = newSample;
  float sum = 0;
  for (int i = 0; i < size; i++) {
    sum += samples[i];
  }
  return sum / size;
}

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float avgTemp = NAN;
  float avgHum = NAN;
  // Reads sensor output
  float rawHum = dht.readHumidity();
  float rawTemp = dht.readTemperature();
  
  if (!isnan(rawTemp) && !isnan(rawHum)) {
    // Implementing smoothing
    if (count < NUM_SAMPLES) {
      tempSamples[count] = rawTemp;
      humSamples[count] = rawHum;
      avgTemp = rawTemp;
      avgHum = rawHum;
      count++;
    } else {
      index = (index + 1) % NUM_SAMPLES;
      avgTemp = getSmoothedAvg(rawTemp, tempSamples, NUM_SAMPLES);
      avgHum = getSmoothedAvg(rawHum, humSamples, NUM_SAMPLES);
    }
    

    // Print averaged temp and hum to terminal
    String text = String(avgTemp, 2) + "," + String(avgHum, 2);
    Serial.println(text);
  } else {
    Serial.println(",,ERROR");
  }
  delay(SAMPLING_RATE*1000);
}
