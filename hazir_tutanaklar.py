import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
from datetime import datetime
from tkcalendar import DateEntry


class HazirTutanaklarModul(ctk.CTkFrame):
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
        self.evrak_yolu = None
        
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
        
        ctk.CTkLabel(header, text="📄 HAZIR TUTANAKLAR", text_color="white",
                     font=("Segoe UI", 18, "bold")).pack(pady=6)
        
        form = ctk.CTkScrollableFrame(self.left, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=15, pady=10)
        
        fnt_label = ("Segoe UI", 12, "bold")
        fnt_input = ("Segoe UI", 12)
        
        # Tutanak Tipi
        ctk.CTkLabel(form, text="📋 Tutanak Tipi", font=fnt_label).pack(anchor="w")
        self.tutanak_tipi = ctk.CTkComboBox(form, 
                                           values=["TAHSİS TUTANAĞI", "TESLİM TUTANAĞI", "SEVK TUTANAĞI"],
                                           height=35, font=fnt_input)
        self.tutanak_tipi.set("TAHSİS TUTANAĞI")
        self.tutanak_tipi.pack(fill="x", pady=(0, 10))
        
        # Tarih
        ctk.CTkLabel(form, text="📅 Tarih", font=fnt_label).pack(anchor="w")
        self.tarih = DateEntry(form, date_pattern="yyyy-mm-dd", font=fnt_input)
        self.tarih.set_date(datetime.now().date())
        self.tarih.pack(fill="x", pady=(0, 10))
        
        # Personel
        ctk.CTkLabel(form, text="👤 Personel", font=fnt_label).pack(anchor="w")
        self.personel = ctk.CTkComboBox(form, values=[], height=35, font=fnt_input)
        self.personel.pack(fill="x", pady=(0, 10))
        
        # İçerik
        ctk.CTkLabel(form, text="📝 İçerik", font=fnt_label).pack(anchor="w")
        self.icerik = ctk.CTkTextbox(form, height=150, font=fnt_input)
        self.icerik.pack(fill="x", pady=(0, 10))
        
        # Evrak Yükleme
        ctk.CTkLabel(form, text="📎 İmzalı Evrak", font=fnt_label).pack(anchor="w")
        evrak_frame = ctk.CTkFrame(form, fg_color="transparent")
        evrak_frame.pack(fill="x", pady=(0, 10))
        
        self.evrak_btn = ctk.CTkButton(evrak_frame, text="📎 Evrak Yükle", fg_color=self.COLOR_PRIMARY,
                                       hover_color=self.COLOR_PRIMARY_HOVER, command=self.evrak_yukle)
        self.evrak_btn.pack(side="left", padx=5)
        
        self.evrak_durum_label = ctk.CTkLabel(evrak_frame, text="Yüklenmedi", font=("Segoe UI", 11))
        self.evrak_durum_label.pack(side="left", padx=5)
        
        # Durum
        ctk.CTkLabel(form, text="✅ Durum", font=fnt_label).pack(anchor="w")
        self.durum = ctk.CTkComboBox(form, values=["TASLAK", "ONAYLANDI", "İPTAL"],
                                    height=35, font=fnt_input)
        self.durum.set("TASLAK")
        self.durum.pack(fill="x", pady=(0, 10))
        
        # Kaydet Butonu
        ctk.CTkButton(form, text="💾 Tutanak Kaydet", fg_color=self.COLOR_SUCCESS,
                      hover_color="#059669", height=40, font=("Segoe UI", 13, "bold"),
                      command=self.kaydet).pack(fill="x", pady=10)
        
        # ================= SAĞ PANEL (LİSTE) =================
        self.right = ctk.CTkFrame(self, fg_color="white", corner_radius=14,
                                  border_width=1, border_color="#E2E8F0")
        self.right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        list_header = ctk.CTkFrame(self.right, fg_color="transparent")
        list_header.pack(fill="x", padx=12, pady=(12, 0))
        
        ctk.CTkLabel(list_header, text="Tutanak Kayıtları", font=("Segoe UI", 17, "bold"),
                     text_color=self.COLOR_TEXT).pack(side="left")
        
        # Filtre
        filter_frame = ctk.CTkFrame(self.right, fg_color="#F1F5F9", corner_radius=10)
        filter_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(filter_frame, text="🔎").pack(side="left", padx=8)
        self.filter_tip = ctk.CTkComboBox(filter_frame, values=["Tümü", "TAHSİS TUTANAĞI", "TESLİM TUTANAĞI", "SEVK TUTANAĞI"],
                                          width=200, height=35)
        self.filter_tip.set("Tümü")
        self.filter_tip.pack(side="left", padx=5)
        self.filter_tip.bind("<<ComboboxSelected>>", lambda e: self.listele())
        
        # Tutanak Listesi
        self.tutanak_tree = ttk.Treeview(
            self.right,
            columns=("tip", "tarih", "personel", "durum"),
            show="headings", height=18
        )
        self.tutanak_tree.heading("tip", text="Tutanak Tipi")
        self.tutanak_tree.heading("tarih", text="Tarih")
        self.tutanak_tree.heading("personel", text="Personel")
        self.tutanak_tree.heading("durum", text="Durum")
        
        self.tutanak_tree.column("tip", width=180, anchor="center")
        self.tutanak_tree.column("tarih", width=120, anchor="center")
        self.tutanak_tree.column("personel", width=200, anchor="w")
        self.tutanak_tree.column("durum", width=120, anchor="center")
        
        self.tutanak_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.tutanak_tree.tag_configure("TASLAK", foreground="#F59E0B")
        self.tutanak_tree.tag_configure("ONAYLANDI", foreground="#16A34A")
        self.tutanak_tree.tag_configure("İPTAL", foreground="#DC2626")
        
        # Butonlar
        btn_frame = ctk.CTkFrame(self.right, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="🔄 Listeyi Yenile", fg_color=self.COLOR_PRIMARY,
                      hover_color=self.COLOR_PRIMARY_HOVER, command=self.listele).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🧹 Temizle", fg_color=self.COLOR_MUTED,
                      hover_color="#475569", command=self.temizle).pack(side="left", padx=5)
    
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
            
            self.personel.configure(values=secenekler)
        except Exception as e:
            print("Personel listesi yenileme hatası:", e)
    
    def evrak_yukle(self):
        dosya = filedialog.askopenfilename(
            title="İmzalı Evrak Seç",
            filetypes=[("PDF", "*.pdf"), ("Resim", "*.png;*.jpg;*.jpeg"), ("Tüm Dosyalar", "*.*")]
        )
        
        if not dosya:
            return
        
        try:
            # Evrak klasörü oluştur
            proje_klasoru = os.path.dirname(os.path.abspath(__file__))
            hedef_klasor = os.path.join(proje_klasoru, "tutanak_evraklari")
            os.makedirs(hedef_klasor, exist_ok=True)
            
            # Dosya kopyala
            uzanti = os.path.splitext(dosya)[1]
            tarih_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            hedef_yol = os.path.join(hedef_klasor, f"tutanak_{tarih_str}{uzanti}")
            
            shutil.copy2(dosya, hedef_yol)
            self.evrak_yolu = hedef_yol
            
            self.evrak_durum_label.configure(text="Yüklendi ✓", text_color="#16A34A")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Evrak yüklenemedi:\n{e}")
    
    def kaydet(self):
        personel_adi = self.personel.get()
        if not personel_adi:
            messagebox.showwarning("Uyarı", "Personel seçin")
            return
        
        personel = self.personel_map.get(personel_adi)
        if not personel:
            messagebox.showerror("Hata", "Personel bulunamadı")
            return
        
        if not self.icerik.get("0.0", "end").strip():
            messagebox.showwarning("Uyarı", "İçerik boş olamaz")
            return
        
        tutanak = {
            "tutanak_tipi": self.tutanak_tipi.get(),
            "tarih": self.tarih.get(),
            "personel_id": personel.get("id"),
            "icerik": self.icerik.get("0.0", "end").strip(),
            "evrak_url": self.evrak_yolu,
            "durum": self.durum.get(),
        }
        
        basarili, sonuc = self.db.hazir_tutanak_kaydet(tutanak)
        if basarili:
            messagebox.showinfo("Başarılı", "Tutanak kaydedildi")
            self.temizle()
            self.listele()
        else:
            messagebox.showerror("Hata", f"Kayıt hatası:\n{sonuc}")
    
    def listele(self):
        for item in self.tutanak_tree.get_children():
            self.tutanak_tree.delete(item)
        
        tip = self.filter_tip.get()
        tip_param = tip if tip != "Tümü" else None
        
        tutanaklar = self.db.hazir_tutanaklar_getir(tip=tip_param)
        
        for t in tutanaklar:
            personel_id = t.get("personel_id")
            personel_adi = ""
            for ad, p in self.personel_map.items():
                if p.get("id") == personel_id:
                    personel_adi = ad
                    break
            
            durum = t.get("durum", "TASLAK")
            self.tutanak_tree.insert("", "end", values=(
                t.get("tutanak_tipi", ""),
                t.get("tarih", ""),
                personel_adi,
                durum
            ), tags=(durum,))
    
    def temizle(self):
        self.tutanak_tipi.set("TAHSİS TUTANAĞI")
        self.tarih.set_date(datetime.now().date())
        self.personel.set("")
        self.icerik.delete("0.0", "end")
        self.evrak_yolu = None
        self.evrak_durum_label.configure(text="Yüklenmedi", text_color="#64748B")
        self.durum.set("TASLAK")
