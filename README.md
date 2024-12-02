El archivo lfs.ino contiene toda la programación necesaria para el funcionamiento del ESP32 en este proyecto. Este código implementa lo siguiente:

Sensado de condiciones ambientales:

Lectura de datos de sensores como:
Temperatura y humedad (sensor DHT11).
Humedad del suelo.
Intensidad de luz (Lux).
pH del suelo.
Conversión de las lecturas a un formato JSON para su transmisión.
Servidor web integrado:

Configuración de un servidor web que permite alojar la interfaz gráfica de usuario (HTML, CSS, JavaScript).
Soporte para WebSocket para comunicación en tiempo real entre el ESP32 y los clientes.
Conexión WiFi:

El ESP32 se conecta a una red WiFi especificada mediante credenciales.
Proporciona una dirección IP local para el acceso al servidor web.
Actualización de lecturas en tiempo real:

Utiliza WebSocket para enviar lecturas periódicas de los sensores a la interfaz gráfica.
Reintenta automáticamente la conexión WebSocket si se pierde.
Gestión de archivos con LittleFS:

Almacena archivos como index.html, style.css y script.js para que sean servidos al cliente.
LittleFS es usado como sistema de archivos dentro del ESP32.
