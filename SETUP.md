# Setup Guide - VOSK + WHISPER

## Step-by-Step Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/vosk-whisper.git
cd vosk-whisper
```

### 2. Python & Virtual Environment Setup

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-all-dev
```

**macOS (with Homebrew):**
```bash
brew install portaudio
```

**Windows:**
- Download and install [FFmpeg](https://ffmpeg.org/download.html)
- Add FFmpeg to your PATH

### 4. Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. GPU Setup (Optional but Recommended)

**For NVIDIA GPU with CUDA:**

Check if CUDA is installed:
```bash
nvidia-smi
```

If not installed, download from [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)

Install CUDA-enabled PyTorch:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 6. Verify Installation

**Test VOSK:**
```bash
python voskrecog.py
```

**Test Whisper:**
```bash
python IndicWhisper.py
```

**Start Main Application:**
```bash
python final_stt.py
```

**Open Web UI:**
```bash
# Linux/macOS
python -m http.server 8000

# Or Windows
python -m http.server 8000
```

Then open browser: `http://localhost:8000`

## Troubleshooting Installation

### Issue: PyAudio Installation Fails

**Solution for Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**Solution for Ubuntu:**
```bash
sudo apt-get install python3-pyaudio
```

**Solution for macOS:**
```bash
brew install portaudio
pip install pyaudio
```

### Issue: CUDA Not Found

Ensure PyTorch is installed with CUDA support:
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

Should print: `True`

If False, reinstall with CUDA:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Issue: VOSK Model Missing

Models are included in `Vosk/` directory. If missing, download from:
- [VOSK Models](https://alphacephei.com/vosk/models)

Extract to the `Vosk/` directory.

### Issue: FFmpeg Not Found

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\Program Files\ffmpeg`
3. Add to PATH: `C:\Program Files\ffmpeg\bin`

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

## Configuration

Edit these files for custom settings:

### `final_stt.py` - Main Configuration
```python
VOSK_MODEL_PATH = "./Vosk/vosk-model-en-in-0.5"  # Change model
WHISPER_MODEL_SIZE = "turbo"                      # Model size
DEVICE = "cuda"                                   # GPU or "cpu"
RATE = 16000                                      # Sample rate
```

### `index.html` - UI Customization
- Open in text editor
- Modify styling and layout
- Update WebSocket connection if needed

## Running

### Quick Start
```bash
# Activate virtual environment first
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Run main application
python final_stt.py

# In another terminal, open web UI
cd vosk-whisper
python -m http.server 8000
# Visit: http://localhost:8000
```

### Production Setup

Consider using a production WSGI server:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 final_stt:app
```

## Docker Setup (Optional)

Create `Dockerfile`:
```dockerfile
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    portaudio19-dev \
    ffmpeg

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "final_stt.py"]
```

Build and run:
```bash
docker build -t vosk-whisper .
docker run --gpus all -p 8765:8765 vosk-whisper
```

## Performance Tips

1. **For accuracy**, use larger models: `medium`, `large`, `turbo`
2. **For speed**, use smaller models: `tiny`, `base`
3. **GPU acceleration**: Always use GPU when available
4. **Memory**: Reduce `MAX_BUFFER_SECONDS` if running out of memory
5. **CPU optimization**: Disable unused features to reduce CPU usage

## First Run Checklist

- [ ] Virtual environment activated
- [ ] `requirements.txt` installed
- [ ] VOSK models in `Vosk/` directory
- [ ] GPU verified with `nvidia-smi` (optional)
- [ ] `python final_stt.py` runs without errors
- [ ] WebSocket server starts on port 8765
- [ ] Web UI opens in browser without connection errors
- [ ] Test audio input from microphone
- [ ] Verify transcription output in web UI

## System Specifications Tested

✅ **Tested on:**
- Windows 10/11 with NVIDIA GPU
- Ubuntu 22.04 with NVIDIA GPU
- macOS with CPU (slower)

✅ **Minimum Requirements:**
- Python 3.8+
- 8GB RAM
- 10GB free storage
- Microphone input

✅ **Recommended for Production:**
- Python 3.10+
- 16GB+ RAM
- NVIDIA GPU (RTX 2080+)
- 20GB free storage
- Professional-grade microphone

## Support

For installation issues:
1. Check system meets minimum requirements
2. Verify Python version: `python --version`
3. Check CUDA: `nvidia-smi` (for GPU)
4. Review error messages carefully
5. Search existing issues on GitHub

## Next Steps

After successful installation:
1. Explore different VOSK models
2. Test Whisper model sizes
3. Customize `NAME_BIAS` for your use case
4. Integrate with your application
5. Deploy to production

---

**Need Help?** See main README.md or create an issue on GitHub.
