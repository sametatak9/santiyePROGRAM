import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
from datetime import datetime
from tkcalendar import DateEntry


class IrsaliyeModul(ctk.CTkFrame):

    def __init__(self, master, db):
        super().__init__(master, fg_color="#EEF2F7")

        self.db = db
        self.COLOR_PRIMARY = "#2563EB"
        self.COLOR_PRIMARY_HOVER = "#1D4ED8"
        self.COLOR_SUCCESS = "#10B981"
        self.COLOR_WARNING = "#F59E0B"
        self.COLOR_DANGER = "#EF4444"
        self.COLOR_MUTED = "#64748B"
        self.COLOR_BORDER = "#CBD5E1"
        self.COLOR_TEXT = "#0F172A"

        self.irsaliye_id = self.db.irsaliye_id_uret()
        self.kalemler = []
        self.secili_sa_id = None
        self.sa_kalemleri = []
        self.cari_map = {}
        self.stok_map = {}
        self.duzenlenen_irsaliye_id = None

        self.setup_ui()
        self.sa_listesini_yenile()
        self.listele()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=32, font=("Segoe UI", 11),
                        background="#FFFFFF", fieldbackground="#FFFFFF")
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"),
                        background="#E2E8F0", foreground="#0F172A")
        style.map("Treeview", background=[("selected", "#DBEAFE")])

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # ================= SOL PANEL =================
        self.left = ctk.CTkFrame(self, fg_color="white", corner_radius=14,
                                 border_width=1, border_color="#E2E8F0")
        self.left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        header = ctk.CTkFrame(self.left, fg_color=self.COLOR_PRIMARY, corner_radius=12)
        header.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(header, text="📦 İRSALİYE GİRİŞİ", text_color="white",
                     font=("Segoe UI", 18, "bold")).pack(pady=6)

        self.ir_label = ctk.CTkLabel(header, text=f"İRSALİYE ID: {self.irsaliye_id}",
                                     text_color="#DBEAFE", font=("Segoe UI", 13))
        self.ir_label.pack(pady=(0, 6))

        self.mod_label = ctk.CTkLabel(header, text="YENİ İRSALİYE", text_color="white",
                                      fg_color="#1E40AF", corner_radius=10, height=24,
                                      font=("Segoe UI", 11, "bold"))
        self.mod_label.pack(pady=(0, 10))

        form = ctk.CTkScrollableFrame(self.left, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=15, pady=10)

        fnt_label = ("Segoe UI", 12, "bold")
        fnt_input = ("Segoe UI", 12)

        # SATIN ALMA TALEP SEÇ
        ctk.CTkLabel(form, text="🔗 Satın Alma Talep (SA ID)", font=fnt_label).pack(anchor="w")
        sa_row = ctk.CTkFrame(form, fg_color="transparent")
        sa_row.pack(fill="x", pady=(0, 10))

        self.sa_combo = ctk.CTkComboBox(sa_row, values=[], height=35, font=fnt_input,
                                         command=self.sa_secildi)
        self.sa_combo.set("")
        self.sa_combo.pack(side="left", fill="x", expand=True)

        ctk.CTkButton(sa_row, text="↻", width=40, height=35,
                      command=self.sa_listesini_yenile).pack(side="left", padx=(5, 0))

        # SA KALEM REFERANS
        self.sa_ref_label = ctk.CTkLabel(
            form, text="Talep kalemleri: —", font=("Segoe UI", 11),
            text_color="#64748B", wraplength=320, justify="left"
        )
        self.sa_ref_label.pack(anchor="w", pady=(0, 8))

        ctk.CTkButton(form, text="📋 Talep Kalemlerini Yükle", height=34,
                      fg_color="#6366F1", hover_color="#4F46E5",
                      command=self.talep_kalemlerini_yukle).pack(fill="x", pady=(0, 12))

        # İRSALİYE BİLGİLERİ
        ctk.CTkLabel(form, text="📅 Tarih", font=fnt_label).pack(anchor="w")
        self.tarih_entry = DateEntry(form, date_pattern="yyyy-mm-dd", font=fnt_input)
        self.tarih_entry.set_date(datetime.now().date())
        self.tarih_entry.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(form, text="📄 İrsaliye No", font=fnt_label).pack(anchor="w")
        self.irsaliye_no = ctk.CTkEntry(form, height=35, font=fnt_input)
        self.irsaliye_no.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(form, text="🏢 Firma", font=fnt_label).pack(anchor="w")
        self.firma = ctk.CTkComboBox(form, values=self.cari_secenekleri_getir(), height=35, font=fnt_input)
        self.firma.set("")
        self.firma.pack(fill="x", pady=(0, 15))

        # KALEM GİRİŞ
        ctk.CTkLabel(form, text="📦 Ürün Adı (Cins)", font=fnt_label).pack(anchor="w")
        self.urun_adi = ctk.CTkComboBox(form, values=self.stok_secenekleri_getir(), height=35, font=fnt_input)
        self.urun_adi.set("")
        self.urun_adi.pack(fill="x", pady=(0, 8))

        row_frame = ctk.CTkFrame(form, fg_color="transparent")
        row_frame.pack(fill="x", pady=(0, 10))

        left_col = ctk.CTkFrame(row_frame, fg_color="transparent")
        left_col.pack(side="left", fill="x", expand=True)
        right_col = ctk.CTkFrame(row_frame, fg_color="transparent")
        right_col.pack(side="left", fill="x", expand=True, padx=(10, 0))

        ctk.CTkLabel(left_col, text="🔢 Teslim Miktar", font=fnt_label).pack(anchor="w")
        self.miktar = ctk.CTkEntry(left_col, height=38)
        self.miktar.pack(fill="x")

        ctk.CTkLabel(right_col, text="📏 Birim", font=fnt_label).pack(anchor="w")
        self.birim = ctk.CTkComboBox(
            right_col,
            values=["ADET", "KG", "TON", "LT", "M3", "MT", "PAKET", "TORBA", "KUTU", "RULO"],
            height=38
        )
        self.birim.set("ADET")
        self.birim.pack(fill="x")

        ctk.CTkButton(form, text="➕ Kalem Ekle", height=40, font=("Segoe UI", 13, "bold"),
                      fg_color="#10B981", hover_color="#059669",
                      command=self.kalem_ekle).pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(self.left, text="📋 Teslim Kalemleri", font=("Segoe UI", 14, "bold"),
                     text_color="#1E293B").pack(anchor="w", padx=10, pady=(5, 5))

        self.kalem_tree = ttk.Treeview(
            self.left, columns=("urun", "miktar", "birim"), show="headings", height=5
        )
        for col, baslik in zip(("urun", "miktar", "birim"), ("Ürün (Cins)", "Miktar", "Birim")):
            self.kalem_tree.heading(col, text=baslik)
        self.kalem_tree.column("urun", width=160)
        self.kalem_tree.column("miktar", width=70)
        self.kalem_tree.column("birim", width=70)
        self.kalem_tree.pack(fill="x", padx=10, pady=5)
        self.kalem_tree.bind("<Double-1>", lambda e: self.kalem_sil())

        # ================= SAĞ PANEL =================
        self.right = ctk.CTkFrame(self, fg_color="white", corner_radius=14,
                                  border_width=1, border_color="#E2E8F0")
        self.right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        list_header = ctk.CTkFrame(self.right, fg_color="transparent")
        list_header.pack(fill="x", padx=12, pady=(12, 0))

        ctk.CTkLabel(list_header, text="İrsaliye Kayıtları", font=("Segoe UI", 17, "bold"),
                     text_color=self.COLOR_TEXT).pack(side="left")

        self.ozet_label = ctk.CTkLabel(list_header, text="0 kayıt", font=("Segoe UI", 11, "bold"),
                                       text_color="#475569", fg_color="#F1F5F9",
                                       corner_radius=10, height=26)
        self.ozet_label.pack(side="right")

        search_frame = ctk.CTkFrame(self.right, fg_color="#F1F5F9", corner_radius=10)
        search_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(search_frame, text="🔎").pack(side="left", padx=8)
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="SA ID veya İrsaliye ID ara...",
                                         height=40, border_width=0, fg_color="white")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=8)
        self.search_entry.bind("<KeyRelease>", lambda e: self.listele())

        self.alt_tree = ttk.Treeview(
            self.right,
            columns=("irsaliye_id", "sa_id", "irsaliye_no", "firma", "tarih", "durum"),
            show="headings", height=12
        )
        kolonlar = [
            ("irsaliye_id", "İrsaliye ID", 170),
            ("sa_id", "SA ID", 170),
            ("irsaliye_no", "İrsaliye No", 100),
            ("firma", "Firma", 130),
            ("tarih", "Tarih", 100),
            ("durum", "Durum", 160),
        ]
        for col, baslik, gen in kolonlar:
            self.alt_tree.heading(col, text=baslik)
            self.alt_tree.column(col, width=gen, anchor="center")
        self.alt_tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.alt_tree.bind("<Double-1>", lambda e: self.irsaliye_yukle())

        self.alt_tree.tag_configure("ONAY2", foreground="#16A34A")
        self.alt_tree.tag_configure("ONAY1", foreground="#F59E0B")
        self.alt_tree.tag_configure("FARK", foreground="#DC2626")
        self.alt_tree.tag_configure("BEKLE", foreground="#64748B")

        # KARŞILAŞTIRMA RAPORU
        ctk.CTkLabel(self.right, text="📊 Karşılaştırma Raporu", font=("Segoe UI", 13, "bold"),
                     text_color=self.COLOR_TEXT).pack(anchor="w", padx=12, pady=(5, 0))

        self.rapor_box = ctk.CTkTextbox(self.right, height=140, font=("Consolas", 11))
        self.rapor_box.pack(fill="x", padx=10, pady=5)
        self.rapor_box.insert("0.0", "Satın alma talebi seçip karşılaştırma yapın.")
        self.rapor_box.configure(state="disabled")

        btn_frame = ctk.CTkFrame(self.right, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(btn_frame, text="💾 Kaydet", fg_color=self.COLOR_PRIMARY,
                      hover_color=self.COLOR_PRIMARY_HOVER, command=self.kaydet).pack(side="left", padx=4)
        ctk.CTkButton(btn_frame, text="🧹 Temizle", fg_color=self.COLOR_MUTED,
                      hover_color="#475569", command=self.temizle).pack(side="left", padx=4)
        ctk.CTkButton(btn_frame, text="📊 Karşılaştır", fg_color="#8B5CF6",
                      hover_color="#7C3AED", command=self.karsilastir).pack(side="left", padx=4)
        ctk.CTkButton(btn_frame, text="✍️ İmzalı Evrak Yükle", fg_color=self.COLOR_SUCCESS,
                      hover_color="#059669", command=self.imzali_evrak_yukle).pack(side="left", padx=4)
        ctk.CTkButton(btn_frame, text="✅ 2. Onay Uygula", fg_color="#0EA5E9",
                      hover_color="#0284C7", command=self.ikinci_onay_uygula).pack(side="left", padx=4)

    # ================= YARDIMCI =================

    def cari_secenekleri_getir(self):
        try:
            cariler = self.db.cari_kartlari_getir()
        except Exception as e:
            print("Cari kart listesi alinamadi:", e)
            cariler = []
        self.cari_map = {}
        secenekler = []
        for c in cariler or []:
            unvan = str(c.get("unvan") or "").strip()
            if not unvan:
                continue
            secenekler.append(unvan)
            self.cari_map[unvan] = c
        return secenekler

    def stok_secenekleri_getir(self):
        try:
            stoklar = self.db.stok_kartlari_getir()
        except Exception as e:
            print("Stok kart listesi alinamadi:", e)
            stoklar = []
        self.stok_map = {}
        secenekler = []
        for s in stoklar or []:
            ad = str(s.get("stok_adi") or "").strip()
            if not ad:
                continue
            secenekler.append(ad)
            self.stok_map[ad] = s
        return secenekler

    def sa_listesini_yenile(self):
        """Satın alma taleplerini listeler ve combobox'ı günceller."""
        try:
            formlar = self.db.satin_alma_formlari_getir() or []
            # Listenin en başına boş bir seçenek ekliyoruz ki ilk açılışta boş kalabilsin
            self.sa_listesi = [""] 
            
            for f in formlar:
                sa_kod = f.get("sa_id")
                if sa_kod:
                    # Görsel olarak daha net olması için talep eden personeli de yanına yazdırıyoruz
                    text = f"{sa_kod} - {f.get('talep_eden', '')}"
                    self.sa_listesi.append(text)
            
            # Combobox'a yeni listeyi yüklüyoruz
            self.sa_combo.configure(values=self.sa_listesi)
            # İlk açılışta listenin 0. elemanını yani boşluğu ("") seçtiriyoruz
            self.sa_combo.set("") 
            
        except Exception as e:
            print("Satın alma listesi yenilenirken hata oluştu:", e)

    def _sa_id_coz(self, combo_deger):
        if not combo_deger:
            return None
        return combo_deger.split(" - ")[0].strip()

    def sa_secildi(self, secim=None):
        self.secili_sa_id = self._sa_id_coz(secim or self.sa_combo.get())
        if not self.secili_sa_id:
            return
        detay = self.db.satin_alma_detay_getir(self.secili_sa_id)
        self.sa_kalemleri = detay.get("kalemler", [])
        if not self.sa_kalemleri:
            self.sa_ref_label.configure(text="Talep kalemleri: bulunamadı")
            return
        satirlar = []
        for k in self.sa_kalemleri:
            satirlar.append(
                f"• {k.get('urun_adi')} — {k.get('talep_edilen_miktar')} {k.get('talep_birimi')}"
            )
        self.sa_ref_label.configure(text="Talep kalemleri:\n" + "\n".join(satirlar))

    def talep_kalemlerini_yukle(self):
        if not self.sa_kalemleri:
            self.sa_secildi()
        if not self.sa_kalemleri:
            messagebox.showwarning("Uyarı", "Önce geçerli bir satın alma talebi seçin")
            return

        for k in self.sa_kalemleri:
            veri = {
                "urun_adi": k.get("urun_adi", ""),
                "miktar": float(k.get("talep_edilen_miktar") or 0),
                "birim": k.get("talep_birimi", "ADET"),
                "sa_kalem_id": k.get("id"),
                "stok_kart_id": k.get("stok_kart_id"),
            }
            if any(v["urun_adi"] == veri["urun_adi"] and v["birim"] == veri["birim"]
                   for v in self.kalemler):
                continue
            self.kalemler.append(veri)
            self.kalem_tree.insert("", "end", values=(veri["urun_adi"], veri["miktar"], veri["birim"]))

        messagebox.showinfo("OK", "Talep kalemleri forma yüklendi. Miktarları düzenleyebilirsiniz.")

    def kalem_ekle(self):
        if not self.urun_adi.get().strip():
            messagebox.showwarning("Uyarı", "Ürün adı boş olamaz")
            return
        try:
            miktar = float(str(self.miktar.get()).replace(",", "."))
        except ValueError:
            messagebox.showwarning("Uyarı", "Miktar sayısal olmalı")
            return
        if miktar <= 0:
            messagebox.showwarning("Uyarı", "Miktar sıfırdan büyük olmalı")
            return

        veri = {
            "urun_adi": self.urun_adi.get().strip(),
            "miktar": miktar,
            "birim": self.birim.get(),
            "sa_kalem_id": None,
            "stok_kart_id": (self.stok_map.get(self.urun_adi.get().strip()) or {}).get("id"),
        }
        self.kalemler.append(veri)
        self.kalem_tree.insert("", "end", values=(veri["urun_adi"], veri["miktar"], veri["birim"]))
        self.urun_adi.set("")
        self.miktar.delete(0, "end")

    def kalem_sil(self):
        secili = self.kalem_tree.selection()
        if not secili:
            return
        index = self.kalem_tree.index(secili[0])
        self.kalem_tree.delete(secili[0])
        del self.kalemler[index]

    def _rapor_goster(self, metin):
        self.rapor_box.configure(state="normal")
        self.rapor_box.delete("0.0", "end")
        self.rapor_box.insert("0.0", metin)
        self.rapor_box.configure(state="disabled")

    # ================= KAYDET / LİSTE =================

    def kaydet(self):
        """İrsaliye formunu ve kalemlerini veritabanına kaydeder."""
        # Combobox'tan seçilen değeri çözüyoruz
        sa_id = self._sa_id_coz(self.sa_combo.get())
        
        # EĞER COMBOBOX BOŞSA veya seçilmediyse sa_id'yi None yapıyoruz
        if not sa_id or str(sa_id).strip() == "" or str(sa_id).lower() == "none":
            sa_id = None  # Veritabanına doğrudan boş (NULL) gidecek

        if not self.kalemler:
            messagebox.showwarning("Uyarı", "En az bir kalem ekleyin")
            return
        if not self.irsaliye_no.get().strip():
            messagebox.showwarning("Uyarı", "İrsaliye numarası zorunludur")
            return

        # ================= MÜKERRER ID ENGELLEME =================
        if not self.duzenlenen_irsaliye_id:
            self.irsaliye_id = self.db.irsaliye_id_uret()
        # =========================================================

        form = {
            "irsaliye_id": self.irsaliye_id,
            "sa_id": sa_id,  # Seçildiyse SA_ID, seçilmediyse None (NULL) gider
            "irsaliye_no": self.irsaliye_no.get().strip(),
            "firma": self.firma.get().strip(),
            "cari_kart_id": (self.cari_map.get(self.firma.get().strip()) or {}).get("id"),
            "tarih": self.tarih_entry.get(),
        }

        db_kalemler = [{
            "irsaliye_id": self.irsaliye_id,
            "sa_kalem_id": k.get("sa_kalem_id"),  # SA seçilmediyse buralar da otomatik None gider
            "stok_kart_id": k.get("stok_kart_id") or (self.stok_map.get(k["urun_adi"]) or {}).get("id"),
            "urun_adi": k["urun_adi"],
            "miktar": k["miktar"],
            "birim": k["birim"],
        } for k in self.kalemler]

        if self.duzenlenen_irsaliye_id:
            basarili, sonuc = self.db.irsaliye_guncelle(self.duzenlenen_irsaliye_id, form)
            if not basarili:
                messagebox.showerror("Hata", f"İrsaliye güncellenemedi:\n{sonuc}")
                return
            ir_id = self.duzenlenen_irsaliye_id
            for dk in db_kalemler:
                dk["irsaliye_id"] = ir_id
            basarili, sonuc = self.db.irsaliye_kalemleri_yenile(ir_id, db_kalemler)
            if not basarili:
                messagebox.showerror("Hata", f"Kalemler güncellenemedi:\n{sonuc}")
                return
            messagebox.showinfo("OK", "İrsaliye güncellendi")
        else:
            basarili, sonuc = self.db.irsaliye_kaydet(form)
            if not basarili:
                messagebox.showerror("Hata", f"İrsaliye kaydedilemedi:\n{sonuc}")
                return
            for dk in db_kalemler:
                basarili, sonuc = self.db.irsaliye_kalem_ekle(dk)
                if not basarili:
                    messagebox.showerror("Hata", f"Kalem eklenemedi:\n{sonuc}")
                    return
            messagebox.showinfo("OK", "İrsaliye kaydedildi")

        self.temizle()
        self.listele()

    def listele(self):
        for i in self.alt_tree.get_children():
            self.alt_tree.delete(i)

        veriler = self.db.irsaliyeler_getir()
        q = self.search_entry.get().lower()
        gorunen = 0

        for v in veriler:
            ir_id = v.get("irsaliye_id", "")
            sa_id = v.get("sa_id", "")
            if q and q not in ir_id.lower() and q not in sa_id.lower():
                continue

            durum = v.get("onay_durumu", "ONAY BEKLİYOR")
            tag = "BEKLE"
            if "2. ONAY" in durum:
                tag = "ONAY2"
            elif "1. ONAY" in durum:
                tag = "ONAY1"
            elif "FARK" in durum:
                tag = "FARK"

            self.alt_tree.insert("", "end", values=(
                ir_id, sa_id, v.get("irsaliye_no", ""),
                v.get("firma", ""), v.get("tarih", ""), durum
            ), tags=(tag,))
            gorunen += 1

        self.ozet_label.configure(text=f"{gorunen} kayıt")

    def temizle(self):
        self.kalemler.clear()
        self.duzenlenen_irsaliye_id = None
        for i in self.kalem_tree.get_children():
            self.kalem_tree.delete(i)
        self.irsaliye_id = self.db.irsaliye_id_uret()
        self.ir_label.configure(text=f"İRSALİYE ID: {self.irsaliye_id}")
        self.mod_label.configure(text="YENİ İRSALİYE", fg_color="#1E40AF")
        self.irsaliye_no.delete(0, "end")
        self.firma.configure(values=self.cari_secenekleri_getir())
        self.firma.set("")
        self.urun_adi.configure(values=self.stok_secenekleri_getir())
        self.urun_adi.set("")
        self.miktar.delete(0, "end")

    def secili_irsaliye_id_getir(self):
        secili = self.alt_tree.selection()
        if not secili:
            messagebox.showwarning("Uyarı", "Listeden bir irsaliye seçin")
            return None
        values = self.alt_tree.item(secili[0], "values")
        return values[0] if values else None

    def irsaliye_yukle(self):
        ir_id = self.secili_irsaliye_id_getir()
        if not ir_id:
            return

        detay = self.db.irsaliye_detay_getir(ir_id)
        form = detay.get("form")
        kalemler = detay.get("kalemler", [])
        if not form:
            messagebox.showerror("Hata", "İrsaliye bulunamadı")
            return

        durum = str(form.get("onay_durumu") or "")
        if "2. ONAY" in durum:
            messagebox.showwarning("Uyarı", "2. onay tamamlanan irsaliye düzenlenemez")
            return

        self.duzenlenen_irsaliye_id = ir_id
        self.irsaliye_id = ir_id
        self.ir_label.configure(text=f"İRSALİYE ID: {ir_id} (DÜZENLEME)")
        self.mod_label.configure(text="DÜZENLEME MODU", fg_color="#B45309")

        sa_id = form.get("sa_id", "")
        for secenek in self.sa_combo.cget("values"):
            if secenek.startswith(sa_id):
                self.sa_combo.set(secenek)
                break
        self.sa_secildi()

        self.irsaliye_no.delete(0, "end")
        self.irsaliye_no.insert(0, form.get("irsaliye_no", ""))
        self.firma.set(form.get("firma", ""))

        try:
            self.tarih_entry.set_date(form.get("tarih"))
        except Exception:
            pass

        self.kalemler.clear()
        for i in self.kalem_tree.get_children():
            self.kalem_tree.delete(i)

        for k in kalemler:
            veri = {
                "urun_adi": k.get("urun_adi", ""),
                "miktar": float(k.get("miktar") or 0),
                "birim": k.get("birim", "ADET"),
                "sa_kalem_id": k.get("sa_kalem_id"),
            }
            self.kalemler.append(veri)
            self.kalem_tree.insert("", "end", values=(veri["urun_adi"], veri["miktar"], veri["birim"]))

    # ================= KARŞILAŞTIRMA & ONAY =================

    def karsilastir(self):
        ir_id = self.secili_irsaliye_id_getir()
        if not ir_id:
            sa_id = self._sa_id_coz(self.sa_combo.get())
            if not sa_id:
                messagebox.showwarning("Uyarı", "Karşılaştırma için irsaliye veya SA ID seçin")
                return
        else:
            detay = self.db.irsaliye_detay_getir(ir_id)
            sa_id = detay.get("form", {}).get("sa_id")
            if not sa_id:
                messagebox.showerror("Hata", "SA ID bulunamadı")
                return

        basarili, sonuc, rapor = self.db.irsaliye_karsilastir(sa_id, ir_id)
        if not basarili:
            messagebox.showerror("Hata", sonuc)
            return

        self._rapor_goster(rapor)

        if ir_id:
            self.db.irsaliye_karsilastirma_raporu_guncelle(ir_id, rapor)
            self.listele()

        if sonuc["genel_uyumlu"]:
            messagebox.showinfo("Karşılaştırma", "Miktar ve cins uyumlu. 2. onay için imzalı evrak yükleyip 2. Onay Uygula'yı kullanın.")
        else:
            messagebox.showwarning("Karşılaştırma", "Uyumsuzluk tespit edildi. Rapor panelinde detayları inceleyin.")

    def ikinci_onay_uygula(self):
        ir_id = self.secili_irsaliye_id_getir()
        if not ir_id:
            return

        detay = self.db.irsaliye_detay_getir(ir_id)
        form = detay.get("form", {})
        if "1. ONAY" not in str(form.get("onay_durumu", "")):
            messagebox.showwarning("Uyarı", "2. onay için önce imzalı evrak yüklenmeli (1. onay)")
            return

        basarili, sonuc, rapor = self.db.irsaliye_karsilastir(form.get("sa_id"), ir_id)
        if not basarili:
            messagebox.showerror("Hata", sonuc)
            return

        self._rapor_goster(rapor)
        yeni_durum = "2. ONAY TAMAMLANDI" if sonuc["genel_uyumlu"] else "FARK VAR — YÖNETİCİ BİLDİRİLDİ"
        self.db.irsaliye_onay_durumu_guncelle(ir_id, yeni_durum, rapor)
        self.listele()

        if sonuc["genel_uyumlu"]:
            messagebox.showinfo("2. Onay", "Miktar ve cins uyumlu — 2. onay tamamlandı.")
        else:
            messagebox.showwarning("2. Onay", "Uyumsuzluk var — yöneticiye bildirildi.")

    def imzali_evrak_yukle(self):
        ir_id = self.secili_irsaliye_id_getir()
        if not ir_id:
            return

        dosya = filedialog.askopenfilename(
            title="İmzalı Teslim Evrakı Seç",
            filetypes=[("Evrak", "*.pdf;*.png;*.jpg;*.jpeg"), ("Tüm Dosyalar", "*.*")]
        )
        if not dosya:
            return

        hedef_klasor = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imzali_irsaliyeler")
        os.makedirs(hedef_klasor, exist_ok=True)
        uzanti = os.path.splitext(dosya)[1]
        hedef_yol = os.path.join(hedef_klasor, f"{ir_id}_1_onay_imzali{uzanti}")

        try:
            shutil.copy2(dosya, hedef_yol)
            basarili, sonuc = self.db.irsaliye_imzali_evrak_guncelle(ir_id, hedef_yol)
        except Exception as e:
            messagebox.showerror("Hata", f"Evrak yüklenemedi:\n{e}")
            return

        if not basarili:
            messagebox.showerror("Hata", f"Onay güncellenemedi:\n{sonuc}")
            return

        messagebox.showinfo("1. Onay", "İmzalı teslim evrakı yüklendi — 1. onay tamamlandı.")
        self.listele()