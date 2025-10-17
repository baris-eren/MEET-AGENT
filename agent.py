import torch
import torchaudio
import whisper
import numpy as np
import librosa
from pyannote.audio import Pipeline
from pyannote.core import Annotation

# --- AYARLAR ---
AUDIO_FILE = "C:\\Users\\baris\\Downloads\\kayit.wav"
HF_TOKEN = "xxxxxhf_ehtqrATTRJXAWEXZGmdFfAykWUerakESHZ"
WHISPER_MODEL_NAME = "medium"
# ----------------

def diarization_and_transcription(audio_file_path, hf_token, whisper_model_name):
    """
    CUDA destekli konuşmacı ayırma + transkripsiyon
    """
    # --- CUDA kontrolü ---
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"⚙️ Kullanılan cihaz: {device}")

    # --- PYANNOTE DİARIZATION ---
    print("1️⃣ pyannote.audio ile konuşmacı bölümlendirme (Diarization) başlatılıyor...")

    try:
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=hf_token
        )
        pipeline.to(device)  # GPU'ya taşı
    except Exception as e:
        print(f"❌ Hata: pyannote modelini yüklerken sorun oluştu.\nAçıklama: {e}")
        return

    # --- SESİ YÜKLEME ---
    print("🎧 Sesi torchaudio ile yüklüyoruz...")
    try:
        waveform, sample_rate = torchaudio.load(audio_file_path)
        waveform = waveform.to(torch.float32).to(device)
        pyannote_audio = {"waveform": waveform.cpu(), "sample_rate": int(sample_rate)}
    except Exception as e:
        print(f"❌ Hata: torchaudio.load başarısız oldu.\nAçıklama: {e}")
        return

    # --- DİARIZATION ---
    print("🔍 Konuşmacı ayırma işlemi başlıyor...")
    try:
        diarization = pipeline(pyannote_audio)
    except Exception as e:
        print(f"❌ Hata: Diarization sırasında sorun oluştu.\nAçıklama: {e}")
        return

    diarization_segments = []
    annotation = diarization.speaker_diarization if hasattr(diarization, "speaker_diarization") else diarization
    for segment, _, speaker in annotation.itertracks(yield_label=True):
        diarization_segments.append({
            "start": float(segment.start),
            "end": float(segment.end),
            "speaker": speaker
        })

    print(f"✅ Diarization tamamlandı. {len(diarization_segments)} segment bulundu.")

    # --- WHISPER MODELİ ---
    print("2️⃣ Whisper modeli yükleniyor...")
    try:
        model = whisper.load_model(whisper_model_name, device=str(device))
    except Exception as e:
        print(f"❌ Hata: Whisper modeli yüklenemedi.\nAçıklama: {e}")
        return

    # --- TRANSKRİPSİYON ---
    print("📝 Transkripsiyon başlatılıyor...")
    try:
        audio, sr = librosa.load(audio_file_path, sr=16000, mono=True)
    except Exception as e:
        print(f"❌ Hata: Ses dosyasını librosa ile yüklerken sorun oluştu.\nAçıklama: {e}")
        return

    sr = 16000
    final_transcript = []

    for seg in diarization_segments:
        start_sec = seg["start"]
        end_sec = seg["end"]
        speaker = seg["speaker"]

        start_sample = int(start_sec * sr)
        end_sample = int(end_sec * sr)

        segment_audio = audio[start_sample:end_sample].astype(np.float32)
        if segment_audio.size == 0:
            continue

        # Segmenti GPU'ya aktar
        segment_tensor = torch.from_numpy(segment_audio).to(device)

        result = model.transcribe(segment_tensor, language="tr")
        text = result["text"].strip()

        if text:
            final_transcript.append({
                "start": start_sec,
                "end": end_sec,
                "speaker": speaker,
                "text": text
            })
            print(f"[{start_sec:.2f}s - {end_sec:.2f}s] {speaker}: {text}")

    # --- SONUÇ ---
    print("\n--- 🧾 Nihai Transkript ---")
    for item in final_transcript:
        print(f"{item['speaker']} ({item['start']:.2f}s - {item['end']:.2f}s): {item['text']}")

if __name__ == "__main__":
    diarization_and_transcription(AUDIO_FILE, HF_TOKEN, WHISPER_MODEL_NAME)
