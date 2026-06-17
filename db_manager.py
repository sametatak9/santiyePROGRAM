import os
import calendar
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client

# .env dosyasının yolunu kesinleştir
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("HATA: SUPABASE_URL veya SUPABASE_KEY .env'de bulunamadı!")

supabase = create_client(url, key)


# =====================================================================
# BAĞLANTI TESTİ
# =====================================================================

def baglanti_test():
    """Supabase bağlantısını ve kritik tabloları test eder."""
    sonuclar = {}
    tablolar = [
        "personel", "yoklamalar",
        "satin_alma_formlari", "satin_alma_kalemleri",
        "irsaliyeler", "irsaliye_kalemleri",
        "faturalar", "fatura_kalemleri", "fatura_irsaliye_baglanti",
        "cari_kartlar", "stok_kartlari",
        "kasa_hareketleri", "arac_kartlari", "demirbas_kartlari",
        "tahsis_kayitlari", "hazir_tutanaklar", "kart_islem_gecmisi",
    ]
    for t in tablolar:
        try:
            res = supabase.table(t).select("id").limit(1).execute()
            sonuclar[t] = f"✅ OK ({len(res.data)} örnek)"
        except Exception as e:
            sonuclar[t] = f"❌ {str(e)[:80]}"
    return sonuclar


# =====================================================================
# PERSONEL MODÜLÜ FONKSİYONLARI
# =====================================================================

def personel_listele():
    try:
        response = supabase.table("personel").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Veritabanı hatası: {e}")
        return []

def personel_kaydet(personel_data):
    try:
        response = supabase.table("personel").insert(personel_data).execute()
        return True, response
    except Exception as e:
        print(f"Kayıt hatası: {e}")
        return False, str(e)

def personel_sil(personel_id):
    try:
        p_id = int(personel_id)
        response = supabase.table("personel").delete().eq("id", p_id).execute()
        return response
    except Exception as e:
        print(f"Hata: {e}")
        return None

def personel_pasif_yap(personel_id, cikis_tarihi):
    try:
        supabase.table("personel") \
            .update({"durum": False, "isten_cikis_tarihi": cikis_tarihi}) \
            .eq("id", personel_id) \
            .execute()
        return True
    except Exception as e:
        print(f"Hata Detayı: {e}")
        return False

def personel_guncelle(personel_id, guncel_data):
    try:
        response = supabase.table("personel").update(guncel_data).eq("id", personel_id).execute()
        return True, response
    except Exception as e:
        return False, str(e)

def aktif_personeller_getir():
    try:
        sonuc = (
            supabase
            .table("personel")
            .select("id,ad,soyad,ise_giris_tarihi,isten_cikis_tarihi,gorev,maas,tc_no,iban_no")
            .eq("durum", True)
            .order("ad")
            .execute()
        )
        return sonuc.data
    except Exception as e:
        print("Aktif personeller getirilirken hata:", e)
        return []

def _tarih_parse(value):
    if not value or str(value).lower() in ("none", "null", "-"):
        return None
    try:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
    except Exception:
        return None


# =====================================================================
# YOKLAMA VE PUANTAJ
# =====================================================================

def yoklama_icin_personel_getir(secilen_tarih):
    try:
        response = supabase.rpc('get_active_personnel', {'target_date': secilen_tarih}).execute()
        return response.data
    except Exception as e:
        print(f"Sorgu hatası: {e}")
        return []

def yoklama_getir(personel_id_or_tarih, yil=None, ay=None):
    if isinstance(personel_id_or_tarih, str) and "-" in personel_id_or_tarih and yil is None and ay is None:
        return personel_gunluk_yoklama_tumu_sorgu(personel_id_or_tarih)

    try:
        p_id = personel_id_or_tarih
        baslangic = f"{yil}-{int(ay):02d}-01"
        if int(ay) == 12:
            bitis = f"{int(yil)+1}-01-01"
        else:
            bitis = f"{yil}-{int(ay)+1:02d}-01"

        sonuc = (
            supabase
            .table("yoklamalar")
            .select("tarih,durum,mesai_saati")
            .eq("personel_id", p_id)
            .gte("tarih", baslangic)
            .lt("tarih", bitis)
            .execute()
        )
        return sonuc.data if sonuc.data else []
    except Exception as e:
        print("Aylık yoklama çekme hatası:", e)
        return []

def personel_gunluk_yoklama_tumu_sorgu(tarih_str):
    try:
        personeller = personel_listele() or []
        yoklama_res = supabase.table("yoklamalar").select("*").eq("tarih", tarih_str).execute()
        yoklamalar = yoklama_res.data or []
        yoklama_map = {v["personel_id"]: v for v in yoklamalar}
        guncel_liste = []
        secili_tarih = _tarih_parse(tarih_str)

        for p in personeller:
            if not p.get("durum", True):
                continue
            ise_giris = _tarih_parse(p.get("ise_giris_tarihi") or p.get("ise_giris"))
            isten_cikis = _tarih_parse(p.get("isten_cikis_tarihi"))
            if secili_tarih and ise_giris and secili_tarih < ise_giris:
                continue
            if secili_tarih and isten_cikis and secili_tarih > isten_cikis:
                continue
            p_id = p["id"]
            durum_veri = yoklama_map.get(p_id, {})
            guncel_liste.append({
                "id": p_id,
                "ad": p.get("ad", ""),
                "soyad": p.get("soyad", ""),
                "gorev": p.get("gorev", p.get("unvan", "İşçi")),
                "yoklama_durum": durum_veri.get("durum") or "Girilmedi",
                "mesai_saati": durum_veri.get("mesai_saati", 0)
            })
        return guncel_liste
    except Exception as e:
        print(f"Günlük toplu yoklama haritalama hatası: {e}")
        return []

def personel_aylik_yoklama_getir(personel_id, yil, ay):
    baslangic = f"{yil}-{ay:02d}-01"
    bitis = f"{yil+1}-01-01" if ay == 12 else f"{yil}-{ay+1:02d}-01"
    try:
        sonuc = (
            supabase
            .table("yoklamalar")
            .select("*")
            .eq("personel_id", personel_id)
            .gte("tarih", baslangic)
            .lt("tarih", bitis)
            .execute()
        )
        return sonuc.data if sonuc.data else []
    except Exception as e:
        print("personel_aylik_yoklama_getir hatası:", e)
        return []

def aylik_yoklama_kaydet(veriler):
    return (
        supabase
        .table("yoklamalar")
        .upsert(veriler, on_conflict="personel_id,tarih")
        .execute()
    )

def personel_gunluk_yoklama_tumu(personel_id, yil, ay):
    try:
        response = supabase.table("yoklamalar").select("*").eq("personel_id", personel_id).execute()
        data = response.data or []
        sonuc = []
        for d in data:
            tarih = d.get("tarih")
            if not tarih:
                continue
            tarih_parcalari = str(tarih).split("-")
            if len(tarih_parcalari) == 3:
                y, m, g = map(int, tarih_parcalari)
                if y == yil and m == ay:
                    sonuc.append(d)
        return sonuc
    except Exception as e:
        print("yoklama çekme hata:", e)
        return []


# =====================================================================
# MAAŞ HESAPLAMA
# =====================================================================

def maas_personeller_getir():
    try:
        return (
            supabase
            .table("personel")
            .select("id,ad,soyad,gorev,maas,tc_no,iban_no,ise_giris_tarihi,isten_cikis_tarihi")
            .eq("durum", True)
            .execute()
            .data or []
        )
    except Exception as e:
        print("Maaş personel listesi çekme hatası:", e)
        return []

def maas_yoklama_getir(personel_id, yil, ay):
    return yoklama_getir(personel_id, yil, ay)

def maas_hesapla(personel, yoklama, gun_sayisi_ay):
    gelen_gun = 0
    toplam_mesai = 0
    for v in yoklama:
        durum = v.get("durum")
        if durum in ["Geldi", "İzinli", "Raporlu"]:
            gelen_gun += 1
        toplam_mesai += float(v.get("mesai_saati") or 0)

    base_maas = float(personel.get("maas") or 0)
    gunluk_ucret = base_maas / 30
    normal_maas = base_maas if gelen_gun >= gun_sayisi_ay else gunluk_ucret * gelen_gun
    saatlik_ucret = gunluk_ucret / 7.5
    mesai_kazanc = toplam_mesai * saatlik_ucret * 1.5
    toplam = normal_maas + mesai_kazanc

    return {
        "gelen_gun": gelen_gun,
        "mesai_saat": toplam_mesai,
        "normal_maas": round(normal_maas, 2),
        "mesai_kazanc": round(mesai_kazanc, 2),
        "toplam_maas": round(toplam, 2)
    }


# =====================================================================
# SATIN ALMA MODÜLÜ
# =====================================================================

def satin_alma_form_kaydet(form):
    try:
        response = supabase.table("satin_alma_formlari").insert({
            "sa_id": form["sa_id"],
            "tarih": form["tarih"],
            "talep_eden": form["talep_eden"],
            "onay_durumu": "ONAY BEKLİYOR"
        }).execute()
        return True, response
    except Exception as e:
        print("Form kayıt hatası:", e)
        return False, str(e)

def satin_alma_kalem_ekle(kalem):
    try:
        stok_kart = stok_kart_bul_veya_olustur(
            kalem["urun_adi"],
            kalem.get("birim") or kalem.get("talep_birimi") or "ADET"
        )
        response = supabase.table("satin_alma_kalemleri").insert({
            "sa_id": kalem["sa_id"],
            "urun_adi": kalem["urun_adi"],
            "stok_kart_id": kalem.get("stok_kart_id") or (stok_kart or {}).get("id"),
            "talep_edilen_miktar": kalem["miktar"],
            "talep_birimi": kalem["birim"],
            "kullanilacak_yer": kalem["yer"],
            "marka": kalem["marka"],
            "aciklama": kalem.get("aciklama")
        }).execute()
        return True, response
    except Exception as e:
        print("Kalem ekleme hatası:", e)
        return False, str(e)

def satin_alma_form_guncelle(sa_id, form):
    try:
        response = (
            supabase
            .table("satin_alma_formlari")
            .update({
                "tarih": form["tarih"],
                "talep_eden": form["talep_eden"],
                "onay_durumu": "ONAY BEKLİYOR"
            })
            .eq("sa_id", sa_id)
            .execute()
        )
        return True, response
    except Exception as e:
        print("Form güncelleme hatası:", e)
        return False, str(e)

def satin_alma_kalemleri_yenile(sa_id, kalemler):
    try:
        supabase.table("satin_alma_kalemleri").delete().eq("sa_id", sa_id).execute()
        if not kalemler:
            return True, None
        for kalem in kalemler:
            stok_kart = stok_kart_bul_veya_olustur(
                kalem.get("urun_adi"),
                kalem.get("talep_birimi") or "ADET"
            )
            kalem["stok_kart_id"] = kalem.get("stok_kart_id") or (stok_kart or {}).get("id")
        response = supabase.table("satin_alma_kalemleri").insert(kalemler).execute()
        return True, response
    except Exception as e:
        print("Kalem yenileme hatası:", e)
        return False, str(e)

def satin_alma_formlari_getir():
    try:
        return supabase.table("satin_alma_formlari") \
            .select("*") \
            .order("tarih", desc=True) \
            .execute().data or []
    except Exception as e:
        print(e)
        return []

def satin_alma_talepleri_getir():
    try:
        return (
            supabase
            .table("satin_alma_formlari")
            .select("*")
            .order("tarih", desc=True)
            .execute()
            .data or []
        )
    except Exception as e:
        print(f"Talep getirme hatası: {e}")
        return []

def satin_alma_detay_getir(sa_id):
    try:
        form_response = (
            supabase
            .table("satin_alma_formlari")
            .select("*")
            .eq("sa_id", sa_id)
            .single()
            .execute()
        )
        kalem_response = (
            supabase
            .table("satin_alma_kalemleri")
            .select("*")
            .eq("sa_id", sa_id)
            .order("id")
            .execute()
        )
        return {
            "form": form_response.data,
            "kalemler": kalem_response.data or []
        }
    except Exception as e:
        print(f"Satın alma detay getirme hatası: {e}")
        return {"form": None, "kalemler": []}

def satin_alma_imzali_evrak_guncelle(sa_id, evrak_yolu):
    try:
        response = (
            supabase
            .table("satin_alma_formlari")
            .update({
                "imzali_evrak_url": evrak_yolu,
                "onay_durumu": "1. ONAY TAMAMLANDI",
                "gonderim_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            .eq("sa_id", sa_id)
            .execute()
        )
        return True, response
    except Exception as e:
        print(f"İmzalı evrak güncelleme hatası: {e}")
        return False, str(e)


# =====================================================================
# İRSALİYE MODÜLÜ
# =====================================================================

def irsaliye_id_uret():
    import uuid
    return f"IR-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"

def irsaliye_kaydet(form):
    try:
        cari_kart = cari_kart_bul_veya_olustur(form.get("firma"), "TEDARIKCI")
        response = supabase.table("irsaliyeler").insert({
            "irsaliye_id": form["irsaliye_id"],
            "sa_id":        form.get("sa_id") or None,   # NULL olabilir
            "irsaliye_no":  form.get("irsaliye_no"),
            "firma":        form.get("firma"),
            "cari_kart_id": form.get("cari_kart_id") or (cari_kart or {}).get("id"),
            "tarih":        form.get("tarih"),
            "onay_durumu":  "ONAY BEKLİYOR",
        }).execute()
        return True, response
    except Exception as e:
        print("İrsaliye kayıt hatası:", e)
        return False, str(e)

def irsaliye_kalem_ekle(kalem):
    try:
        stok_kart = stok_kart_bul_veya_olustur(kalem["urun_adi"], kalem.get("birim") or "ADET")
        response = supabase.table("irsaliye_kalemleri").insert({
            "irsaliye_id":  kalem["irsaliye_id"],
            "sa_kalem_id":  kalem.get("sa_kalem_id"),
            "stok_kart_id": kalem.get("stok_kart_id") or (stok_kart or {}).get("id"),
            "urun_adi":     kalem["urun_adi"],
            "miktar":       kalem["miktar"],
            "birim":        kalem["birim"],
        }).execute()
        return True, response
    except Exception as e:
        print("İrsaliye kalem ekleme hatası:", e)
        return False, str(e)

def irsaliye_kalemleri_yenile(irsaliye_id, kalemler):
    try:
        supabase.table("irsaliye_kalemleri").delete().eq("irsaliye_id", irsaliye_id).execute()
        if not kalemler:
            return True, None
        for kalem in kalemler:
            stok_kart = stok_kart_bul_veya_olustur(kalem.get("urun_adi"), kalem.get("birim") or "ADET")
            kalem["stok_kart_id"] = kalem.get("stok_kart_id") or (stok_kart or {}).get("id")
        response = supabase.table("irsaliye_kalemleri").insert(kalemler).execute()
        return True, response
    except Exception as e:
        print("İrsaliye kalem yenileme hatası:", e)
        return False, str(e)

def irsaliye_guncelle(irsaliye_id, form):
    try:
        cari_kart = cari_kart_bul_veya_olustur(form.get("firma"), "TEDARIKCI")
        response = (
            supabase
            .table("irsaliyeler")
            .update({
                "irsaliye_no":  form.get("irsaliye_no"),
                "firma":        form.get("firma"),
                "cari_kart_id": form.get("cari_kart_id") or (cari_kart or {}).get("id"),
                "tarih":        form.get("tarih"),
                "onay_durumu":  "ONAY BEKLİYOR",
            })
            .eq("irsaliye_id", irsaliye_id)
            .execute()
        )
        return True, response
    except Exception as e:
        print("İrsaliye güncelleme hatası:", e)
        return False, str(e)

def irsaliyeler_getir(sa_id=None):
    try:
        query = supabase.table("irsaliyeler").select("*").order("tarih", desc=True)
        if sa_id:
            query = query.eq("sa_id", sa_id)
        return query.execute().data or []
    except Exception as e:
        print("İrsaliye listeleme hatası:", e)
        return []

def irsaliye_detay_getir(irsaliye_id):
    try:
        form_response = (
            supabase
            .table("irsaliyeler")
            .select("*")
            .eq("irsaliye_id", irsaliye_id)
            .single()
            .execute()
        )
        kalem_response = (
            supabase
            .table("irsaliye_kalemleri")
            .select("*")
            .eq("irsaliye_id", irsaliye_id)
            .order("id")
            .execute()
        )
        return {
            "form": form_response.data,
            "kalemler": kalem_response.data or [],
        }
    except Exception as e:
        print(f"İrsaliye detay getirme hatası: {e}")
        return {"form": None, "kalemler": []}

def sa_id_irsaliye_kalemleri_topla(sa_id):
    """1 SA'ya bağlı TÜM irsaliyelerin kalemlerini toplar (N irsaliye → 1 SA)."""
    try:
        irsaliye_listesi = irsaliyeler_getir(sa_id)
        tum_kalemler = []
        for ir in irsaliye_listesi:
            detay = irsaliye_detay_getir(ir["irsaliye_id"])
            tum_kalemler.extend(detay.get("kalemler", []))
        return tum_kalemler
    except Exception as e:
        print("İrsaliye kalem toplama hatası:", e)
        return []

def irsaliye_imzali_evrak_guncelle(irsaliye_id, evrak_yolu):
    try:
        response = (
            supabase
            .table("irsaliyeler")
            .update({
                "imzali_evrak_url": evrak_yolu,
                "onay_durumu": "1. ONAY TAMAMLANDI",
            })
            .eq("irsaliye_id", irsaliye_id)
            .execute()
        )
        return True, response
    except Exception as e:
        print(f"İrsaliye imzalı evrak güncelleme hatası: {e}")
        return False, str(e)

def irsaliye_karsilastir(sa_id, irsaliye_id=None):
    """SA kalemleri vs irsaliye kalemleri (N irsaliye toplanarak karşılaştırılır)."""
    from irsaliye_karsilastir import karsilastir, rapor_metni_olustur

    # --- ESNEKLEŞTİRME: SA_ID YOKSA DOĞRUDAN RAPOR ÜRET ---
    if not sa_id or str(sa_id).strip() == "" or str(sa_id).lower() == "none":
        rapor_bos = (
            "KIBRITCI İRSALİYE KONTROL RAPORU\n"
            "==================================\n"
            f"İrsaliye ID: {irsaliye_id or 'Bilinmiyor'}\n"
            "Satın Alma ID: — (Doğrudan İrsaliye Girişi)\n\n"
            "Bu irsaliye herhangi bir Satın Alma Talebine bağlı olmadan direkt girilmiştir.\n"
            "Miktar karşılaştırması devre dışıdır. Kontrolü manuel yapınız.\n\n"
            "Finans Sonucu: MANUEL KONTROL BEKLENİYOR"
        )
        sonuc_bos = {
            "genel_uyumlu": True, 
            "form_uyumlu": True, 
            "kalem_uyumlu": True,
            "form_ozet": {"toplam_talep": 0, "toplam_teslim": 0, "fark": 0},
            "kalemler": []
        }
        return True, sonuc_bos, rapor_bos
    # -----------------------------------------------------

    detay = satin_alma_detay_getir(sa_id)
    satin_alma_kalemleri = detay.get("kalemler", [])
    if not satin_alma_kalemleri:
        return False, "Satın alma kalemleri bulunamadı", None

    irsaliye_kalemleri = sa_id_irsaliye_kalemleri_topla(sa_id)
    sonuc = karsilastir(satin_alma_kalemleri, irsaliye_kalemleri)
    ir_id = irsaliye_id or (sa_id + " (tüm irsaliyeler)")
    rapor = rapor_metni_olustur(sa_id, ir_id, sonuc)
    return True, sonuc, rapor

def irsaliye_onay_durumu_guncelle(irsaliye_id, onay_durumu, karsilastirma_raporu=None):
    try:
        guncelleme = {"onay_durumu": onay_durumu}
        if karsilastirma_raporu is not None:
            guncelleme["karsilastirma_raporu"] = karsilastirma_raporu
        response = (
            supabase
            .table("irsaliyeler")
            .update(guncelleme)
            .eq("irsaliye_id", irsaliye_id)
            .execute()
        )
        return True, response
    except Exception as e:
        print("İrsaliye onay durumu güncelleme hatası:", e)
        return False, str(e)

def irsaliye_karsilastirma_raporu_guncelle(irsaliye_id, karsilastirma_raporu):
    try:
        response = (
            supabase
            .table("irsaliyeler")
            .update({"karsilastirma_raporu": karsilastirma_raporu})
            .eq("irsaliye_id", irsaliye_id)
            .execute()
        )
        return True, response
    except Exception as e:
        print("İrsaliye karşılaştırma raporu güncelleme hatası:", e)
        return False, str(e)


# =====================================================================
# FATURA MODÜLÜ  (YENİ — TAM İMPLEMENTASYON)
# =====================================================================

def fatura_id_uret():
    import uuid
    return f"FT-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"

def fatura_kaydet(form):
    """
    form = {
      fatura_no, tarih, cari_kart_id,
      toplam_tutar, kdv_tutar, genel_toplam,
      durum, rapor
    }
    Döner: (True, fatura_id) veya (False, hata_mesaji)
    """
    try:
        response = supabase.table("faturalar").insert({
            "fatura_no":     form["fatura_no"],
            "tarih":         form.get("tarih"),
            "cari_kart_id":  form.get("cari_kart_id"),
            "toplam_tutar":  form.get("toplam_tutar"),
            "kdv_tutar":     form.get("kdv_tutar"),
            "genel_toplam":  form.get("genel_toplam"),
            "durum":         form.get("durum", "KONTROL BEKLIYOR"),
            "rapor":         form.get("rapor"),
        }).execute()
        kayit = (response.data or [None])[0]
        return True, (kayit or {}).get("id")
    except Exception as e:
        print("Fatura kayıt hatası:", e)
        return False, str(e)

def fatura_guncelle(fatura_id, form):
    try:
        response = (
            supabase.table("faturalar")
            .update({
                "fatura_no":    form.get("fatura_no"),
                "tarih":        form.get("tarih"),
                "cari_kart_id": form.get("cari_kart_id"),
                "toplam_tutar": form.get("toplam_tutar"),
                "kdv_tutar":    form.get("kdv_tutar"),
                "genel_toplam": form.get("genel_toplam"),
                "durum":        form.get("durum"),
                "rapor":        form.get("rapor"),
            })
            .eq("id", fatura_id)
            .execute()
        )
        return True, response
    except Exception as e:
        print("Fatura güncelleme hatası:", e)
        return False, str(e)

def fatura_kalem_ekle(kalem):
    """
    kalem = { fatura_id, urun_adi, miktar, birim,
              birim_fiyat, kdv_oran, toplam, stok_kart_id }
    """
    try:
        stok_kart = stok_kart_bul_veya_olustur(kalem["urun_adi"], kalem.get("birim") or "ADET")
        response = supabase.table("fatura_kalemleri").insert({
            "fatura_id":    kalem["fatura_id"],
            "urun_adi":     kalem["urun_adi"],
            "miktar":       kalem.get("miktar"),
            "birim":        kalem.get("birim"),
            "birim_fiyat":  kalem.get("birim_fiyat"),
            "kdv_oran":     kalem.get("kdv_oran", 20),
            "toplam":       kalem.get("toplam"),
            "stok_kart_id": kalem.get("stok_kart_id") or (stok_kart or {}).get("id"),
        }).execute()
        return True, response
    except Exception as e:
        print("Fatura kalem ekleme hatası:", e)
        return False, str(e)

def fatura_kalemleri_yenile(fatura_id, kalemler):
    try:
        supabase.table("fatura_kalemleri").delete().eq("fatura_id", fatura_id).execute()
        if not kalemler:
            return True, None
        for k in kalemler:
            stok_kart = stok_kart_bul_veya_olustur(k.get("urun_adi"), k.get("birim") or "ADET")
            k["fatura_id"] = fatura_id
            k["stok_kart_id"] = k.get("stok_kart_id") or (stok_kart or {}).get("id")
        response = supabase.table("fatura_kalemleri").insert(kalemler).execute()
        return True, response
    except Exception as e:
        print("Fatura kalemleri yenileme hatası:", e)
        return False, str(e)

def fatura_irsaliye_bagla(fatura_id, irsaliye_id, sa_id=None):
    """1 faturaya birden fazla irsaliye bağla."""
    try:
        response = supabase.table("fatura_irsaliye_baglanti").upsert({
            "fatura_id":   fatura_id,
            "irsaliye_id": irsaliye_id,
            "sa_id":       sa_id,
        }, on_conflict="fatura_id,irsaliye_id").execute()
        return True, response
    except Exception as e:
        print("Fatura-irsaliye bağlantı hatası:", e)
        return False, str(e)

def fatura_irsaliye_baglantilari_getir(fatura_id):
    try:
        return (
            supabase.table("fatura_irsaliye_baglanti")
            .select("*")
            .eq("fatura_id", fatura_id)
            .execute()
            .data or []
        )
    except Exception as e:
        print("Fatura-irsaliye bağlantıları getirme hatası:", e)
        return []

def fatura_irsaliye_baglantiyi_sil(fatura_id, irsaliye_id):
    try:
        supabase.table("fatura_irsaliye_baglanti") \
            .delete() \
            .eq("fatura_id", fatura_id) \
            .eq("irsaliye_id", irsaliye_id) \
            .execute()
        return True
    except Exception as e:
        print("Fatura-irsaliye bağlantı silme hatası:", e)
        return False

def faturalar_getir():
    try:
        return (
            supabase.table("faturalar")
            .select("*")
            .order("tarih", desc=True)
            .execute()
            .data or []
        )
    except Exception as e:
        print("Fatura listeleme hatası:", e)
        return []

def fatura_detay_getir(fatura_id):
    """Fatura + kalemleri + bağlı irsaliyeler."""
    try:
        fatura_res = (
            supabase.table("faturalar")
            .select("*")
            .eq("id", fatura_id)
            .single()
            .execute()
        )
        kalem_res = (
            supabase.table("fatura_kalemleri")
            .select("*")
            .eq("fatura_id", fatura_id)
            .order("id")
            .execute()
        )
        baglanti_res = (
            supabase.table("fatura_irsaliye_baglanti")
            .select("*")
            .eq("fatura_id", fatura_id)
            .execute()
        )
        return {
            "fatura":       fatura_res.data,
            "kalemler":     kalem_res.data or [],
            "irsaliyeler":  baglanti_res.data or [],
        }
    except Exception as e:
        print(f"Fatura detay getirme hatası: {e}")
        return {"fatura": None, "kalemler": [], "irsaliyeler": []}

def fatura_karsilastir(fatura_id):
    """
    Faturaya bağlı tüm irsaliyelerin kümülatif kalemleri ile
    fatura kalemlerini karşılaştırır.
    Döner: (True, sonuc_dict, rapor_str) veya (False, hata, None)
    """
    from irsaliye_karsilastir import karsilastir, rapor_metni_olustur

    detay = fatura_detay_getir(fatura_id)
    fatura = detay.get("fatura")
    if not fatura:
        return False, "Fatura bulunamadı", None

    fatura_kalemleri_listesi = detay.get("kalemler", [])
    if not fatura_kalemleri_listesi:
        return False, "Fatura kalemi girilmemiş", None

    # Bağlı irsaliyelerden tüm kalemleri topla
    baglanti_listesi = detay.get("irsaliyeler", [])
    tum_ir_kalemleri = []
    for bag in baglanti_listesi:
        ir_detay = irsaliye_detay_getir(bag["irsaliye_id"])
        tum_ir_kalemleri.extend(ir_detay.get("kalemler", []))

    if not tum_ir_kalemleri:
        return False, "Bağlı irsaliye kalemi bulunamadı", None

    # fatura_kalemleri → satin_alma_kalemleri formatına dönüştür
    fk_donusturulmus = []
    for fk in fatura_kalemleri_listesi:
        fk_donusturulmus.append({
            "urun_adi":            fk.get("urun_adi"),
            "talep_edilen_miktar": fk.get("miktar"),
            "talep_birimi":        fk.get("birim"),
        })

    sonuc = karsilastir(fk_donusturulmus, tum_ir_kalemleri)
    rapor = rapor_metni_olustur(
        f"FATURA:{fatura.get('fatura_no')}",
        f"{len(baglanti_listesi)} irsaliye",
        sonuc
    )
    return True, sonuc, rapor

def fatura_onay_durumu_guncelle(fatura_id, durum, rapor=None):
    try:
        guncelleme = {"durum": durum}
        if rapor:
            guncelleme["rapor"] = rapor
        supabase.table("faturalar").update(guncelleme).eq("id", fatura_id).execute()
        return True
    except Exception as e:
        print("Fatura onay güncelleme hatası:", e)
        return False

def fatura_imzali_evrak_guncelle(fatura_id, evrak_yolu):
    try:
        supabase.table("faturalar").update({
            "imzali_evrak_url": evrak_yolu,
            "durum": "ONAYLANDI",
        }).eq("id", fatura_id).execute()
        return True, None
    except Exception as e:
        print("Fatura imzalı evrak hatası:", e)
        return False, str(e)


# =====================================================================
# GENEL MODÜL YARDIMCILARI
# =====================================================================

def generic_listele(table_name, order_by="created_at"):
    try:
        query = supabase.table(table_name).select("*")
        if order_by:
            query = query.order(order_by, desc=True)
        return query.execute().data or []
    except Exception as e:
        print(f"{table_name} listeleme hatası:", e)
        return []

def generic_kaydet(table_name, data, record_id=None):
    try:
        if record_id:
            response = supabase.table(table_name).update(data).eq("id", record_id).execute()
        else:
            response = supabase.table(table_name).insert(data).execute()
        return True, response
    except Exception as e:
        print(f"{table_name} kayıt hatası:", e)
        return False, str(e)

def cari_kartlari_getir(kart_tipi=None):
    try:
        query = supabase.table("cari_kartlar").select("*").order("unvan")
        if kart_tipi:
            query = query.eq("kart_tipi", kart_tipi)
        return query.execute().data or []
    except Exception as e:
        print("Cari kart listeleme hatası:", e)
        return []

def stok_kartlari_getir():
    try:
        return supabase.table("stok_kartlari").select("*").order("stok_adi").execute().data or []
    except Exception as e:
        print("Stok kart listeleme hatası:", e)
        return []

def cari_kart_bul_veya_olustur(unvan, kart_tipi="TEDARIKCI"):
    unvan = (unvan or "").strip()
    if not unvan:
        return None
    try:
        mevcut = (
            supabase.table("cari_kartlar")
            .select("*")
            .ilike("unvan", unvan)
            .limit(1)
            .execute()
            .data or []
        )
        if mevcut:
            return mevcut[0]
        response = supabase.table("cari_kartlar").insert({
            "kart_tipi": kart_tipi,
            "unvan": unvan,
            "durum": "AKTIF",
        }).execute()
        return (response.data or [None])[0]
    except Exception as e:
        print("Cari kart oluşturma hatası:", e)
        return None

def kasa_hareketi_kaydet(hareket):
    """Kasa hareketi kaydeder (giriş/çıkış)."""
    try:
        response = supabase.table("kasa_hareketleri").insert({
            "tarih": hareket.get("tarih"),
            "hareket_tipi": hareket.get("hareket_tipi"),  # GIRIS/CIKIS
            "tutar": hareket.get("tutar"),
            "aciklama": hareket.get("aciklama"),
            "referans_tipi": hareket.get("referans_tipi"),  # FATURA/IRSALIYE/MAAS/DIGER
            "referans_id": hareket.get("referans_id"),
            "fatura_kodu": hareket.get("fatura_kodu"),
            "irsaliye_id": hareket.get("irsaliye_id"),
        }).execute()
        return True, response
    except Exception as e:
        print("Kasa hareketi kayıt hatası:", e)
        return False, str(e)

def kasa_hareketleri_getir(baslangic_tarih=None, bitis_tarih=None):
    """Kasa hareketlerini tarih aralığına göre getirir."""
    try:
        query = supabase.table("kasa_hareketleri").select("*").order("tarih", desc=True)
        if baslangic_tarih:
            query = query.gte("tarih", baslangic_tarih)
        if bitis_tarih:
            query = query.lte("tarih", bitis_tarih)
        return query.execute().data or []
    except Exception as e:
        print("Kasa hareketleri getirme hatası:", e)
        return []

def kasa_haftalik_raporu(yil, hafta):
    """Haftalık kasa raporu oluşturur."""
    try:
        from datetime import datetime, timedelta
        
        # Haftanın başlangıç ve bitiş tarihlerini hesapla
        baslangic = datetime.strptime(f"{yil}-W{hafta}-1", "%Y-W%W-%w").date()
        bitis = baslangic + timedelta(days=6)
        
        baslangic_str = baslangic.strftime("%Y-%m-%d")
        bitis_str = bitis.strftime("%Y-%m-%d")
        
        hareketler = kasa_hareketleri_getir(baslangic_str, bitis_str)
        
        giris_toplam = sum(float(h.get("tutar") or 0) for h in hareketler if h.get("hareket_tipi") == "GIRIS")
        cikis_toplam = sum(float(h.get("tutar") or 0) for h in hareketler if h.get("hareket_tipi") == "CIKIS")
        bakiye = giris_toplam - cikis_toplam
        
        return {
            "yil": yil,
            "hafta": hafta,
            "baslangic_tarih": baslangic_str,
            "bitis_tarih": bitis_str,
            "hareketler": hareketler,
            "giris_toplam": giris_toplam,
            "cikis_toplam": cikis_toplam,
            "bakiye": bakiye
        }
    except Exception as e:
        print("Haftalık kasa raporu hatası:", e)
        return None

def arac_kaydet(arac):
    """Araç/iş makinesi kaydeder."""
    try:
        response = supabase.table("arac_kartlari").insert({
            "plaka": arac.get("plaka"),
            "arac_tipi": arac.get("arac_tipi"),  # ARAC/IS_MAKINESI/DEMIRBAS
            "marka": arac.get("marka"),
            "model": arac.get("model"),
            "yil": arac.get("yil"),
            "km": arac.get("km", 0),
            "km_bakim": arac.get("km_bakim"),
            "yag_bakim": arac.get("yag_bakim"),
            "muayene_tarihi": arac.get("muayene_tarihi"),
            "durum": arac.get("durum", "AKTIF"),
            "aciklama": arac.get("aciklama"),
        }).execute()
        return True, response
    except Exception as e:
        print("Araç kayıt hatası:", e)
        return False, str(e)

def araclar_getir(arac_tipi=None):
    """Araçları listeler."""
    try:
        query = supabase.table("arac_kartlari").select("*").order("plaka")
        if arac_tipi:
            query = query.eq("arac_tipi", arac_tipi)
        return query.execute().data or []
    except Exception as e:
        print("Araç listeleme hatası:", e)
        return []

def arac_guncelle(arac_id, arac):
    """Araç bilgilerini günceller."""
    try:
        response = (
            supabase.table("arac_kartlari")
            .update({
                "plaka": arac.get("plaka"),
                "arac_tipi": arac.get("arac_tipi"),
                "marka": arac.get("marka"),
                "model": arac.get("model"),
                "yil": arac.get("yil"),
                "km": arac.get("km"),
                "km_bakim": arac.get("km_bakim"),
                "yag_bakim": arac.get("yag_bakim"),
                "muayene_tarihi": arac.get("muayene_tarihi"),
                "durum": arac.get("durum"),
                "aciklama": arac.get("aciklama"),
            })
            .eq("id", arac_id)
            .execute()
        )
        return True, response
    except Exception as e:
        print("Araç güncelleme hatası:", e)
        return False, str(e)

def arac_km_girisi_km(km_giris):
    """Araç km girişi kaydeder."""
    try:
        response = supabase.table("arac_km_girisleri").insert({
            "arac_id": km_giris.get("arac_id"),
            "tarih": km_giris.get("tarih"),
            "km": km_giris.get("km"),
            "personel_id": km_giris.get("personel_id"),
            "aciklama": km_giris.get("aciklama"),
        }).execute()
        
        # Araç km'sini güncelle
        supabase.table("arac_kartlari").update({
            "km": km_giris.get("km")
        }).eq("id", km_giris.get("arac_id")).execute()
        
        return True, response
    except Exception as e:
        print("KM giriş hatası:", e)
        return False, str(e)

def arac_km_girisleri_getir(arac_id=None, baslangic=None, bitis=None):
    """Araç km girişlerini listeler."""
    try:
        query = supabase.table("arac_km_girisleri").select("*").order("tarih", desc=True)
        if arac_id:
            query = query.eq("arac_id", arac_id)
        if baslangic:
            query = query.gte("tarih", baslangic)
        if bitis:
            query = query.lte("tarih", bitis)
        return query.execute().data or []
    except Exception as e:
        print("KM girişleri listeleme hatası:", e)
        return []

def tahsis_kaydet(tahsis):
    """Demirbaş/araç tahsisini kaydeder."""
    try:
        response = supabase.table("tahsis_kayitlari").insert({
            "arac_id": tahsis.get("arac_id"),
            "personel_id": tahsis.get("personel_id"),
            "tahsis_tarihi": tahsis.get("tahsis_tarihi"),
            "iade_tarihi": tahsis.get("iade_tarihi"),
            "durum": tahsis.get("durum", "TAHSISLI"),
            "aciklama": tahsis.get("aciklama"),
        }).execute()
        return True, response
    except Exception as e:
        print("Tahsis kayıt hatası:", e)
        return False, str(e)

def tahsisleri_getir(arac_id=None, personel_id=None):
    """Tahsisleri listeler."""
    try:
        query = supabase.table("tahsis_kayitlari").select("*").order("tahsis_tarihi", desc=True)
        if arac_id:
            query = query.eq("arac_id", arac_id)
        if personel_id:
            query = query.eq("personel_id", personel_id)
        return query.execute().data or []
    except Exception as e:
        print("Tahsis listeleme hatası:", e)
        return []

def kamp_odasi_kaydet(oda):
    """Kamp odası kaydeder."""
    try:
        response = supabase.table("kamp_odalari").insert({
            "yerleske_adi": oda.get("yerleske_adi"),
            "kogus_no": oda.get("kogus_no"),
            "oda_no": oda.get("oda_no"),
            "kapasite": oda.get("kapasite", 6),
            "firma_tipi": oda.get("firma_tipi"),  # ANA_FIRMA/TASERON
            "durum": oda.get("durum", "BOŞ"),
        }).execute()
        return True, response
    except Exception as e:
        print("Kamp odası kayıt hatası:", e)
        return False, str(e)

def kamp_odalari_getir(yerleske_adi=None):
    """Kamp odalarını listeler."""
    try:
        query = supabase.table("kamp_odalari").select("*").order("yerleske_adi, kogus_no, oda_no")
        if yerleske_adi:
            query = query.eq("yerleske_adi", yerleske_adi)
        return query.execute().data or []
    except Exception as e:
        print("Kamp odaları listeleme hatası:", e)
        return []

def kamp_kayit_kaydet(kayit):
    """Kamp kaydı (personel oda ataması) ekler."""
    try:
        response = supabase.table("kamp_kayitlari").insert({
            "personel_id": kayit.get("personel_id"),
            "oda_id": kayit.get("oda_id"),
            "giris_tarihi": kayit.get("giris_tarihi"),
            "cikis_tarihi": kayit.get("cikis_tarihi"),
            "durum": kayit.get("durum", "AKTIF"),
        }).execute()
        
        # Oda durumunu güncelle
        if kayit.get("durum") == "AKTIF":
            supabase.table("kamp_odalari").update({
                "durum": "DOLU"
            }).eq("id", kayit.get("oda_id")).execute()
        
        return True, response
    except Exception as e:
        print("Kamp kaydı hatası:", e)
        return False, str(e)

def kamp_kayitlari_getir(personel_id=None, oda_id=None):
    """Kamp kayıtlarını listeler."""
    try:
        query = supabase.table("kamp_kayitlari").select("*").order("giris_tarihi", desc=True)
        if personel_id:
            query = query.eq("personel_id", personel_id)
        if oda_id:
            query = query.eq("oda_id", oda_id)
        return query.execute().data or []
    except Exception as e:
        print("Kamp kayıtları listeleme hatası:", e)
        return []

def kamp_sarf_malzeme_kaydet(malzeme):
    """Kamp sarf malzemesi kaydeder."""
    try:
        response = supabase.table("kamp_sarf_malzemeleri").insert({
            "malzeme_adi": malzeme.get("malzeme_adi"),
            "miktar": malzeme.get("miktar"),
            "birim": malzeme.get("birim", "ADET"),
            "giris_tarihi": malzeme.get("giris_tarihi"),
            "yerleske_adi": malzeme.get("yerleske_adi"),
            "aciklama": malzeme.get("aciklama"),
        }).execute()
        return True, response
    except Exception as e:
        print("Kamp sarf malzemesi kayıt hatası:", e)
        return False, str(e)

def kamp_sarf_malzemeleri_getir(yerleske_adi=None):
    """Kamp sarf malzemelerini listeler."""
    try:
        query = supabase.table("kamp_sarf_malzemeleri").select("*").order("giris_tarihi", desc=True)
        if yerleske_adi:
            query = query.eq("yerleske_adi", yerleske_adi)
        return query.execute().data or []
    except Exception as e:
        print("Kamp sarf malzemeleri listeleme hatası:", e)
        return []

def kamp_faaliyet_kaydet(faaliyet):
    """Kamp faaliyeti kaydeder."""
    try:
        response = supabase.table("kamp_faaliyetleri").insert({
            "personel_id": faaliyet.get("personel_id"),
            "tarih": faaliyet.get("tarih"),
            "faaliyet_tipi": faaliyet.get("faaliyet_tipi"),
            "aciklama": faaliyet.get("aciklama"),
            "yerleske_adi": faaliyet.get("yerleske_adi"),
        }).execute()
        return True, response
    except Exception as e:
        print("Kamp faaliyeti kayıt hatası:", e)
        return False, str(e)

def kamp_faaliyetleri_getir(personel_id=None, tarih=None):
    """Kamp faaliyetlerini listeler."""
    try:
        query = supabase.table("kamp_faaliyetleri").select("*").order("tarih", desc=True)
        if personel_id:
            query = query.eq("personel_id", personel_id)
        if tarih:
            query = query.eq("tarih", tarih)
        return query.execute().data or []
    except Exception as e:
        print("Kamp faaliyetleri listeleme hatası:", e)
        return []

def saha_faaliyeti_kaydet(faaliyet):
    """Saha faaliyeti kaydeder."""
    try:
        response = supabase.table("saha_faaliyetleri").insert({
            "personel_id": faaliyet.get("personel_id"),
            "tarih": faaliyet.get("tarih"),
            "is_niteligi": faaliyet.get("is_niteligi") or faaliyet.get("is_niteliği"),
            "parsel": faaliyet.get("parsel"),
            "blok": faaliyet.get("blok"),
            "aciklama": faaliyet.get("aciklama"),
            "foto_url": faaliyet.get("foto_url"),
        }).execute()
        return True, response
    except Exception as e:
        print("Saha faaliyeti kayıt hatası:", e)
        return False, str(e)

def saha_faaliyetleri_getir(personel_id=None, tarih=None, parsel=None):
    """Saha faaliyetlerini listeler."""
    try:
        query = supabase.table("saha_faaliyetleri").select("*").order("tarih", desc=True)
        if personel_id:
            query = query.eq("personel_id", personel_id)
        if tarih:
            query = query.eq("tarih", tarih)
        if parsel:
            query = query.eq("parsel", parsel)
        return query.execute().data or []
    except Exception as e:
        print("Saha faaliyetleri listeleme hatası:", e)
        return []

def saha_aylik_raporu(yil, ay):
    """Aylık saha faaliyet raporu oluşturur."""
    try:
        baslangic = f"{yil}-{ay:02d}-01"
        bitis = f"{yil+1}-01-01" if ay == 12 else f"{yil}-{ay+1:02d}-01"
        
        faaliyetler = saha_faaliyetleri_getir()
        rapor_faaliyetleri = []
        
        for f in faaliyetler:
            tarih = f.get("tarih", "")
            if baslangic <= tarih < bitis:
                rapor_faaliyetleri.append(f)
        
        return {
            "yil": yil,
            "ay": ay,
            "baslangic_tarih": baslangic,
            "bitis_tarih": bitis,
            "faaliyetler": rapor_faaliyetleri
        }
    except Exception as e:
        print("Aylık saha raporu hatası:", e)
        return None

def hazir_tutanak_kaydet(tutanak):
    """Hazır tutanak kaydeder."""
    try:
        response = supabase.table("hazir_tutanaklar").insert({
            "tutanak_tipi": tutanak.get("tutanak_tipi"),  # TAHISIS/TESLIM/SEVK
            "tarih": tutanak.get("tarih"),
            "personel_id": tutanak.get("personel_id"),
            "icerik": tutanak.get("icerik"),
            "evrak_url": tutanak.get("evrak_url"),
            "durum": tutanak.get("durum", "TASLAK"),
        }).execute()
        return True, response
    except Exception as e:
        print("Hazır tutanak kayıt hatası:", e)
        return False, str(e)

def hazir_tutanaklar_getir(tip=None, personel_id=None):
    """Hazır tutanakları listeler."""
    try:
        query = supabase.table("hazir_tutanaklar").select("*").order("tarih", desc=True)
        if tip:
            query = query.eq("tutanak_tipi", tip)
        if personel_id:
            query = query.eq("personel_id", personel_id)
        return query.execute().data or []
    except Exception as e:
        print("Hazır tutanaklar listeleme hatası:", e)
        return []

def stok_kart_bul_veya_olustur(stok_adi, birim="ADET"):
    stok_adi = (stok_adi or "").strip()
    if not stok_adi:
        return None
    try:
        mevcut = (
            supabase.table("stok_kartlari")
            .select("*")
            .ilike("stok_adi", stok_adi)
            .limit(1)
            .execute()
            .data or []
        )
        if mevcut:
            return mevcut[0]
        response = supabase.table("stok_kartlari").insert({
            "stok_adi": stok_adi,
            "birim": birim or "ADET",
            "durum": "AKTIF",
        }).execute()
        return (response.data or [None])[0]
    except Exception as e:
        print("Stok kart oluşturma hatası:", e)
        return None

def kart_gecmisi_getir(kart_tipi, kart_id):
    try:
        return (
            supabase
            .table("kart_islem_gecmisi")
            .select("*")
            .eq("kart_tipi", kart_tipi)
            .eq("kart_id", kart_id)
            .order("tarih", desc=True)
            .execute()
            .data or []
        )
    except Exception as e:
        print("Kart geçmişi listeleme hatası:", e)
        return []

def kart_gecmisi_ekle(kart_tipi, kart_id, islem_tipi, belge_no, aciklama, tutar=None):
    try:
        response = supabase.table("kart_islem_gecmisi").insert({
            "kart_tipi":  kart_tipi,
            "kart_id":    kart_id,
            "islem_tipi": islem_tipi,
            "belge_no":   belge_no,
            "aciklama":   aciklama,
            "tutar":      tutar,
            "tarih":      datetime.now().strftime("%Y-%m-%d"),
        }).execute()
        return True, response
    except Exception as e:
        print("Kart geçmişi ekleme hatası:", e)
        return False, str(e)

def cari_kart_bul_veya_olustur_v2(unvan, kart_tipi="TEDARIKCI"):
    """Alias — yeni modüller için. cari_kart_bul_veya_olustur ile aynı davranışı gösterir."""
    return cari_kart_bul_veya_olustur(unvan, kart_tipi)

def fatura_kodu_uret():
    """Fatura takibi için benzersiz bir kod (FT-YYYYMMDD-XXXX) üretir."""
    import uuid
    from datetime import datetime
    return f"FT-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"
    return f"FT-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"