import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry


class AracDemirbasModul(ctk.CTkFrame):
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
        
        self.duzenlenen_arac_id = None
        self.personel_map = {}
        
        self.setup_ui()
        self.personel_listesini_yenile()
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
        
        # ================= SOL PANEL (FORM) =================
        self.left = ctk.CTkFrame(self, fg_color="white", corner_radius=14,
                                 border_width=1, border_color="#E2E8F0")
        self.left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        header = ctk.CTkFrame(self.left, fg_color=self.COLOR_PRIMARY, corner_radius=12)
        header.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(header, text="🚗 ARAÇ/DEMİRBAŞ KAYIT", text_color="white",
                     font=("Segoe UI", 18, "bold")).pack(pady=6)
        
        self.mod_label = ctk.CTkLabel(header, text="YENİ KAYIT", text_color="white",
                                      fg_color="#1E40AF", corner_radius=10, height=24,
                                      font=("Segoe UI", 11, "bold"))
        self.mod_label.pack(pady=(0, 10))
        
        form = ctk.CTkScrollableFrame(self.left, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=15, pady=10)
        
        fnt_label = ("Segoe UI", 12, "bold")
        fnt_input = ("Segoe UI", 12)
        
        # Araç Tipi
        ctk.CTkLabel(form, text="📋 Tip", font=fnt_label).pack(anchor="w")
        self.arac_tipi = ctk.CTkComboBox(form, values=["ARAC", "IS_MAKINESI", "DEMIRBAS"],
                                         height=35, font=fnt_input)
        self.arac_tipi.set("ARAC")
        self.arac_tipi.pack(fill="x", pady=(0, 10))
        
        # Plaka/Demirbaş No
        ctk.CTkLabel(form, text="🔖 Plaka / Demirbaş No", font=fnt_label).pack(anchor="w")
        self.plaka = ctk.CTkEntry(form, height=35, font=fnt_input)
        self.plaka.pack(fill="x", pady=(0, 10))
        
        # Marka / Model (tek alan - DB'de marka_model olarak tutulur)
        ctk.CTkLabel(form, text="🏷 Marka / Model", font=fnt_label).pack(anchor="w")
        self.marka_model = ctk.CTkEntry(form, height=35, font=fnt_input, placeholder_text="Örn: Ford Transit 2022")
        self.marka_model.pack(fill="x", pady=(0, 10))
        
        # Sorumlu Personel
        ctk.CTkLabel(form, text="👤 Sorumlu Personel", font=fnt_label).pack(anchor="w")
        self.sorumlu_personel = ctk.CTkComboBox(form, values=[], height=35, font=fnt_input)
        self.sorumlu_personel.set("")
        self.sorumlu_personel.pack(fill="x", pady=(0, 10))
        
        # Mevcut KM
        ctk.CTkLabel(form, text="🔢 Mevcut KM", font=fnt_label).pack(anchor="w")
        self.mevcut_km = ctk.CTkEntry(form, height=35, font=fnt_input)
        self.mevcut_km.pack(fill="x", pady=(0, 10))
        
        # KM Bakım Aralığı
        ctk.CTkLabel(form, text="🔧 KM Bakım Aralığı", font=fnt_label).pack(anchor="w")
        self.km_bakim_araligi = ctk.CTkEntry(form, height=35, font=fnt_input, placeholder_text="Örn: 10000")
        self.km_bakim_araligi.pack(fill="x", pady=(0, 10))
        
        # Yağ Bakım KM
        ctk.CTkLabel(form, text="🛢️ Yağ Bakım KM", font=fnt_label).pack(anchor="w")
        self.yag_bakim_km = ctk.CTkEntry(form, height=35, font=fnt_input, placeholder_text="Örn: 5000")
        self.yag_bakim_km.pack(fill="x", pady=(0, 10))
        
        # Muayene Tarihi
        ctk.CTkLabel(form, text="📋 Muayene Tarihi", font=fnt_label).pack(anchor="w")
        self.muayene_tarihi = DateEntry(form, date_pattern="yyyy-mm-dd", font=fnt_input)
        self.muayene_tarihi.pack(fill="x", pady=(0, 10))
        
        # Sigorta Tarihi
        ctk.CTkLabel(form, text="🛡️ Sigorta Tarihi", font=fnt_label).pack(anchor="w")
        self.sigorta_tarihi = DateEntry(form, date_pattern="yyyy-mm-dd", font=fnt_input)
        self.sigorta_tarihi.pack(fill="x", pady=(0, 10))
        
        # Durum
        ctk.CTkLabel(form, text="✅ Durum", font=fnt_label).pack(anchor="w")
        self.durum = ctk.CTkComboBox(form, values=["AKTIF", "PASIF", "BAKIMDA"],
                                    height=35, font=fnt_input)
        self.durum.set("AKTIF")
        self.durum.pack(fill="x", pady=(0, 10))
        
        # Notlar
        ctk.CTkLabel(form, text="📝 Notlar", font=fnt_label).pack(anchor="w")
        self.aciklama = ctk.CTkTextbox(form, height=80, font=fnt_input)
        self.aciklama.pack(fill="x", pady=(0, 10))
        
        # Butonlar
        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(btn_frame, text="💾 Kaydet", fg_color=self.COLOR_SUCCESS,
                      hover_color="#059669", command=self.kaydet).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🧹 Temizle", fg_color=self.COLOR_MUTED,
                      hover_color="#475569", command=self.temizle).pack(side="left", padx=5)
        
        # ================= SAĞ PANEL (LİSTE + KM GİRİŞİ) =================
        self.right = ctk.CTkFrame(self, fg_color="white", corner_radius=14,
                                  border_width=1, border_color="#E2E8F0")
        self.right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Sekmeler
        self.tabview = ctk.CTkTabview(self.right, width=800)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Araç Listesi
        self.tab_araclar = self.tabview.add("Araç Listesi")
        self.setup_araclar_tab()
        
        # Tab 2: KM Girişleri
        self.tab_km = self.tabview.add("KM Girişleri")
        self.setup_km_tab()
        
        # Tab 3: Tahsisler
        self.tab_tahsis = self.tabview.add("Tahsisler")
        self.setup_tahsis_tab()
    
    def setup_araclar_tab(self):
        list_header = ctk.CTkFrame(self.tab_araclar, fg_color="transparent")
        list_header.pack(fill="x", padx=12, pady=(12, 0))
        
        ctk.CTkLabel(list_header, text="Kayıtlı Araçlar/Demirbaşlar", font=("Segoe UI", 17, "bold"),
                     text_color=self.COLOR_TEXT).pack(side="left")
        
        search_frame = ctk.CTkFrame(self.tab_araclar, fg_color="#F1F5F9", corner_radius=10)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(search_frame, text="🔎").pack(side="left", padx=8)
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Plaka veya marka ara...",
                                         height=40, border_width=0, fg_color="white")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=8)
        self.search_entry.bind("<KeyRelease>", lambda e: self.listele())
        
        self.araclar_tree = ttk.Treeview(
            self.tab_araclar,
            columns=("plaka", "tip", "marka_model", "km", "durum"),
            show="headings", height=12
        )
        kolonlar = [
            ("plaka", "Plaka/No", 120),
            ("tip", "Tip", 100),
            ("marka_model", "Marka/Model", 160),
            ("km", "KM", 80),
            ("durum", "Durum", 100),
        ]
        for col, baslik, gen in kolonlar:
            self.araclar_tree.heading(col, text=baslik)
            self.araclar_tree.column(col, width=gen, anchor="center")
        self.araclar_tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.araclar_tree.bind("<Double-1>", lambda e: self.arac_yukle())
        
        self.araclar_tree.tag_configure("AKTIF", foreground="#16A34A")
        self.araclar_tree.tag_configure("PASIF", foreground="#64748B")
        self.araclar_tree.tag_configure("BAKIMDA", foreground="#F59E0B")
        
        btn_frame = ctk.CTkFrame(self.tab_araclar, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="✏️ Düzenle", fg_color=self.COLOR_WARNING,
                      hover_color="#D97706", command=self.arac_yukle).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Sil", fg_color=self.COLOR_DANGER,
                      hover_color="#DC2626", command=self.arac_sil).pack(side="left", padx=5)
    
    def setup_km_tab(self):
        # Araç Seçimi
        arac_sec_frame = ctk.CTkFrame(self.tab_km, fg_color="#F1F5F9", corner_radius=10)
        arac_sec_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(arac_sec_frame, text="Araç Seç:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=8)
        self.km_arac_combo = ctk.CTkComboBox(arac_sec_frame, values=[], width=200, height=35)
        self.km_arac_combo.pack(side="left", padx=5)
        ctk.CTkButton(arac_sec_frame, text="↻", width=40, height=35,
                      command=self.km_arac_listesini_yenile).pack(side="left", padx=5)
        
        # KM Giriş Formu
        km_form = ctk.CTkFrame(self.tab_km, fg_color="white", corner_radius=10,
                               border_width=1, border_color="#E2E8F0")
        km_form.pack(fill="x", padx=10, pady=5)
        
        row1 = ctk.CTkFrame(km_form, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(row1, text="Tarih:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.km_tarih = DateEntry(row1, date_pattern="yyyy-mm-dd", font=("Segoe UI", 11))
        self.km_tarih.set_date(datetime.now().date())
        self.km_tarih.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="KM:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.km_deger = ctk.CTkEntry(row1, width=150, height=35)
        self.km_deger.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="Personel:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.km_personel = ctk.CTkComboBox(row1, values=[], width=200, height=35)
        self.km_personel.pack(side="left", padx=5)
        
        row2 = ctk.CTkFrame(km_form, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(row2, text="Açıklama:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.km_aciklama = ctk.CTkEntry(row2, height=35)
        self.km_aciklama.pack(side="left", fill="x", expand=True, padx=5)
        
        ctk.CTkButton(row2, text="➕ KM Ekle", fg_color=self.COLOR_SUCCESS,
                      hover_color="#059669", command=self.km_ekle).pack(side="left", padx=5)
        
        # KM Listesi
        self.km_tree = ttk.Treeview(
            self.tab_km,
            columns=("tarih", "km", "personel", "aciklama"),
            show="headings", height=10
        )
        self.km_tree.heading("tarih", text="Tarih")
        self.km_tree.heading("km", text="KM")
        self.km_tree.heading("personel", text="Personel")
        self.km_tree.heading("aciklama", text="Açıklama")
        
        self.km_tree.column("tarih", width=120, anchor="center")
        self.km_tree.column("km", width=100, anchor="center")
        self.km_tree.column("personel", width=200, anchor="w")
        self.km_tree.column("aciklama", width=250, anchor="w")
        
        self.km_tree.pack(fill="both", expand=True, padx=10, pady=5)
    
    def setup_tahsis_tab(self):
        # Tahsis Formu
        tahsis_form = ctk.CTkFrame(self.tab_tahsis, fg_color="white", corner_radius=10,
                                    border_width=1, border_color="#E2E8F0")
        tahsis_form.pack(fill="x", padx=10, pady=10)
        
        row1 = ctk.CTkFrame(tahsis_form, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(row1, text="Araç:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.tahsis_arac = ctk.CTkComboBox(row1, values=[], width=200, height=35)
        self.tahsis_arac.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="Personel:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.tahsis_personel = ctk.CTkComboBox(row1, values=[], width=200, height=35)
        self.tahsis_personel.pack(side="left", padx=5)
        
        row2 = ctk.CTkFrame(tahsis_form, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(row2, text="Tahsis Tarihi:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.tahsis_tarih = DateEntry(row2, date_pattern="yyyy-mm-dd", font=("Segoe UI", 11))
        self.tahsis_tarih.set_date(datetime.now().date())
        self.tahsis_tarih.pack(side="left", padx=5)
        
        ctk.CTkLabel(row2, text="İade Tarihi:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.tahsis_iade = DateEntry(row2, date_pattern="yyyy-mm-dd", font=("Segoe UI", 11))
        self.tahsis_iade.pack(side="left", padx=5)
        
        ctk.CTkButton(row2, text="➕ Tahsis Et", fg_color=self.COLOR_SUCCESS,
                      hover_color="#059669", command=self.tahsis_ekle).pack(side="left", padx=5)
        
        # Tahsis Listesi
        self.tahsis_tree = ttk.Treeview(
            self.tab_tahsis,
            columns=("arac", "personel", "tahsis_tarih", "iade_tarih", "durum"),
            show="headings", height=12
        )
        self.tahsis_tree.heading("arac", text="Araç")
        self.tahsis_tree.heading("personel", text="Personel")
        self.tahsis_tree.heading("tahsis_tarih", text="Tahsis Tarihi")
        self.tahsis_tree.heading("iade_tarih", text="İade Tarihi")
        self.tahsis_tree.heading("durum", text="Durum")
        
        self.tahsis_tree.column("arac", width=150, anchor="w")
        self.tahsis_tree.column("personel", width=200, anchor="w")
        self.tahsis_tree.column("tahsis_tarih", width=120, anchor="center")
        self.tahsis_tree.column("iade_tarih", width=120, anchor="center")
        self.tahsis_tree.column("durum", width=100, anchor="center")
        
        self.tahsis_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.tahsis_tree.tag_configure("TAHSISLI", foreground="#16A34A")
        self.tahsis_tree.tag_configure("IADE", foreground="#64748B")
    
    def personel_listesini_yenile(self):
        try:
            personeller = self.db.aktif_personeller_getir()
            secenekler = []
            self.personel_map = {}
            for p in personeller or []:
                ad_soyad = f"{p.get('ad', '')} {p.get('soyad', '')}".strip()
                if not ad_soyad:
                    continue
                secenekler.append(ad_soyad)
                self.personel_map[ad_soyad] = p
            
            self.km_personel.configure(values=secenekler)
            self.tahsis_personel.configure(values=secenekler)
            self.sorumlu_personel.configure(values=[""] + secenekler)
        except Exception as e:
            print("Personel listesi yenileme hatası:", e)
    
    def km_arac_listesini_yenile(self):
        try:
            araclar = self.db.araclar_getir()
            secenekler = []
            for a in araclar or []:
                plaka = a.get("plaka", "")
                if plaka:
                    secenekler.append(plaka)
            
            self.km_arac_combo.configure(values=secenekler)
            self.tahsis_arac.configure(values=secenekler)
        except Exception as e:
            print("Araç listesi yenileme hatası:", e)
    
    def kaydet(self):
        if not self.plaka.get().strip():
            messagebox.showwarning("Uyarı", "Plaka/Demirbaş No zorunludur")
            return
        
        try:
            mevcut_km = float(self.mevcut_km.get() or 0)
        except ValueError:
            messagebox.showwarning("Uyarı", "KM sayısal olmalı")
            return

        try:
            km_bakim_araligi = float(self.km_bakim_araligi.get()) if self.km_bakim_araligi.get().strip() else None
        except ValueError:
            messagebox.showwarning("Uyarı", "KM bakım aralığı sayısal olmalı")
            return

        try:
            yag_bakim_km = float(self.yag_bakim_km.get()) if self.yag_bakim_km.get().strip() else None
        except ValueError:
            messagebox.showwarning("Uyarı", "Yağ bakım KM sayısal olmalı")
            return

        sorumlu_adi = self.sorumlu_personel.get().strip()
        sorumlu_personel_id = self.personel_map.get(sorumlu_adi, {}).get("id") if sorumlu_adi else None
        
        arac = {
            "arac_tipi": self.arac_tipi.get(),
            "plaka": self.plaka.get().strip(),
            "marka_model": self.marka_model.get().strip(),
            "sorumlu_personel_id": sorumlu_personel_id,
            "mevcut_km": mevcut_km,
            "km_bakim_araligi": km_bakim_araligi,
            "yag_bakim_km": yag_bakim_km,
            "muayene_tarihi": self.muayene_tarihi.get(),
            "sigorta_tarihi": self.sigorta_tarihi.get(),
            "durum": self.durum.get(),
            "aciklama": self.aciklama.get("0.0", "end").strip(),
        }
        
        if self.duzenlenen_arac_id:
            basarili, sonuc = self.db.arac_guncelle(self.duzenlenen_arac_id, arac)
            if basarili:
                messagebox.showinfo("Başarılı", "Araç güncellendi")
            else:
                messagebox.showerror("Hata", f"Güncelleme hatası:\n{sonuc}")
        else:
            basarili, sonuc = self.db.arac_kaydet(arac)
            if basarili:
                messagebox.showinfo("Başarılı", "Araç kaydedildi")
            else:
                messagebox.showerror("Hata", f"Kayıt hatası:\n{sonuc}")
        
        self.temizle()
        self.listele()
        self.km_arac_listesini_yenile()
    
    def listele(self):
        for item in self.araclar_tree.get_children():
            self.araclar_tree.delete(item)
        
        araclar = self.db.araclar_getir()
        q = self.search_entry.get().lower()
        
        for a in araclar:
            plaka = (a.get("plaka") or "").lower()
            marka_model = (a.get("marka_model") or "").lower()
            if q and q not in plaka and q not in marka_model:
                continue
            
            durum = a.get("durum", "AKTIF")
            self.araclar_tree.insert("", "end", values=(
                a.get("plaka", ""),
                a.get("arac_tipi", ""),
                a.get("marka_model", ""),
                a.get("mevcut_km", 0),
                durum
            ), tags=(durum,))
    
    def arac_yukle(self):
        secili = self.araclar_tree.selection()
        if not secili:
            messagebox.showwarning("Uyarı", "Listeden bir araç seçin")
            return
        
        values = self.araclar_tree.item(secili[0], "values")
        plaka = values[0]
        
        araclar = self.db.araclar_getir()
        arac = next((a for a in araclar if a.get("plaka") == plaka), None)
        
        if not arac:
            messagebox.showerror("Hata", "Araç bulunamadı")
            return
        
        self.duzenlenen_arac_id = arac.get("id")
        self.mod_label.configure(text="DÜZENLEME MODU", fg_color="#B45309")
        
        self.arac_tipi.set(arac.get("arac_tipi", ""))
        self.plaka.delete(0, "end")
        self.plaka.insert(0, arac.get("plaka", ""))
        self.marka_model.delete(0, "end")
        self.marka_model.insert(0, arac.get("marka_model", ""))

        sorumlu_id = arac.get("sorumlu_personel_id")
        sorumlu_adi = ""
        if sorumlu_id:
            for ad, p in self.personel_map.items():
                if p.get("id") == sorumlu_id:
                    sorumlu_adi = ad
                    break
        self.sorumlu_personel.set(sorumlu_adi)

        self.mevcut_km.delete(0, "end")
        self.mevcut_km.insert(0, str(arac.get("mevcut_km", 0)))
        self.km_bakim_araligi.delete(0, "end")
        self.km_bakim_araligi.insert(0, str(arac.get("km_bakim_araligi") or ""))
        self.yag_bakim_km.delete(0, "end")
        self.yag_bakim_km.insert(0, str(arac.get("yag_bakim_km") or ""))
        
        try:
            self.muayene_tarihi.set_date(arac.get("muayene_tarihi"))
        except Exception:
            pass

        try:
            self.sigorta_tarihi.set_date(arac.get("sigorta_tarihi"))
        except Exception:
            pass
        
        self.durum.set(arac.get("durum", "AKTIF"))
        self.aciklama.delete("0.0", "end")
        self.aciklama.insert("0.0", arac.get("aciklama", "") or arac.get("notlar", ""))
    
    def arac_sil(self):
        secili = self.araclar_tree.selection()
        if not secili:
            messagebox.showwarning("Uyarı", "Listeden bir araç seçin")
            return
        
        values = self.araclar_tree.item(secili[0], "values")
        plaka = values[0]
        
        if not messagebox.askyesno("Onay", f"{plaka} plakalı aracı silmek istiyor musunuz?"):
            return
        
        try:
            araclar = self.db.araclar_getir()
            arac = next((a for a in araclar if a.get("plaka") == plaka), None)
            if arac:
                self.db.supabase.table("arac_kartlari").delete().eq("id", arac.get("id")).execute()
                messagebox.showinfo("Başarılı", "Araç silindi")
                self.listele()
                self.km_arac_listesini_yenile()
        except Exception as e:
            messagebox.showerror("Hata", f"Silme hatası:\n{e}")
    
    def temizle(self):
        self.duzenlenen_arac_id = None
        self.mod_label.configure(text="YENİ KAYIT", fg_color="#1E40AF")
        self.arac_tipi.set("ARAC")
        self.plaka.delete(0, "end")
        self.marka_model.delete(0, "end")
        self.sorumlu_personel.set("")
        self.mevcut_km.delete(0, "end")
        self.km_bakim_araligi.delete(0, "end")
        self.yag_bakim_km.delete(0, "end")
        self.muayene_tarihi.set_date(datetime.now().date())
        self.sigorta_tarihi.set_date(datetime.now().date())
        self.durum.set("AKTIF")
        self.aciklama.delete("0.0", "end")
    
    def km_ekle(self):
        plaka = self.km_arac_combo.get()
        if not plaka:
            messagebox.showwarning("Uyarı", "Araç seçin")
            return
        
        try:
            km = float(self.km_deger.get())
            if km <= 0:
                messagebox.showwarning("Uyarı", "KM 0'dan büyük olmalı")
                return
        except ValueError:
            messagebox.showwarning("Uyarı", "KM sayısal olmalı")
            return
        
        araclar = self.db.araclar_getir()
        arac = next((a for a in araclar if a.get("plaka") == plaka), None)
        if not arac:
            messagebox.showerror("Hata", "Araç bulunamadı")
            return
        
        personel_adi = self.km_personel.get()
        personel_id = self.personel_map.get(personel_adi, {}).get("id")
        
        km_giris = {
            "arac_id": arac.get("id"),
            "tarih": self.km_tarih.get(),
            "km": km,
            "personel_id": personel_id,
            "aciklama": self.km_aciklama.get(),
        }
        
        basarili, sonuc = self.db.arac_km_girisi_km(km_giris)
        if basarili:
            messagebox.showinfo("Başarılı", "KM girişi kaydedildi")
            self.km_deger.delete(0, "end")
            self.km_aciklama.delete(0, "end")
            self.km_listesi_getir()
            self.listele()
        else:
            messagebox.showerror("Hata", f"Kayıt hatası:\n{sonuc}")
    
    def km_listesi_getir(self):
        for item in self.km_tree.get_children():
            self.km_tree.delete(item)
        
        plaka = self.km_arac_combo.get()
        if not plaka:
            return
        
        araclar = self.db.araclar_getir()
        arac = next((a for a in araclar if a.get("plaka") == plaka), None)
        if not arac:
            return
        
        km_girisleri = self.db.arac_km_girisleri_getir(arac.get("id"))
        
        for km in km_girisleri:
            personel_id = km.get("personel_id")
            personel_adi = ""
            if personel_id:
                for ad, p in self.personel_map.items():
                    if p.get("id") == personel_id:
                        personel_adi = ad
                        break
            
            self.km_tree.insert("", "end", values=(
                km.get("tarih", ""),
                km.get("km", 0),
                personel_adi,
                km.get("aciklama", ""),
            ))
    
    def tahsis_ekle(self):
        plaka = self.tahsis_arac.get()
        personel_adi = self.tahsis_personel.get()
        
        if not plaka or not personel_adi:
            messagebox.showwarning("Uyarı", "Araç ve personel seçin")
            return
        
        araclar = self.db.araclar_getir()
        arac = next((a for a in araclar if a.get("plaka") == plaka), None)
        personel = self.personel_map.get(personel_adi)
        
        if not arac or not personel:
            messagebox.showerror("Hata", "Araç veya personel bulunamadı")
            return
        
        tahsis = {
            "arac_id": arac.get("id"),
            "personel_id": personel.get("id"),
            "tahsis_tarihi": self.tahsis_tarih.get(),
            "iade_tarihi": self.tahsis_iade.get() if self.tahsis_iade.get() else None,
            "durum": "TAHSISLI",
            "aciklama": "",
        }
        
        basarili, sonuc = self.db.tahsis_kaydet(tahsis)
        if basarili:
            messagebox.showinfo("Başarılı", "Tahsis kaydedildi")
            self.tahsis_listesi_getir()
        else:
            messagebox.showerror("Hata", f"Kayıt hatası:\n{sonuc}")
    
    def tahsis_listesi_getir(self):
        for item in self.tahsis_tree.get_children():
            self.tahsis_tree.delete(item)
        
        tahsisler = self.db.tahsisleri_getir()
        
        for t in tahsisler:
            arac_id = t.get("arac_id")
            personel_id = t.get("personel_id")
            
            araclar = self.db.araclar_getir()
            arac = next((a for a in araclar if a.get("id") == arac_id), None)
            
            personel_adi = ""
            for ad, p in self.personel_map.items():
                if p.get("id") == personel_id:
                    personel_adi = ad
                    break
            
            durum = t.get("durum", "TAHSISLI")
            self.tahsis_tree.insert("", "end", values=(
                arac.get("plaka", "") if arac else "-",
                personel_adi,
                t.get("tahsis_tarihi", ""),
                t.get("iade_tarihi", "-"),
                durum
            ), tags=(durum,))