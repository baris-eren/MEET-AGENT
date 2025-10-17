import pyaudio
import wave
import keyboard # Yeni kütüphane
import sys

# Kayıt Durdurma Bayrağı
kayit_devam_ediyor = True

def kayit_durdur():
    """Ctrl+Q basıldığında çağrılacak işlev."""
    global kayit_devam_ediyor
    print("\n[BİLGİ] Ctrl+Q tuşları algılandı. Kayıt sonlandırılıyor...")
    kayit_devam_ediyor = False

# Ctrl+Q tuş kombinasyonunu dinlemeye başla
keyboard.add_hotkey('ctrl+q', kayit_durdur)

# Ses kaydı parametreleri
FORMAT = pyaudio.paInt16    # Örnek formatı (16-bit)
KANALLAR = 1                # Tek kanal (mono)
ORNEKLEME_ORANI = 44100     # Örnekleme oranı (Hz)
CHUNK = 1024                # Bir seferde okunacak çerçeve sayısı
CIKIS_DOSYASI = "ctrl_q_kayit.wav"  # Kaydedilecek dosya adı

# PyAudio örneği oluştur
ses = pyaudio.PyAudio()

# Ses akışını (stream) başlat
print("Kayıt başlıyor. Durdurmak için 'Ctrl+Q' tuşlarına aynı anda basın...")
akis = ses.open(format=FORMAT,
                channels=KANALLAR,
                rate=ORNEKLEME_ORANI,
                input=True,
                frames_per_buffer=CHUNK)

# Kaydedilen verileri saklamak için bir liste
cerceveler = []

try:
    # 'kayit_devam_ediyor' True olduğu sürece döngüde kal
    while kayit_devam_ediyor:
        veri = akis.read(CHUNK)
        cerceveler.append(veri)

except Exception as e:
    # Olası diğer hatalar
    print(f"Bir hata oluştu: {e}")

finally:
    # Tuş dinleyiciyi kaldır
    keyboard.remove_hotkey('ctrl+q')
    
    # Akışı durdur ve PyAudio'yu sonlandır
    akis.stop_stream()
    akis.close()
    ses.terminate()
    
    # WAV dosyasını kaydet
    if cerceveler: # Eğer veri kaydedilmişse
        print(f"Veriler {CIKIS_DOSYASI} dosyasına yazılıyor...")
        wf = wave.open(CIKIS_DOSYASI, 'wb')
        wf.setnchannels(KANALLAR)
        wf.setsampwidth(ses.get_sample_size(FORMAT))
        wf.setframerate(ORNEKLEME_ORANI)
        wf.writeframes(b''.join(cerceveler))
        wf.close()
        print(f"Kayıt başarıyla {CIKIS_DOSYASI} dosyasına kaydedildi.")
    else:
        print("Kayıt verisi bulunamadı. Dosya oluşturulmadı.")