# Ege Bölgesi CBS (Coğrafi Bilgi Sistemi)

## Proje Hakkında
Bu proje, Ege Bölgesi'nin kritik altyapı ve kamu hizmetlerini (okullar, hastaneler, toplanma alanları, deprem verileri vb.) tek bir harita üzerinde, hızlı ve etkileşimli bir şekilde sunmak için geliştirildi. Leaflet harita kütüphanesi kullanılarak tamamen tarayıcı üzerinde (client-side) çalışacak şekilde tasarlandı.

Temel amacımız, on binlerce noktasal veriyi tarayıcıyı yormadan haritaya dökmek ve kullanıcıya "hangi ilde ne kadar eğitim kurumu var, şu an ekranda kaç tane eczane veya toplanma alanı görüyorum" gibi istatistikleri anlık olarak, görsel bir şölenle verebilmek.

## Temel Özellikler
- **Bölgeye Tam Odak:** Harita varsayılan olarak İzmir, Manisa, Aydın, Muğla, Denizli, Uşak, Kütahya ve Afyonkarahisar'ı kapsayacak şekilde sınırlandırıldı (Bounding Box). Haritada kaybolsanız bile "📍 Bölgeye Dön" tuşuyla Ege'nin kalbine yumuşak bir iniş yapabilirsiniz.
- **Dinamik Veri Akışı:** MEB okulları, hastaneler ve eczaneler gibi büyük sabit veri setlerinin yanında, Kandilli Rasathanesi'nden çekilen canlı deprem verileri de haritaya anlık olarak işlenir.
- **Anlık İstatistik Motoru:** Siz haritayı kaydırdıkça veya yakınlaştırdıkça (zoom/pan), sadece o an ekranda görünen tesislerin sayısı anlık olarak hesaplanır ve yan panele yansır.
- **Gecikmesiz Altlık (Basemap) Değişimi:** Uydu, topoğrafya, varsayılan sokak veya açık (light) harita modları arasında hiçbir takılma veya yeniden yükleme olmadan saniyesinde geçiş yapabilirsiniz.
- **Akıllı Veri Senkronizasyonu:** Haritanın şişmemesi için büyük JSON verileri (okullar.json vb.) sayfa ilk açıldığında değil, "Veri Senkronizasyonu" butonuna basıldığında sisteme çekilir. Hız ve performans her şeydir.
- **Admin Yönetim Paneli:** `/admin/` dizinindeki modern panel üzerinden tüm CBS veri setlerini hem interaktif tablo olarak hem de ham JSON/KOD olarak inceleyip canlı olarak düzenleyebilirsiniz.

## Kurulum ve Hızlı Başlatma
Projeyi çalıştırmanın en kolay ve önerilen yolu proje ana dizinindeki başlatıcıyı kullanmaktır:

1. **Tek Tıkla Başlatma (Önerilen):**
   - Klasördeki **`baslat.bat`** dosyasına çift tıklayın.
   - Bilgisayarınızda Python yüklü değilse sizi doğrudan resmi indirme sayfasına yönlendirir.
   - Python mevcutsa gerekli ortamı hazırlar, yerel sunucuyu ayağa kaldırır ve tarayıcınızda projeyi otomatik olarak açar (`http://localhost:3000/`).

2. **Manuel Başlatma:**
   - Bir terminal açıp proje dizinine gidin:
     ```bash
     python server.py
     ```
   - Harita için: `http://localhost:3000/`
   - Yönetim paneli için: `http://localhost:3000/admin/`

## Proje Yapısı
- `baslat.bat`: Windows için tek tıkla Python kontrolü yapan, sunucuyu ve tarayıcıyı başlatan komut dosyası.
- `server.py`: Dahili Python kütüphaneleriyle çalışan, haritayı ve Admin paneli API'lerini sunan hafif HTTP sunucusu.
- `ege_cbs.html`: Arayüzün, Leaflet harita motorunun ve katman analizlerinin çalıştığı ana harita sayfası.
- `admin/`: Veri setlerini görüntüleme ve düzenleme imkanı sunan Admin Yönetim Paneli.
- `data/`: 8 Ege iline ait okullar, hastaneler, eczaneler, diri fay hatları, depremler, yollar vb. coğrafi verilerin bulunduğu dizin (.js ve .json).

## Geliştirici
Bu sistem **Rainbow.dev** tarafından klavyeye dökülmüştür. 🚀

Daha fazla proje, geri bildirim veya iletişim için https://rainbowdev.com.tr adresine göz atabilirsiniz.
