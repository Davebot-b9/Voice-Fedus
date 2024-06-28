# # instantiate the pipeline
# import os
# from pyannote.audio import Pipeline
# from dotenv import load_dotenv

# load_dotenv()
# HUGGING_FACE_ACCESS_TOKEN = os.getenv("HUGGING_API")
# pipeline = Pipeline.from_pretrained(
#     "pyannote/speaker-diarization-3.1",
#     use_auth_token=HUGGING_FACE_ACCESS_TOKEN)

# # run the pipeline on an audio file
# diarization = pipeline("audio.wav", min_speakers=2, max_speakers=5)

# # dump the diarization output to disk using RTTM format
# with open("audio.rttm", "w") as rttm:
#     diarization.write_rttm(rttm)

import pyttsx3 as pyttsx
def say(text):
    engine = pyttsx.init()
    engine.setProperty('voice','com.apple.speech.synthesis.voice.alex')
    engine.say(text)
    engine.runAndWait()

print(say("Hola, como estas?"))
