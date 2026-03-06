# import json
# import queue
# import threading
# import time
# import numpy as np
# import pyaudio
# import torch

# from vosk import Model as VoskModel, KaldiRecognizer
# from faster_whisper import WhisperModel

# # =========================
# # CONFIG
# # =========================
# SAMPLE_RATE = 16000
# CHUNK_SIZE = 4096
# WHISPER_INTERVAL = 2.0   # seconds (tradeoff: latency vs accuracy)

# VOSK_MODEL_PATH = "./Vosk/vosk-model-en-in-0.5"
# WHISPER_MODEL_SIZE = "medium.en"

# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# # =========================
# # MODELS
# # =========================
# vosk_model = VoskModel(VOSK_MODEL_PATH)
# vosk_recognizer = KaldiRecognizer(vosk_model, SAMPLE_RATE)
# vosk_recognizer.SetWords(True)

# whisper_model = WhisperModel(
#     WHISPER_MODEL_SIZE,
#     device=DEVICE,
#     compute_type="float16" if DEVICE == "cuda" else "int8",
# )

# # =========================
# # AUDIO SETUP
# # =========================
# p = pyaudio.PyAudio()
# stream = p.open(
#     format=pyaudio.paInt16,
#     channels=1,
#     rate=SAMPLE_RATE,
#     input=True,
#     frames_per_buffer=CHUNK_SIZE,
# )

# audio_queue = queue.Queue()
# whisper_buffer = []

# # =========================
# # AUDIO CAPTURE THREAD
# # =========================
# def audio_collector():
#     while True:
#         data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
#         audio_queue.put(data)

# # =========================
# # WHISPER THREAD
# # =========================
# def whisper_worker():
#     last_time = time.time()

#     while True:
#         if time.time() - last_time >= WHISPER_INTERVAL and whisper_buffer:
#             audio = b"".join(whisper_buffer)
#             whisper_buffer.clear()

#             audio_np = np.frombuffer(audio, dtype=np.int16).astype(np.float32) / 32768.0

#             segments, _ = whisper_model.transcribe(
#                 audio_np,
#                 language="en",
#                 beam_size=1,
#                 vad_filter=True,
#             )

#             text = " ".join(seg.text.strip() for seg in segments)
#             if text:
#                 print(f"\n🧠 Whisper refined: {text}\n")

#             last_time = time.time()

#         time.sleep(0.05)

# # =========================
# # MAIN LOOP (VOSK)
# # =========================
# print("🎙 Live hybrid ASR started (Ctrl+C to stop)\n")

# threading.Thread(target=audio_collector, daemon=True).start()
# threading.Thread(target=whisper_worker, daemon=True).start()

# try:
#     while True:
#         data = audio_queue.get()
#         whisper_buffer.append(data)

#         if vosk_recognizer.AcceptWaveform(data):
#             result = json.loads(vosk_recognizer.Result())
#             if result.get("text"):
#                 print(result["text"], end=" ", flush=True)
#         else:
#             partial = json.loads(vosk_recognizer.PartialResult())
#             if partial.get("partial"):
#                 print(partial["partial"], end="\r", flush=True)

# except KeyboardInterrupt:
#     print("\n🛑 Stopped")

# finally:
#     stream.stop_stream()
#     stream.close()
#     p.terminate()














import json
import queue
import threading
import time
import numpy as np
import pyaudio
import torch

from vosk import Model as VoskModel, KaldiRecognizer
from faster_whisper import WhisperModel

# =========================
# CONFIG
# =========================
SAMPLE_RATE = 16000
CHUNK_SIZE = 4096
WHISPER_INTERVAL = 2.0

VOSK_MODEL_PATH = "./Vosk/vosk-model-en-in-0.5"
WHISPER_MODEL_SIZE = "medium.en"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# =========================
# MODELS
# =========================
vosk_model = VoskModel(VOSK_MODEL_PATH)
vosk_recognizer = KaldiRecognizer(vosk_model, SAMPLE_RATE)
vosk_recognizer.SetWords(True)

whisper_model = WhisperModel(
    WHISPER_MODEL_SIZE,
    device=DEVICE,
    compute_type="float16" if DEVICE == "cuda" else "int8",
)

# =========================
# AUDIO SETUP
# =========================
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=SAMPLE_RATE,
    input=True,
    frames_per_buffer=CHUNK_SIZE,
)

audio_queue = queue.Queue()
whisper_buffer = []

# =========================
# AUDIO CAPTURE THREAD
# =========================
def audio_collector():
    while True:
        data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
        audio_queue.put(data)

# =========================
# WHISPER THREAD (SILENT)
# =========================
def whisper_worker():
    last_time = time.time()

    while True:
        if time.time() - last_time >= WHISPER_INTERVAL and whisper_buffer:
            audio = b"".join(whisper_buffer)
            whisper_buffer.clear()

            audio_np = np.frombuffer(audio, dtype=np.int16).astype(np.float32) / 32768.0

            # Whisper runs silently (no printing)
            whisper_model.transcribe(
                audio_np,
                language="en",
                beam_size=1,
                vad_filter=True,
            )

            last_time = time.time()

        time.sleep(0.05)

# =========================
# MAIN LOOP (WORD-BY-WORD)
# =========================
print("🎙 Live ASR started (Ctrl+C to stop)\n")

last_partial = ""

threading.Thread(target=audio_collector, daemon=True).start()
threading.Thread(target=whisper_worker, daemon=True).start()

try:
    while True:
        data = audio_queue.get()
        whisper_buffer.append(data)

        if vosk_recognizer.AcceptWaveform(data):
            result = json.loads(vosk_recognizer.Result())
            final_text = result.get("text", "").strip()
            if final_text:
                print("\n" + final_text)   # final sentence
                last_partial = ""

        else:
            partial = json.loads(vosk_recognizer.PartialResult())
            current = partial.get("partial", "").strip()

            if current and current.startswith(last_partial):
                new_words = current[len(last_partial):].strip()
                if new_words:
                    print(new_words, end=" ", flush=True)
                last_partial = current

except KeyboardInterrupt:
    print("\n🛑 Stopped")

finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
