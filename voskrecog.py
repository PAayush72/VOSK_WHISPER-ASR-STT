# from vosk import Model,KaldiRecognizer
# import pyaudio


# model = Model("./Vosk/vosk-model-small-en-in-0.4")
# recognizer = KaldiRecognizer(model,16000)

# mic = pyaudio.PyAudio()
# stream = mic.open(rate=16000,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=8192)
# stream.start_stream()

# while True:
#     data = stream.read(4096)
#     if len(data) == 0:
#         break

#     if recognizer.AcceptWaveform(data):   
#         print(recognizer.Result())
    


from vosk import Model, KaldiRecognizer
import pyaudio
import json

# =========================
# MODEL
# =========================
model = Model("./Vosk/vosk-model-gu-0.42")
recognizer = KaldiRecognizer(model, 16000)
recognizer.SetWords(True)

# =========================
# AUDIO
# =========================
mic = pyaudio.PyAudio()
stream = mic.open(
    rate=16000,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=4096
)
stream.start_stream()

print("🎙 Live word-by-word transcription (Ctrl+C to stop)\n")

# =========================
# STATE
# =========================
last_partial = ""

try:
    while True:
        data = stream.read(4096, exception_on_overflow=False)

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").strip()

            if text:
                print(text)   # ✅ final sentence on new line
                last_partial = ""

        else:
            partial = json.loads(recognizer.PartialResult())
            current = partial.get("partial", "").strip()

            if current and current != last_partial:
                # Print ONLY new words
                new_text = current[len(last_partial):].strip()
                if new_text:
                    print(new_text, end=" ", flush=True)
                last_partial = current

except KeyboardInterrupt:
    print("\n🛑 Stopped")

finally:
    stream.stop_stream()
    stream.close()
    mic.terminate()
