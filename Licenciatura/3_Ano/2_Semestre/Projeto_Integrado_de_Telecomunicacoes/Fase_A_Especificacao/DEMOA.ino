#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"
#include "spo2_algorithm.h"
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <math.h>

// ============================================
// CONFIGURAÇÕES DE REDE
// ============================================
const char* ssid = "NOS-A097";
const char* password = "ARC43TZ3";
const char* mqtt_server = "192.168.56.1";
const int mqtt_port = 1883;
const char* mqtt_client_id = "HealthSync_Sensor_001";

// ============================================
// TÓPICOS MQTT
// ============================================
const char* temp_topic = "sensor/001/temperatura";
const char* hr_topic = "sensor/001/frequencia_cardiaca";
const char* spo2_topic = "sensor/001/oxigenacao";
const char* movement_topic = "sensor/001/movimento";
const char* config_topic = "sensor/001/config";

// ============================================
// PINOS E INSTÂNCIAS
// ============================================
#define RED_PIN 25
#define GREEN_PIN 26
#define BLUE_PIN 27
#define BUZZER_PIN 15
#define ONE_WIRE_BUS 4

MAX30105 particleSensor;
Adafruit_MPU6050 mpu;
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
WiFiClient espClient;
PubSubClient mqttClient(espClient);

// ============================================
// VARIÁVEIS GLOBAIS
// ============================================
// Para cálculo de BPM
const byte RATE_SIZE = 8;
byte rates[RATE_SIZE];
byte rateSpot = 0;
long lastBeat = 0;
float beatsPerMinute, beatAvg;

// Para SpO2
#define BUFFER_SIZE 100
uint32_t irBuffer[BUFFER_SIZE];
uint32_t redBuffer[BUFFER_SIZE];
int bufferIndex = 0;
int32_t spo2;
int8_t validSPO2;

// Para temperatura
float temperatureC;
unsigned long lastTempRequest = 0;
bool tempRequested = false;

// Para MPU6050 (queda)
bool fallDetected = false;
unsigned long lastMPURead = 0;
const int MPU_READ_INTERVAL = 10; // ms

// Timers
unsigned long lastReconnectAttempt = 0;
const unsigned long RECONNECT_INTERVAL = 5000;
unsigned long lastPublish = 0;
const unsigned long PUBLISH_INTERVAL = 2000;

// ============================================
// FUNÇÕES DE CONFIGURAÇÃO
// ============================================
void setupWifi() {
  Serial.print("Conectando a ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println("Endereço IP: ");
  Serial.println(WiFi.localIP());
}

void setupSensors() {
  // MAX30105
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30105 não encontrado");
    while (1);
  }
  particleSensor.setup();
  particleSensor.setPulseAmplitudeRed(0x1F);
  particleSensor.setPulseAmplitudeIR(0x1F);

  // MPU6050
  if (!mpu.begin()) {
    Serial.println("MPU6050 não encontrado");
    while (1);
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  // DS18B20
  sensors.begin();

  // LEDs e Buzzer
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
}

void setup() {
  Serial.begin(9600);
  while (!Serial); // Para placas com USB nativo

  setupWifi();
  setupSensors();

  mqttClient.setServer(mqtt_server, mqtt_port);
  mqttClient.setCallback(mqttCallback);
}

// ============================================
// FUNÇÕES MQTT
// ============================================
void reconnectMQTT() {
  if (millis() - lastReconnectAttempt > RECONNECT_INTERVAL) {
    lastReconnectAttempt = millis();
    
    Serial.print("Tentando conectar ao MQTT...");
    if (mqttClient.connect(mqtt_client_id)) {
      Serial.println("conectado");
      mqttClient.subscribe(config_topic);
    } else {
      Serial.print("falhou, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" tentando novamente em 5s");
    }
  }
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Mensagem recebida [");
  Serial.print(topic);
  Serial.print("] ");
  
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println(message);

  if (String(topic) == config_topic) {
    if (message == "stop") {
      Serial.println("Comando STOP recebido");
    } else if (message.startsWith("interval:")) {
      int newInterval = message.substring(9).toInt();
      Serial.print("Novo intervalo definido: ");
      Serial.println(newInterval);
    }
  }
}

void publishData() {
  if (millis() - lastPublish > PUBLISH_INTERVAL) {
    lastPublish = millis();

    if (!mqttClient.connected()) {
      reconnectMQTT();
      return;
    }

    // Publica todos os dados
    mqttClient.publish(temp_topic, String(temperatureC).c_str());
    mqttClient.publish(hr_topic, String(beatAvg).c_str());
    mqttClient.publish(spo2_topic, String(spo2).c_str());
    mqttClient.publish(movement_topic, String(fallDetected ? "1" : "0").c_str());

    Serial.println("Dados publicados via MQTT");
  }
}

// ============================================
// FUNÇÕES DE LEITURA DE SENSORES
// ============================================
void readMAX30105() {
  long irValue = particleSensor.getIR();
  long redValue = particleSensor.getRed();

  if (irValue > 50000) { // Dedo detectado
    // Detecção de batimento cardíaco
    if (checkForBeat(irValue) == true) {
      long delta = millis() - lastBeat;
      lastBeat = millis();
      
      beatsPerMinute = 60 / (delta / 1000.0);
      if (beatsPerMinute < 255 && beatsPerMinute > 20) {
        rates[rateSpot++] = (byte)beatsPerMinute;
        rateSpot %= RATE_SIZE;
        
        // Calcula média
        beatAvg = 0;
        for (byte x = 0; x < RATE_SIZE; x++)
          beatAvg += rates[x];
        beatAvg /= RATE_SIZE;
      }
    }

    // Cálculo de SpO2
    irBuffer[bufferIndex] = irValue;
    redBuffer[bufferIndex] = redValue;
    bufferIndex++;
    
    if (bufferIndex >= BUFFER_SIZE) {
      bufferIndex = 0;
      maxim_heart_rate_and_oxygen_saturation(irBuffer, BUFFER_SIZE, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);
    }
  }
}

void readDS18B20() {
  if (!tempRequested && millis() - lastTempRequest >= 2000) {
    sensors.requestTemperatures();
    lastTempRequest = millis();
    tempRequested = true;
  } else if (tempRequested && millis() - lastTempRequest >= 750) {
    temperatureC = sensors.getTempCByIndex(0);
    tempRequested = false;
  }
}

void readMPU6050() {
  if (millis() - lastMPURead >= MPU_READ_INTERVAL) {
    lastMPURead = millis();
    
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    
    float aTotal = sqrt(a.acceleration.x*a.acceleration.x + 
                       a.acceleration.y*a.acceleration.y + 
                       a.acceleration.z*a.acceleration.z);
    
    // Lógica simplificada de detecção de queda
    if (aTotal < 5.0) {
      fallDetected = true;
    } else {
      fallDetected = false;
    }
  }
}

// ============================================
// LOOP PRINCIPAL
// ============================================
void loop() {
  if (!mqttClient.connected()) {
    reconnectMQTT();
  }
  mqttClient.loop();

  readMAX30105();
  readDS18B20();
  readMPU6050();
  publishData();

  // Controle de LEDs baseado no estado
  if (fallDetected) {
    digitalWrite(RED_PIN, HIGH);
    digitalWrite(GREEN_PIN, LOW);
    tone(BUZZER_PIN, 1000);
  } else {
    digitalWrite(RED_PIN, LOW);
    digitalWrite(GREEN_PIN, HIGH);
    noTone(BUZZER_PIN);
  }
}