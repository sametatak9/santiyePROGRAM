"""
form_dogrulama.py
-----------------
Tüm modüllerde kullanılabilecek yeniden kullanılabilir form bileşenleri.
• SayiEntry       – sadece sayı kabul eden giriş alanı (int veya float)
• TarihEntry      – YYYY-AA-GG formatını zorlayan alan
• ZorunluEntry    – boş bırakılamaz, kenarlık renkli uyarı verir
• FormLabel       – zorunlu (*) ve ipucu destekli etiket
• DogrulamaLabel  – alan altındaki hata/başarı mesaj etiketi
• form_dogrula()  – birden fazla alanı tek seferde doğrulayan yardımcı
"""
import re
import customtkinter as ctk
from ui_theme import UI


# ======================================================================
# RENK SABITLERI
# ======================================================================
RENK_NORMAL    = UI.BORDER        # "#E2E8F0"
RENK_HATA      = UI.DANGER        # "#DC2626"
RENK_TAMAM     = UI.SUCCESS       # "#16A34A"
RENK_UYARI     = UI.WARNING       # "#F59E0B"
RENK_ODAK      = UI.PRIMARY       # "#2563EB"


# ======================================================================
# FormLabel  – zorunlu (*) ve ipucu destekli etiket
# ======================================================================
class FormLabel(ctk.CTkFrame):
    """
    Kullanım:
        FormLabel(parent, "Miktar", zorunlu=True, ipucu="Sadece rakam giriniz")
    """
    def __init__(self, master, metin, zorunlu=False, ipucu="", **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)

        etiket_metin = metin + ("  *" if zorunlu else "")
        self.etiket = ctk.CTkLabel(
            self, text=etiket_metin,
            font=(UI.FONT, 12, "bold"),
            text_color=UI.TEXT if not zorunlu else UI.TEXT,
            anchor="w",
        )
        self.etiket.grid(row=0, column=0, sticky="w")

        if ipucu:
            self.ipucu_label = ctk.CTkLabel(
                self, text=f"ℹ  {ipucu}",
                font=(UI.FONT, 10),
                text_color=UI.TEXT_MUTED,
                anchor="w",
            )
            self.ipucu_label.grid(row=1, column=0, sticky="w", pady=(0, 2))


# ======================================================================
# DogrulamaLabel  – alanın altındaki hata / bilgi mesajı
# ======================================================================
class DogrulamaLabel(ctk.CTkLabel):
    """
    Kullanım:
        hata = DogrulamaLabel(parent)
        hata.hata_goster("Bu alan zorunludur.")
        hata.temizle()
    """
    def __init__(self, master, **kwargs):
        super().__init__(
            master, text="", font=(UI.FONT, 10),
            text_color=RENK_HATA, anchor="w", **kwargs,
        )

    def hata_goster(self, mesaj: str):
        self.configure(text=f"⚠  {mesaj}", text_color=RENK_HATA)

    def basari_goster(self, mesaj: str):
        self.configure(text=f"✓  {mesaj}", text_color=RENK_TAMAM)

    def bilgi_goster(self, mesaj: str):
        self.configure(text=f"ℹ  {mesaj}", text_color=RENK_UYARI)

    def temizle(self):
        self.configure(text="")


# ======================================================================
# SayiEntry  – sadece sayı kabul eden CTkEntry
# ======================================================================
class SayiEntry(ctk.CTkEntry):
    """
    Parametreler
    -----------
    sadece_tam   : True → yalnızca tam sayı (int); False → ondalıklı da kabul
    min_deger    : izin verilen minimum değer (None = sınırsız)
    max_deger    : izin verilen maksimum değer (None = sınırsız)
    hata_widget  : DogrulamaLabel örneği – varsa hata mesajını oraya yazar

    Kullanım:
        m = SayiEntry(parent, placeholder_text="0", width=120)
        deger = m.deger_al()   # float döner, geçersizse None
        gecerli = m.dogrula()  # bool
    """

    def __init__(self, master, sadece_tam=False,
                 min_deger=None, max_deger=None,
                 hata_widget=None, **kwargs):
        kwargs.setdefault("border_color", RENK_NORMAL)
        kwargs.setdefault("border_width", 1)
        super().__init__(master, **kwargs)

        self.sadece_tam  = sadece_tam
        self.min_deger   = min_deger
        self.max_deger   = max_deger
        self.hata_widget = hata_widget

        vcmd = (self.register(self._karakter_kontrol), "%P")
        self.configure(validate="key", validatecommand=vcmd)

        self.bind("<FocusIn>",  self._odak_aldı)
        self.bind("<FocusOut>", self._odak_kaybetti)

    # -- dahili --------------------------------------------------------
    def _karakter_kontrol(self, yeni_metin):
        """Yalnızca izin verilen karakterlerin girilmesine izin verir."""
        if yeni_metin == "" or yeni_metin == "-":
            return True
        if self.sadece_tam:
            return yeni_metin.lstrip("-").isdigit()
        else:
            # ondalıklı: rakam, tek nokta/virgül, isteğe bağlı eksi
            temiz = yeni_metin.replace(",", ".")
            try:
                float(temiz)
                return True
            except ValueError:
                # tek ondalık noktayı da izin ver ("3." gibi)
                return bool(re.fullmatch(r"-?\d*\.?\d*", temiz))

    def _odak_aldı(self, _event):
        self.configure(border_color=RENK_ODAK)

    def _odak_kaybetti(self, _event):
        gecerli = self.dogrula()
        self.configure(border_color=RENK_TAMAM if gecerli else RENK_HATA)

    # -- genel kullanım ------------------------------------------------
    def deger_al(self):
        """Girilen değeri float/int olarak döner. Geçersizse None."""
        metin = self.get().strip().replace(",", ".")
        if not metin:
            return None
        try:
            return int(metin) if self.sadece_tam else float(metin)
        except ValueError:
            return None

    def dogrula(self):
        """True = geçerli, False = hatalı. Hata varsa hata_widget'ı günceller."""
        deger = self.deger_al()

        if deger is None:
            self._hata("Geçerli bir sayı giriniz.")
            return False

        if self.min_deger is not None and deger < self.min_deger:
            self._hata(f"Minimum değer: {self.min_deger}")
            return False

        if self.max_deger is not None and deger > self.max_deger:
            self._hata(f"Maksimum değer: {self.max_deger}")
            return False

        self._temizle_hata()
        return True

    def _hata(self, mesaj):
        self.configure(border_color=RENK_HATA)
        if self.hata_widget:
            self.hata_widget.hata_goster(mesaj)

    def _temizle_hata(self):
        self.configure(border_color=RENK_TAMAM)
        if self.hata_widget:
            self.hata_widget.temizle()


# ======================================================================
# ZorunluEntry  – boş bırakılamaz
# ======================================================================
class ZorunluEntry(ctk.CTkEntry):
    """
    Boş bırakılırsa kenarlık kırmızı olur ve hata_widget'a mesaj yazar.

    Kullanım:
        e = ZorunluEntry(parent, placeholder_text="Firma adı giriniz",
                         hata_widget=hata_label, max_uzunluk=100)
        gecerli = e.dogrula()
    """

    def __init__(self, master, hata_widget=None, max_uzunluk=None, **kwargs):
        kwargs.setdefault("border_color", RENK_NORMAL)
        kwargs.setdefault("border_width", 1)
        super().__init__(master, **kwargs)

        self.hata_widget  = hata_widget
        self.max_uzunluk  = max_uzunluk

        self.bind("<FocusIn>",  self._odak_aldı)
        self.bind("<FocusOut>", self._odak_kaybetti)

    def _odak_aldı(self, _event):
        self.configure(border_color=RENK_ODAK)

    def _odak_kaybetti(self, _event):
        self.dogrula()

    def dogrula(self):
        metin = self.get().strip()
        if not metin:
            self.configure(border_color=RENK_HATA)
            if self.hata_widget:
                self.hata_widget.hata_goster("Bu alan zorunludur.")
            return False

        if self.max_uzunluk and len(metin) > self.max_uzunluk:
            self.configure(border_color=RENK_HATA)
            if self.hata_widget:
                self.hata_widget.hata_goster(
                    f"En fazla {self.max_uzunluk} karakter girilebilir.")
            return False

        self.configure(border_color=RENK_TAMAM)
        if self.hata_widget:
            self.hata_widget.temizle()
        return True

    def deger_al(self):
        return self.get().strip()


# ======================================================================
# TarihEntry  – YYYY-AA-GG doğrulaması
# ======================================================================
class TarihEntry(ctk.CTkEntry):
    """
    Klavye ile yazılmış tarihi YYYY-MM-DD formatında doğrular.
    (tkcalendar.DateEntry yerine kullanılmaz, sadece metin tarih alanları için)

    Kullanım:
        t = TarihEntry(parent, placeholder_text="YYYY-AA-GG",
                       hata_widget=hata_label)
        gecerli = t.dogrula()
        deger   = t.deger_al()   # "2024-06-01" veya None
    """

    FORMAT = "%Y-%m-%d"

    def __init__(self, master, hata_widget=None, **kwargs):
        kwargs.setdefault("border_color", RENK_NORMAL)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("placeholder_text", "YYYY-AA-GG")
        super().__init__(master, **kwargs)

        self.hata_widget = hata_widget
        self.bind("<FocusOut>", self._odak_kaybetti)
        self.bind("<FocusIn>",  lambda _: self.configure(border_color=RENK_ODAK))

    def _odak_kaybetti(self, _event):
        self.dogrula()

    def dogrula(self):
        from datetime import datetime
        metin = self.get().strip()
        if not metin:
            self.configure(border_color=RENK_HATA)
            if self.hata_widget:
                self.hata_widget.hata_goster("Tarih zorunludur (YYYY-AA-GG).")
            return False
        try:
            datetime.strptime(metin, self.FORMAT)
            self.configure(border_color=RENK_TAMAM)
            if self.hata_widget:
                self.hata_widget.temizle()
            return True
        except ValueError:
            self.configure(border_color=RENK_HATA)
            if self.hata_widget:
                self.hata_widget.hata_goster("Geçersiz tarih. Örnek: 2024-06-01")
            return False

    def deger_al(self):
        return self.get().strip() if self.dogrula() else None


# ======================================================================
# form_dogrula()  – toplu doğrulama yardımcısı
# ======================================================================
def form_dogrula(*alanlar):
    """
    Birden fazla doğrulama yapılabilen alan nesnesini tek seferde kontrol eder.
    Her nesnenin .dogrula() metodu olmalıdır.

    Döner: (True, []) veya (False, [hatalı_alan_listesi])

    Kullanım:
        gecerli, hatali = form_dogrula(ad_entry, miktar_entry, tarih_entry)
        if not gecerli:
            return
    """
    hatalar = []
    for alan in alanlar:
        if hasattr(alan, "dogrula"):
            if not alan.dogrula():
                hatalar.append(alan)
    return (len(hatalar) == 0, hatalar)


# ======================================================================
# onay_kutusu_olustur()  – iki seçenekli küçük switch
# ======================================================================
def onay_kutusu_olustur(parent, metin, varsayilan=False, **kwargs):
    """Hızlı CTkSwitch oluşturur."""
    return ctk.CTkSwitch(
        parent, text=metin,
        font=(UI.FONT, 12),
        progress_color=UI.PRIMARY,
        **kwargs,
    )
