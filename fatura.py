import os
import shutil
from datetime import datetime
from tkinter import filedialog, messagebox, ttk
import customtkinter as ctk
from tkcalendar import DateEntry

class FaturaModul(ctk.CTkFrame):
    def __init__(self, master, db):
        super().__init__(master, fg_color="#EEF2F7")
        self.db = db
        self.fatura_kodu = self.db.fatura_kodu_uret()
        self.duzenlenen_fatura_kodu = None
        self.kalemler = []          # Faturanın aktif kalemleri
        self.secilen_irsaliyeler = [] # Seçilen çoklu irsaliye ID'leri
        self.cari_listesi = []      # Combobox için cari isimleri
        
        self._build()
        self.sa_listesini_yenile()
        self.cari_listesini_yenile() # Cari kartları yükleyen yeni fonksiyon
        self.listele()

    def _build(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10), background="#FFFFFF", fieldbackground="#FFFFFF")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#E2E8F0", foreground="#0F172A")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ================= SOL TARAF: FORM GİRİŞ ALANI =================
        left_panel = ctk.CTkFrame(self, width=420, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E2E8F0")
        left_panel.grid(row=0, column=0, rowspan=2, sticky="nsw", padx=16, pady=16)
        left_panel.pack_propagate(False)

        ctk.CTkLabel(left_panel, text="FATURA BİLGİLERİ", font=("Segoe UI", 16, "bold"), text_color="#1E293B").pack(anchor="w", padx=20, pady=(20, 10))

        # Satın Alma Bağlantısı (Opsiyonel)
        ctk.CTkLabel(left_panel, text="Satın Alma Talebi Bağlantısı (Opsiyonel):", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=20, pady=(5, 2))
        self.sa_combo = ctk.CTkComboBox(left_panel, width=380, values=[""])
        self.sa_combo.pack(padx=20, pady=2)

        # Firma / Cari Ünvan (HEM SEÇİLEBİLİR HEM ELLE YAZILABİLİR COMBOBOX)
        ctk.CTkLabel(left_panel, text="Firma / Cari Ünvan (Seçin veya Elle Yazın):", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
        self.cari_combo = ctk.CTkComboBox(left_panel, width=380, values=[""])
        self.cari_combo.pack(padx=20, pady=2)

        # Çoklu İrsaliye Seçim Butonu
        ctk.CTkLabel(left_panel, text="İrsaliye Bağlantıları (Çoklu Seçim):", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
        self.irsaliye_btn = ctk.CTkButton(left_panel, text="İrsaliyeleri Seç (0 Seçildi)", fg_color="#475569", hover_color="#334155", width=380, command=self.irsaliye_secim_penceresi_acan)
        self.irsaliye_btn.pack(padx=20, pady=2)

        # Fatura No
        ctk.CTkLabel(left_panel, text="Fatura Numarası:", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
        self.fatura_no = ctk.CTkEntry(left_panel, width=380, placeholder_text="Örn: FT-20260012")
        self.fatura_no.pack(padx=20, pady=2)

        # Fatura Tarihi
        ctk.CTkLabel(left_panel, text="Fatura Tarihi:", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
        self.fatura_tarihi_entry = DateEntry(left_panel, width=38, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.fatura_tarihi_entry.pack(padx=20, pady=2, anchor="w")

        # Finansal Tutarlar PANELİ
        tutar_frame = ctk.CTkFrame(left_panel, fg_color="#F8FAFC", corner_radius=8, border_width=1, border_color="#E2E8F0")
        tutar_frame.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(tutar_frame, text="Matrah (KDV Hariç Tutar):", font=("Segoe UI", 11)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.toplam_tutar_entry = ctk.CTkEntry(tutar_frame, width=150, placeholder_text="0.00")
        self.toplam_tutar_entry.grid(row=0, column=1, padx=10, pady=5)
        self.toplam_tutar_entry.bind("<KeyRelease>", lambda e: self.tutar_hesapla())

        ctk.CTkLabel(tutar_frame, text="KDV Oranı (%):", font=("Segoe UI", 11)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.kdv_orani_entry = ctk.CTkEntry(tutar_frame, width=150, placeholder_text="20")
        self.kdv_orani_entry.insert(0, "20")
        self.kdv_orani_entry.grid(row=1, column=1, padx=10, pady=5)
        self.kdv_orani_entry.bind("<KeyRelease>", lambda e: self.tutar_hesapla())

        ctk.CTkLabel(tutar_frame, text="Genel Toplam (KDV Dahil):", font=("Segoe UI", 11, "bold")).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.genel_toplam_entry = ctk.CTkEntry(tutar_frame, width=150, placeholder_text="0.00", fg_color="#F1F5F9")
        self.genel_toplam_entry.grid(row=2, column=1, padx=10, pady=5)

        # ANA AKSİYON BUTONLARI
        self.btn_kaydet = ctk.CTkButton(left_panel, text="Faturayı Kaydet", fg_color="#10B981", hover_color="#059669", height=40, font=("Segoe UI", 12, "bold"), command=self.kaydet)
        self.btn_kaydet.pack(fill="x", padx=20, pady=(10, 5))

        ctk.CTkButton(left_panel, text="Formu Temizle", fg_color="#64748B", hover_color="#475569", command=self.temizle).pack(fill="x", padx=20, pady=5)

        # ================= SAĞ TARAF: LİSTELER VE MALZEME SEKMESİ =================
        right_panel = ctk.CTkFrame(self, fg_color="transparent")
        right_panel.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(0, 16), pady=16)

        # ÜST: Mevcut Faturaların Listesi
        ctk.CTkLabel(right_panel, text="SİSTEMDEKİ FATURALAR", font=("Segoe UI", 14, "bold"), text_color="#1E293B").pack(anchor="w", pady=(0, 5))
        
        tree_frame = ctk.CTkFrame(right_panel, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E2E8F0")
        tree_frame.pack(fill="both", expand=True, pady=(0, 15))

        self.tree = ttk.Treeview(tree_frame, columns=("kod", "no", "firma", "tarih", "matrah", "toplam", "durum"), show="headings")
        self.tree.heading("kod", text="Fatura Kodu")
        self.tree.heading("no", text="Fatura No")
        self.tree.heading("firma", text="Firma / Cari")
        self.tree.heading("tarih", text="Fatura Tarihi")
        self.tree.heading("matrah", text="Matrah")
        self.tree.heading("toplam", text="Genel Toplam")
        self.tree.heading("durum", text="3'lü Kontrol Durumu")

        self.tree.column("kod", width=120, anchor="center")
        self.tree.column("no", width=110, anchor="center")
        self.tree.column("firma", width=180, anchor="w")
        self.tree.column("tarih", width=100, anchor="center")
        self.tree.column("matrah", width=90, anchor="e")
        self.tree.column("toplam", width=100, anchor="e")
        self.tree.column("durum", width=140, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # ALT PANEL: FATURA KALEMLERİ
        kalem_panel = ctk.CTkFrame(right_panel, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E2E8F0")
        kalem_panel.pack(fill="both", expand=True)

        kalem_ust_bar = ctk.CTkFrame(kalem_panel, fg_color="transparent")
        kalem_ust_bar.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(kalem_ust_bar, text="FATURA MALZEME KALEMLERİ", font=("Segoe UI", 12, "bold"), text_color="#1E293B").pack(side="left")
        ctk.CTkButton(kalem_ust_bar, text="+ Ekstra Kalem Ekle", width=140, fg_color="#2563EB", hover_color="#1D4ED8", command=self.manuel_kalem_ekle_penceresi).pack(side="right")

        self.kalem_tree = ttk.Treeview(kalem_panel, columns=("urun", "miktar", "birim", "fiyat", "kdv", "toplam"), show="headings", height=6)
        self.kalem_tree.heading("urun", text="Ürün / Hizmet Adı")
        self.kalem_tree.heading("miktar", text="Miktar")
        self.kalem_tree.heading("birim", text="Birim")
        self.kalem_tree.heading("fiyat", text="Birim Fiyat")
        self.kalem_tree.heading("kdv", text="KDV %")
        self.kalem_tree.heading("toplam", text="Toplam Tutar")

        self.kalem_tree.column("urun", width=220, anchor="w")
        self.kalem_tree.column("miktar", width=80, anchor="center")
        self.kalem_tree.column("birim", width=70, anchor="center")
        self.kalem_tree.column("fiyat", width=90, anchor="e")
        self.kalem_tree.column("kdv", width=60, anchor="center")
        self.kalem_tree.column("toplam", width=100, anchor="e")
        self.kalem_tree.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        aksiyon_bar = ctk.CTkFrame(kalem_panel, fg_color="transparent")
        aksiyon_bar.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkButton(aksiyon_bar, text="Faturayı / Fiyatları Kontrol Et", fg_color="#3B82F6", hover_color="#2563EB", command=self.karsilastir).pack(side="left", padx=5)
        ctk.CTkButton(aksiyon_bar, text="Fatura Görseli / Evrak Yükle", fg_color="#8B5CF6", hover_color="#7C3AED", command=self.evrak_yukle).pack(side="left", padx=5)

    # ================= CARİ LİSTESİNİ VERİTABANINDAN YENİLEME =================
    def cari_listesini_yenile(self):
        """Sistemdeki cari kartları combobox'a yükler."""
        try:
            # Supabase üzerindeki cari_kartlar tablosundan firma adlarını çekiyoruz
            res = self.db.supabase.table("cari_kartlar").select("firma_adi").execute()
            veriler = res.data or []
            
            # Tekrarlayan kayıtları engellemek için set kullanıyoruz
            firmalar = sorted(list(set([f.get("firma_adi", "").strip() for f in veriler if f.get("firma_adi")])))
            
            self.cari_listesi = [""] + firmalar
            self.cari_combo.configure(values=self.cari_listesi)
            self.cari_combo.set("") # İlk açılışta boş kalsın
        except Exception as e:
            print("Cari listesi yüklenirken hata oluştu:", e)

    # ================= DİNAMİK ÇOKLU İRSALİYE SEÇİM POPUP PENCERESİ =================
    def irsaliye_secim_penceresi_acan(self):
        # Kullanıcının combobox'tan seçtiği VEYA elle yazdığı firma adını alıyoruz
        firma_adi = self.cari_combo.get().strip()
        
        if not firma_adi:
            messagebox.showwarning("Uyarı", "Lütfen önce 'Firma / Cari Ünvan' alanını seçin veya elle yazın!\nSistem yazılan firmaya ait irsaliyeleri getirecektir.")
            return

        popup = ctk.CTkToplevel(self)
        popup.title(f"{firma_adi} - İrsaliye Seçimi")
        popup.geometry("620://500")
        popup.grab_set()

        ctk.CTkLabel(popup, text=f"'{firma_adi}' Firmasının Gönderdiği İrsaliyeler", font=("Segoe UI", 14, "bold")).pack(pady=10)

        # Tüm irsaliyeleri çekip seçilen firmaya göre filtreleme yapıyoruz
        try:
            tum_irsaliyeler = self.db.irsaliyeler_getir() or []
        except:
            try:
                res = self.db.supabase.table("irsaliyeler").select("*").execute()
                tum_irsaliyeler = res.data or []
            except Exception as e:
                print("İrsaliyeler çekilemedi:", e)
                tum_irsaliyeler = []

        # BÜYÜK/KÜÇÜK HARF DUYARLILIĞINI ORTADAN KALDIRARAK FİLTRELEME
        firma_irsaliyeleri = [i for i in tum_irsaliyeler if str(i.get("firma", "")).strip().lower() == firma_adi.lower()]

        if not firma_irsaliyeleri:
            ctk.CTkLabel(popup, text=f"Sistemde '{firma_adi}' firmasına ait faturalandırılmamış irsaliye bulunamadı.", text_color="#EF4444", font=("Segoe UI", 11, "bold")).pack(pady=50)
            ctk.CTkButton(popup, text="Kapat", width=100, command=popup.destroy).pack()
            return

        scroll_frame = ctk.CTkScrollableFrame(popup, width=560, height=320)
        scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        checkbox_map = {}
        for irs in firma_irsaliyeleri:
            ir_id = irs.get("irsaliye_id") or irs.get("id")
            ir_no = irs.get("irsaliye_no", "")
            ir_tarih = irs.get("tarih", "")
            
            txt = f"İrsaliye ID: {ir_id} | No: {ir_no} | Tarih: {ir_tarih}"
            
            var = ctk.StringVar(value="on" if ir_id in self.secilen_irsaliyeler else "off")
            cb = ctk.CTkCheckBox(scroll_frame, text=txt, variable=var, onvalue="on", offvalue="off")
            cb.pack(anchor="w", padx=10, pady=6)
            checkbox_map[ir_id] = var

        def secimleri_onayla():
            self.secilen_irsaliyeler = [ir_id for ir_id, var in checkbox_map.items() if var.get() == "on"]
            self.irsaliye_btn.configure(text=f"İrsaliyeler Seç ({len(self.secilen_irsaliyeler)} Seçildi)")
            popup.destroy()
            
            # Kalemleri otomatik aşağıya aktarır
            self.irsaliye_kalemlerini_faturaya_dok()

        ctk.CTkButton(popup, text="Seçilen İrsaliye Kalemlerini Faturaya Aktar", fg_color="#10B981", hover_color="#059669", command=secimleri_onayla).pack(pady=15)

    def irsaliye_kalemlerini_faturaya_dok(self):
        self.kalemler = [] 
        for ir_id in self.secilen_irsaliyeler:
            try:
                res = self.db.supabase.table("irsaliye_kalemleri").select("*").eq("irsaliye_id", ir_id).execute()
                kalemler = res.data or []
            except Exception as e:
                print("İrsaliye kalemleri çekilemedi:", e)
                kalemler = []

            for k in kalemler:
                miktar = float(k.get("miktar") or 0)
                self.kalemler.append({
                    "sa_kalem_id": k.get("sa_kalem_id"),
                    "stok_kart_id": k.get("stok_kart_id"),
                    "urun_adi": k.get("urun_adi", ""),
                    "miktar": miktar,
                    "birim": k.get("birim", "ADET"),
                    "birim_fiyat": 0.0,
                    "kdv_orani": 20.0,
                    "toplam_tutar": 0.0
                })
        
        self.kalem_tree_yenile()
        self.matrah_ve_genel_toplam_otomatik_hesapla()

    def manuel_kalem_ekle_penceresi(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Ekstra Kalem / Maliyet Ekle")
        popup.geometry("400x350")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Ürün / Hizmet Adı:").pack(pady=(15,2))
        urun_entry = ctk.CTkEntry(popup, width=300)
        urun_entry.pack()

        ctk.CTkLabel(popup, text="Miktar:").pack(pady=(10,2))
        miktar_entry = ctk.CTkEntry(popup, width=300)
        miktar_entry.insert(0, "1")
        miktar_entry.pack()

        ctk.CTkLabel(popup, text="Birim Fiyat (KDV Hariç):").pack(pady=(10,2))
        fiyat_entry = ctk.CTkEntry(popup, width=300)
        fiyat_entry.insert(0, "0")
        fiyat_entry.pack()

        def ekle_ve_kapat():
            if not urun_entry.get().strip():
                messagebox.showwarning("Hata", "Ürün adı boş olamaz")
                return
            try:
                m = float(miktar_entry.get() or 1)
                f = float(fiyat_entry.get() or 0)
            except:
                messagebox.showerror("Hata", "Miktar ve Fiyat sayısal olmalıdır!")
                return

            self.kalemler.append({
                "sa_kalem_id": None,
                "stok_kart_id": None,
                "urun_adi": urun_entry.get().strip(),
                "miktar": m,
                "birim": "ADET",
                "birim_fiyat": f,
                "kdv_orani": 20.0,
                "toplam_tutar": round(m * f, 2)
            })
            self.kalem_tree_yenile()
            self.matrah_ve_genel_toplam_otomatik_hesapla()
            popup.destroy()

        ctk.CTkButton(popup, text="Kalemi Listeye Ekle", fg_color="#2563EB", command=ekle_ve_kapat).pack(pady=20)

    def kalem_tree_yenile(self):
        for item in self.kalem_tree.get_children():
            self.kalem_tree.delete(item)
        for idx, k in enumerate(self.kalemler):
            self.kalem_tree.insert("", "end", iid=str(idx), values=(
                k["urun_adi"], k["miktar"], k["birim"], k["birim_fiyat"], k["kdv_orani"], k["toplam_tutar"]
            ))

    def matrah_ve_genel_toplam_otomatik_hesapla(self):
        toplam_matrah = sum(float(k["toplam_tutar"]) for k in self.kalemler)
        self.toplam_tutar_entry.delete(0, "end")
        self.toplam_tutar_entry.insert(0, f"{toplam_matrah:.2f}")
        self.tutar_hesapla()

    def tutar_hesapla(self):
        try:
            matrah = float(self.toplam_tutar_entry.get() or 0)
            kdv = float(self.kdv_orani_entry.get() or 20)
            genel_toplam = matrah * (1 + kdv / 100)
            self.genel_toplam_entry.delete(0, "end")
            self.genel_toplam_entry.insert(0, f"{genel_toplam:.2f}")
        except:
            pass

    def sa_listesini_yenile(self):
        try:
            formlar = self.db.satin_alma_formlari_getir() or []
            self.sa_listesi = [""]
            for f in formlar:
                kod = f.get("sa_id") or f.get("form_kodu") or f.get("id")
                if kod:
                    self.sa_listesi.append(f"{kod} - {f.get('firma_adi', f.get('tedarikci',''))}")
            self.sa_combo.configure(values=self.sa_listesi)
            self.sa_combo.set("")
        except Exception as e:
            print("Fatura modülü sa yenileme hatası:", e)

    def listele(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            faturalar = self.db.supabase.table("faturalar").select("*").order("created_at", desc=True).execute().data or []
            for f in faturalar:
                self.tree.insert("", "end", values=(
                    f.get("fatura_kodu"), f.get("fatura_no"), f.get("cari_unvan"),
                    f.get("fatura_tarihi"), f.get("toplam_tutar"), f.get("genel_toplam"),
                    f.get("onay_durumu", "BEKLEMEDE")
                ))
        except Exception as e:
            print("Faturalar listelenirken hata:", e)

    def _sa_id_coz(self, text):
        if not text or " - " not in text: return text
        return text.split(" - ")[0]

    def kaydet(self):
        sa_id = self._sa_id_coz(self.sa_combo.get())
        if not sa_id or str(sa_id).strip() == "": sa_id = None

        firma_girilen = self.cari_combo.get().strip()
        if not firma_girilen:
            messagebox.showwarning("Uyarı", "Firma adı boş bırakılamaz!")
            return
        if not self.fatura_no.get().strip():
            messagebox.showwarning("Uyarı", "Fatura numarası zorunludur")
            return
        if not self.kalemler:
            messagebox.showwarning("Uyarı", "Faturaya aktarılmış veya eklenmiş kalem bulunmamaktadır!")
            return

        if not self.duzenlenen_fatura_kodu:
            self.fatura_kodu = self.db.fatura_kodu_uret()

        kod = self.duzenlenen_fatura_kodu or self.fatura_kodu
        
        form = {
            "fatura_kodu": kod,
            "sa_id": sa_id,
            "fatura_no": self.fatura_no.get().strip(),
            "cari_unvan": firma_girilen, # Seçilen veya elle yazılan firma buraya gider
            "fatura_tarihi": self.fatura_tarihi_entry.get(),
            "toplam_tutar": float(self.toplam_tutar_entry.get() or 0),
            "kdv_orani": float(self.kdv_orani_entry.get() or 20),
            "genel_toplam": float(self.genel_toplam_entry.get() or 0),
        }

        db_kalemler = [{
            "fatura_kodu": kod,
            "sa_kalem_id": k.get("sa_kalem_id"),
            "stok_kart_id": k.get("stok_kart_id"),
            "urun_adi": k["urun_adi"],
            "miktar": k["miktar"],
            "birim": k["birim"],
            "birim_fiyat": k["birim_fiyat"],
            "kdv_orani": k["kdv_orani"],
            "toplam_tutar": k["toplam_tutar"],
        } for k in self.kalemler]

        if self.duzenlenen_fatura_kodu:
            ok, sonuc = self.db.fatura_guncelle(kod, form)
            if ok: self.db.fatura_kalemleri_yenile(kod, db_kalemler)
        else:
            ok, sonuc = self.db.fatura_kaydet(form)
            if ok:
                for dk in db_kalemler:
                    self.db.fatura_kalem_ekle(dk)
                
                for irs_id in self.secilen_irsaliyeler:
                    try:
                        self.db.supabase.table("fatura_irsaliye_baglanti").insert({
                            "fatura_kodu": kod,
                            "irsaliye_id": irs_id
                        }).execute()
                    except Exception as e:
                        print("Bağlantı tablosu yazım hatası:", e)

        messagebox.showinfo("Başarılı", "Fatura kaydı tamamlandı.")
        self.temizle()
        self.listele()

    def temizle(self):
        self.duzenlenen_fatura_kodu = None
        self.fatura_no.delete(0, "end")
        self.cari_combo.set("")
        self.toplam_tutar_entry.delete(0, "end")
        self.genel_toplam_entry.delete(0, "end")
        self.sa_combo.set("")
        self.secilen_irsaliyeler = []
        self.irsaliye_btn.configure(text="İrsaliyeler Seç (0 Seçildi)")
        self.kalemler = []
        self.kalem_tree_yenile()

    def karsilastir(self):
        """Fatura kalemlerini irsaliye kalemleri ile karşılaştırır."""
        if not self.kalemler:
            messagebox.showwarning("Uyarı", "Fatura kalemleri boş!")
            return
        
        if not self.secilen_irsaliyeler:
            messagebox.showwarning("Uyarı", "Karşılaştırma için önce irsaliye seçin!")
            return
        
        try:
            # İrsaliye kalemlerini topla
            irsaliye_kalemleri = []
            for ir_id in self.secilen_irsaliyeler:
                res = self.db.supabase.table("irsaliye_kalemleri").select("*").eq("irsaliye_id", ir_id).execute()
                irsaliye_kalemleri.extend(res.data or [])
            
            if not irsaliye_kalemleri:
                messagebox.showwarning("Uyarı", "Seçilen irsaliyelerde kalem bulunamadı!")
                return
            
            # Karşılaştırma raporu oluştur
            rapor = "FATURA - İRSALİYE KARŞILAŞTIRMA RAPORU\n"
            rapor += "=" * 50 + "\n\n"
            
            # Ürün bazında karşılaştırma
            fatura_map = {}
            for k in self.kalemler:
                urun = k["urun_adi"]
                if urun not in fatura_map:
                    fatura_map[urun] = 0
                fatura_map[urun] += k["miktar"]
            
            irsaliye_map = {}
            for k in irsaliye_kalemleri:
                urun = k["urun_adi"]
                if urun not in irsaliye_map:
                    irsaliye_map[urun] = 0
                irsaliye_map[urun] += k["miktar"]
            
            # Rapor detayları
            tum_urunler = set(list(fatura_map.keys()) + list(irsaliye_map.keys()))
            
            for urun in sorted(tum_urunler):
                f_miktar = fatura_map.get(urun, 0)
                i_miktar = irsaliye_map.get(urun, 0)
                fark = f_miktar - i_miktar
                
                durum = "✅ UYUMLU" if abs(fark) < 0.01 else "❌ FARK VAR"
                rapor += f"{urun}:\n"
                rapor += f"  Fatura: {f_miktar}\n"
                rapor += f"  İrsaliye: {i_miktar}\n"
                rapor += f"  Fark: {fark}\n"
                rapor += f"  Durum: {durum}\n\n"
            
            # Genel durum
            genel_uyumlu = all(abs(fatura_map.get(u, 0) - irsaliye_map.get(u, 0)) < 0.01 for u in tum_urunler)
            rapor += "=" * 50 + "\n"
            rapor += f"GENEL DURUM: {'✅ TÜM KALEMLER UYUMLU' if genel_uyumlu else '❌ UYUMSUZLUK VAR'}\n"
            
            # Raporu göster
            popup = ctk.CTkToplevel(self)
            popup.title("Karşılaştırma Raporu")
            popup.geometry("600x500")
            
            ctk.CTkLabel(popup, text="FATURA - İRSALİYE KARŞILAŞTIRMA RAPORU", 
                        font=("Segoe UI", 14, "bold")).pack(pady=10)
            
            rapor_box = ctk.CTkTextbox(popup, width=550, height=400, font=("Consolas", 10))
            rapor_box.pack(padx=10, pady=10)
            rapor_box.insert("0.0", rapor)
            rapor_box.configure(state="disabled")
            
            if genel_uyumlu:
                messagebox.showinfo("Sonuç", "Tüm kalemler uyumlu!")
            else:
                messagebox.showwarning("Sonuç", "Bazı kalemlerde uyumsuzluk var!")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Karşılaştırma hatası:\n{e}")

    def evrak_yukle(self):
        """Fatura görseli/evrağını yükler."""
        dosya = filedialog.askopenfilename(
            title="Fatura Evrağı Seç",
            filetypes=[("PDF", "*.pdf"), ("Resim", "*.png;*.jpg;*.jpeg"), ("Tüm Dosyalar", "*.*")]
        )
        
        if not dosya:
            return
        
        try:
            # Evrak klasörü oluştur
            proje_klasoru = os.path.dirname(os.path.abspath(__file__))
            hedef_klasor = os.path.join(proje_klasoru, "fatura_evraklari")
            os.makedirs(hedef_klasor, exist_ok=True)
            
            # Dosya kopyala
            uzanti = os.path.splitext(dosya)[1]
            fatura_kodu = self.duzenlenen_fatura_kodu or self.fatura_kodu
            hedef_yol = os.path.join(hedef_klasor, f"{fatura_kodu}_evrak{uzanti}")
            
            shutil.copy2(dosya, hedef_yol)
            
            # Veritabanına güncelle
            if self.duzenlenen_fatura_kodu:
                self.db.supabase.table("faturalar").update({
                    "evrak_url": hedef_yol,
                    "onay_durumu": "EVRAK YÜKLENDİ"
                }).eq("fatura_kodu", self.duzenlenen_fatura_kodu).execute()
            else:
                messagebox.showinfo("Bilgi", "Evrak kaydedildi. Fatura kaydedildiğinde otomatik bağlanacak.")
                self.evrak_yolu = hedef_yol
            
            messagebox.showinfo("Başarılı", f"Evrak yüklendi:\n{hedef_yol}")
            self.listele()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Evrak yüklenemedi:\n{e}")