import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry


class KampYonetimiModul(ctk.CTkFrame):
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
        
        self.personel_map = {}
        self.oda_map = {}
        
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
        self.grid_rowconfigure(0, weight=1)
        
        # ================= ANA PANEL =================
        main_panel = ctk.CTkFrame(self, fg_color="white", corner_radius=14,
                                 border_width=1, border_color="#E2E8F0")
        main_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # HEADER
        header = ctk.CTkFrame(main_panel, fg_color=self.COLOR_PRIMARY, corner_radius=12)
        header.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(header, text="🏕️ KAMP GİRİŞLERİ YÖNETİMİ", text_color="white",
                     font=("Segoe UI", 18, "bold")).pack(pady=6)
        
        # Sekmeler
        self.tabview = ctk.CTkTabview(main_panel, width=1000)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Oda Yönetimi
        self.tab_oda = self.tabview.add("Oda Yönetimi")
        self.setup_oda_tab()
        
        # Tab 2: Personel Yerleşimi
        self.tab_yerlesim = self.tabview.add("Personel Yerleşimi")
        self.setup_yerlesim_tab()
        
        # Tab 3: Sarf Malzemeler
        self.tab_sarf = self.tabview.add("Sarf Malzemeler")
        self.setup_sarf_tab()
        
        # Tab 4: Faaliyetler
        self.tab_faaliyet = self.tabview.add("Faaliyetler")
        self.setup_faaliyet_tab()
    
    def setup_oda_tab(self):
        # Oda Ekleme Formu
        oda_form = ctk.CTkFrame(self.tab_oda, fg_color="#F1F5F9", corner_radius=10)
        oda_form.pack(fill="x", padx=10, pady=10)
        
        row1 = ctk.CTkFrame(oda_form, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(row1, text="Yerleşke:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.yerleske_adi = ctk.CTkComboBox(row1, values=["Yerleşke A", "Yerleşke B", "Yerleşke C", "Yerleşke D"],
                                             width=150, height=35)
        self.yerleske_adi.set("Yerleşke A")
        self.yerleske_adi.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="Koğuş No:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.kogus_no = ctk.CTkEntry(row1, width=100, height=35)
        self.kogus_no.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="Oda No:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.oda_no = ctk.CTkEntry(row1, width=100, height=35)
        self.oda_no.pack(side="left", padx=5)
        
        row2 = ctk.CTkFrame(oda_form, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(row2, text="Kapasite:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.kapasite = ctk.CTkComboBox(row2, values=["5", "6"], width=100, height=35)
        self.kapasite.set("6")
        self.kapasite.pack(side="left", padx=5)
        
        ctk.CTkLabel(row2, text="Firma Tipi:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.firma_tipi = ctk.CTkComboBox(row2, values=["ANA_FIRMA", "TASERON"], width=150, height=35)
        self.firma_tipi.set("ANA_FIRMA")
        self.firma_tipi.pack(side="left", padx=5)
        
        ctk.CTkButton(row2, text="➕ Oda Ekle", fg_color=self.COLOR_SUCCESS,
                      hover_color="#059669", command=self.oda_ekle).pack(side="left", padx=10)
        
        # Oda Listesi
        self.oda_tree = ttk.Treeview(
            self.tab_oda,
            columns=("yerleske", "kogus", "oda", "kapasite", "firma", "durum"),
            show="headings", height=15
        )
        self.oda_tree.heading("yerleske", text="Yerleşke")
        self.oda_tree.heading("kogus", text="Koğuş No")
        self.oda_tree.heading("oda", text="Oda No")
        self.oda_tree.heading("kapasite", text="Kapasite")
        self.oda_tree.heading("firma", text="Firma Tipi")
        self.oda_tree.heading("durum", text="Durum")
        
        self.oda_tree.column("yerleske", width=150, anchor="center")
        self.oda_tree.column("kogus", width=100, anchor="center")
        self.oda_tree.column("oda", width=100, anchor="center")
        self.oda_tree.column("kapasite", width=80, anchor="center")
        self.oda_tree.column("firma", width=120, anchor="center")
        self.oda_tree.column("durum", width=100, anchor="center")
        
        self.oda_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.oda_tree.tag_configure("BOŞ", foreground="#16A34A")
        self.oda_tree.tag_configure("DOLU", foreground="#DC2626")
        
        btn_frame = ctk.CTkFrame(self.tab_oda, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="🔄 Listeyi Yenile", fg_color=self.COLOR_PRIMARY,
                      hover_color=self.COLOR_PRIMARY_HOVER, command=self.oda_listesi_getir).pack(side="left", padx=5)
    
    def setup_yerlesim_tab(self):
        # Personel Yerleşim Formu
        yerlesim_form = ctk.CTkFrame(self.tab_yerlesim, fg_color="#F1F5F9", corner_radius=10)
        yerlesim_form.pack(fill="x", padx=10, pady=10)
        
        row1 = ctk.CTkFrame(yerlesim_form, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(row1, text="Personel:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.yerlesim_personel = ctk.CTkComboBox(row1, values=[], width=200, height=35)
        self.yerlesim_personel.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="Oda:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.yerlesim_oda = ctk.CTkComboBox(row1, values=[], width=200, height=35)
        self.yerlesim_oda.pack(side="left", padx=5)
        
        row2 = ctk.CTkFrame(yerlesim_form, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(row2, text="Giriş Tarihi:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.giris_tarihi = DateEntry(row2, date_pattern="yyyy-mm-dd", font=("Segoe UI", 11))
        self.giris_tarihi.set_date(datetime.now().date())
        self.giris_tarihi.pack(side="left", padx=5)
        
        ctk.CTkLabel(row2, text="Çıkış Tarihi:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.cikis_tarihi = DateEntry(row2, date_pattern="yyyy-mm-dd", font=("Segoe UI", 11))
        self.cikis_tarihi.pack(side="left", padx=5)
        
        ctk.CTkButton(row2, text="➕ Yerleş", fg_color=self.COLOR_SUCCESS,
                      hover_color="#059669", command=self.personel_yerlestir).pack(side="left", padx=10)
        
        # Yerleşim Listesi
        self.yerlesim_tree = ttk.Treeview(
            self.tab_yerlesim,
            columns=("personel", "oda", "giris", "cikis", "durum"),
            show="headings", height=15
        )
        self.yerlesim_tree.heading("personel", text="Personel")
        self.yerlesim_tree.heading("oda", text="Oda")
        self.yerlesim_tree.heading("giris", text="Giriş Tarihi")
        self.yerlesim_tree.heading("cikis", text="Çıkış Tarihi")
        self.yerlesim_tree.heading("durum", text="Durum")
        
        self.yerlesim_tree.column("personel", width=200, anchor="w")
        self.yerlesim_tree.column("oda", width=200, anchor="w")
        self.yerlesim_tree.column("giris", width=120, anchor="center")
        self.yerlesim_tree.column("cikis", width=120, anchor="center")
        self.yerlesim_tree.column("durum", width=100, anchor="center")
        
        self.yerlesim_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.yerlesim_tree.tag_configure("AKTIF", foreground="#16A34A")
        self.yerlesim_tree.tag_configure("PASIF", foreground="#64748B")
        
        btn_frame = ctk.CTkFrame(self.tab_yerlesim, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="🔄 Listeyi Yenile", fg_color=self.COLOR_PRIMARY,
                      hover_color=self.COLOR_PRIMARY_HOVER, command=self.yerlesim_listesi_getir).pack(side="left", padx=5)
    
    def setup_sarf_tab(self):
        # Sarf Malzeme Formu
        sarf_form = ctk.CTkFrame(self.tab_sarf, fg_color="#F1F5F9", corner_radius=10)
        sarf_form.pack(fill="x", padx=10, pady=10)
        
        row1 = ctk.CTkFrame(sarf_form, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(row1, text="Malzeme Adı:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.malzeme_adi = ctk.CTkEntry(row1, width=200, height=35)
        self.malzeme_adi.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="Miktar:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.malzeme_miktar = ctk.CTkEntry(row1, width=100, height=35)
        self.malzeme_miktar.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="Birim:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.malzeme_birim = ctk.CTkComboBox(row1, values=["ADET", "KG", "LT", "PAKET"], width=100, height=35)
        self.malzeme_birim.set("ADET")
        self.malzeme_birim.pack(side="left", padx=5)
        
        row2 = ctk.CTkFrame(sarf_form, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(row2, text="Yerleşke:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.sarf_yerleske = ctk.CTkComboBox(row2, values=["Yerleşke A", "Yerleşke B", "Yerleşke C", "Yerleşke D"],
                                              width=150, height=35)
        self.sarf_yerleske.set("Yerleşke A")
        self.sarf_yerleske.pack(side="left", padx=5)
        
        ctk.CTkLabel(row2, text="Tarih:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.sarf_tarih = DateEntry(row2, date_pattern="yyyy-mm-dd", font=("Segoe UI", 11))
        self.sarf_tarih.set_date(datetime.now().date())
        self.sarf_tarih.pack(side="left", padx=5)
        
        ctk.CTkButton(row2, text="➕ Ekle", fg_color=self.COLOR_SUCCESS,
                      hover_color="#059669", command=self.sarf_malzeme_ekle).pack(side="left", padx=10)
        
        # Sarf Malzeme Listesi
        self.sarf_tree = ttk.Treeview(
            self.tab_sarf,
            columns=("malzeme", "miktar", "birim", "tarih", "yerleske"),
            show="headings", height=15
        )
        self.sarf_tree.heading("malzeme", text="Malzeme Adı")
        self.sarf_tree.heading("miktar", text="Miktar")
        self.sarf_tree.heading("birim", text="Birim")
        self.sarf_tree.heading("tarih", text="Tarih")
        self.sarf_tree.heading("yerleske", text="Yerleşke")
        
        self.sarf_tree.column("malzeme", width=200, anchor="w")
        self.sarf_tree.column("miktar", width=100, anchor="center")
        self.sarf_tree.column("birim", width=80, anchor="center")
        self.sarf_tree.column("tarih", width=120, anchor="center")
        self.sarf_tree.column("yerleske", width=150, anchor="center")
        
        self.sarf_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        btn_frame = ctk.CTkFrame(self.tab_sarf, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="🔄 Listeyi Yenile", fg_color=self.COLOR_PRIMARY,
                      hover_color=self.COLOR_PRIMARY_HOVER, command=self.sarf_listesi_getir).pack(side="left", padx=5)
    
    def setup_faaliyet_tab(self):
        # Faaliyet Formu
        faaliyet_form = ctk.CTkFrame(self.tab_faaliyet, fg_color="#F1F5F9", corner_radius=10)
        faaliyet_form.pack(fill="x", padx=10, pady=10)
        
        row1 = ctk.CTkFrame(faaliyet_form, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(row1, text="Personel:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.faaliyet_personel = ctk.CTkComboBox(row1, values=[], width=200, height=35)
        self.faaliyet_personel.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="Faaliyet Tipi:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.faaliyet_tipi = ctk.CTkComboBox(row1, values=["TEMİZLİK", "YEMEK", "GÜVENLİK", "BAKIM", "DİĞER"],
                                               width=150, height=35)
        self.faaliyet_tipi.set("TEMİZLİK")
        self.faaliyet_tipi.pack(side="left", padx=5)
        
        row2 = ctk.CTkFrame(faaliyet_form, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(row2, text="Tarih:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.faaliyet_tarih = DateEntry(row2, date_pattern="yyyy-mm-dd", font=("Segoe UI", 11))
        self.faaliyet_tarih.set_date(datetime.now().date())
        self.faaliyet_tarih.pack(side="left", padx=5)
        
        ctk.CTkLabel(row2, text="Yerleşke:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.faaliyet_yerleske = ctk.CTkComboBox(row2, values=["Yerleşke A", "Yerleşke B", "Yerleşke C", "Yerleşke D"],
                                                  width=150, height=35)
        self.faaliyet_yerleske.set("Yerleşke A")
        self.faaliyet_yerleske.pack(side="left", padx=5)
        
        ctk.CTkButton(row2, text="➕ Ekle", fg_color=self.COLOR_SUCCESS,
                      hover_color="#059669", command=self.faaliyet_ekle).pack(side="left", padx=10)
        
        row3 = ctk.CTkFrame(faaliyet_form, fg_color="transparent")
        row3.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(row3, text="Açıklama:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.faaliyet_aciklama = ctk.CTkEntry(row3, height=35)
        self.faaliyet_aciklama.pack(side="left", fill="x", expand=True, padx=5)
        
        # Faaliyet Listesi
        self.faaliyet_tree = ttk.Treeview(
            self.tab_faaliyet,
            columns=("personel", "tip", "tarih", "yerleske", "aciklama"),
            show="headings", height=12
        )
        self.faaliyet_tree.heading("personel", text="Personel")
        self.faaliyet_tree.heading("tip", text="Faaliyet Tipi")
        self.faaliyet_tree.heading("tarih", text="Tarih")
        self.faaliyet_tree.heading("yerleske", text="Yerleşke")
        self.faaliyet_tree.heading("aciklama", text="Açıklama")
        
        self.faaliyet_tree.column("personel", width=200, anchor="w")
        self.faaliyet_tree.column("tip", width=120, anchor="center")
        self.faaliyet_tree.column("tarih", width=120, anchor="center")
        self.faaliyet_tree.column("yerleske", width=150, anchor="center")
        self.faaliyet_tree.column("aciklama", width=250, anchor="w")
        
        self.faaliyet_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        btn_frame = ctk.CTkFrame(self.tab_faaliyet, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="🔄 Listeyi Yenile", fg_color=self.COLOR_PRIMARY,
                      hover_color=self.COLOR_PRIMARY_HOVER, command=self.faaliyet_listesi_getir).pack(side="left", padx=5)
    
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
            
            self.yerlesim_personel.configure(values=secenekler)
            self.faaliyet_personel.configure(values=secenekler)
        except Exception as e:
            print("Personel listesi yenileme hatası:", e)
    
    def oda_ekle(self):
        if not self.kogus_no.get().strip() or not self.oda_no.get().strip():
            messagebox.showwarning("Uyarı", "Koğuş ve oda numarası zorunludur")
            return
        
        try:
            kapasite = int(self.kapasite.get())
        except ValueError:
            messagebox.showwarning("Uyarı", "Kapasite sayısal olmalı")
            return
        
        oda = {
            "yerleske_adi": self.yerleske_adi.get(),
            "kogus_no": self.kogus_no.get().strip(),
            "oda_no": self.oda_no.get().strip(),
            "kapasite": kapasite,
            "firma_tipi": self.firma_tipi.get(),
            "durum": "BOŞ",
        }
        
        basarili, sonuc = self.db.kamp_odasi_kaydet(oda)
        if basarili:
            messagebox.showinfo("Başarılı", "Oda kaydedildi")
            self.kogus_no.delete(0, "end")
            self.oda_no.delete(0, "end")
            self.oda_listesi_getir()
            self.oda_listesini_yenile()
        else:
            messagebox.showerror("Hata", f"Kayıt hatası:\n{sonuc}")
    
    def oda_listesi_getir(self):
        for item in self.oda_tree.get_children():
            self.oda_tree.delete(item)
        
        odalar = self.db.kamp_odalari_getir()
        
        for o in odalar:
            durum = o.get("durum", "BOŞ")
            self.oda_tree.insert("", "end", values=(
                o.get("yerleske_adi", ""),
                o.get("kogus_no", ""),
                o.get("oda_no", ""),
                o.get("kapasite", 0),
                o.get("firma_tipi", ""),
                durum
            ), tags=(durum,))
    
    def oda_listesini_yenile(self):
        try:
            odalar = self.db.kamp_odalari_getir()
            secenekler = []
            self.oda_map = {}
            for o in odalar:
                oda_text = f"{o.get('yerleske_adi')} - Koğuş {o.get('kogus_no')} - Oda {o.get('oda_no')}"
                secenekler.append(oda_text)
                self.oda_map[oda_text] = o
            
            self.yerlesim_oda.configure(values=secenekler)
        except Exception as e:
            print("Oda listesi yenileme hatası:", e)
    
    def personel_yerlestir(self):
        personel_adi = self.yerlesim_personel.get()
        oda_text = self.yerlesim_oda.get()
        
        if not personel_adi or not oda_text:
            messagebox.showwarning("Uyarı", "Personel ve oda seçin")
            return
        
        personel = self.personel_map.get(personel_adi)
        oda = self.oda_map.get(oda_text)
        
        if not personel or not oda:
            messagebox.showerror("Hata", "Personel veya oda bulunamadı")
            return
        
        kayit = {
            "personel_id": personel.get("id"),
            "oda_id": oda.get("id"),
            "giris_tarihi": self.giris_tarihi.get(),
            "cikis_tarihi": self.cikis_tarihi.get() if self.cikis_tarihi.get() else None,
            "durum": "AKTIF",
        }
        
        basarili, sonuc = self.db.kamp_kayit_kaydet(kayit)
        if basarili:
            messagebox.showinfo("Başarılı", "Personel yerleştirildi")
            self.yerlesim_listesi_getir()
            self.oda_listesi_getir()
        else:
            messagebox.showerror("Hata", f"Kayıt hatası:\n{sonuc}")
    
    def yerlesim_listesi_getir(self):
        for item in self.yerlesim_tree.get_children():
            self.yerlesim_tree.delete(item)
        
        kayitlar = self.db.kamp_kayitlari_getir()
        
        for k in kayitlar:
            personel_id = k.get("personel_id")
            oda_id = k.get("oda_id")
            
            personel_adi = ""
            for ad, p in self.personel_map.items():
                if p.get("id") == personel_id:
                    personel_adi = ad
                    break
            
            odalar = self.db.kamp_odalari_getir()
            oda = next((o for o in odalar if o.get("id") == oda_id), None)
            oda_text = ""
            if oda:
                oda_text = f"{oda.get('yerleske_adi')} - Koğuş {oda.get('kogus_no')} - Oda {oda.get('oda_no')}"
            
            durum = k.get("durum", "AKTIF")
            self.yerlesim_tree.insert("", "end", values=(
                personel_adi,
                oda_text,
                k.get("giris_tarihi", ""),
                k.get("cikis_tarihi", "-"),
                durum
            ), tags=(durum,))
    
    def sarf_malzeme_ekle(self):
        if not self.malzeme_adi.get().strip():
            messagebox.showwarning("Uyarı", "Malzeme adı zorunludur")
            return
        
        try:
            miktar = float(self.malzeme_miktar.get())
            if miktar <= 0:
                messagebox.showwarning("Uyarı", "Miktar 0'dan büyük olmalı")
                return
        except ValueError:
            messagebox.showwarning("Uyarı", "Miktar sayısal olmalı")
            return
        
        malzeme = {
            "malzeme_adi": self.malzeme_adi.get().strip(),
            "miktar": miktar,
            "birim": self.malzeme_birim.get(),
            "giris_tarihi": self.sarf_tarih.get(),
            "yerleske_adi": self.sarf_yerleske.get(),
            "aciklama": "",
        }
        
        basarili, sonuc = self.db.kamp_sarf_malzeme_kaydet(malzeme)
        if basarili:
            messagebox.showinfo("Başarılı", "Sarf malzemesi kaydedildi")
            self.malzeme_adi.delete(0, "end")
            self.malzeme_miktar.delete(0, "end")
            self.sarf_listesi_getir()
        else:
            messagebox.showerror("Hata", f"Kayıt hatası:\n{sonuc}")
    
    def sarf_listesi_getir(self):
        for item in self.sarf_tree.get_children():
            self.sarf_tree.delete(item)
        
        malzemeler = self.db.kamp_sarf_malzemeleri_getir()
        
        for m in malzemeler:
            self.sarf_tree.insert("", "end", values=(
                m.get("malzeme_adi", ""),
                m.get("miktar", 0),
                m.get("birim", ""),
                m.get("giris_tarihi", ""),
                m.get("yerleske_adi", ""),
            ))
    
    def faaliyet_ekle(self):
        personel_adi = self.faaliyet_personel.get()
        if not personel_adi:
            messagebox.showwarning("Uyarı", "Personel seçin")
            return
        
        personel = self.personel_map.get(personel_adi)
        if not personel:
            messagebox.showerror("Hata", "Personel bulunamadı")
            return
        
        faaliyet = {
            "personel_id": personel.get("id"),
            "tarih": self.faaliyet_tarih.get(),
            "faaliyet_tipi": self.faaliyet_tipi.get(),
            "aciklama": self.faaliyet_aciklama.get(),
            "yerleske_adi": self.faaliyet_yerleske.get(),
        }
        
        basarili, sonuc = self.db.kamp_faaliyet_kaydet(faaliyet)
        if basarili:
            messagebox.showinfo("Başarılı", "Faaliyet kaydedildi")
            self.faaliyet_aciklama.delete(0, "end")
            self.faaliyet_listesi_getir()
        else:
            messagebox.showerror("Hata", f"Kayıt hatası:\n{sonuc}")
    
    def faaliyet_listesi_getir(self):
        for item in self.faaliyet_tree.get_children():
            self.faaliyet_tree.delete(item)
        
        faaliyetler = self.db.kamp_faaliyetleri_getir()
        
        for f in faaliyetler:
            personel_id = f.get("personel_id")
            personel_adi = ""
            for ad, p in self.personel_map.items():
                if p.get("id") == personel_id:
                    personel_adi = ad
                    break
            
            self.faaliyet_tree.insert("", "end", values=(
                personel_adi,
                f.get("faaliyet_tipi", ""),
                f.get("tarih", ""),
                f.get("yerleske_adi", ""),
                f.get("aciklama", ""),
            ))
    
    def listele(self):
        self.oda_listesi_getir()
        self.oda_listesini_yenile()
        self.yerlesim_listesi_getir()
        self.sarf_listesi_getir()
        self.faaliyet_listesi_getir()
