# Descripción general

Este código utiliza la API de OpenAI para transcribir un archivo de audio, extraer información clave de la transcripción y generar un documento de Microsoft Word con las actas de la reunión.

## Carga de la clave API de OpenAI

El código carga la clave API de OpenAI desde un archivo .env utilizando la biblioteca dotenv.

## Transcripción de audio

La función transcribe_audi<wbr>o() utiliza la API de transcripciones de audio de OpenAI para transcribir un archivo de audio proporcionado en formato WAV.

## Extracción de información clave

La función meeting_minutes<wbr>() toma la transcripción de audio como entrada y extrae la siguiente información clave:

- Resumen abstracto: Un resumen conciso de la discusión.
- Puntos clave: Una lista de los puntos principales debatidos.
- Elementos de acción: Una lista de tareas o acciones acordadas.
- Sentimiento: Un análisis del sentimiento general de la discusión.
Generación de actas de reunión

La función save_as_docx() genera un documento de Microsoft Word con las actas de la reunión. El documento incluye secciones para cada tipo de información clave extraída.

## Flujo del programa

Carga la clave API de OpenAI.
Transcribe el archivo de audio.
Extrae información clave de la transcripción.
Genera un documento de Microsoft Word con las actas de la reunión.

### Bibliotecas utilizadas

- dotenv: Carga variables de entorno desde un archivo .env.
- openai: Interfaz con la API de OpenAI.
- docx: Crea y manipula documentos de Microsoft Word.