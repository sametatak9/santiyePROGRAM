import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
from datetime import datetime
from tkcalendar import DateEntry


class SahaFaaliyetiModul(ctk.CTkFrame):
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
        self.foto_sayaci = 0
        
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
        
        ctk.CTkLabel(header, text="🏗️ GÜNLÜK SAHA FAALİYETİ", text_color="white",
                     font=("Segoe UI", 18, "bold")).pack(pady=6)
        
        form = ctk.CTkScrollableFrame(self.left, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=15, pady=10)
        
        fnt_label = ("Segoe UI", 12, "bold")
        fnt_input = ("Segoe UI", 12)
        
        # Tarih
        ctk.CTkLabel(form, text="📅 Tarih", font=fnt_label).pack(anchor="w")
        self.tarih = DateEntry(form, date_pattern="yyyy-mm-dd", font=fnt_input)
        self.tarih.set_date(datetime.now().date())
        self.tarih.pack(fill="x", pady=(0, 10))
        
        # Personel
        ctk.CTkLabel(form, text="👤 Personel", font=fnt_label).pack(anchor="w")
        self.personel = ctk.CTkComboBox(form, values=[], height=35, font=fnt_input)
        self.personel.pack(fill="x", pady=(0, 10))
        
        # İş Niteliği
        ctk.CTkLabel(form, text="🔧 İş Niteliği", font=fnt_label).pack(anchor="w")
        self.is_nitelig = ctk.CTkComboBox(form, 
                                          values=["Anahtarcı", "Usta", "Tesisatçı", "Drenajcı", "Düz İşçi", "Temizlikçi", "Demirci", "Marangoz", "Elektrikçi"],
                                          height=35, font=fnt_input)
        self.is_nitelig.pack(fill="x", pady=(0, 10))
        
        # Parsel
        ctk.CTkLabel(form, text="📍 Parsel", font=fnt_label).pack(anchor="w")
        self.parsel = ctk.CTkComboBox(form, values=["Parsel A", "Parsel B", "Parsel C"], height=35, font=fnt_input)
        self.parsel.pack(fill="x", pady=(0, 10))
        
        # Blok
        ctk.CTkLabel(form, text="🏢 Blok", font=fnt_label).pack(anchor="w")
        self.blok = ctk.CTkComboBox(form, values=[f"Blok {i}" for i in range(1, 11)], height=35, font=fnt_input)
        self.blok.pack(fill="x", pady=(0, 10))
        
        # Açıklama
        ctk.CTkLabel(form, text="📝 Açıklama", font=fnt_label).pack(anchor="w")
        self.aciklama = ctk.CTkTextbox(form, height=80, font=fnt_input)
        self.aciklama.pack(fill="x", pady=(0, 10))
        
        # Fotoğraf Yükleme
        ctk.CTkLabel(form, text="📷 Fotoğraflar (Max 5)", font=fnt_label).pack(anchor="w")
        foto_frame = ctk.CTkFrame(form, fg_color="transparent")
        foto_frame.pack(fill="x", pady=(0, 10))
        
        self.foto_btn = ctk.CTkButton(foto_frame, text="📷 Fotoğraf Ekle", fg_color=self.COLOR_PRIMARY,
                                       hover_color=self.COLOR_PRIMARY_HOVER, command=self.foto_ekle)
        self.foto_btn.pack(side="left", padx=5)
        
        self.foto_sayisi_label = ctk.CTkLabel(foto_frame, text="0/5", font=("Segoe UI", 11, "bold"))
        self.foto_sayisi_label.pack(side="left", padx=5)
        
        self.foto_listesi = []
        
        # Kaydet Butonu
        ctk.CTkButton(form, text="💾 Faaliyeti Kaydet", fg_color=self.COLOR_SUCCESS,
                      hover_color="#059669", height=40, font=("Segoe UI", 13, "bold"),
                      command=self.kaydet).pack(fill="x", pady=10)
        
        # ================= SAĞ PANEL (LİSTE + RAPOR) =================
        self.right = ctk.CTkFrame(self, fg_color="white", corner_radius=14,
                                  border_width=1, border_color="#E2E8F0")
        self.right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Sekmeler
        self.tabview = ctk.CTkTabview(self.right, width=800)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Faaliyet Listesi
        self.tab_liste = self.tabview.add("Faaliyet Listesi")
        self.setup_liste_tab()
        
        # Tab 2: Aylık Rapor
        self.tab_rapor = self.tabview.add("Aylık Rapor")
        self.setup_rapor_tab()
    
    def setup_liste_tab(self):
        # Filtreler
        filter_frame = ctk.CTkFrame(self.tab_liste, fg_color="#F1F5F9", corner_radius=10)
        filter_frame.pack(fill="x", padx=10, pady=10)
        
        row1 = ctk.CTkFrame(filter_frame, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(row1, text="Tarih:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.filter_tarih = DateEntry(row1, date_pattern="yyyy-mm-dd", font=("Segoe UI", 11))
        self.filter_tarih.set_date(datetime.now().date())
        self.filter_tarih.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="Parsel:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.filter_parsel = ctk.CTkComboBox(row1, values=["Tümü", "Parsel A", "Parsel B", "Parsel C"],
                                               width=120, height=35)
        self.filter_parsel.set("Tümü")
        self.filter_parsel.pack(side="left", padx=5)
        
        ctk.CTkButton(row1, text="🔍 Filtrele", fg_color=self.COLOR_PRIMARY,
                      hover_color=self.COLOR_PRIMARY_HOVER, command=self.filtrele).pack(side="left", padx=10)
        
        # Faaliyet Listesi
        self.faaliyet_tree = ttk.Treeview(
            self.tab_liste,
            columns=("tarih", "personel", "is_nitelig", "parsel", "blok", "aciklama"),
            show="headings", height=15
        )
        self.faaliyet_tree.heading("tarih", text="Tarih")
        self.faaliyet_tree.heading("personel", text="Personel")
        self.faaliyet_tree.heading("is_nitelig", text="İş Niteliği")
        self.faaliyet_tree.heading("parsel", text="Parsel")
        self.faaliyet_tree.heading("blok", text="Blok")
        self.faaliyet_tree.heading("aciklama", text="Açıklama")
        
        self.faaliyet_tree.column("tarih", width=120, anchor="center")
        self.faaliyet_tree.column("personel", width=180, anchor="w")
        self.faaliyet_tree.column("is_nitelig", width=120, anchor="center")
        self.faaliyet_tree.column("parsel", width=100, anchor="center")
        self.faaliyet_tree.column("blok", width=80, anchor="center")
        self.faaliyet_tree.column("aciklama", width=250, anchor="w")
        
        self.faaliyet_tree.pack(fill="both", expand=True, padx=10, pady=5)
    
    def setup_rapor_tab(self):
        # Rapor Filtreleri
        rapor_filter = ctk.CTkFrame(self.tab_rapor, fg_color="#F1F5F9", corner_radius=10)
        rapor_filter.pack(fill="x", padx=10, pady=10)
        
        row1 = ctk.CTkFrame(rapor_filter, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(row1, text="Yıl:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.rapor_yil = ctk.CTkComboBox(row1, values=[str(y) for y in range(2024, 2030)],
                                          width=100, height=35)
        self.rapor_yil.set(str(datetime.now().year))
        self.rapor_yil.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="Ay:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        self.rapor_ay = ctk.CTkComboBox(row1, values=[str(a) for a in range(1, 13)],
                                        width=100, height=35)
        self.rapor_ay.set(str(datetime.now().month))
        self.rapor_ay.pack(side="left", padx=5)
        
        ctk.CTkButton(row1, text="📊 Rapor Oluştur", fg_color=self.COLOR_SUCCESS,
                      hover_color="#059669", command=self.rapor_olustur).pack(side="left", padx=10)
        
        # Rapor Görüntüleme
        self.rapor_text = ctk.CTkTextbox(self.tab_rapor, height=400, font=("Consolas", 10))
        self.rapor_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.rapor_text.insert("0.0", "Rapor oluşturmak için yıl ve ay seçip 'Rapor Oluştur' butonuna tıklayın.")
        self.rapor_text.configure(state="disabled")
    
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
    
    def foto_ekle(self):
        if self.foto_sayaci >= 5:
            messagebox.showwarning("Uyarı", "Maksimum 5 fotoğraf yükleyebilirsiniz")
            return
        
        dosya = filedialog.askopenfilename(
            title="Fotoğraf Seç",
            filetypes=[("Resim", "*.png;*.jpg;*.jpeg"), ("Tüm Dosyalar", "*.*")]
        )
        
        if not dosya:
            return
        
        try:
            # Fotoğraf klasörü oluştur
            proje_klasoru = os.path.dirname(os.path.abspath(__file__))
            hedef_klasor = os.path.join(proje_klasoru, "saha_fotograflari")
            os.makedirs(hedef_klasor, exist_ok=True)
            
            # Dosya kopyala
            uzanti = os.path.splitext(dosya)[1]
            tarih_str = datetime.now().strftime("%Y%m%d")
            hedef_yol = os.path.join(hedef_klasor, f"saha_{tarih_str}_{self.foto_sayaci + 1}{uzanti}")
            
            shutil.copy2(dosya, hedef_yol)
            self.foto_listesi.append(hedef_yol)
            self.foto_sayaci += 1
            
            self.foto_sayisi_label.configure(text=f"{self.foto_sayaci}/5")
            
            if self.foto_sayaci >= 5:
                self.foto_btn.configure(state="disabled")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Fotoğraf yüklenemedi:\n{e}")
    
    def kaydet(self):
        personel_adi = self.personel.get()
        if not personel_adi:
            messagebox.showwarning("Uyarı", "Personel seçin")
            return
        
        personel = self.personel_map.get(personel_adi)
        if not personel:
            messagebox.showerror("Hata", "Personel bulunamadı")
            return
        
        faaliyet = {
            "personel_id": personel.get("id"),
            "tarih": self.tarih.get(),
            "is_niteliği": self.is_nitelig.get(),
            "parsel": self.parsel.get(),
            "blok": self.blok.get(),
            "aciklama": self.aciklama.get("0.0", "end").strip(),
            "foto_url": ",".join(self.foto_listesi) if self.foto_listesi else None,
        }
        
        basarili, sonuc = self.db.saha_faaliyeti_kaydet(faaliyet)
        if basarili:
            messagebox.showinfo("Başarılı", "Saha faaliyeti kaydedildi")
            self.temizle()
            self.listele()
        else:
            messagebox.showerror("Hata", f"Kayıt hatası:\n{sonuc}")
    
    def listele(self):
        for item in self.faaliyet_tree.get_children():
            self.faaliyet_tree.delete(item)
        
        faaliyetler = self.db.saha_faaliyetleri_getir()
        
        for f in faaliyetler:
            personel_id = f.get("personel_id")
            personel_adi = ""
            for ad, p in self.personel_map.items():
                if p.get("id") == personel_id:
                    personel_adi = ad
                    break
            
            self.faaliyet_tree.insert("", "end", values=(
                f.get("tarih", ""),
                personel_adi,
                f.get("is_niteliği", ""),
                f.get("parsel", ""),
                f.get("blok", ""),
                f.get("aciklama", ""),
            ))
    
    def filtrele(self):
        for item in self.faaliyet_tree.get_children():
            self.faaliyet_tree.delete(item)
        
        tarih = self.filter_tarih.get()
        parsel = self.filter_parsel.get()
        
        faaliyetler = self.db.saha_faaliyetleri_getir(tarih=tarih, parsel=parsel if parsel != "Tümü" else None)
        
        for f in faaliyetler:
            personel_id = f.get("personel_id")
            personel_adi = ""
            for ad, p in self.personel_map.items():
                if p.get("id") == personel_id:
                    personel_adi = ad
                    break
            
            self.faaliyet_tree.insert("", "end", values=(
                f.get("tarih", ""),
                personel_adi,
                f.get("is_niteliği", ""),
                f.get("parsel", ""),
                f.get("blok", ""),
                f.get("aciklama", ""),
            ))
    
    def rapor_olustur(self):
        try:
            yil = int(self.rapor_yil.get())
            ay = int(self.rapor_ay.get())
            
            rapor = self.db.saha_aylik_raporu(yil, ay)
            
            if not rapor:
                messagebox.showwarning("Uyarı", "Rapor oluşturulamadı")
                return
            
            # Rapor metni oluştur
            rapor_metni = f"KIBRITCI - GÜNLÜK SAHA FAALİYET RAPORU\n"
            rapor_metni += "=" * 60 + "\n\n"
            rapor_metni += f"Dönem: {yil} - {ay:02d}\n"
            rapor_metni += f"Tarih Aralığı: {rapor['baslangic_tarih']} - {rapor['bitis_tarih']}\n"
            rapor_metni += f"Toplam Kayıt: {len(rapor['faaliyetler'])}\n\n"
            rapor_metni += "-" * 60 + "\n\n"
            
            # Tarihe göre grupla
            tarih_gruplari = {}
            for f in rapor['faaliyetler']:
                tarih = f.get("tarih", "")
                if tarih not in tarih_gruplari:
                    tarih_gruplari[tarih] = []
                tarih_gruplari[tarih].append(f)
            
            for tarih in sorted(tarih_gruplari.keys(), reverse=True):
                rapor_metni += f"TARİH: {tarih}\n"
                rapor_metni += "-" * 40 + "\n"
                
                for f in tarih_gruplari[tarih]:
                    personel_id = f.get("personel_id")
                    personel_adi = ""
                    for ad, p in self.personel_map.items():
                        if p.get("id") == personel_id:
                            personel_adi = ad
                            break
                    
                    rapor_metni += f"  Personel: {personel_adi}\n"
                    rapor_metni += f"  İş Niteliği: {f.get('is_niteliği', '')}\n"
                    rapor_metni += f"  Lokasyon: {f.get('parsel', '')} - {f.get('blok', '')}\n"
                    rapor_metni += f"  Açıklama: {f.get('aciklama', '')}\n"
                    rapor_metni += f"  Fotoğraf: {'Var' if f.get('foto_url') else 'Yok'}\n"
                    rapor_metni += "\n"
                
                rapor_metni += "-" * 40 + "\n\n"
            
            self.rapor_text.configure(state="normal")
            self.rapor_text.delete("0.0", "end")
            self.rapor_text.insert("0.0", rapor_metni)
            self.rapor_text.configure(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Rapor oluşturma hatası:\n{e}")
    
    def temizle(self):
        self.personel.set("")
        self.is_nitelig.set("Anahtarcı")
        self.parsel.set("Parsel A")
        self.blok.set("Blok 1")
        self.aciklama.delete("0.0", "end")
        self.foto_listesi = []
        self.foto_sayaci = 0
        self.foto_sayisi_label.configure(text="0/5")
        self.foto_btn.configure(state="normal")
