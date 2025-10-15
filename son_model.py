from groq import Groq
import os
import json

# --- GÜVENLİK NOTU ---
# API anahtarını doğrudan koda yazmak yerine, bir .env dosyası ve python-dotenv
# kütüphanesi ile yönetmek en güvenli yöntemdir.
# from dotenv import load_dotenv
# load_dotenv()
# API_KEY = os.getenv("GROQ_API_KEY")

# Lütfen kendi Groq API anahtarınızı buraya yapıştırın
API_KEY = "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"

try:
    client = Groq(api_key=API_KEY)
except Exception as e:
    print(f"Groq istemcisi başlatılırken hata oluştu: {e}")
    client = None

def analyze_transcript_with_high_accuracy(transcript_text: str) -> str:
    """
    Transkripti analiz eder ve %100 doğruluk hedefiyle detaylı bir JSON çıktısı üretir.
    """
    # <<< EN ÖNEMLİ DEĞİŞİKLİK BURADA: PROMPT'U DETAYLANDIRDIK >>>
    prompt = f"""
    Sen, toplantı notlarını %100 doğrulukla analiz eden, detay odaklı ve kıdemli bir proje yönetimi asistanısın.
    Görevin, sana verilen transkriptteki her detayı, imayı ve bağlantıyı yakalayarak en kapsamlı ve doğru JSON çıktısını oluşturmaktır.

    JSON YAPISI VE KURALLARI:
    
    1.  **"toplanti_ozeti" alanı:**
        * Sadece genel konuları değil, alınan kararların arkasındaki **nedenleri** de ekle (örneğin, tasarım gecikmesinin sebebi yönetimden gelen renk değişikliği talebi).
        * Toplantı başında belirtilen **tamamlanmış somut işleri** dahil et (örneğin, kullanıcı kayıt modülünün bitmesi).
        * Öne çıkan **kilit stratejik bilgileri** vurgula (örneğin, pazarlama için 'anlık senkronizasyon' özelliğinin seçilmesi).

    2.  **"gorevler" listesi:**
        * Bu liste, toplantıda belirtilen **TÜM** aksiyon maddelerini eksiksiz içermelidir.
        * **En önemlisi:** "Ona bugün bakıyoruz" gibi üstü kapalı veya zımni görevleri de tespit edip listeye eklemelisin.
        * Her görev için şu bilgileri eksiksiz doldur:
            * `"sorumlu"`: Görevi kimin veya hangi ekibin yapacağı.
            * `"gorev"`: Yapılacak işin, başka bir bağlama ihtiyaç duyulmayacak kadar net ve detaylı tanımı.
            * `"teslim_tarihi"`: Metinde belirtilen son teslim tarihi (Örn: 'Bugün içinde', 'Yarın öğlene kadar', 'Cuma günü sonuna kadar').

    Lütfen SADECE ve SADECE aşağıda belirtilen formatta geçerli bir JSON çıktısı ver. Başka hiçbir metin, yorum veya markdown formatlaması ekleme.

    {{
      "toplanti_ozeti": "...",
      "gorevler": [
        {{
          "sorumlu": "...",
          "gorev": "...",
          "teslim_tarihi": "..."
        }}
      ]
    }}

    ---
    **İŞLENECEK TOPLANTI METNİ:**
    {transcript_text}
    ---
    """
    
    try:
        print("--- Analiz Başlatılıyor (Yüksek Doğruluklu Llama-3.3 Modeli ile) ---")
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            # En son çalışan, güncel model adını kullanıyoruz
            model="llama-3.3-70b-versatile", 
            temperature=0.05, # Daha kesin ve deterministik sonuçlar için sıcaklığı düşürdük
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f'{{"hata": "API çağrısı sırasında bir sorun oluştu.", "detay": "{e}"}}'

# --- Ana Program Akışı ---
if __name__ == "__main__":
    if not client:
        print("API istemcisi başlatılamadığı için program durduruldu.")
    else:
        # Örnek metninizi buraya yapıştırın veya bir dosyadan okuyun
        ornek_toplanti_metni = """
        Örnek Toplantı Metni: "Q-Bilişim - Proje Alfa Haftalık Değervelendirme"
        Katılımcılar: Selin (Proje Yöneticisi), Barış (Yazılım Geliştirme Lideri), Deniz (UX/UI Tasarımcısı), Murat (Pazarlama Uzmanı).
        Transkript:
        Selin: Herkese merhaba arkadaşlar, Proje Alfa'nın 3. hafta değerlendirme toplantısına hoş geldiniz. Gündemimiz yoğun, o yüzden hızlıca başlayalım. Geçen haftaki hedeflerimize ne kadar ulaştık ve bu hafta bizi neler bekliyor, bunları konuşacağız. Barış, teknik tarafla başlayalım. Geliştirme sürecinde son durum nedir?
        Barış: Selamlar Selin. Geçen hafta konuştuğumuz gibi, kullanıcı kayıt ve giriş modülünü tamamladık. Test ekibine dün sabah itibarıyla ilettik. İlk geri bildirimler olumlu, sadece şifre sıfırlama akışında küçük bir bug tespit ettiler, ona da bugün bakıyoruz. Ancak ana modül %90 oranında tamamlandı diyebilirim. Bu hafta ise profil yönetimi ekranlarına başlamayı planlıyoruz. Yalnız bir konuya değinmem lazım, Deniz'den beklediğimiz yeni profil ekranı tasarımları henüz bize ulaşmadı. Bu durum bizi biraz yavaşlatabilir.
        Deniz: Merhaba Barış, evet o konuda bir gecikme oldu, farkındayım. Sebebi şu; geçen hafta yönetim bizden logonun renk paletinde küçük bir değişiklik istedi. Bu değişiklik arayüzdeki tüm bileşenleri etkilediği için, profil ekranı dahil olmak üzere tüm tasarımları yeni renk paletine göre güncellemem gerekti. Şu an %70'i bitti. Sana söz, en geç yarın öğlene kadar profil ekranının son halini Figma üzerinden paylaşmış olacağım.
        Selin: Anladım Deniz, bu önemli bir bilgi. Yönetimden gelen bu tarz ani istekleri anında benimle de paylaş ki planlamayı ona göre güncelleyelim. Demek ki Barış, sizin ekip yarın öğleden sonra tasarımlara kavuşacak. Bu durumda hafta sonuna kadar profil ekranının ön yüz geliştirmesini bitirebilir misiniz?
        Barış: Yarın öğleden sonra alırsak, evet, Cuma akşamına kadar en azından temel iskeleti ve fonksiyonları tamamlarız. Ekibimden Can'ı doğrudan bu işe atayacağım.
        Selin: Harika. O zaman ilk görevimizi not alıyorum: Can, Cuma günü sonuna kadar profil ekranının ön yüz geliştirmesini tamamlayacak. Teşekkürler Barış. Gelelim pazarlama tarafına. Murat, sendeki son durumlar nedir? Rakip analizi raporu ne aşamada?
        Murat: Merhaba herkese. Rakip analizi raporu tamamlandı ve dün akşam sana e-posta ile gönderdim Selin. Özetle, pazarda iki büyük rakibimiz var ama bizim hedeflediğimiz "kolay kullanım" nişi hala boşlukta. Raporda detaylıca belirttim. Bunun dışında, lansman için düşündüğümüz sosyal medya kampanyasının ön hazırlıklarına başladım. "Alfa ile Hayatını Kolaylaştır" sloganı üzerine bir konsept düşünüyorum. Ancak bu kampanyayı netleştirmek için projenin hangi özelliklerinin öne çıkarılacağına karar vermemiz lazım. Barış, sence en can alıcı, pazarlamaya değer teknik özelliğimiz ne olur?
        Barış: Bence bizim en güçlü yanımız, verileri anlık olarak senkronize etme hızımız olacak. Rakiplerde bu işlem 3-5 saniye sürerken bizde milisaniyeler içinde gerçekleşiyor. Bunu vurgulayabiliriz.
        Selin: Güzel bir nokta. Murat, o zaman Barış'ın belirttiği bu "anlık senkronizasyon" özelliğini ana pazarlama mesajlarımıza dahil edelim. Lütfen önümüzdeki hafta Salı gününe kadar, bu özelliği de içeren 3 farklı kampanya sloganı ve kısa bir sunum hazırla. Bu sunumu hem yönetime hem de tüm ekibe yapacağız.
        Murat: Anlaşıldı Selin. Salı gününe kadar 3 yeni slogan ve kısa bir sunum hazırlıyorum.
        Selin: Süper bir ekip çalışması. Son bir konu daha var. Projenin beta test süreci. Bu süreci lansmandan 2 hafta önce, yani ayın 25'inde başlatmayı planlıyorum. Bunun için bize en az 50 kişilik bir beta kullanıcı listesi lazım. Bu listeyi kim oluşturabilir?
        Murat: Pazarlama departmanındaki stajyer arkadaşımız bu konuda bize yardımcı olabilir. Mevcut müşteri veri tabanımızdan teknolojiye en yatkın olanları filtreleyebiliriz. Ben bu görevi üstlenebilirim.
        Selin: Tamamdır Murat, harika olur. O zaman Murat'ın ekibi, 20 Ekim tarihine kadar 50 kişilik bir beta kullanıcı listesi hazırlayıp bana iletecek. Arkadaşlar, bugünkü gündemimiz bu kadardı. Toparlayacak olursak; yazılım ekibi bu hafta profil ekranına odaklanıyor, pazarlama yeni kampanya sunumunu hazırlıyor ve beta listesi oluşturuluyor. Herkesin görevleri net mi?
        Selin: Harika. O zaman toplantıyı sonlandırıyorum. Hepinize iyi çalışmalar dilerim.
        """
        
        analiz_sonucu_str = analyze_transcript_with_high_accuracy(ornek_toplanti_metni)
        
        print("\n--- ANALİZ SONUCU (HAM METİN) ---")
        print(analiz_sonucu_str)

        try:
            # <<< ÇÖZÜM BURADA: Gelen metni JSON'a çevirmeden önce temizliyoruz >>>
            # Modelin eklediği markdown kod bloğu sarmalayıcılarını ve boşlukları kaldır
            clean_str = analiz_sonucu_str.strip()
            if clean_str.startswith("```json"):
                clean_str = clean_str[7:] # Baştaki "```json" ifadesini atla
            if clean_str.endswith("```"):
                clean_str = clean_str[:-3] # Sondaki "```" ifadesini atla
            
            # Temizlenmiş metni JSON olarak ayrıştır
            veri = json.loads(clean_str.strip())
            
            if "hata" in veri:
                print("\n--- BİLGİ ---")
                print(f"Bir hata oluştuğu için sonuçlar dosyaya kaydedilmedi: {veri.get('detay', '')}")
            else:
                with open("toplanti_analizi_detayli.json", "w", encoding="utf-8") as file:
                    json.dump(veri, file, ensure_ascii=False, indent=4)
                
                print("\n--- BİLGİ ---")
                print("Analiz sonucu başarıyla 'toplanti_analizi_detayli.json' dosyasına kaydedildi.")

        except json.JSONDecodeError:
            print("\n--- HATA ---")
            print("Temizlenmiş metin bile geçerli bir JSON formatında değil. Lütfen API ham çıktısını kontrol edin.")
        except Exception as e:
            print(f"\nDosyaya yazılırken beklenmedik bir hata oluştu: {e}")