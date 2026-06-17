import customtkinter as ctk

import db_manager
from db_manager import aktif_personeller_getir, yoklama_getir
from fatura import FaturaModul
from irsaliye import IrsaliyeModul
from maas_arayuz import MaasArayuz
from personel_modul import PersonelKayitFrame
from satin_alma import SatinAlmaModul
from ui_theme import UI, apply_app_theme, menu_button, page_badge
from arac_demirbas import AracDemirbasModul
from kasa_raporu import KasaRaporuModul
from kamp_yonetimi import KampYonetimiModul
from saha_faaliyeti import SahaFaaliyetiModul
from hazir_tutanaklar import HazirTutanaklarModul
from cari_kartlar_modul import CariKartlarModul
from stok_kartlar_modul import StokKartlariModul
from yeni_moduller import (
    AracTakipModul,
    DemirbasModul,
    EpostaMerkeziModul,
    RaporMerkeziModul,
    TahsisModul,
)
from yoklama_modul import YoklamaPanel
from baglanti_kontrol import baglanti_kontrolu_goster

apply_app_theme()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("KIBRITCI ERP")
        self.geometry("1600x950")
        self.minsize(1200, 700)
        self.configure(fg_color=UI.BG)

        self.db_manager = db_manager
        self.active_menu = None
        self.menu_buttons = {}

        # ──────────────────────────────────────────────
        # Program açılışında bağlantı kontrolü göster
        # Ana pencereyi gizle, kontrol bitince aç
        # ──────────────────────────────────────────────
        self.withdraw()
        self.after(100, self._baglanti_kontrol_baslat)

    def _baglanti_kontrol_baslat(self):
        baglanti_kontrolu_goster(self, self._baglanti_sonrasi_ac)

    def _baglanti_sonrasi_ac(self):
        """Bağlantı kontrolü tamamlandıktan sonra ana pencereyi aç."""
        self._build_sidebar()
        self._build_content()
        self.deiconify()
        self.show_personel_frame()

    # ================================================================
    # SIDEBAR
    # ================================================================
    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=260, fg_color=UI.SIDEBAR,
                                    corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=18, pady=(24, 18))

        ctk.CTkLabel(brand, text="KIBRITCI ERP",
                     font=(UI.FONT, 23, "bold"), text_color="white",
                     anchor="w").pack(fill="x")
        ctk.CTkLabel(brand, text="Şantiye Yönetim Sistemi",
                     font=(UI.FONT, 11), text_color="#94A3B8",
                     anchor="w").pack(fill="x", pady=(2, 0))

        self.menu_area = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        self.menu_area.pack(fill="both", expand=True)

        ctk.CTkLabel(self.menu_area, text="MODÜLLER",
                     font=(UI.FONT, 11, "bold"), text_color="#94A3B8",
                     anchor="w").pack(fill="x", padx=22, pady=(12, 8))

        menu_items = [
            ("personel_grup",  "PERSONEL",            None),
            ("personel",       "Personel Yönetimi",   self.show_personel_frame),
            ("yoklama",        "Yoklama ve Puantaj",   self.show_yoklama_frame),
            ("maas",           "Maaş Hesaplama",       self.show_maas_frame),
            ("finans_grup",    "FİNANS",               None),
            ("cari",           "Cari Kartlar",         self.show_cari_frame),
            ("stok",           "Stok Kartları",        self.show_stok_frame),
            ("satin_alma",     "Satın Alma Talep",     self.show_satin_alma_frame),
            ("irsaliye",       "İrsaliye Girişi",      self.show_irsaliye_frame),
            ("fatura",         "Fatura Girişi",        self.show_fatura_frame),
            ("kasa",           "Haftalık Kasa",        self.show_kasa_frame),
            ("idari_grup",     "İDARİ İŞLER",          None),
            ("arac",           "Araç ve Bakım",        self.show_arac_frame),
            ("demirbas",       "Demirbaş Kartları",    self.show_demirbas_frame),
            ("tahsis",         "Tahsisleme",           self.show_tahsis_frame),
            ("tutanak",        "Hazır Tutanaklar",     self.show_tutanak_frame),
            ("kamp",           "Kamp Yönetimi",        self.show_kamp_frame),
            ("saha",           "Saha Faaliyetleri",    self.show_saha_frame),
            ("rapor_grup",     "RAPOR VE İLETİŞİM",    None),
            ("rapor",          "Rapor Merkezi",        self.show_rapor_frame),
            ("eposta",         "E-Posta Merkezi",      self.show_eposta_frame),
        ]

        for key, text, command in menu_items:
            if command is None:
                ctk.CTkLabel(self.menu_area, text=text,
                             font=(UI.FONT, 10, "bold"), text_color="#64748B",
                             anchor="w").pack(fill="x", padx=22, pady=(12, 4))
                continue
            btn = menu_button(self.menu_area, text,
                              lambda k=key, c=command: self._navigate(k, c))
            btn.pack(fill="x", padx=14, pady=3)
            self.menu_buttons[key] = btn

        footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        footer.pack(side="bottom", fill="x", padx=18, pady=18)
        ctk.CTkLabel(footer, text="v1.0  |  Supabase bağlı",
                     text_color="#64748B", font=(UI.FONT, 11),
                     anchor="w").pack(fill="x")

    # ================================================================
    # CONTENT AREA
    # ================================================================
    def _build_content(self):
        self.right_container = ctk.CTkFrame(self, fg_color="transparent")
        self.right_container.pack(side="right", fill="both", expand=True)

        self.topbar = ctk.CTkFrame(self.right_container, height=74,
                                   fg_color=UI.SURFACE, corner_radius=0)
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        title_block = ctk.CTkFrame(self.topbar, fg_color="transparent")
        title_block.pack(side="left", padx=24, pady=12)

        self.page_title = ctk.CTkLabel(title_block, text="Dashboard",
                                       font=(UI.FONT, 22, "bold"),
                                       text_color=UI.TEXT, anchor="w")
        self.page_title.pack(anchor="w")

        self.page_subtitle = ctk.CTkLabel(title_block,
                                          text="Kıbrıtçı şantiye operasyonları",
                                          font=(UI.FONT, 11),
                                          text_color=UI.TEXT_MUTED, anchor="w")
        self.page_subtitle.pack(anchor="w")

        self.status_badge = page_badge(self.topbar, "Hazır")
        self.status_badge.pack(side="right", padx=24)

        self.main_frame = ctk.CTkFrame(self.right_container,
                                       fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=18, pady=18)

    # ================================================================
    # NAVİGASYON YARDIMCILARI
    # ================================================================
    def _navigate(self, key, command):
        self._set_active_menu(key)
        command()

    def _set_active_menu(self, active_key):
        self.active_menu = active_key
        for key, btn in self.menu_buttons.items():
            if key == active_key:
                btn.configure(fg_color=UI.PRIMARY, hover_color=UI.PRIMARY_HOVER)
            else:
                btn.configure(fg_color="transparent", hover_color=UI.SIDEBAR_SOFT)

    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def set_page(self, key, title, subtitle):
        self._set_active_menu(key)
        self.page_title.configure(text=title)
        self.page_subtitle.configure(text=subtitle)
        self.status_badge.configure(text="Aktif modül")

    # ================================================================
    # PERSONEL
    # ================================================================
    def show_personel_frame(self):
        self.clear_main()
        self.set_page("personel", "Personel Yönetimi",
                      "Kayıt, düzenleme, durum ve personel raporları")
        PersonelKayitFrame(self.main_frame).pack(fill="both", expand=True)

    def show_yoklama_frame(self):
        self.clear_main()
        self.set_page("yoklama", "Yoklama ve Puantaj",
                      "Günlük yoklama, mesai ve aylık puantaj takibi")
        YoklamaPanel(self.main_frame).pack(fill="both", expand=True)

    def show_maas_frame(self):
        self.clear_main()
        self.set_page("maas", "Maaş Hesaplama",
                      "Yoklama verilerine göre hakediş ve mesai hesabı")
        MaasArayuz(
            self.main_frame,
            veri_getir_func=yoklama_getir,
            personel_getir_func=aktif_personeller_getir,
        ).pack(fill="both", expand=True)

    # ================================================================
    # FİNANS
    # ================================================================
    def show_cari_frame(self):
        self.clear_main()
        self.set_page("cari", "Cari Kartlar",
                      "Tedarikçi, taşeron, müşteri ve cari kart geçmişi")
        CariKartlarModul(self.main_frame, db=self.db_manager).pack(
            fill="both", expand=True)

    def show_stok_frame(self):
        self.clear_main()
        self.set_page("stok", "Stok Kartları",
                      "Malzeme kartları ve satın alma/fatura kalem altyapısı")
        StokKartlariModul(self.main_frame, db=self.db_manager).pack(
            fill="both", expand=True)

    def show_satin_alma_frame(self):
        self.clear_main()
        self.set_page("satin_alma", "Satın Alma Talep",
                      "Talep formu, kalemler, PDF ve imzalı evrak akışı")
        SatinAlmaModul(self.main_frame, db=self.db_manager).pack(
            fill="both", expand=True)

    def show_irsaliye_frame(self):
        self.clear_main()
        self.set_page("irsaliye", "İrsaliye Girişi",
                      "Teslimat, imzalı evrak ve satın alma karşılaştırması")
        IrsaliyeModul(self.main_frame, db=self.db_manager).pack(
            fill="both", expand=True)

    def show_fatura_frame(self):
        self.clear_main()
        self.set_page("fatura", "Fatura Girişi",
                      "Fatura, satın alma ve irsaliye karşılaştırma modeli")
        FaturaModul(self.main_frame, db=self.db_manager).pack(
            fill="both", expand=True)

    def show_kasa_frame(self):
        self.clear_main()
        self.set_page("kasa", "Haftalık Kasa",
                      "Fiş yüklemeli kasa hareketleri ve haftalık takip")
        KasaRaporuModul(self.main_frame, db=self.db_manager).pack(
            fill="both", expand=True)

    # ================================================================
    # İDARİ İŞLER
    # ================================================================
    def show_arac_frame(self):
        self.clear_main()
        self.set_page("arac", "Araç ve Bakım",
                      "KM, muayene, yağ bakımı ve sorumlu personel takibi")
        AracDemirbasModul(self.main_frame, db=self.db_manager).pack(
            fill="both", expand=True)

    def show_demirbas_frame(self):
        self.clear_main()
        self.set_page("demirbas", "Demirbaş Kartları",
                      "Demirbaş kayıt ve tahsis altyapısı")
        DemirbasModul(self.main_frame, db=self.db_manager).pack(
            fill="both", expand=True)

    def show_tahsis_frame(self):
        self.clear_main()
        self.set_page("tahsis", "Tahsisleme",
                      "Araç ve demirbaş tahsis/iade takipleri")
        TahsisModul(self.main_frame, db=self.db_manager).pack(
            fill="both", expand=True)

    def show_tutanak_frame(self):
        self.clear_main()
        self.set_page("tutanak", "Hazır Tutanaklar",
                      "Tahsis, teslim ve sevk tutanak kayıtları")
        HazirTutanaklarModul(self.main_frame, db=self.db_manager).pack(
            fill="both", expand=True)

    def show_kamp_frame(self):
        self.clear_main()
        self.set_page("kamp", "Kamp Yönetimi",
                      "Yerleşke, oda, personel ve demirbaş sayım takipleri")
        KampYonetimiModul(self.main_frame, db=self.db_manager).pack(
            fill="both", expand=True)

    def show_saha_frame(self):
        self.clear_main()
        self.set_page("saha", "Saha Faaliyetleri",
                      "Günlük saha çalışma kayıtları ve fotoğraf takibi")
        SahaFaaliyetiModul(self.main_frame, db=self.db_manager).pack(
            fill="both", expand=True)

    # ================================================================
    # RAPOR VE İLETİŞİM
    # ================================================================
    def show_rapor_frame(self):
        self.clear_main()
        self.set_page("rapor", "Rapor Merkezi",
                      "Tüm modüllerden PDF, Excel ve kart geçmişi raporları")
        RaporMerkeziModul(self.main_frame, db=self.db_manager).pack(
            fill="both", expand=True)

    def show_eposta_frame(self):
        self.clear_main()
        self.set_page("eposta", "E-Posta Merkezi",
                      "Rapor ve evrak gönderim takip merkezi")
        EpostaMerkeziModul(self.main_frame, db=self.db_manager).pack(
            fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
