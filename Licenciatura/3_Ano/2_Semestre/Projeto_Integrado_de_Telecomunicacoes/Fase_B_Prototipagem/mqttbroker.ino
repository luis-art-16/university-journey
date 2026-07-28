#include <WiFi.h>           // Biblioteca WiFi para ESP32
#include <PubSubClient.h>   // Biblioteca MQTT

// Configurações WiFi
const char* ssid = "SUA_REDE_WIFI";
const char* password = "SUA_SENHA_WIFI";

// Configurações MQTT
const char* mqtt_server = "192.168.x.x";  // IP do seu PC (local)
const int mqtt_port = 1883;
const char* mqtt_client_id = "HealthSync_Sensor_001"; // ID único para cada sensor

WiFiClient espClient;                     // Cliente WiFi
PubSubClient client(espClient);           // Cliente MQTT

// Tópicos MQTT
const char* temp_topic = "001/temperatura";
const char* hr_topic = "001/frequencia_cardiaca";
const char* spo2_topic = "001/oxigenacao";
const char* movement_topic = "001/movimento";
const char* config_topic = "001/config";

void setup() {
  Serial.begin(115200);
  
  // Conecta ao WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Conectado ao WiFi");
  
  // Configura MQTT
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();
  
  // Seu código principal aqui...
}

void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(mqtt_client_id)) {
      Serial.println("connected");
      client.subscribe(config_topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  // Lidar com mensagens recebidas
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  if (String(topic) == config_topic) {
    if (message == "stop") {
      // Parar a recolha de dados
    } else if (message.startsWith("interval:")) {
      int newInterval = message.substring(9).toInt();
      // Aplicar novo intervalo
    }
  }
}