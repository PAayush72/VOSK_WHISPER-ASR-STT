import sounddevice as sd
import numpy as np
import queue
import wave
import time
import os
from faster_whisper import WhisperModel

RATE = 16000
CHANNELS = 1
CHUNK_SEC = 3.0        # whisper window
OVERLAP_SEC = 0.5
DEVICE = "cuda"

model = WhisperModel(
    "medium",
    device="cuda",
    compute_type="float16"
)



audio_q = queue.Queue()

def audio_callback(indata, frames, time_info, status):
    audio_q.put(indata.copy())

stream = sd.InputStream(
    samplerate=RATE,
    channels=CHANNELS,
    callback=audio_callback,
    blocksize=int(RATE * 0.2)
)

print("🎤 Listening (IndicWhisper only)...")

buffer = np.zeros((0, 1), dtype=np.float32)

with stream:
    while True:
        data = audio_q.get()
        buffer = np.concatenate((buffer, data))

        duration = len(buffer) / RATE

        if duration >= CHUNK_SEC:
            chunk = buffer[:int(RATE * CHUNK_SEC)]
            buffer = buffer[int(RATE * (CHUNK_SEC - OVERLAP_SEC)):]
            
            tmp = "chunk.wav"
            with wave.open(tmp, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(RATE)
                wf.writeframes((chunk * 32767).astype(np.int16))

            segments, _ = model.transcribe(
                tmp,
                language="hi",   # or "gu", "en"
                beam_size=1,
                vad_filter=True
            )

            text = " ".join(s.text for s in segments).strip()
            if text:
                print(f"📝 {text}")
