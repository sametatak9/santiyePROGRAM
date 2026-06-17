import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry


class KasaRaporuModul(ctk.CTkFrame):
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
        self.grid_rowconfigure(0, weight=1)
        
        # ================= ANA PANEL =================
        main_panel = ctk.CTkFrame(self, fg_color="white", corner_radius=14,
                                 border_width=1, border_color="#E2E8F0")
        main_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # HEADER
        header = ctk.CTkFrame(main_panel, fg_color=self.COLOR_PRIMARY, corner_radius=12)
        header.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(header, text="💰 HAFTALIK KASA RAPORU", text_color="white",
                     font=("Segoe UI", 18, "bold")).pack(pady=6)
        
        # FİLTRE PANELİ
        filter_frame = ctk.CTkFrame(main_panel, fg_color="#F1F5F9", corner_radius=10)
        filter_frame.pack(fill="x", padx=10, pady=10)
        
        # Yıl ve Hafta Seçimi
        row1 = ctk.CTkFrame(filter_frame, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(row1, text="Yıl:", font=("Segoe UI", 12, "bold")).pack(side="left", padx=5)
        self.yil_combo = ctk.CTkComboBox(row1, values=[str(y) for y in range(2024, 2030)],
                                         width=100, height=35)
        self.yil_combo.set(str(datetime.now().year))
        self.yil_combo.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="Hafta:", font=("Segoe UI", 12, "bold")).pack(side="left", padx=5)
        self.hafta_combo = ctk.CTkComboBox(row1, values=[str(h) for h in range(1, 53)],
                                           width=100, height=35)
        self.hafta_combo.set(str(self._get_current_week()))
        self.hafta_combo.pack(side="left", padx=5)
        
        ctk.CTkButton(row1, text="📊 Rapor Getir", fg_color=self.COLOR_PRIMARY,
                      hover_color=self.COLOR_PRIMARY_HOVER, command=self.rapor_getir).pack(side="left", padx=10)
        
        # Tarih Aralığı Seçimi
        row2 = ctk.CTkFrame(filter_frame, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(row2, text="Başlangıç:", font=("Segoe UI", 12, "bold")).pack(side="left", padx=5)
        self.baslangic_entry = DateEntry(row2, date_pattern="yyyy-mm-dd", font=("Segoe UI", 11))
        self.baslangic_entry.set_date(self._get_week_start(datetime.now().year, self._get_current_week()))
        self.baslangic_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(row2, text="Bitiş:", font=("Segoe UI", 12, "bold")).pack(side="left", padx=5)
        self.bitis_entry = DateEntry(row2, date_pattern="yyyy-mm-dd", font=("Segoe UI", 11))
        self.bitis_entry.set_date(self._get_week_end(datetime.now().year, self._get_current_week()))
        self.bitis_entry.pack(side="left", padx=5)
        
        # ÖZET PANELİ
        summary_frame = ctk.CTkFrame(main_panel, fg_color="#F8FAFC", corner_radius=10,
                                     border_width=1, border_color="#E2E8F0")
        summary_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(summary_frame, text="HAFTALIK ÖZET", font=("Segoe UI", 13, "bold"),
                     text_color=self.COLOR_TEXT).pack(anchor="w", padx=10, pady=(10, 5))
        
        summary_row = ctk.CTkFrame(summary_frame, fg_color="transparent")
        summary_row.pack(fill="x", padx=10, pady=5)
        
        self.giris_label = ctk.CTkLabel(summary_row, text="Giriş: ₺0.00",
                                        font=("Segoe UI", 14, "bold"), text_color=self.COLOR_SUCCESS)
        self.giris_label.pack(side="left", padx=10)
        
        self.cikis_label = ctk.CTkLabel(summary_row, text="Çıkış: ₺0.00",
                                        font=("Segoe UI", 14, "bold"), text_color=self.COLOR_DANGER)
        self.cikis_label.pack(side="left", padx=10)
        
        self.bakiye_label = ctk.CTkLabel(summary_row, text="Bakiye: ₺0.00",
                                         font=("Segoe UI", 14, "bold"), text_color=self.COLOR_PRIMARY)
        self.bakiye_label.pack(side="left", padx=10)
        
        # HAREKET LİSTESİ
        ctk.CTkLabel(main_panel, text="KASA HAREKETLERİ", font=("Segoe UI", 14, "bold"),
                     text_color=self.COLOR_TEXT).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.tree = ttk.Treeview(main_panel, columns=("tarih", "tip", "tutar", "aciklama", "ref"),
                                show="headings", height=15)
        self.tree.heading("tarih", text="Tarih")
        self.tree.heading("tip", text="Tip")
        self.tree.heading("tutar", text="Tutar")
        self.tree.heading("aciklama", text="Açıklama")
        self.tree.heading("ref", text="Referans")
        
        self.tree.column("tarih", width=120, anchor="center")
        self.tree.column("tip", width=80, anchor="center")
        self.tree.column("tutar", width=120, anchor="e")
        self.tree.column("aciklama", width=250, anchor="w")
        self.tree.column("ref", width=150, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.tree.tag_configure("GIRIS", foreground="#16A34A")
        self.tree.tag_configure("CIKIS", foreground="#DC2626")
        
        # BUTONLAR
        btn_frame = ctk.CTkFrame(main_panel, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="➕ Hareket Ekle", fg_color=self.COLOR_SUCCESS,
                      hover_color="#059669", command=self.hareket_ekle_penceresi).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="📄 PDF Dışa Aktar", fg_color=self.COLOR_PRIMARY,
                      hover_color=self.COLOR_PRIMARY_HOVER, command=self.pdf_aktar).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🧹 Temizle", fg_color=self.COLOR_MUTED,
                      hover_color="#475569", command=self.temizle).pack(side="left", padx=5)
    
    def _get_current_week(self):
        return datetime.now().isocalendar()[1]
    
    def _get_week_start(self, year, week):
        return datetime.strptime(f"{year}-W{week}-1", "%Y-W%W-%w").date()
    
    def _get_week_end(self, year, week):
        return self._get_week_start(year, week) + timedelta(days=6)
    
    def rapor_getir(self):
        try:
            yil = int(self.yil_combo.get())
            hafta = int(self.hafta_combo.get())
            
            # Tarihleri güncelle
            baslangic = self._get_week_start(yil, hafta)
            bitis = self._get_week_end(yil, hafta)
            self.baslangic_entry.set_date(baslangic)
            self.bitis_entry.set_date(bitis)
            
            # Veritabanından rapor al
            rapor = self.db.kasa_haftalik_raporu(yil, hafta)
            
            if not rapor:
                messagebox.showwarning("Uyarı", "Rapor alınamadı")
                return
            
            # Özetleri güncelle
            self.giris_label.configure(text=f"Giriş: ₺{rapor['giris_toplam']:.2f}")
            self.cikis_label.configure(text=f"Çıkış: ₺{rapor['cikis_toplam']:.2f}")
            self.bakiye_label.configure(text=f"Bakiye: ₺{rapor['bakiye']:.2f}")
            
            # Listeyi güncelle
            self.listele(rapor['hareketler'])
            
        except Exception as e:
            messagebox.showerror("Hata", f"Rapor getirme hatası:\n{e}")
    
    def listele(self, hareketler=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if hareketler is None:
            baslangic = self.baslangic_entry.get()
            bitis = self.bitis_entry.get()
            hareketler = self.db.kasa_hareketleri_getir(baslangic, bitis)
        
        for h in hareketler:
            tip = h.get("hareket_tipi", "")
            tag = "GIRIS" if tip == "GIRIS" else "CIKIS"
            
            ref = h.get("referans_tipi", "")
            ref_id = h.get("referans_id", "")
            if ref and ref_id:
                ref_text = f"{ref}: {ref_id}"
            else:
                ref_text = "-"
            
            self.tree.insert("", "end", values=(
                h.get("tarih", ""),
                "Giriş" if tip == "GIRIS" else "Çıkış",
                f"₺{float(h.get('tutar') or 0):.2f}",
                h.get("aciklama", ""),
                ref_text
            ), tags=(tag,))
    
    def hareket_ekle_penceresi(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Kasa Hareketi Ekle")
        popup.geometry("500x450")
        popup.grab_set()
        
        ctk.CTkLabel(popup, text="KASA HAREKETİ EKLE", font=("Segoe UI", 14, "bold")).pack(pady=10)
        
        form = ctk.CTkFrame(popup, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(form, text="Tarih:", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tarih_entry = DateEntry(form, date_pattern="yyyy-mm-dd")
        tarih_entry.set_date(datetime.now().date())
        tarih_entry.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(form, text="Hareket Tipi:", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tip_combo = ctk.CTkComboBox(form, values=["GIRIS", "CIKIS"])
        tip_combo.set("GIRIS")
        tip_combo.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(form, text="Tutar:", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tutar_entry = ctk.CTkEntry(form, placeholder_text="0.00")
        tutar_entry.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(form, text="Açıklama:", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        aciklama_entry = ctk.CTkEntry(form, placeholder_text="Açıklama girin...")
        aciklama_entry.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(form, text="Referans Tipi:", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        ref_combo = ctk.CTkComboBox(form, values=["DIGER", "FATURA", "IRSALIYE", "MAAS"])
        ref_combo.set("DIGER")
        ref_combo.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(form, text="Referans ID:", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        ref_id_entry = ctk.CTkEntry(form, placeholder_text="Opsiyonel")
        ref_id_entry.pack(fill="x", pady=(0, 10))
        
        def kaydet():
            try:
                tutar = float(tutar_entry.get())
                if tutar <= 0:
                    messagebox.showwarning("Uyarı", "Tutar 0'dan büyük olmalı")
                    return
                
                hareket = {
                    "tarih": tarih_entry.get(),
                    "hareket_tipi": tip_combo.get(),
                    "tutar": tutar,
                    "aciklama": aciklama_entry.get(),
                    "referans_tipi": ref_combo.get(),
                    "referans_id": ref_id_entry.get() or None,
                }
                
                basarili, sonuc = self.db.kasa_hareketi_kaydet(hareket)
                if basarili:
                    messagebox.showinfo("Başarılı", "Kasa hareketi kaydedildi")
                    popup.destroy()
                    self.rapor_getir()
                else:
                    messagebox.showerror("Hata", f"Kayıt hatası:\n{sonuc}")
            except ValueError:
                messagebox.showwarning("Uyarı", "Tutar sayısal olmalı")
            except Exception as e:
                messagebox.showerror("Hata", f"Hata:\n{e}")
        
        ctk.CTkButton(popup, text="Kaydet", fg_color=self.COLOR_SUCCESS,
                      hover_color="#059669", command=kaydet).pack(pady=10)
    
    def pdf_aktar(self):
        messagebox.showinfo("Bilgi", "PDF dışa aktarma özelliği yakında eklenecek.")
    
    def temizle(self):
        self.giris_label.configure(text="Giriş: ₺0.00")
        self.cikis_label.configure(text="Çıkış: ₺0.00")
        self.bakiye_label.configure(text="Bakiye: ₺0.00")
        for item in self.tree.get_children():
            self.tree.delete(item)
