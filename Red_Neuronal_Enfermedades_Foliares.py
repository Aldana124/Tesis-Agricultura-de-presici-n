# Importación de bibliotecas y configuración inicial
# ---------------------------------------------
# Este bloque importa las bibliotecas necesarias para la implementación, como TensorFlow y Keras,
# que manejan la creación y entrenamiento de la red neuronal, así como herramientas para preprocesamiento
# y visualización de datos. También configura la ruta para descargar la base de datos desde Kaggle.

import kagglehub
aryashah2k_mango_leaf_disease_dataset_path = kagglehub.dataset_download('aryashah2k/mango-leaf-disease-dataset')
print('Data source import complete.')

import tensorflow as tf
import keras
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, Dropout, BatchNormalization, Conv2D, MaxPooling2D
from keras import regularizers
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

print("TensorFlow version:", tf.__version__)
print("Keras version:", keras.__version__)

# Carga y configuración inicial de los datos
# ---------------------------------------------
# Define el tamaño de las imágenes, el tamaño del lote y el número de clases.
# Prepara el conjunto de datos descargado para ser procesado por la red neuronal.

data = tf.keras.preprocessing.image_dataset_from_directory(aryashah2k_mango_leaf_disease_dataset_path)
img_size = (224, 224)
batch_size = 64
n_classes = 8

# Preprocesamiento y aumento de datos
# ---------------------------------------------
# Configura un generador de datos que normaliza las imágenes y aplica transformaciones
# como desplazamientos, cizalladura, y rotaciones para aumentar la variedad en los datos
# de entrenamiento y reducir el riesgo de sobreajuste.

datagen = ImageDataGenerator(
    rescale=1./255,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.3,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.20
)

# División de datos para entrenamiento y validación
# ---------------------------------------------
# Separa los datos en dos conjuntos: uno para entrenar el modelo (80%) y otro para validar
# su rendimiento (20%).

print("Datos para entrenamiento:")
train_data = datagen.flow_from_directory(
    aryashah2k_mango_leaf_disease_dataset_path,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)

print("Datos para validación:")
val_data = datagen.flow_from_directory(
    aryashah2k_mango_leaf_disease_dataset_path,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'
)

# Visualización de algunas imágenes
# ---------------------------------------------
# Muestra algunas imágenes del conjunto de datos para verificar la calidad y variabilidad
# de las imágenes que se usarán en el modelo.

plt.figure(figsize=(15, 15))
for images, labels in data.take(1):
    for i in range(9):
        ax = plt.subplot(3, 3, i + 1)
        ax.imshow(images[i].numpy().astype('uint8'))
        ax.axis('off')

# Configuración del modelo preentrenado
# ---------------------------------------------
# Carga un modelo preentrenado (InceptionV3) para reutilizar sus características aprendidas
# en otras bases de datos. Se congelan las capas preentrenadas para que no se actualicen
# durante el entrenamiento.

from tensorflow.keras.layers import Input, GlobalAveragePooling2D

input_layer = Input(shape=(224, 224, 3))
pre_trained = InceptionV3(weights='imagenet', include_top=False, input_tensor=input_layer)

for layer in pre_trained.layers:
    layer.trainable = False

# Añadir capas personalizadas al modelo
# ---------------------------------------------
# Agrega capas densas encima del modelo preentrenado para adaptar el modelo
# a la clasificación de las 8 categorías de enfermedades foliares.

x = pre_trained.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.001))(x)
x = BatchNormalization()(x)
x = Dropout(0.3)(x)
x = Dense(64, activation='relu', kernel_regularizer=regularizers.l1(0.001))(x)
x = BatchNormalization()(x)
x = Dropout(0.3)(x)
output_layer = Dense(8, activation='softmax')(x)

# Construir y compilar el modelo
# ---------------------------------------------
# Une todas las capas para formar un modelo completo y lo compila,
# definiendo el optimizador, la función de pérdida y las métricas.

model = Model(inputs=pre_trained.input, outputs=output_layer)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

# Entrenamiento del modelo
# ---------------------------------------------
# Entrena el modelo usando los datos preprocesados. Se implementan estrategias
# de regularización como Early Stopping y ModelCheckpoint para mejorar el rendimiento
# y evitar sobreajuste.

early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
model_checkpoint = ModelCheckpoint('final.keras', save_best_only=True, monitor='val_loss')

history = model.fit(
    train_data,
    epochs=20,
    validation_data=val_data,
    callbacks=[early_stopping, model_checkpoint]
)

# Evaluación de resultados
# ---------------------------------------------
# Genera gráficos de precisión y pérdida para analizar el desempeño del modelo durante
# el entrenamiento y validación.

plt.plot(history.history['accuracy'], label='Precisión de entrenamiento')
plt.plot(history.history['val_accuracy'], label='Precisión de validación')
plt.xlabel('Épocas')
plt.ylabel('Precisión')
plt.legend()
plt.show()

plt.plot(history.history['loss'], label='Pérdida de entrenamiento')
plt.plot(history.history['val_loss'], label='Pérdida de validación')
plt.xlabel('Épocas')
plt.ylabel('Pérdida')
plt.legend()
plt.show()

# Guardado del modelo y conversión a TensorFlow.js
# ---------------------------------------------
# Guarda el modelo entrenado en formato H5 y lo convierte a un formato compatible
# con TensorFlow.js para su uso en aplicaciones web.

model.save('modelo.h5')

import tensorflowjs as tfjs
!tensorflowjs_converter --input_format keras modelo.h5 carpeta_salida

# Compresión y descarga del modelo
import shutil
shutil.make_archive('modelo', 'zip', 'carpeta_salida')

from google.colab import files
files.download('modelito.zip')
