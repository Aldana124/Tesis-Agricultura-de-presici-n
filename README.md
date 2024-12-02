1. index.html
Descripción: Archivo principal que define la estructura y el contenido de la interfaz gráfica de usuario.
Propósito:
Muestra las lecturas de los sensores en tiempo real (temperatura, humedad, pH, luz, y humedad del suelo).
Incluye enlaces y secciones visuales para facilitar la interacción del usuario con el sistema.
Contenido clave:
Títulos y etiquetas organizadas en un diseño de cuadrícula (grid).
Elementos HTML con identificadores (id) que se actualizan dinámicamente con las lecturas de los sensores.
2. style.css
Descripción: Hoja de estilos que define el diseño visual y la disposición de los elementos en la interfaz.
Propósito:
Mejora la experiencia visual de los usuarios, definiendo colores, fuentes y espaciado.
Estiliza las tarjetas individuales que muestran las lecturas de los sensores.
Aspectos destacados:
Estilo limpio y centrado para que la interfaz sea clara y fácil de entender.
Diseño responsivo utilizando grid-template-columns para ajustar las tarjetas automáticamente a diferentes tamaños de pantalla.
3. script.js
Descripción: Archivo JavaScript que controla la lógica de interacción de la interfaz.
Propósito:
Establece y gestiona la conexión con el ESP32 mediante WebSocket.
Solicita lecturas de los sensores y actualiza dinámicamente los valores en la interfaz.
Características clave:
Reintento automático de conexión en caso de fallo.
Conversión de datos JSON enviados por el ESP32 en actualizaciones visibles en la página.
Funcionamiento General
Carga de la interfaz:

Cuando un cliente accede al ESP32, el archivo index.html se carga automáticamente desde el sistema de archivos LittleFS.
Los estilos (style.css) y la funcionalidad (script.js) también son servidos desde el ESP32.
Comunicación en tiempo real:

La conexión WebSocket permite que los datos de los sensores se actualicen en tiempo real sin necesidad de recargar la página.
Visualización:

Las lecturas de los sensores se muestran en tarjetas estilizadas, ofreciendo una interfaz clara y organizada para el monitoreo de las condiciones del campo.
