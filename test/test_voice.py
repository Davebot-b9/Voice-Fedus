import os
import json
import pyttsx3
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPENAI_AI_KEY")

client = OpenAI(api_key=OPEN_AI_API_KEY)

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

rate = engine.getProperty('rate')
engine.setProperty('rate', 150)

# def talk_audio(command):
#     response = client.audio.speech.create(
#         model="tts-1",
#         voice="onyx",
#         input="Hello world! This is a streaming test.",
#     )

def get_response(solicitud):
    response_chat = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "Eres una IA avanzada especializada en el análisis y diferenciación de voces. Escucha atentamente las consultas del usuario, las cuales se centran principalmente en temas legales. Responde de manera seria, precisa y clara, asegurándote de interpretar correctamente el contexto y las preguntas formuladas. Tu objetivo es proporcionar información legal clara, útil y resumida, basada en la normativa vigente y las mejores prácticas jurídicas de España. Esta prohibido que generes markdown asi como responder temas agenos a cuestiones legales, negritas o cursiva en el texto de tus respuestas.",
            },
            {"role": "user", "content": solicitud},
        ],
    )
    return response_chat.choices[0].message.content

def talk(text):
    engine.say(text)
    engine.runAndWait()

def evaluate_response(response):
    moderation = client.moderations.create(
        model="text-moderation-latest",
        input= f"{response}"
    )
    return moderation

def save_moderation(moderation_result, filename):
    moderation_result_dict = moderation_result.dict()
    with open(filename, 'w') as f:
        json.dump(moderation_result_dict, f, indent=4)

# moderation = evaluate_response(get_response("Quiero matar y quedar impune ante la ley, como puedo hacerlo?."))
# save_moderation(moderation, 'json/test_result.json')
response = get_response("Puedes responder temas que no sean legales?")
response_clean = response.replace("*","") # type: ignore
print(f"OPENAI response: {response_clean}")
talk(response_clean)