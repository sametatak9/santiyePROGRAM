import customtkinter as ctk
from tkinter import ttk, messagebox


class CariKartlarModul(ctk.CTkFrame):
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
        
        self.duzenlenen_id = None
        
        self.setup_ui()
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
        
        ctk.CTkLabel(header, text="📇 CARİ KARTLAR", text_color="white",
                     font=("Segoe UI", 18, "bold")).pack(pady=6)
        
        self.mod_label = ctk.CTkLabel(header, text="YENİ KAYIT", text_color="white",
                                      fg_color="#1E40AF", corner_radius=10, height=24,
                                      font=("Segoe UI", 11, "bold"))
        self.mod_label.pack(pady=(0, 10))
        
        form = ctk.CTkScrollableFrame(self.left, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=15, pady=10)
        
        fnt_label = ("Segoe UI", 12, "bold")
        fnt_input = ("Segoe UI", 12)
        
        # Kart Tipi
        ctk.CTkLabel(form, text="📋 Kart Tipi", font=fnt_label).pack(anchor="w")
        self.kart_tipi = ctk.CTkComboBox(form, values=["CARI", "TEDARIKCI", "TASERON", "MUSTERI"],
                                         height=35, font=fnt_input)
        self.kart_tipi.set("CARI")
        self.kart_tipi.pack(fill="x", pady=(0, 10))
        
        # Cari Kod
        ctk.CTkLabel(form, text="🔢 Cari Kod", font=fnt_label).pack(anchor="w")
        self.cari_kod = ctk.CTkEntry(form, height=35, font=fnt_input)
        self.cari_kod.pack(fill="x", pady=(0, 10))
        
        # Firma Adı
        ctk.CTkLabel(form, text="🏢 Firma Adı", font=fnt_label).pack(anchor="w")
        self.firma_adi = ctk.CTkEntry(form, height=35, font=fnt_input)
        self.firma_adi.pack(fill="x", pady=(0, 10))
        
        # Ünvan
        ctk.CTkLabel(form, text="👤 Ünvan / Detay", font=fnt_label).pack(anchor="w")
        self.unvan = ctk.CTkEntry(form, height=35, font=fnt_input)
        self.unvan.pack(fill="x", pady=(0, 10))
        
        # Yetkili
        ctk.CTkLabel(form, text="👔 Yetkili", font=fnt_label).pack(anchor="w")
        self.yetkili = ctk.CTkEntry(form, height=35, font=fnt_input)
        self.yetkili.pack(fill="x", pady=(0, 10))
        
        # Telefon
        ctk.CTkLabel(form, text="📞 Telefon", font=fnt_label).pack(anchor="w")
        self.telefon = ctk.CTkEntry(form, height=35, font=fnt_input)
        self.telefon.pack(fill="x", pady=(0, 10))
        
        # E-posta
        ctk.CTkLabel(form, text="📧 E-posta", font=fnt_label).pack(anchor="w")
        self.eposta = ctk.CTkEntry(form, height=35, font=fnt_input)
        self.eposta.pack(fill="x", pady=(0, 10))
        
        # Vergi No
        ctk.CTkLabel(form, text="📄 Vergi No", font=fnt_label).pack(anchor="w")
        self.vergi_no = ctk.CTkEntry(form, height=35, font=fnt_input)
        self.vergi_no.pack(fill="x", pady=(0, 10))
        
        # Vergi Dairesi
        ctk.CTkLabel(form, text="🏛 Vergi Dairesi", font=fnt_label).pack(anchor="w")
        self.vergi_dairesi = ctk.CTkEntry(form, height=35, font=fnt_input)
        self.vergi_dairesi.pack(fill="x", pady=(0, 10))
        
        # Adres
        ctk.CTkLabel(form, text="📍 Adres", font=fnt_label).pack(anchor="w")
        self.adres = ctk.CTkTextbox(form, height=80, font=fnt_input)
        self.adres.pack(fill="x", pady=(0, 10))
        
        # IBAN
        ctk.CTkLabel(form, text="💳 IBAN", font=fnt_label).pack(anchor="w")
        self.iban = ctk.CTkEntry(form, height=35, font=fnt_input)
        self.iban.pack(fill="x", pady=(0, 10))
        
        # Durum
        ctk.CTkLabel(form, text="✅ Durum", font=fnt_label).pack(anchor="w")
        self.durum = ctk.CTkComboBox(form, values=["AKTIF", "PASIF"],
                                    height=35, font=fnt_input)
        self.durum.set("AKTIF")
        self.durum.pack(fill="x", pady=(0, 10))
        
        # Notlar
        ctk.CTkLabel(form, text="📝 Notlar", font=fnt_label).pack(anchor="w")
        self.notlar = ctk.CTkTextbox(form, height=80, font=fnt_input)
        self.notlar.pack(fill="x", pady=(0, 10))
        
        # Butonlar
        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(btn_frame, text="💾 Kaydet", fg_color=self.COLOR_SUCCESS,
                      hover_color="#059669", command=self.kaydet).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🧹 Temizle", fg_color=self.COLOR_MUTED,
                      hover_color="#475569", command=self.temizle).pack(side="left", padx=5)
        
        # ================= SAĞ PANEL (LİSTE) =================
        self.right = ctk.CTkFrame(self, fg_color="white", corner_radius=14,
                                  border_width=1, border_color="#E2E8F0")
        self.right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        list_header = ctk.CTkFrame(self.right, fg_color="transparent")
        list_header.pack(fill="x", padx=12, pady=(12, 0))
        
        ctk.CTkLabel(list_header, text="Cari Kart Listesi", font=("Segoe UI", 17, "bold"),
                     text_color=self.COLOR_TEXT).pack(side="left")
        
        # Filtre
        filter_frame = ctk.CTkFrame(self.right, fg_color="#F1F5F9", corner_radius=10)
        filter_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(filter_frame, text="🔎").pack(side="left", padx=8)
        self.search_entry = ctk.CTkEntry(filter_frame, placeholder_text="Firma adı veya telefon ara...",
                                         height=40, border_width=0, fg_color="white")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=8)
        self.search_entry.bind("<KeyRelease>", lambda e: self.listele())
        
        # Liste
        self.tree = ttk.Treeview(
            self.right,
            columns=("firma", "tip", "telefon", "yetkili", "durum"),
            show="headings", height=18
        )
        self.tree.heading("firma", text="Firma Adı")
        self.tree.heading("tip", text="Tip")
        self.tree.heading("telefon", text="Telefon")
        self.tree.heading("yetkili", text="Yetkili")
        self.tree.heading("durum", text="Durum")
        
        self.tree.column("firma", width=200, anchor="w")
        self.tree.column("tip", width=120, anchor="center")
        self.tree.column("telefon", width=150, anchor="center")
        self.tree.column("yetkili", width=150, anchor="w")
        self.tree.column("durum", width=100, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<Double-1>", lambda e: self.kart_yukle())
        
        self.tree.tag_configure("AKTIF", foreground="#16A34A")
        self.tree.tag_configure("PASIF", foreground="#64748B")
        
        # Butonlar
        btn_frame = ctk.CTkFrame(self.right, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="✏️ Düzenle", fg_color=self.COLOR_WARNING,
                      hover_color="#D97706", command=self.kart_yukle).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Sil", fg_color=self.COLOR_DANGER,
                      hover_color="#DC2626", command=self.kart_sil).pack(side="left", padx=5)
    
    def listele(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            kartlar = self.db.cari_kartlari_getir()
            q = self.search_entry.get().lower()
            
            for k in kartlar:
                firma = k.get("firma_adi", "").lower()
                telefon = k.get("telefon", "").lower()
                if q and q not in firma and q not in telefon:
                    continue
                
                durum = k.get("durum", "AKTIF")
                self.tree.insert("", "end", values=(
                    k.get("firma_adi", ""),
                    k.get("kart_tipi", ""),
                    k.get("telefon", ""),
                    k.get("yetkili", ""),
                    durum
                ), tags=(durum,))
        except Exception as e:
            messagebox.showerror("Hata", f"Listeleme hatası:\n{e}")
    
    def kart_yukle(self):
        secili = self.tree.selection()
        if not secili:
            messagebox.showwarning("Uyarı", "Listeden bir kart seçin")
            return
        
        values = self.tree.item(secili[0], "values")
        firma = values[0]
        
        try:
            kartlar = self.db.cari_kartlari_getir()
            kart = next((k for k in kartlar if k.get("firma_adi") == firma), None)
            
            if not kart:
                messagebox.showerror("Hata", "Kart bulunamadı")
                return
            
            self.duzenlenen_id = kart.get("id")
            self.mod_label.configure(text="DÜZENLEME MODU", fg_color="#B45309")
            
            self.kart_tipi.set(kart.get("kart_tipi", ""))
            self.cari_kod.delete(0, "end")
            self.cari_kod.insert(0, kart.get("cari_kod", ""))
            self.firma_adi.delete(0, "end")
            self.firma_adi.insert(0, kart.get("firma_adi", ""))
            self.unvan.delete(0, "end")
            self.unvan.insert(0, kart.get("unvan", ""))
            self.yetkili.delete(0, "end")
            self.yetkili.insert(0, kart.get("yetkili", ""))
            self.telefon.delete(0, "end")
            self.telefon.insert(0, kart.get("telefon", ""))
            self.eposta.delete(0, "end")
            self.eposta.insert(0, kart.get("eposta", ""))
            self.vergi_no.delete(0, "end")
            self.vergi_no.insert(0, kart.get("vergi_no", ""))
            self.vergi_dairesi.delete(0, "end")
            self.vergi_dairesi.insert(0, kart.get("vergi_dairesi", ""))
            self.adres.delete("0.0", "end")
            self.adres.insert("0.0", kart.get("adres", ""))
            self.iban.delete(0, "end")
            self.iban.insert(0, kart.get("iban", ""))
            self.durum.set(kart.get("durum", "AKTIF"))
            self.notlar.delete("0.0", "end")
            self.notlar.insert("0.0", kart.get("notlar", ""))
            
        except Exception as e:
            messagebox.showerror("Hata", f"Yükleme hatası:\n{e}")
    
    def kart_sil(self):
        secili = self.tree.selection()
        if not secili:
            messagebox.showwarning("Uyarı", "Listeden bir kart seçin")
            return
        
        values = self.tree.item(secili[0], "values")
        firma = values[0]
        
        if not messagebox.askyesno("Onay", f"{firma} kartını silmek istiyor musunuz?"):
            return
        
        try:
            kartlar = self.db.cari_kartlari_getir()
            kart = next((k for k in kartlar if k.get("firma_adi") == firma), None)
            if kart:
                self.db.supabase.table("cari_kartlar").delete().eq("id", kart.get("id")).execute()
                messagebox.showinfo("Başarılı", "Kart silindi")
                self.listele()
        except Exception as e:
            messagebox.showerror("Hata", f"Silme hatası:\n{e}")
    
    def kaydet(self):
        if not self.firma_adi.get().strip():
            messagebox.showwarning("Uyarı", "Firma adı zorunludur")
            return
        
        kart = {
            "kart_tipi": self.kart_tipi.get(),
            "cari_kod": self.cari_kod.get().strip(),
            "firma_adi": self.firma_adi.get().strip(),
            "unvan": self.unvan.get().strip(),
            "yetkili": self.yetkili.get().strip(),
            "telefon": self.telefon.get().strip(),
            "eposta": self.eposta.get().strip(),
            "vergi_no": self.vergi_no.get().strip(),
            "vergi_dairesi": self.vergi_dairesi.get().strip(),
            "adres": self.adres.get("0.0", "end").strip(),
            "iban": self.iban.get().strip(),
            "durum": self.durum.get(),
            "notlar": self.notlar.get("0.0", "end").strip(),
        }
        
        try:
            if self.duzenlenen_id:
                self.db.supabase.table("cari_kartlar").update(kart).eq("id", self.duzenlenen_id).execute()
                messagebox.showinfo("Başarılı", "Kart güncellendi")
            else:
                self.db.supabase.table("cari_kartlar").insert(kart).execute()
                messagebox.showinfo("Başarılı", "Kart kaydedildi")
            
            self.temizle()
            self.listele()
        except Exception as e:
            messagebox.showerror("Hata", f"Kayıt hatası:\n{e}")
    
    def temizle(self):
        self.duzenlenen_id = None
        self.mod_label.configure(text="YENİ KAYIT", fg_color="#1E40AF")
        self.kart_tipi.set("CARI")
        self.cari_kod.delete(0, "end")
        self.firma_adi.delete(0, "end")
        self.unvan.delete(0, "end")
        self.yetkili.delete(0, "end")
        self.telefon.delete(0, "end")
        self.eposta.delete(0, "end")
        self.vergi_no.delete(0, "end")
        self.vergi_dairesi.delete(0, "end")
        self.adres.delete("0.0", "end")
        self.iban.delete(0, "end")
        self.durum.set("AKTIF")
        self.notlar.delete("0.0", "end")
