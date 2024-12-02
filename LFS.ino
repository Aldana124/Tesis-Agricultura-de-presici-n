#include <Arduino.h>
#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include "LittleFS.h"
#include <Arduino_JSON.h>
#include <Adafruit_Sensor.h>
#include "DHT.h"
#include "ph_surveyor.h"

// Configuración de los sensores (sección de inicialización de sensores)
// En esta sección se configuran los sensores utilizados: pH, humedad del suelo, DHT (temperatura y humedad), y el sensor de luz.
Surveyor_pH pH = Surveyor_pH(35);
#define humidity 32
#define DHTPIN 33
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
#define light_sensor_pin 34

// Variables de los sensores y control interno
// En esta sección se inicializan las variables necesarias para almacenar datos de los sensores y controlar la lógica interna.
float demo = 2;
int contador = 0;
uint16_t humidity_level = 0;
uint16_t light_level = 0;
float lux = 0;
uint16_t moisture = 0;
uint16_t temperature = 0;
float phhh = 0;

// Configuración de red WiFi (sección de credenciales)
// Credenciales necesarias para la conexión del ESP32 a una red WiFi.
const char* ssid = "iPhone (64)";
const char* password = "DEAP240102";

// Configuración del servidor web y WebSocket (sección de comunicación)
// Se crean los objetos necesarios para manejar el servidor web y las conexiones en tiempo real vía WebSocket.
AsyncWebServer server(80);
AsyncWebSocket ws("/ws");

// Configuración de la estructura JSON (sección de datos)
// Esta sección define una estructura JSON para almacenar y enviar datos de los sensores.
JSONVar readings;

// Temporizador para actualizar lecturas periódicamente
unsigned long lastTime = 0;
unsigned long timerDelay = 3000;

// Función para obtener lecturas de los sensores
// En esta sección se recolectan datos de todos los sensores conectados y se almacenan en formato JSON.
String getSensorReadings() {
  humidity_level = analogRead(humidity);
  humidity_level = map(humidity_level, 2400, 4095, 100, 0) / 2; 
  moisture = dht.readHumidity();
  temperature = dht.readTemperature();
  light_level = analogRead(light_sensor_pin);
  lux = (250.0 / (0.0037 * light_level)) - 25.0;
  phhh = pH.read_ph();

  readings["temperature"] = String(temperature);
  readings["humidity"] = String(moisture);
  readings["soil"] = String(humidity_level);
  readings["pressure"] = String(lux);
  readings["ph"] = String(phhh);

  return JSON.stringify(readings);
}

// Inicialización del sistema de archivos (LittleFS)
// Esta sección prepara el sistema de archivos para alojar contenido como el archivo HTML de la interfaz gráfica.
void initLittleFS() {
  if (!LittleFS.begin(true)) {
    Serial.println("Error al montar LittleFS");
  } else {
    Serial.println("LittleFS montado con éxito");
  }
}

// Configuración de WiFi (sección de conectividad)
// Esta sección establece la conexión a la red WiFi usando las credenciales proporcionadas.
void initWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(1000);
  }
  Serial.println(WiFi.localIP());
}

// Función para notificar clientes a través de WebSocket
// En esta sección se envían las lecturas de los sensores a todos los clientes conectados.
void notifyClients(String sensorReadings) {
  ws.textAll(sensorReadings);
}

// Manejo de mensajes recibidos por WebSocket
// Esta función procesa los mensajes recibidos de los clientes WebSocket y responde con las lecturas de los sensores si es necesario.
void handleWebSocketMessage(void *arg, uint8_t *data, size_t len) {
  AwsFrameInfo *info = (AwsFrameInfo*)arg;
  if (info->final && info->index == 0 && info->len == len && info->opcode == WS_TEXT) {
    String sensorReadings = getSensorReadings();
    notifyClients(sensorReadings);
  }
}

// Eventos del WebSocket (conexión, desconexión, etc.)
// En esta sección se manejan los eventos principales relacionados con los clientes WebSocket.
void onEvent(AsyncWebSocket *server, AsyncWebSocketClient *client, AwsEventType type, void *arg, uint8_t *data, size_t len) {
  switch (type) {
    case WS_EVT_CONNECT:
      Serial.printf("Cliente WebSocket #%u conectado desde %s\n", client->id(), client->remoteIP().toString().c_str());
      break;
    case WS_EVT_DISCONNECT:
      Serial.printf("Cliente WebSocket #%u desconectado\n", client->id());
      break;
    case WS_EVT_DATA:
      handleWebSocketMessage(arg, data, len);
      break;
    case WS_EVT_PONG:
    case WS_EVT_ERROR:
      break;
  }
}

// Inicialización del WebSocket
// Esta sección configura el WebSocket y lo asocia con el servidor web.
void initWebSocket() {
  ws.onEvent(onEvent);
  server.addHandler(&ws);
}

void setup() {
  // Configuración inicial de los sensores, red y servidor
  Serial.begin(115200);
  Serial.println(F("Prueba del sensor DHT"));
  dht.begin();

  if (pH.begin()) {
    Serial.println("EEPROM cargado correctamente");
  }

  initWiFi();
  initLittleFS();
  initWebSocket();

  // Configuración de rutas para el servidor web
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(LittleFS, "/index.html", "text/html");
  });

  server.serveStatic("/", LittleFS, "/");

  // Iniciar el servidor web
  server.begin();
}

void loop() {
  // Lógica principal del sistema (lecturas periódicas y notificaciones)
  if ((millis() - lastTime) > timerDelay) {
    String sensorReadings = getSensorReadings();
    notifyClients(sensorReadings);
    lastTime = millis();

    // Lógica de demostración para controlar la variable `demo`
    contador++;
    if (contador == 20) {
      contador = 0;
      demo = 2.1;
    } else {
      demo = 2;
    }
  }

  // Limpiar clientes desconectados del WebSocket
  ws.cleanupClients();
}
