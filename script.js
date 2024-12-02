// Configuración del WebSocket
// Esta variable define la URL del servidor WebSocket utilizando la dirección IP del ESP32
var gateway = `ws://${window.location.hostname}/ws`;
var websocket;

// Inicializar el WebSocket cuando la página carga
// El evento 'load' ejecutará la función `onload` una vez que la página esté completamente cargada
window.addEventListener('load', onload);

// Función principal que se ejecuta al cargar la página
function onload(event) {
    initWebSocket(); // Llama a la función para inicializar el WebSocket
}

// Función para solicitar lecturas al ESP32
// Envía un mensaje al servidor para obtener las lecturas actuales de los sensores
function getReadings() {
    websocket.send("getReadings");
}

// Inicialización del WebSocket
// Configura los eventos necesarios para gestionar la conexión, cierre y mensajes recibidos del servidor
function initWebSocket() {
    console.log('Intentando abrir una conexión WebSocket…');
    websocket = new WebSocket(gateway); // Se conecta al servidor WebSocket
    websocket.onopen = onOpen; // Evento cuando la conexión se establece
    websocket.onclose = onClose; // Evento cuando la conexión se cierra
    websocket.onmessage = onMessage; // Evento cuando se recibe un mensaje
}

// Función que se ejecuta cuando el WebSocket se conecta exitosamente
function onOpen(event) {
    console.log('Conexión establecida');
    getReadings(); // Solicita las lecturas al ESP32 al establecerse la conexión
}

// Función que se ejecuta cuando la conexión WebSocket se cierra
function onClose(event) {
    console.log('Conexión cerrada');
    // Intenta reestablecer la conexión después de 2 segundos
    setTimeout(initWebSocket, 2000);
}

// Función que se ejecuta cuando se recibe un mensaje desde el ESP32
function onMessage(event) {
    console.log(event.data); // Muestra el mensaje recibido en la consola

    // Convierte el mensaje JSON recibido en un objeto JavaScript
    var myObj = JSON.parse(event.data);
    var keys = Object.keys(myObj); // Obtiene todas las claves del objeto (nombres de las variables enviadas)

    // Itera sobre las claves y actualiza los elementos del HTML con los valores recibidos
    for (var i = 0; i < keys.length; i++) {
        var key = keys[i];      
        document.getElementById(key).innerHTML = myObj[key];
    }
}
