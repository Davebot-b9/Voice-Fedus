import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI
import pyttsx3
import speech_recognition as sr

load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPENAI_AI_KEY")

NAME = 'Fedo'

client = OpenAI(api_key=OPEN_AI_API_KEY)

listener = sr.Recognizer()

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

rate = engine.getProperty('rate')
engine.setProperty('rate', 160)

promt_personal = "Eres una IA avanzada especializada en el análisis y diferenciación de voces. Escucha atentamente las consultas del usuario, las cuales se centran principalmente en temas legales. Responde de manera seria, precisa y clara, asegurándote de interpretar correctamente el contexto y las preguntas formuladas. Tu objetivo es proporcionar información legal clara, útil y resumida, basada en la normativa vigente y las mejores prácticas jurídicas exclusivamente de México. Esta prohibido que generes markdown, negritas o cursiva en el texto de tus respuestas asi como responder temas agenos a cuestiones legales."

def recognize_voice():
    with sr.Microphone() as source:
        print('listening...')
        audio = listener.listen(source)

        try:
            command = listener.recognize_whisper(audio, language='es', model="base")
            print(f'Recognized command: {command}')
            return command.lower()
        except sr.UnknownValueError:
            return talk("Could not understand audio")
        except sr.RequestError:
            return talk("Could not request results; check your network connection")

def talk(text):
    engine.say(text)
    engine.runAndWait()

def get_response(voice):
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
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

def evaluate_consult(response):
    moderation = client.moderations.create(
        model="text-moderation-latest",
        input= f"{response}"
    )
    return moderation

def save_moderation_result(moderation_result, filename):
    with open(filename, 'w') as f:
        moderation_result_dict = moderation_result.dict()
        json.dump(moderation_result_dict, f, indent=4)

def main():
    talk(f"Bienvenido, mi nombre es {NAME}, tu asistente virtual de voz. ¿En qué tema legal puedo ayudarte?")
    while True:
        command = recognize_voice()
        if command:
            response = get_response(command)
            moderation_result = evaluate_consult(command)
            save_moderation_result(moderation_result, 'json/moderation_consult_fedus.json')
            response_clean = response.replace("*","") # type: ignore
            print(f'OpenAI response: {response_clean}')
            talk(response_clean)
        elif command == "":
            talk("Hemos concluido con la asistencia legal. Gracias por su atención.")
            break

if __name__ == "__main__":
    main()