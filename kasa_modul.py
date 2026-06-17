"""
KİBRİTÇİ ERP — HAFTALIK KASA MODÜLÜ
- Gelir / Gider hareketi girişi
- Fiş evrak yükleme
- Haftalık özet ve bakiye
- Kategori bazlı harcama dağılımı
- PDF rapor
"""

import os
import shutil
import calendar
from datetime import datetime, date, timedelta
from tkinter import messagebox, filedialog
import customtkinter as ctk
from tkinter import ttk

from ui_theme import UI

# ─────────────────────────────────────────────────────────────
KATEGORILER = [
    "GENEL", "MALZEME", "İŞÇİLİK", "YAKIT", "KIRA",
    "FATURA/SA ÖDEME", "AVANS", "İADE", "DİĞER"
]
HAREKET_TIPLERI = ["GELİR", "GİDER"]


# ─────────────────────────────────────────────────────────────
class KasaModul(ctk.CTkFrame):

    def __init__(self, master, db):
        super().__init__(master, fg_color=UI.BG)
        self.db = db
        self.secili_id = None
        self.cari_map = {}

        self._build()
        self._cari_yukle()
        self._listele()

    # ══════════════════════════════════════════════════════════
    # UI İNŞA
    # ══════════════════════════════════════════════════════════
    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # ── SOL PANEL (FORM) ──────────────────────────────────
        sol = ctk.CTkFrame(self, fg_color=UI.SURFACE,
                           corner_radius=UI.RADIUS_LG,
                           border_width=1, border_color=UI.BORDER)
        sol.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        sol.grid_rowconfigure(1, weight=1)

        # Header
        hdr = ctk.CTkFrame(sol, fg_color=UI.PRIMARY, corner_radius=UI.RADIUS_MD)
        hdr.grid(row=0, column=0, sticky="ew", padx=12, pady=12)

        ctk.CTkLabel(hdr, text="💰 KASA HAREKETİ",
                     font=(UI.FONT, 17, "bold"), text_color="white").pack(
            anchor="w", padx=14, pady=(10, 2))
        ctk.CTkLabel(hdr, text="Gelir / Gider fişi girişi",
                     font=(UI.FONT, 11), text_color="#DBEAFE").pack(
            anchor="w", padx=14, pady=(0, 10))

        # Form alanları
        form = ctk.CTkScrollableFrame(sol, fg_color="transparent")
        form.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 8))
        sol.grid_columnconfigure(0, weight=1)

        def lbl(text):
            ctk.CTkLabel(form, text=text, font=(UI.FONT, 11, "bold"),
                         text_color=UI.TEXT, anchor="w").pack(fill="x", pady=(8, 2))

        def entry(h=36):
            e = ctk.CTkEntry(form, height=h, border_color=UI.BORDER)
            e.pack(fill="x")
            return e

        def combo(values):
            c = ctk.CTkComboBox(form, values=values, height=36,
                                border_color=UI.BORDER)
            c.set(values[0])
            c.pack(fill="x")
            return c

        lbl("Tarih (YYYY-MM-DD)")
        self.e_tarih = entry()
        self.e_tarih.insert(0, date.today().isoformat())

        lbl("Hareket Tipi")
        self.e_tip = combo(HAREKET_TIPLERI)

        lbl("Kategori")
        self.e_kat = combo(KATEGORILER)

        lbl("Fiş No")
        self.e_fis = entry()

        lbl("Cari / Firma")
        self.e_cari = ctk.CTkComboBox(form, values=[""], height=36,
                                       border_color=UI.BORDER)
        self.e_cari.set("")
        self.e_cari.pack(fill="x")

        lbl("Tutar (₺)")
        self.e_tutar = entry()

        lbl("Açıklama")
        self.e_acik = ctk.CTkTextbox(form, height=72, border_width=1,
                                      border_color=UI.BORDER)
        self.e_acik.pack(fill="x")

        # Fiş evrak
        lbl("Fiş / Evrak")
        fis_row = ctk.CTkFrame(form, fg_color="transparent")
        fis_row.pack(fill="x", pady=(0, 4))
        self.lbl_evrak = ctk.CTkLabel(fis_row, text="Yüklenmedi",
                                       font=(UI.FONT, 11),
                                       text_color=UI.TEXT_MUTED)
        self.lbl_evrak.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(fis_row, text="📎 Seç", width=70, height=30,
                      fg_color=UI.SURFACE_SOFT, text_color=UI.PRIMARY,
                      hover_color=UI.BORDER,
                      command=self._evrak_sec).pack(side="right")
        self._evrak_yolu = None

        # Butonlar
        btn_row = ctk.CTkFrame(sol, fg_color="transparent")
        btn_row.grid(row=2, column=0, sticky="ew", padx=12, pady=10)

        ctk.CTkButton(btn_row, text="💾 Kaydet", height=38,
                      fg_color=UI.PRIMARY, hover_color=UI.PRIMARY_HOVER,
                      command=self._kaydet).pack(side="left", fill="x",
                                                  expand=True, padx=(0, 4))
        ctk.CTkButton(btn_row, text="🧹 Temizle", height=38,
                      fg_color=UI.TEXT_MUTED, hover_color="#475569",
                      command=self._temizle).pack(side="left", fill="x",
                                                   expand=True, padx=(4, 0))

        # ── SAĞ PANEL (LİSTE + ÖZET) ─────────────────────────
        sag = ctk.CTkFrame(self, fg_color=UI.SURFACE,
                           corner_radius=UI.RADIUS_LG,
                           border_width=1, border_color=UI.BORDER)
        sag.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        sag.grid_rowconfigure(2, weight=1)
        sag.grid_columnconfigure(0, weight=1)

        # ── KPI KART SATIRI ──────────────────────────────────
        kpi = ctk.CTkFrame(sag, fg_color="transparent")
        kpi.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
        kpi.grid_columnconfigure((0, 1, 2, 3), weight=1)

        def kpi_kart(parent, col, label, renk):
            f = ctk.CTkFrame(parent, fg_color=renk,
                             corner_radius=UI.RADIUS_MD)
            f.grid(row=0, column=col, sticky="ew", padx=4)
            ctk.CTkLabel(f, text=label, font=(UI.FONT, 10),
                         text_color="white").pack(anchor="w", padx=10, pady=(8, 0))
            val = ctk.CTkLabel(f, text="0 ₺", font=(UI.FONT, 15, "bold"),
                               text_color="white")
            val.pack(anchor="w", padx=10, pady=(0, 8))
            return val

        self.kpi_gelir  = kpi_kart(kpi, 0, "TOPLAM GELİR",  "#16A34A")
        self.kpi_gider  = kpi_kart(kpi, 1, "TOPLAM GİDER",  "#DC2626")
        self.kpi_bakiye = kpi_kart(kpi, 2, "BAKİYE",         "#2563EB")
        self.kpi_kayit  = kpi_kart(kpi, 3, "KAYIT SAYISI",   "#6B7280")

        # ── FİLTRE BARI ──────────────────────────────────────
        filt = ctk.CTkFrame(sag, fg_color=UI.SURFACE_SOFT,
                            corner_radius=UI.RADIUS_MD)
        filt.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 6))

        ctk.CTkLabel(filt, text="📅 Hafta:", font=(UI.FONT, 11),
                     text_color=UI.TEXT_MUTED).pack(side="left", padx=(10, 4), pady=8)

        haftalar = self._hafta_listesi()
        self.combo_hafta = ctk.CTkComboBox(filt, values=haftalar, width=200,
                                            height=32,
                                            command=lambda _: self._listele())
        self.combo_hafta.set(haftalar[0] if haftalar else "")
        self.combo_hafta.pack(side="left", padx=4)

        ctk.CTkLabel(filt, text="Tip:", font=(UI.FONT, 11),
                     text_color=UI.TEXT_MUTED).pack(side="left", padx=(10, 4))
        self.combo_tip_filtre = ctk.CTkComboBox(
            filt, values=["TÜMÜ", "GELİR", "GİDER"], width=100,
            height=32, command=lambda _: self._listele())
        self.combo_tip_filtre.set("TÜMÜ")
        self.combo_tip_filtre.pack(side="left", padx=4)

        self.e_ara = ctk.CTkEntry(filt, placeholder_text="🔍 Ara...",
                                   height=32, width=160, border_width=0,
                                   fg_color=UI.SURFACE)
        self.e_ara.pack(side="left", padx=8)
        self.e_ara.bind("<KeyRelease>", lambda _: self._listele())

        ctk.CTkButton(filt, text="📄 PDF Rapor", height=32, width=110,
                      fg_color=UI.SUCCESS, hover_color="#15803D",
                      command=self._pdf_rapor).pack(side="right", padx=8)

        # ── TABLO ────────────────────────────────────────────
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Kasa.Treeview", rowheight=30,
                        font=(UI.FONT, 11),
                        background="#FFFFFF",
                        fieldbackground="#FFFFFF")
        style.configure("Kasa.Treeview.Heading",
                        font=(UI.FONT, 11, "bold"),
                        background="#E2E8F0", foreground="#0F172A")
        style.map("Kasa.Treeview", background=[("selected", "#DBEAFE")])

        cols = ("tarih", "tip", "kat", "fis", "cari", "tutar", "evrak")
        self.tree = ttk.Treeview(sag, columns=cols, show="headings",
                                  height=16, style="Kasa.Treeview")

        basliklar = [
            ("tarih", "Tarih", 90),
            ("tip",   "Tip",   70),
            ("kat",   "Kategori", 110),
            ("fis",   "Fiş No", 90),
            ("cari",  "Cari/Firma", 140),
            ("tutar", "Tutar (₺)", 100),
            ("evrak", "Evrak", 60),
        ]
        for col, bas, gen in basliklar:
            self.tree.heading(col, text=bas)
            self.tree.column(col, width=gen, anchor="center")

        self.tree.tag_configure("gelir", foreground="#16A34A")
        self.tree.tag_configure("gider", foreground="#DC2626")
        self.tree.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 4))

        sb_y = ttk.Scrollbar(sag, orient="vertical",
                              command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb_y.set)
        sb_y.grid(row=2, column=1, sticky="ns", pady=(0, 4))
        sag.grid_columnconfigure(1, weight=0)

        self.tree.bind("<Double-1>", lambda _: self._kaydi_ac())

        # Alt butonlar
        alt = ctk.CTkFrame(sag, fg_color="transparent")
        alt.grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 12))

        ctk.CTkButton(alt, text="✏ Düzenle", height=34, width=110,
                      fg_color=UI.SURFACE_SOFT, text_color=UI.PRIMARY,
                      hover_color=UI.BORDER,
                      command=self._kaydi_ac).pack(side="left", padx=(0, 4))
        ctk.CTkButton(alt, text="🗑 Sil", height=34, width=80,
                      fg_color="#FEE2E2", text_color="#DC2626",
                      hover_color="#FECACA",
                      command=self._sil).pack(side="left", padx=4)
        ctk.CTkButton(alt, text="📎 Evrak Aç", height=34, width=110,
                      fg_color=UI.SURFACE_SOFT, text_color="#6B7280",
                      hover_color=UI.BORDER,
                      command=self._evrak_ac).pack(side="left", padx=4)

        self._kayitlar = []

    # ══════════════════════════════════════════════════════════
    # YARDIMCILAR
    # ══════════════════════════════════════════════════════════
    def _hafta_listesi(self):
        """Son 12 haftayı YYYY-Whh formatında döner."""
        bugun = date.today()
        haftalar = []
        for i in range(12):
            d = bugun - timedelta(weeks=i)
            iso = d.isocalendar()
            haftalar.append(f"{iso[0]}-W{iso[1]:02d}")
        return haftalar

    def _hafta_aralik(self, hafta_str):
        """YYYY-Whh → (pazartesi, pazar) date tuple."""
        try:
            yil, hafta = hafta_str.split("-W")
            pzt = date.fromisocalendar(int(yil), int(hafta), 1)
            paz = pzt + timedelta(days=6)
            return pzt, paz
        except Exception:
            return None, None

    def _cari_yukle(self):
        try:
            cariler = self.db.cari_kartlari_getir() or []
            self.cari_map = {}
            vals = [""]
            for c in cariler:
                unvan = (c.get("unvan") or "").strip()
                if unvan:
                    self.cari_map[unvan] = c
                    vals.append(unvan)
            self.e_cari.configure(values=vals)
        except Exception as e:
            print("Cari yükleme hatası:", e)

    def _form_deger(self, widget):
        if isinstance(widget, ctk.CTkTextbox):
            return widget.get("0.0", "end").strip()
        return widget.get().strip()

    # ══════════════════════════════════════════════════════════
    # KAYDET
    # ══════════════════════════════════════════════════════════
    def _kaydet(self):
        tarih  = self._form_deger(self.e_tarih)
        tip    = self._form_deger(self.e_tip)
        kat    = self._form_deger(self.e_kat)
        fis    = self._form_deger(self.e_fis)
        cari_u = self._form_deger(self.e_cari)
        tutar  = self._form_deger(self.e_tutar)
        acik   = self._form_deger(self.e_acik)

        if not tarih:
            messagebox.showwarning("Uyarı", "Tarih zorunludur.")
            return
        try:
            tutar_f = float(tutar.replace(",", "."))
            if tutar_f <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Uyarı", "Geçerli bir tutar girin.")
            return

        # Hafta hesapla
        try:
            t = date.fromisoformat(tarih)
            iso = t.isocalendar()
            hafta = f"{iso[0]}-W{iso[1]:02d}"
        except Exception:
            hafta = ""

        # Cari
        cari_kart = self.cari_map.get(cari_u)
        cari_id   = (cari_kart or {}).get("id")

        # Evrak kopyala
        evrak_yolu = None
        if self._evrak_yolu:
            hedef = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "kasa_fisleri"
            )
            os.makedirs(hedef, exist_ok=True)
            ext = os.path.splitext(self._evrak_yolu)[1]
            ad  = f"FIS_{fis or datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
            evrak_yolu = os.path.join(hedef, ad)
            try:
                shutil.copy2(self._evrak_yolu, evrak_yolu)
            except Exception as e:
                messagebox.showwarning("Uyarı", f"Evrak kopyalanamadı:\n{e}")
                evrak_yolu = self._evrak_yolu

        data = {
            "tarih":         tarih,
            "hafta":         hafta,
            "hareket_tipi":  tip,
            "kategori":      kat,
            "fis_no":        fis or None,
            "cari_unvan":    cari_u or None,
            "cari_kart_id":  cari_id,
            "tutar":         tutar_f,
            "aciklama":      acik or None,
            "fis_evrak_url": evrak_yolu,
        }

        ok, sonuc = self.db.generic_kaydet("kasa_hareketleri", data,
                                            self.secili_id)
        if not ok:
            messagebox.showerror("Hata", str(sonuc))
            return

        messagebox.showinfo("OK", "Kasa hareketi kaydedildi.")
        self._temizle()
        self._listele()

    # ══════════════════════════════════════════════════════════
    # LİSTE
    # ══════════════════════════════════════════════════════════
    def _listele(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        hafta    = self.combo_hafta.get()
        tip_f    = self.combo_tip_filtre.get()
        ara      = self.e_ara.get().lower()
        pzt, paz = self._hafta_aralik(hafta)

        kayitlar = self.db.generic_listele("kasa_hareketleri", "tarih") or []
        self._kayitlar = kayitlar

        toplam_gelir = 0.0
        toplam_gider = 0.0
        gorunen = 0

        for k in kayitlar:
            tarih_str = str(k.get("tarih") or "")
            # Hafta filtresi
            if pzt and tarih_str:
                try:
                    kt = date.fromisoformat(tarih_str[:10])
                    if not (pzt <= kt <= paz):
                        continue
                except Exception:
                    pass

            tip = (k.get("hareket_tipi") or "").upper()

            # Tip filtresi
            if tip_f != "TÜMÜ" and tip != tip_f:
                continue

            # Arama
            haystack = " ".join([
                tarih_str,
                k.get("fis_no") or "",
                k.get("cari_unvan") or "",
                k.get("aciklama") or "",
                k.get("kategori") or "",
            ]).lower()
            if ara and ara not in haystack:
                continue

            tutar = float(k.get("tutar") or 0)
            if tip == "GELİR":
                toplam_gelir += tutar
                tag = "gelir"
            else:
                toplam_gider += tutar
                tag = "gider"

            evrak = "✅" if k.get("fis_evrak_url") else "—"

            self.tree.insert("", "end", iid=str(k["id"]), tags=(tag,),
                             values=(
                                 tarih_str[:10],
                                 tip,
                                 k.get("kategori") or "—",
                                 k.get("fis_no") or "—",
                                 k.get("cari_unvan") or "—",
                                 f"{tutar:,.2f}",
                                 evrak,
                             ))
            gorunen += 1

        bakiye = toplam_gelir - toplam_gider
        self.kpi_gelir.configure(text=f"{toplam_gelir:,.2f} ₺")
        self.kpi_gider.configure(text=f"{toplam_gider:,.2f} ₺")
        self.kpi_bakiye.configure(text=f"{bakiye:,.2f} ₺",
                                   text_color="white" if bakiye >= 0 else "#FCA5A5")
        self.kpi_kayit.configure(text=str(gorunen))

    # ══════════════════════════════════════════════════════════
    # KAYIT AÇ / SİL / EVRAK
    # ══════════════════════════════════════════════════════════
    def _secili_kayit(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Uyarı", "Listeden bir kayıt seçin.")
            return None
        iid = sel[0]
        for k in self._kayitlar:
            if str(k.get("id")) == iid:
                return k
        return None

    def _kaydi_ac(self):
        k = self._secili_kayit()
        if not k:
            return
        self.secili_id = k["id"]

        self.e_tarih.delete(0, "end")
        self.e_tarih.insert(0, str(k.get("tarih") or "")[:10])

        self.e_tip.set(k.get("hareket_tipi") or "GİDER")
        self.e_kat.set(k.get("kategori") or "GENEL")

        self.e_fis.delete(0, "end")
        self.e_fis.insert(0, k.get("fis_no") or "")

        self.e_cari.set(k.get("cari_unvan") or "")

        self.e_tutar.delete(0, "end")
        self.e_tutar.insert(0, str(k.get("tutar") or ""))

        self.e_acik.delete("0.0", "end")
        self.e_acik.insert("0.0", k.get("aciklama") or "")

        evrak = k.get("fis_evrak_url")
        self._evrak_yolu = evrak
        self.lbl_evrak.configure(
            text=os.path.basename(evrak) if evrak else "Yüklenmedi")

    def _sil(self):
        k = self._secili_kayit()
        if not k:
            return
        if not messagebox.askyesno("Sil", "Bu kaydı silmek istediğinize emin misiniz?"):
            return
        try:
            self.db.supabase.table("kasa_hareketleri").delete().eq(
                "id", k["id"]).execute()
            self._temizle()
            self._listele()
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def _evrak_sec(self):
        dosya = filedialog.askopenfilename(
            title="Fiş / Evrak Seç",
            filetypes=[("Evrak", "*.pdf;*.png;*.jpg;*.jpeg"),
                       ("Tüm Dosyalar", "*.*")]
        )
        if dosya:
            self._evrak_yolu = dosya
            self.lbl_evrak.configure(
                text=os.path.basename(dosya), text_color=UI.SUCCESS)

    def _evrak_ac(self):
        k = self._secili_kayit()
        if not k:
            return
        yol = k.get("fis_evrak_url")
        if not yol or not os.path.exists(yol):
            messagebox.showinfo("Bilgi", "Evrak dosyası bulunamadı.")
            return
        os.startfile(yol)

    def _temizle(self):
        self.secili_id  = None
        self._evrak_yolu = None
        self.e_tarih.delete(0, "end")
        self.e_tarih.insert(0, date.today().isoformat())
        self.e_tip.set("GİDER")
        self.e_kat.set("GENEL")
        self.e_fis.delete(0, "end")
        self.e_cari.set("")
        self.e_tutar.delete(0, "end")
        self.e_acik.delete("0.0", "end")
        self.lbl_evrak.configure(text="Yüklenmedi", text_color=UI.TEXT_MUTED)

    # ══════════════════════════════════════════════════════════
    # PDF RAPOR
    # ══════════════════════════════════════════════════════════
    def _pdf_rapor(self):
        hafta    = self.combo_hafta.get()
        pzt, paz = self._hafta_aralik(hafta)

        kayitlar = []
        toplam_gelir = 0.0
        toplam_gider = 0.0

        for k in (self._kayitlar or []):
            tarih_str = str(k.get("tarih") or "")
            if pzt and tarih_str:
                try:
                    kt = date.fromisoformat(tarih_str[:10])
                    if not (pzt <= kt <= paz):
                        continue
                except Exception:
                    pass
            t = float(k.get("tutar") or 0)
            tip = (k.get("hareket_tipi") or "").upper()
            if tip == "GELİR":
                toplam_gelir += t
            else:
                toplam_gider += t
            kayitlar.append(k)

        if not kayitlar:
            messagebox.showinfo("Bilgi", "Seçili haftada kayıt yok.")
            return

        try:
            from fpdf import FPDF
        except ImportError:
            messagebox.showerror("Hata", "fpdf2 paketi yüklü değil:\npip install fpdf2")
            return

        pdf = FPDF(orientation="L", unit="mm", format="A4")
        pdf.add_page()

        proje = os.path.dirname(os.path.abspath(__file__))
        font_r = os.path.join(proje, "DejaVuSans.ttf")
        font_b = os.path.join(proje, "DejaVuSans-Bold.ttf")
        if os.path.exists(font_r):
            pdf.add_font("DV", "",  font_r, uni=True)
            pdf.add_font("DV", "B", font_b, uni=True)
            F, FB = "DV", "DV"
        else:
            F, FB = "Helvetica", "Helvetica"

        # Header bant
        pdf.set_fill_color(18, 52, 86)
        pdf.rect(0, 0, 297, 28, "F")

        logo = os.path.join(proje, "logo-kibritci.png")
        if os.path.exists(logo):
            pdf.image(logo, 6, 4, 18)

        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(28, 6)
        pdf.set_font(FB, "B", 16)
        pdf.cell(180, 8, "KİBRİTÇİ İNŞAAT", 0, 2, "L")
        pdf.set_font(F, "", 10)
        pdf.set_x(28)
        pdf.cell(180, 6, f"HAFTALIK KASA RAPORU  |  {hafta}", 0, 0, "L")

        pdf.set_text_color(180, 220, 255)
        pdf.set_xy(220, 8)
        pdf.set_font(F, "", 9)
        pdf.cell(60, 5, f"Tarih: {date.today().strftime('%d.%m.%Y')}", 0, 2, "R")

        # KPI kutuları
        pdf.ln(10)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font(FB, "B", 11)
        pdf.set_fill_color(220, 252, 231)
        pdf.cell(80, 14, f"TOPLAM GELİR: {toplam_gelir:,.2f} TL", 1, 0, "C", True)
        pdf.set_fill_color(254, 226, 226)
        pdf.cell(80, 14, f"TOPLAM GİDER: {toplam_gider:,.2f} TL", 1, 0, "C", True)
        bakiye = toplam_gelir - toplam_gider
        pdf.set_fill_color(219, 234, 254)
        pdf.cell(80, 14, f"BAKİYE: {bakiye:,.2f} TL", 1, 1, "C", True)

        pdf.ln(4)

        # Tablo başlıkları
        col_w = [28, 28, 40, 32, 60, 32, 60]
        baslik = ["Tarih", "Tip", "Kategori", "Fiş No", "Cari/Firma",
                  "Tutar (TL)", "Açıklama"]
        pdf.set_fill_color(31, 78, 121)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(FB, "B", 9)
        for i, b in enumerate(baslik):
            pdf.cell(col_w[i], 9, b, 1, 0, "C", True)
        pdf.ln()

        pdf.set_font(F, "", 8)
        for idx, k in enumerate(kayitlar):
            tip = (k.get("hareket_tipi") or "").upper()
            if tip == "GELİR":
                pdf.set_fill_color(240, 255, 244)
                pdf.set_text_color(22, 101, 52)
            else:
                pdf.set_fill_color(255, 245, 245)
                pdf.set_text_color(153, 27, 27)

            tutar_str = f"{float(k.get('tutar') or 0):,.2f}"
            satirlar = [
                str(k.get("tarih") or "")[:10],
                tip,
                str(k.get("kategori") or "—"),
                str(k.get("fis_no") or "—"),
                str(k.get("cari_unvan") or "—"),
                tutar_str,
                (str(k.get("aciklama") or "—"))[:40],
            ]
            for i, val in enumerate(satirlar):
                pdf.cell(col_w[i], 8, val, 1, 0, "C", True)
            pdf.ln()

        # Footer
        pdf.set_y(-14)
        pdf.set_text_color(140, 140, 140)
        pdf.set_font(F, "", 8)
        pdf.cell(0, 6, "Kibritçi İnşaat | Kasa Takip Sistemi", 0, 0, "C")

        # Kaydet
        masaustu = os.path.join(os.path.expanduser("~"), "Desktop")
        dosya_adi = f"Kasa_Raporu_{hafta}_{datetime.now().strftime('%H%M')}.pdf"
        tam_yol = os.path.join(masaustu, dosya_adi)
        pdf.output(tam_yol)
        messagebox.showinfo("PDF Hazır", f"Masaüstüne kaydedildi:\n{dosya_adi}")
        try:
            os.startfile(tam_yol)
        except Exception:
            pass