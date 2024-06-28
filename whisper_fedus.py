import os
from dotenv import load_dotenv
from openai import OpenAI
from fpdf import FPDF
from pydub import AudioSegment

load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPENAI_AI_KEY")

client = OpenAI(api_key=OPEN_AI_API_KEY)

def transcribe_audio(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return transcription.text

#function principal
def meeting_minutes(transcription):
    abstract_summary = abstract_summary_extraction(transcription)
    key_points = key_points_extraction(transcription)
    action_items = action_item_extraction(transcription)
    sentiment = sentiment_analysis(transcription)
    return {
        'sumario': abstract_summary,
        'puntos_clave': key_points,
        'elementos_de_accion': action_items,
        'sentimientos': sentiment
    }

def abstract_summary_extraction(transcription):
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "Eres una IA altamente cualificada y entrenada en comprensión y resumen lingüístico. Me gustaría que leyeras el siguiente texto y lo resumieras en un párrafo conciso en español. Intente retener los puntos más importantes, proporcionando un resumen coherente y legible que pueda ayudar a una persona a entender los puntos principales de la discusión sin necesidad de leer todo el texto. Evite detalles innecesarios o puntos tangenciales."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response.choices[0].message.content

def key_points_extraction(transcription):
    response = client.chat.completions.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "Usted es un experto en inteligencia artificial especializado en destilar la información en puntos clave. A partir del siguiente texto, identifique y enumere los puntos principales que se han debatido o planteado. Deben ser las ideas, conclusiones o temas más importantes que son cruciales para la esencia del debate. Su objetivo es proporcionar una lista que alguien pueda leer para comprender rápidamente de qué se habló."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response.choices[0].message.content

def action_item_extraction(transcription):
    response = client.chat.completions.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "Usted es un experto en IA que analiza conversaciones y extrae elementos de acción. Revisa el texto e identifica las tareas, asignaciones o acciones que se acordaron o se mencionaron como necesarias. Puede tratarse de tareas asignadas a personas concretas o de acciones generales que el grupo haya decidido emprender. Enumere estas acciones de forma clara y concisa."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response.choices[0].message.content

def sentiment_analysis(transcription):
    response = client.chat.completions.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "Como IA experta en análisis del lenguaje y las emociones, su tarea consiste en analizar el sentimiento del siguiente texto. Tenga en cuenta el tono general de la discusión, la emoción transmitida por el lenguaje utilizado y el contexto en el que se utilizan las palabras y frases. Indique si el sentimiento es en general positivo, negativo o neutro, y explique brevemente su análisis siempre que sea posible."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response.choices[0].message.content

def voice_transcription(text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input= text
    )
    return response.stream_to_file("audio/MinutesVoice.wav")

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Minutas', 0, 1, 'C')
        self.ln(10)
    
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body, 'J')
        self.ln()

def save_as_pdf(minutes, filename):
    pdf = PDF()
    pdf.add_page()
    for key, value in minutes.items():
        heading = ' '.join(word.capitalize() for word in key.split('_'))
        pdf.chapter_title(heading)
        pdf.chapter_body(value)
    pdf.output(filename)

# audio_file_path = AudioSegment.from_wav("audio/junta_lunes_24_06_2024.wav")
# ten_minutes = 10 * 60 * 1000

# first_ten_minutes = audio_file_path[:ten_minutes]

audio_file_path = "audio/junta_lunes_24_06_2024.wav"
transcription = transcribe_audio(audio_file_path)
minutes = meeting_minutes(transcription)
print(minutes)

save_as_pdf(minutes, 'pdf/meeting_minutes.pdf')
voice_transcription(minutes['sentimientos'])