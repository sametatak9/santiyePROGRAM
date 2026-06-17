"""
baglanti_kontrol.py
-------------------
Program açılışında Supabase bağlantısını ve tüm tabloları test eder.
Ana pencere gösterilmeden önce bu ekran açılır.
"""
import threading
import customtkinter as ctk
from ui_theme import UI


TABLOLAR = [
    ("personel",                 "Personel"),
    ("yoklamalar",               "Yoklama / Puantaj"),
    ("satin_alma_formlari",      "Satın Alma Formları"),
    ("satin_alma_kalemleri",     "Satın Alma Kalemleri"),
    ("irsaliyeler",              "İrsaliyeler"),
    ("irsaliye_kalemleri",       "İrsaliye Kalemleri"),
    ("faturalar",                "Faturalar"),
    ("fatura_kalemleri",         "Fatura Kalemleri"),
    ("fatura_irsaliye_baglanti", "Fatura–İrsaliye Bağlantı"),
    ("cari_kartlar",             "Cari Kartlar"),
    ("stok_kartlari",            "Stok Kartları"),
    ("kasa_hareketleri",         "Kasa Hareketleri"),
    ("arac_kartlari",            "Araç Kartları"),
    ("arac_km_girisleri",        "Araç KM Girişleri"),
    ("demirbas_kartlari",        "Demirbaş Kartları"),
    ("tahsis_kayitlari",         "Tahsis Kayıtları"),
    ("kamp_odalari",             "Kamp Odaları"),
    ("kamp_kayitlari",           "Kamp Kayıtları"),
    ("kamp_sarf_malzemeleri",    "Kamp Sarf Malzemeleri"),
    ("kamp_faaliyetleri",        "Kamp Faaliyetleri"),
    ("saha_faaliyetleri",        "Saha Faaliyetleri"),
    ("hazir_tutanaklar",         "Hazır Tutanaklar"),
    ("kart_islem_gecmisi",       "Kart İşlem Geçmişi"),
]


class BaglantiKontrol(ctk.CTkToplevel):
    """
    Uygulama açılışında gösterilen Supabase bağlantı test ekranı.
    Test bitince 'Devam Et' aktifleşir veya hata sayısı gösterilir.
    """

    def __init__(self, master, on_devam):
        super().__init__(master)
        self.on_devam = on_devam
        self.title("KIBRITCI ERP — Sistem Kontrolü")
        self.geometry("620x680")
        self.resizable(False, False)
        self.configure(fg_color=UI.BG)
        self.protocol("WM_DELETE_WINDOW", self._kapat)
        self.grab_set()

        self._build_ui()
        self.after(300, self._baslat)

    # ------------------------------------------------------------------ #
    # UI
    # ------------------------------------------------------------------ #
    def _build_ui(self):
        # Başlık
        baslik = ctk.CTkFrame(self, fg_color=UI.SIDEBAR, corner_radius=0, height=80)
        baslik.pack(fill="x")
        baslik.pack_propagate(False)

        ctk.CTkLabel(
            baslik, text="🔌  Supabase Bağlantı Kontrolü",
            font=(UI.FONT, 18, "bold"), text_color="white", anchor="w",
        ).pack(side="left", padx=24, pady=0)

        # Genel durum
        self.durum_label = ctk.CTkLabel(
            self, text="Bağlantı test ediliyor…",
            font=(UI.FONT, 13), text_color=UI.TEXT_MUTED,
        )
        self.durum_label.pack(pady=(16, 4))

        # İlerleme çubuğu
        self.progress = ctk.CTkProgressBar(self, width=560, height=8,
                                           fg_color=UI.BORDER, progress_color=UI.PRIMARY)
        self.progress.set(0)
        self.progress.pack(pady=(0, 14))

        # Tablo listesi (kaydırılabilir)
        kart = ctk.CTkFrame(self, fg_color=UI.SURFACE, corner_radius=12,
                            border_width=1, border_color=UI.BORDER)
        kart.pack(fill="both", expand=True, padx=20, pady=(0, 14))

        self.scroll = ctk.CTkScrollableFrame(kart, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=4, pady=4)

        self.satir_widgets = {}
        for tablo, ad in TABLOLAR:
            satir = ctk.CTkFrame(self.scroll, fg_color="transparent")
            satir.pack(fill="x", pady=3, padx=6)

            ikon = ctk.CTkLabel(satir, text="⏳", width=28,
                                font=(UI.FONT, 14), anchor="center")
            ikon.pack(side="left")

            ctk.CTkLabel(satir, text=ad, anchor="w",
                         font=(UI.FONT, 12), text_color=UI.TEXT,
                         width=260).pack(side="left", padx=6)

            mesaj = ctk.CTkLabel(satir, text="Bekleniyor…", anchor="w",
                                 font=(UI.FONT, 11), text_color=UI.TEXT_MUTED)
            mesaj.pack(side="left")

            self.satir_widgets[tablo] = (ikon, mesaj)

        # Alt buton alanı
        alt = ctk.CTkFrame(self, fg_color="transparent")
        alt.pack(fill="x", padx=20, pady=(0, 18))

        self.ozet_label = ctk.CTkLabel(alt, text="",
                                       font=(UI.FONT, 12, "bold"), anchor="w")
        self.ozet_label.pack(side="left")

        self.devam_btn = ctk.CTkButton(
            alt, text="Devam Et →",
            font=(UI.FONT, 13, "bold"), height=40, width=140,
            fg_color=UI.PRIMARY, hover_color=UI.PRIMARY_HOVER,
            state="disabled", command=self._devam,
        )
        self.devam_btn.pack(side="right")

        self.atla_btn = ctk.CTkButton(
            alt, text="Hatayla Devam Et",
            font=(UI.FONT, 11), height=40, width=150,
            fg_color=UI.WARNING, hover_color="#D97706",
            state="disabled", command=self._devam,
        )
        self.atla_btn.pack(side="right", padx=(0, 8))

    # ------------------------------------------------------------------ #
    # Test mantığı (arka plan thread)
    # ------------------------------------------------------------------ #
    def _baslat(self):
        threading.Thread(target=self._test_calis, daemon=True).start()

    def _test_calis(self):
        import db_manager
        toplam = len(TABLOLAR)
        hata_sayisi = 0

        for i, (tablo, _ad) in enumerate(TABLOLAR):
            try:
                res = db_manager.supabase.table(tablo).select("id").limit(1).execute()
                self.after(0, self._guncelle_satir, tablo, True,
                           f"✅  Bağlı  ({len(res.data)} kayıt)")
            except Exception as e:
                hata_sayisi += 1
                kisa = str(e)[:60]
                self.after(0, self._guncelle_satir, tablo, False,
                           f"❌  {kisa}")

            self.after(0, self.progress.set, (i + 1) / toplam)
            self.after(0, self.durum_label.configure,
                       {"text": f"Test ediliyor… {i+1}/{toplam}"})

        self.after(0, self._tamamlandi, hata_sayisi)

    def _guncelle_satir(self, tablo, basarili, mesaj):
        ikon_w, mesaj_w = self.satir_widgets[tablo]
        if basarili:
            ikon_w.configure(text="✅")
            mesaj_w.configure(text=mesaj, text_color=UI.SUCCESS)
        else:
            ikon_w.configure(text="❌")
            mesaj_w.configure(text=mesaj, text_color=UI.DANGER)

    def _tamamlandi(self, hata_sayisi):
        toplam = len(TABLOLAR)
        if hata_sayisi == 0:
            self.durum_label.configure(
                text=f"✅  Tüm {toplam} tablo başarıyla bağlandı!",
                text_color=UI.SUCCESS,
            )
            self.ozet_label.configure(
                text=f"{toplam}/{toplam} tablo OK", text_color=UI.SUCCESS)
            self.devam_btn.configure(state="normal")
        else:
            self.durum_label.configure(
                text=f"⚠️  {hata_sayisi} tabloda sorun tespit edildi.",
                text_color=UI.WARNING,
            )
            self.ozet_label.configure(
                text=f"{toplam - hata_sayisi}/{toplam} tablo OK  |  {hata_sayisi} hatalı",
                text_color=UI.WARNING,
            )
            self.devam_btn.configure(state="normal")
            self.atla_btn.configure(state="normal")

    # ------------------------------------------------------------------ #
    # Kontroller
    # ------------------------------------------------------------------ #
    def _devam(self):
        self.grab_release()
        self.destroy()
        self.on_devam()

    def _kapat(self):
        import sys
        sys.exit(0)


def baglanti_kontrolu_goster(ana_pencere, on_devam):
    """main.py'den çağrılır. Ana pencere gizlenirken bu ekran önce açılır."""
    pencere = BaglantiKontrol(ana_pencere, on_devam)
    pencere.focus()
