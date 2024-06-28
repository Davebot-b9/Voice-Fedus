import torchaudio
from speechbrain.inference import Pretrained

# Cargar el modelo preentrenado
model = Pretrained.from_hparams(source="speechbrain/emotion-diarization-wavlm-large", savedir="tmpdir")

# Realizar la diarización en el archivo de audio
audio_file_path = "audio/EarningsCall.wav"
signal, fs = torchaudio.load(audio_file_path)
# diarization = model.diarize_batch(signal)

# Imprimir los resultados
# print(diarization)
