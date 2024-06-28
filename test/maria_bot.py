import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPENAI_AI_KEY")

client = OpenAI(api_key=OPEN_AI_API_KEY)

def get_response_maria(consult):
    path_pdf = os.path.join("pdf", "Maria_bot_accesspack.pdf")
    with open(path_pdf, "rb") as content_assistant:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": f"{content_assistant.read()}",
                },
                {
                    "role": "user",
                    "content": consult,
                }
            ],
            temperature=0,
        )
    return response.choices[0].message.content

get_response_maria("Hola")
