# Kibritci ERP Yol Haritasi

Bu belge programi bozmadan, moduller halinde ilerlemek icin ana sirayi tutar.

## 0. Tasarim ve Temel Altyapi

- Ortak renk, font, radius ve buton dili `ui_theme.py` icinde toplandi.
- Ana uygulama kabugu modernlestirildi.
- Cari kart, stok kart, fatura, kasa, arac, demirbas, tahsis, tutanak, rapor ve eposta ekranlari ana menuye eklendi.
- Yeni tablolar icin `migrations/003_modul_kartlari_ve_operasyonlar.sql` hazirlandi.
- Sonraki adim: modulleri tek tek bu tasarim diline tasimak.
- Supabase migration kontrolu: irsaliye ek kolonlari SQL Editor'de uygulanmali.

## 1. Personel Yonetimi

### Personel Kayit

Hedef tablo: `personel_kayit` veya mevcut tablo korunacaksa `personel`.

Alanlar:
- TC no
- Ad soyad
- Gorev
- Maas
- Dogum tarihi
- Telefon no
- Cinsiyet
- Departman
- Ise giris tarihi
- Fotograf
- Ikametgah ilce
- Ikametgah il
- Ikametgah detay
- Banka adi
- Sube adi
- IBAN no
- Baba adi
- Anne adi
- Anne kizlık soyadi
- SGK giris tarihi
- Isten cikis tarihi
- Durum: aktif/pasif

Islemler:
- Personel kaydet
- Duzenle
- Isten cikar
- Kaydi sil
- Arama ve filtreleme

### Yoklama ve Mesai

- Geldi, Yok, Rapor, Izin durumlari
- Mesai saati girisi
- Maas hesabi icin veri tutma
- Aylik puantaj tablosu
- Yonetim raporu

### Maas Hesaplama

- Gelinen gun / ayin cektigi gun katsayisi
- Katsayi * maas
- Mesai saati * saatlik ucret * 1.5
- Kesinti / avans
- PDF ve Excel raporu

### Personel Izin Formu

- Personel listesinden izin formu olusturma
- Kibritci logolu PDF
- Santiye sefi ve izin isteyen imzasi zorunlu alanlar
- Onaya gonderme
- Imzali evrak yuklenince izin onaylandi kaydi
- Gecmis izin arama ve kontrol

## 2. Finansal Yonetim

### Satin Alma Talep Formu

- Mevcut modul var.
- Sonraki adim: tasarim standardi ve onay akisini netlestirme.

### Irsaliye Girisi

- Satin alma talebine bagli irsaliye girisi
- Imzali teslim evraki yuklenince 1. onay
- Miktar ve cins satin alma ile uyarsa 2. onay
- Uymazsa fark raporu

### Fatura Girisi

- Fatura, satin alma ve irsaliyelerle karsilastirilir
- Miktar/tutar uyusmasina gore rapor uretilir

### Haftalik Kasa Raporu

- Haftalik gelir/gider
- Kasa hareketleri
- PDF/Excel ozet

## 3. Idari Isler Yonetimi

### Arac, Is Makinesi ve Demirbas Kayit

- Arac/is makinesi/demirbas kaydi
- KM bakimi
- Yag bakimi
- Muayene tarihi
- Gunluk KM ve harcama takibi
- Personel ile iliskilendirme
- Kullanim raporu

### Tahsisleme

- Demirbas/personel tahsisi
- Teslim ve iade sureci
- Tutanak kaydi

### Kamp Girisleri Yonetimi

- Yerleske, kogus ve oda krokisi
- Personel oda eslestirme
- Ana firma/taseron ayrimi
- Sarf malzeme depo kaydi ve sayimi
- Kamp personeli faaliyet raporlari

### Gunluk Saha Faaliyet Raporu

- Personel yoklamasi
- Gorev/nitelik atamasi
- Parsel/blok secimi
- Fotografli is tanimi
- Logolu gunluk/aylik rapor
- Kayit basina en fazla 5 fotograf

### Hazir Tutanaklar

- Tahsis tutanagi
- Teslim tutanagi
- Sevk tutanagi
- Personel secimiyle otomatik doldurma
- Kayit altinda tutma

### Rapor Merkezi

- Tum modullerden raporlar
- PDF/Excel merkezi
- Filtreleme ve arama

### E-Posta Merkezi

- Rapor ve evrak gonderimi
- Hazir alici listeleri
- Gonderim gecmisi
