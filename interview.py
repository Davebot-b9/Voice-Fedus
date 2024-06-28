import os
from dotenv import load_dotenv
from openai import OpenAI
import pyttsx3
import speech_recognition as sr

load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPENAI_AI_KEY")

NAME = 'Ana'

# Inicializa el cliente de OpenAI
client = OpenAI(api_key=OPEN_AI_API_KEY)

listener = sr.Recognizer()

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

rate = engine.getProperty('rate')
engine.setProperty('rate', 145)

promt_personal = "Eres un asistente virtual de IA avanzada especializada en realizar entrevistas para contratar personal de reparto de productos en México. Tu tarea es llevar a cabo una entrevista profesional, escuchando atentamente las respuestas del candidato y formulando preguntas una a una de manera seria, precisa y clara. Asegúrate de realizar una pregunta a la vez, interpreta correctamente el contexto de las respuestas y las preguntas formuladas. Recuerda que está prohibido utilizar markdown, negritas o cursiva en tus respuestas, así como abordar temas ajenos al puesto de reparto de productos."

questions_default = [
    "¿Como te llamas y cual es tu lugar de procedencia?",
    "¿Cuentas con vehiculo personal?",
    "¿Cúal es tu engomado?",
    "¿Tiene licencia para conducir?",
    "¿Has trabajado en reparto?",
    "¿Cuando puedes iniciar a laborar con nosotros?",
]

def recognize_voice():
    with sr.Microphone() as source:
        print('listening...')
        audio = listener.listen(source)

        try:
            command = listener.recognize_whisper(audio, language='es', model="base")
            print(f'Recognized command: {command}')
            return command.lower()
        except sr.UnknownValueError:
            talk("No pude entender el audio")
            return ""
        except sr.RequestError:
            talk("No se pudieron solicitar los resultados; verifica tu conexión de red")
            return ""

def talk(text):
    engine.say(text)
    engine.runAndWait()

def get_response(voice):
    response = client.chat.completions.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": promt_personal
            },
            {
                "role": "user",
                "content": voice
            }
        ],
    )
    return response.choices[0].message.content

# def evaluate_information_complete(response):
#     # Implementa aquí la lógica para evaluar si la información es suficiente para concluir la entrevista
#     # Por ejemplo, puedes contar el número de rondas de preguntas adicionales realizadas y definir un límite.
#     return False  # Modifica esta función según tu criterio de conclusión

def main():
    talk(f"Bienvenido, mi nombre es {NAME}, soy tu asistente el día de hoy. ¿Estás listo para tu entrevista?")
    command = recognize_voice()
    
    if command:
        rounds = 0
        while True:
            rounds += 1
            if rounds >= 6:
                talk("Gracias por tu tiempo, pasaras en un momento con un asesor para continuar con el proceso de reclutamiento. La entrevista ha concluido.")
                break
            response = get_response(command)
            response_clean = response.replace("*", "")  # type: ignore
            print(f'OpenAI response: {response_clean}')
            talk(response_clean)
            command = recognize_voice()

if __name__ == "__main__":
    main()
