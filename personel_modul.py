from datetime import date
from fpdf import FPDF
import customtkinter as ctk
from tkinter import messagebox  # 1. HATA DÜZELTİLDİ: Import eklendi
from personel_ekleme_penceresi import PersonelEklePenceresi
from db_manager import personel_listele
from db_manager import personel_sil
from db_manager import personel_guncelle

class PersonelKayitFrame(ctk.CTkFrame):
    def __init__(self, master):
        self.COLOR_BG = "#F1F5F9"
        self.COLOR_CARD = "#FFFFFF"
        self.COLOR_BORDER = "#E2E8F0"
        self.COLOR_PRIMARY = "#2563EB"
        self.COLOR_PRIMARY_HOVER = "#1D4ED8"
        self.COLOR_SUCCESS = "#16A34A"
        self.COLOR_TEXT = "#0F172A"

        super().__init__(master, fg_color=self.COLOR_BG)
        # ANA YERLEŞİM
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)

        # SOL TARAF (FORM)
        self.left_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent",
            scrollbar_button_color="#CBD5E1",
            scrollbar_button_hover_color="#94A3B8"
        )
        self.left_frame.pack(side="left", fill="both", expand=True)

        # SAĞ TARAF (PERSONEL LİSTESİ)
        self.right_frame = ctk.CTkFrame(
            self.content_frame,
            width=420,
            fg_color=self.COLOR_CARD,
            corner_radius=15,
            border_width=1,
            border_color=self.COLOR_BORDER
        )
        self.right_frame.pack(side="right", fill="y", padx=(0,20), pady=10)
        self.right_frame.pack_propagate(False)
        # --- YARDIMCI FONKSİYON (Giriş kutuları için standart) ---
        def create_labeled_entry(parent, label_text, row, col, columnspan=1):
            frame = ctk.CTkFrame(parent, fg_color="transparent")
            frame.grid(row=row, column=col, columnspan=columnspan, padx=5, pady=5, sticky="ew")
            
            # Etiketler: Koyu yazı
            lbl = ctk.CTkLabel(
            frame,
            text=label_text,
            font=("Segoe UI", 11, "bold"),
            text_color="#334155"
        )
            lbl.pack(anchor="w")
            
            # Giriş Kutusu: Beyaz arka plan, Siyah yazı
            ent = ctk.CTkEntry(
            frame,
            height=38,
            corner_radius=8,
            fg_color="#FFFFFF",
            text_color="#0F172A",
            placeholder_text_color="#94A3B8",
            border_width=1,
            border_color=self.COLOR_BORDER
        )
            ent.pack(fill="x")
            return ent

        # 0. ANA KAPSAYICI (Beyaz Kart görünümü)

        self.main_container = ctk.CTkFrame(
            self.left_frame,
            fg_color=self.COLOR_CARD,
            corner_radius=16,
            border_width=1,
            border_color=self.COLOR_BORDER
        )
        self.main_container.pack(fill="x", padx=20, pady=10)
        self.title_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        self.title_frame.pack(fill="x", padx=15, pady=(15, 5))

        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="👤  Personel Bilgileri",
            font=("Segoe UI", 20, "bold"),
            text_color="#0F172A"
        )
        self.title_label.pack(side="left")

        self.subtitle_label = ctk.CTkLabel(
            self.title_frame,
            text="Kayıt, düzenleme ve personel yönetimi",
            font=("Segoe UI", 11),
            text_color="#64748B"
        )
        self.subtitle_label.pack(side="left", padx=12)
        # Başlık ve Butonlar
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=10, pady=(10, 0))

        self.btn_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.btn_box.pack(side="right")
        # Örnek: Diğer butonların yanına ekleyin
        ctk.CTkButton(
            self.btn_box,
            text="📄 PDF RAPORU",
            width=120,
            height=40,
            corner_radius=10,
            font=("Segoe UI", 11, "bold"),
            fg_color="#EF4444", # Kırmızı renk
            command=self.pdf_rapor_olustur
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            self.btn_box,
            text="+ Yeni Personel",
            width=140,
            height=40,
            corner_radius=10,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.COLOR_SUCCESS,
            hover_color="#15803D",
            command=self.yeni_personel_penceresini_ac
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            self.btn_box,
            text="💾 Güncelle",
            width=140,
            height=40,
            corner_radius=10,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.COLOR_PRIMARY,
            hover_color=self.COLOR_PRIMARY_HOVER,
            command=self.personeli_guncelle_islem
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            self.btn_box,
            text="🧹 Temizle",
            width=120,
            height=40,
            corner_radius=10,
            font=("Segoe UI", 11, "bold"),
            fg_color="#64748B",
            hover_color="#475569",
            command=self.formu_ve_listeyi_sifirla
        ).pack(side="left", padx=5)
        # 1. ÜST GİRİŞ ALANLARI
        self.top_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=10, pady=10)

        # Fotoğraf kısmı
        self.photo_frame = ctk.CTkFrame(
            self.top_frame,
            width=90,
            height=90,
            fg_color="#F8FAFC",
            corner_radius=12,
            border_width=1,
            border_color=self.COLOR_BORDER
        )
        self.photo_frame.grid(row=0, column=0, rowspan=3, padx=10, pady=10)
        self.photo_label = ctk.CTkLabel(
            self.photo_frame,
            text="📷\nFotoğraf Yok",
            font=("Segoe UI", 14),
            text_color="#94A3B8",
            justify="center"
        )
        self.photo_label.pack(expand=True, fill="both")

        # Girişleri oluştur
        self.tc_entry = create_labeled_entry(self.top_frame, "TC Kimlik No", 0, 1)
        self.ad_entry = create_labeled_entry(self.top_frame, "Adı", 0, 2)
        self.soyad_entry = create_labeled_entry(self.top_frame, "Soyadı", 0, 3)
        self.baba_entry = create_labeled_entry(self.top_frame, "Baba Adı", 0, 4)
        self.dogum_entry = create_labeled_entry(self.top_frame, "Doğum Tarihi", 1, 1)
        
        # Cinsiyet ComboBox
        self.cinsiyet_frame = ctk.CTkFrame(
            self.top_frame,
            fg_color="transparent"
        )
        self.cinsiyet_frame.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        ctk.CTkLabel(
            self.cinsiyet_frame,
            text="Cinsiyet",
            font=("Segoe UI", 11, "bold"),
            text_color="#334155"
        ).pack(anchor="w")
        self.cinsiyet_combo = ctk.CTkComboBox(
            self.cinsiyet_frame,
            values=["Erkek", "Kadın"],
            height=38,
            corner_radius=8,
            fg_color="#FFFFFF",
            border_color=self.COLOR_BORDER,
            button_color=self.COLOR_PRIMARY,
            button_hover_color=self.COLOR_PRIMARY_HOVER,
            dropdown_fg_color="#FFFFFF"
        )
        self.cinsiyet_combo.pack(fill="x")
        
        self.tel_entry = create_labeled_entry(self.top_frame, "Telefon No", 1, 3)
        self.email_entry = create_labeled_entry(self.top_frame, "E-posta", 1, 4)
        self.adres_entry = create_labeled_entry(self.top_frame, "Adres", 2, 1, columnspan=2)
        self.il_entry = create_labeled_entry(self.top_frame, "İkamet İl", 2, 3)
        self.ilce_entry = create_labeled_entry(self.top_frame, "İkamet İlçe", 2, 4)
        
        for i in range(1, 5): self.top_frame.grid_columnconfigure(i, weight=1)

        # --- 2. SEKMELER ---
        self.tabs_container = ctk.CTkFrame(
            self.left_frame,
            fg_color=self.COLOR_CARD,
            corner_radius=16,
            border_width=1,
            border_color=self.COLOR_BORDER
        )
        self.tabs_container.pack(fill="x", padx=20, pady=10)

    # ==========================
        # PERSONEL LİSTESİ (SAĞ PANEL)
        # ==========================

        self.list_container = ctk.CTkFrame(
            self.right_frame,
            fg_color="transparent"
        )
        self.list_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.list_header = ctk.CTkFrame(
            self.list_container,
            height=50,
            fg_color="#F8FAFC",
            corner_radius=10
        )
        self.list_header.pack(fill="x")

        ctk.CTkLabel(
            self.list_header,
            text="👥 PERSONEL LİSTESİ",
            font=("Segoe UI", 14, "bold")
        ).pack(side="left", padx=10)

        self.arama_entry = ctk.CTkEntry(
            self.list_header,
            placeholder_text="Ara...",
            width=180
        )
        self.arama_entry.pack(side="right", padx=10)

        self.arama_entry.bind(
            "<KeyRelease>",
            lambda e: self.tabloyu_guncelle()
        )

        self.personel_frame = ctk.CTkScrollableFrame(
            self.list_container,
            fg_color="transparent",
            orientation="vertical" # Bu dikey kaydırmayı korur
        )
        self.personel_frame.pack(fill="both", expand=True, pady=(10,0))

        self.tabloyu_guncelle()

        # =========================
        # TAB SYSTEM
        # =========================
        self.tabs = ctk.CTkTabview(
            self.tabs_container,
            height=140,
            fg_color="transparent",

            segmented_button_fg_color="#F1F5F9",
            segmented_button_unselected_color="#FFFFFF",
            segmented_button_unselected_hover_color="#E2E8F0",

            segmented_button_selected_color=self.COLOR_PRIMARY,
            segmented_button_selected_hover_color=self.COLOR_PRIMARY_HOVER,

            text_color="#0F172A",  # sadece bu var (genel text)
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0"
        )
        self.tabs.pack(fill="x", padx=10, pady=10)

        self.tab1 = self.tabs.add("💼 Çalışma Bilgileri")
        self.tab2 = self.tabs.add("🏦 Banka Bilgileri")

        # =========================
        # TAB1 ROOT
        # =========================
        self.tab1_root = ctk.CTkFrame(self.tab1, fg_color="transparent")
        self.tab1_root.pack(fill="both", expand=True)

        # =========================
        # TAB2 ROOT
        # =========================
        self.tab2_root = ctk.CTkFrame(self.tab2, fg_color="transparent")
        self.tab2_root.pack(fill="both", expand=True)

        # =========================
        # STİL SİSTEMİ
        # =========================
        self.FONT_LABEL = ("Segoe UI", 11, "bold")

        self.INPUT_STYLE = {
            "height": 38,
            "corner_radius": 8,
            "fg_color": "#FFFFFF",
            "text_color": "#0F172A",
            "border_width": 1,
            "border_color": self.COLOR_BORDER
        }

        # =========================
        # FIELD HELPER (HATASIZ)
        # =========================
        def add_field(parent, label, widget, row, col):

            ctk.CTkLabel(
                parent,
                text=label,
                font=self.FONT_LABEL,
                text_color="#334155"
            ).grid(row=row*2, column=col, sticky="w", padx=10, pady=(10, 2))

            # ===================== COMBOBOX ÖZEL DÜZEN =====================
            if isinstance(widget, ctk.CTkComboBox):
                widget.configure(
                    height=38,
                    corner_radius=8,
                    fg_color="#FFFFFF",
                    border_color=self.COLOR_BORDER,
                    button_color=self.COLOR_PRIMARY,
                    button_hover_color=self.COLOR_PRIMARY_HOVER,
                    dropdown_fg_color="#FFFFFF"
                )
            else:
                widget.configure(**self.INPUT_STYLE)

            widget.grid(
                row=row*2+1,
                column=col,
                padx=10,
                pady=(0, 10),
                sticky="ew"
            )


        self.add_field = add_field

        # =========================
        # CARD BUILDER
        # =========================
        def create_card(parent, title):
            card = ctk.CTkFrame(
                parent,
                fg_color=self.COLOR_CARD,
                corner_radius=14,
                border_width=1,
                border_color=self.COLOR_BORDER
            )
            card.pack(fill="x", padx=10, pady=8)

            ctk.CTkLabel(
                card,
                text=title,
                font=("Segoe UI", 13, "bold"),
                text_color=self.COLOR_TEXT
            ).pack(anchor="w", padx=15, pady=(10, 5))

            body = ctk.CTkFrame(card, fg_color="transparent")
            body.pack(fill="x", padx=10, pady=10)

            body.grid_columnconfigure((0,1,2), weight=1)

            return body

        self.create_card = create_card

        # =========================
        # 🟦 CARD 1 - İŞ BİLGİLERİ
        # =========================
        body1 = self.create_card(self.tab1_root, "💼 İş Bilgileri")

        self.gorev_combo = ctk.CTkComboBox(body1, values=["Kalıp Ustası", "Düz İşçi", "Mühendis", "Mimar", "İdari Pers.", "Parsel Şef", "Şantiye Şef", "Formen", "Teknik", "Formen", "Şenör"])
        self.dept_combo = ctk.CTkComboBox(body1, values=["Şantiye", "Ofis"])
        self.ise_giris_entry = ctk.CTkEntry(body1)

        self.ucret_tipi_combo = ctk.CTkComboBox(body1, values=["Aylık", "Günlük", "Saatlik"])
        self.maas_entry = ctk.CTkEntry(body1)
        self.sgk_combo = ctk.CTkComboBox(body1, values=["SGK'lı", "Sigortasız", "Stajyer"])

        self.add_field(body1, "Görev", self.gorev_combo, 0, 0)
        self.add_field(body1, "Departman", self.dept_combo, 0, 1)
        self.add_field(body1, "İşe Giriş", self.ise_giris_entry, 0, 2)

        self.add_field(body1, "Ücret Tipi", self.ucret_tipi_combo, 1, 0)
        self.add_field(body1, "Brüt Maaş", self.maas_entry, 1, 1)
        self.add_field(body1, "SGK", self.sgk_combo, 1, 2)

        self.durum_switch = ctk.CTkSwitch(
            body1, 
            text="Aktif", 
            command=self.durum_degistir,
            font=("Segoe UI", 11, "bold"),
            progress_color="#22c55e" # İlk açılışta yeşil başlasın
        )
        self.durum_switch.select() # Varsayılan olarak açık (Aktif) başlasın
        self.durum_switch.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        self.sigorta_giris_entry = ctk.CTkEntry(body1)
        self.isten_cikis_entry = ctk.CTkEntry(body1)

        self.add_field(body1, "Sigorta Giriş", self.sigorta_giris_entry, 2, 1)
        self.add_field(body1, "İşten Çıkış", self.isten_cikis_entry, 2, 2)

        # =========================
        # 🟨 CARD 2 - BANKA
        # =========================
        body2 = self.create_card(self.tab2_root, "🏦 Banka Bilgileri")

        self.banka_adi_entry = ctk.CTkEntry(body2)
        self.sube_adi_entry = ctk.CTkEntry(body2)
        self.iban_no_entry = ctk.CTkEntry(body2)

        self.add_field(body2, "Banka Adı", self.banka_adi_entry, 0, 0)
        self.add_field(body2, "Şube Adı", self.sube_adi_entry, 0, 1)
        self.add_field(body2, "IBAN", self.iban_no_entry, 1, 0)
    
    def secili_personelleri_getir(self):
        secilenler = []
        # personel_frame içindeki tüm satırları (satir frame'leri) gez
        for satir in self.personel_frame.winfo_children():
            # Satır içindeki tüm widget'ları tara (ust_katman içindekileri bulmak için)
            for ust_katman in satir.winfo_children():
                # Eğer bu widget bir frame ise (ust_katman), onun içindeki checkbox'ı ara
                if isinstance(ust_katman, ctk.CTkFrame):
                    for widget in ust_katman.winfo_children():
                        if isinstance(widget, ctk.CTkCheckBox) and widget.get() == 1:
                            if hasattr(widget, 'personel_data'):
                                secilenler.append(widget.personel_data)
        return secilenler
    def turkce_karakter_duzelt(self, metin):
            mapping = {
                'ç': 'c', 'Ç': 'C', 'ğ': 'g', 'Ğ': 'G', 'ı': 'i', 'İ': 'I',
                'ö': 'o', 'Ö': 'O', 'ş': 's', 'Ş': 'S', 'ü': 'u', 'Ü': 'U'
            }
            for tr, eng in mapping.items():
                metin = metin.replace(tr, eng)
            return metin

        # Kullanımı:
            ad_soyad = self.turkce_karakter_duzelt(f"{p.get('ad', '')} {p.get('soyad', '')}")
            pdf.cell(50, 10, ad_soyad, 1)

    def pdf_rapor_olustur(self):
        from fpdf import FPDF
        from tkinter import messagebox
        from datetime import datetime
        import os

        secili_olanlar = self.secili_personelleri_getir()

        if not secili_olanlar:
            messagebox.showwarning(
                "Uyarı",
                "Lütfen önce en az bir personel seçin!"
            )
            return

        pdf = FPDF(
            orientation="L",
            unit="mm",
            format="A4"
        )

        # FONTLAR
        proje_klasoru = r"C:\Users\DELL\source\repos\santiyePROGRAM"

        font_path = os.path.join(proje_klasoru, "DejaVuSans.ttf")
        bold_font_path = os.path.join(proje_klasoru, "DejaVuSans-Bold.ttf")

        pdf.add_font("DejaVu", "", font_path, uni=True)
        pdf.add_font("DejaVu", "B", bold_font_path, uni=True)

        pdf.add_page()

        # ====================================================
        # LOGO
        # ====================================================

        logo_path = os.path.join(
            proje_klasoru,
            "logo-kibritci.png"
        )

        # ÜST MAVİ BANT
        pdf.set_fill_color(18, 52, 86)
        pdf.rect(0, 0, 297, 30, "F")

        if os.path.exists(logo_path):
            pdf.image(logo_path, 8, 4, 20)

        # BAŞLIK
        pdf.set_text_color(255, 255, 255)

        pdf.set_xy(35, 7)
        pdf.set_font("DejaVu", "B", 18)
        pdf.cell(
            180,
            8,
            "KIBRITCI INSAAT",
            0,
            0,
            "L"
        )

        pdf.set_xy(35, 16)
        pdf.set_font("DejaVu", "", 10)
        pdf.cell(
            180,
            6,
            "PERSONEL DETAY RAPORU",
            0,
            0,
            "L"
        )

        pdf.set_xy(235, 8)
        pdf.set_font("DejaVu", "", 9)
        pdf.cell(
            50,
            5,
            f"Tarih : {datetime.now().strftime('%d.%m.%Y')}",
            0,
            2,
            "R"
        )

        pdf.cell(
            50,
            5,
            f"Saat : {datetime.now().strftime('%H:%M')}",
            0,
            0,
            "R"
        )

        # ====================================================
        # ÖZET KUTULARI
        # ====================================================

        pdf.ln(25)

        toplam_maas = 0

        for p in secili_olanlar:
            try:
                toplam_maas += float(
                    str(
                        p.get("maas", 0)
                    ).replace(",", ".")
                )
            except:
                pass

        pdf.set_fill_color(245, 247, 250)

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("DejaVu", "B", 10)

        pdf.cell(
            70,
            12,
            f"TOPLAM PERSONEL : {len(secili_olanlar)}",
            1,
            0,
            "C",
            True
        )

        pdf.cell(10)

        pdf.cell(
            90,
            12,
            f"TOPLAM MAAS : {toplam_maas:,.2f} TL",
            1,
            1,
            "C",
            True
        )

        pdf.ln(8)

        # ====================================================
        # TABLO
        # ====================================================

        headers = [
            "AD SOYAD",
            "TC NO",
            "TELEFON",
            "CINSIYET",
            "DOGUM TAR.",
            "ISE GIRIS",
            "MAAS",
            "IBAN"
        ]

        widths = [
            45,
            30,
            30,
            20,
            25,
            25,
            25,
            70
        ]

        pdf.set_fill_color(31, 78, 121)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("DejaVu", "B", 9)

        for i, header in enumerate(headers):
            pdf.cell(
                widths[i],
                10,
                header,
                1,
                0,
                "C",
                True
            )

        pdf.ln()

        # ====================================================
        # SATIRLAR
        # ====================================================

        pdf.set_font("DejaVu", "", 8)

        for i, p in enumerate(secili_olanlar):

            if i % 2 == 0:
                pdf.set_fill_color(255, 255, 255)
            else:
                pdf.set_fill_color(245, 247, 250)

            pdf.set_text_color(40, 40, 40)

            pdf.cell(
                widths[0],
                9,
                f"{p.get('ad','')} {p.get('soyad','')}",
                1,
                0,
                "L",
                True
            )

            pdf.cell(
                widths[1],
                9,
                str(p.get("tc_no", "-")),
                1,
                0,
                "C",
                True
            )

            pdf.cell(
                widths[2],
                9,
                str(p.get("telefon", "-")),
                1,
                0,
                "C",
                True
            )

            pdf.cell(
                widths[3],
                9,
                str(p.get("cinsiyet", "-")),
                1,
                0,
                "C",
                True
            )

            pdf.cell(
                widths[4],
                9,
                str(p.get("dogum_tarihi", "-")),
                1,
                0,
                "C",
                True
            )

            pdf.cell(
                widths[5],
                9,
                str(p.get("ise_giris", "-")),
                1,
                0,
                "C",
                True
            )

            # Maaş Yeşil
            pdf.set_text_color(0, 130, 0)

            pdf.cell(
                widths[6],
                9,
                f"{p.get('maas','0')} TL",
                1,
                0,
                "C",
                True
            )

            pdf.set_text_color(40, 40, 40)

            pdf.cell(
                widths[7],
                9,
                str(p.get("iban", "-")),
                1,
                1,
                "C",
                True
            )

        # ====================================================
        # FOOTER
        # ====================================================

        pdf.set_y(-15)

        pdf.set_draw_color(220, 220, 220)

        pdf.line(
            10,
            pdf.get_y(),
            287,
            pdf.get_y()
        )

        pdf.set_font("DejaVu", "", 8)

        pdf.set_text_color(120, 120, 120)

        pdf.cell(
            0,
            8,
            "Kibritci Insaat | Personel Takip Sistemi",
            0,
            0,
            "C"
        )

        # ====================================================
        # KAYDET
        # ====================================================

        masaustu = os.path.join(
            os.path.expanduser("~"),
            "Desktop"
        )

        dosya_adi = (
            f"Kibritci_Personel_Raporu_"
            f"{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        )

        pdf.output(
            os.path.join(
                masaustu,
                dosya_adi
            )
        )

        messagebox.showinfo(
            "Başarılı",
            f"Rapor oluşturuldu.\n\n{dosya_adi}"
        )

    def durum_degistir(self):
        if self.durum_switch.get() == 1:
            # Aktifse: Yeşil progress çubuğu ve yeşil yazı
            self.durum_switch.configure(text="Aktif", progress_color="#22c55e", text_color="#16a34a")
        else:
            # Pasifse: Kırmızı progress çubuğu ve kırmızı yazı
            self.durum_switch.configure(text="Pasif", progress_color="#ef4444", text_color="#dc2626")            

    def iban_cozumle(self, event):
        iban = self.iban_no_entry.get().replace(" ", "").upper()
        if len(iban) >= 26: # Basit bir uzunluk kontrolü
            # TR ile başlıyorsa örnek ayrıştırma
            self.banka_adi_entry.delete(0, 'end')
            self.banka_adi_entry.insert(0, "Otomatik Ayrıştırıldı") # Buraya kendi banka kod listeni bağlayabilirsin

    def secili_duzenle(self):
        # Tüm checkboxları tara, işaretli olanı bul
        for widget in self.personel_frame.winfo_children():
            # widget'in içindeki checkbox'ı bul (winfo_children ile)
            cb = widget.winfo_children()[0] 
            if isinstance(cb, ctk.CTkCheckBox) and cb.get() == 1:
                self.verileri_yukari_aktar(cb.personel_data)
                return
    def duzenle_secili(self):
        # Seçili olanları topla
        secilenler = []
        for widget in self.personel_frame.winfo_children():
            checkbox = next((w for w in widget.winfo_children() if isinstance(w, ctk.CTkCheckBox)), None)
            if checkbox and checkbox.get() == 1:
                secilenler.append(checkbox.personel_data)
        
        # Hata Yönetimi
        if len(secilenler) == 0:
            messagebox.showwarning("Uyarı", "Lütfen düzenlemek için bir personel seçin!")
        elif len(secilenler) > 1:
            messagebox.showerror("Hata", "Aynı anda sadece bir personel düzenlenebilir!")
        else:
            self.verileri_yukari_aktar(secilenler[0])

    
    def yeni_personel_penceresini_ac(self):
        # Pencere sınıfını burada çağırıyoruz
        pencere = PersonelEklePenceresi(self.winfo_toplevel(), refresh_callback=self.tabloyu_guncelle)

    def tabloyu_guncelle(self):
        # Listeyi temizle
        for widget in self.personel_frame.winfo_children():
            widget.destroy()

        arama_metni = self.arama_entry.get().lower() if hasattr(self, 'arama_entry') else ""

        try:
            personeller = personel_listele()
            if not personeller:
                return

            for p in personeller:
                ad_soyad = f"{p.get('ad', '').lower()} {p.get('soyad', '').lower()}"
                if arama_metni not in ad_soyad:
                    continue

                durum = p.get('durum')
                is_aktif = (durum == True or durum == 1)

                # =========================
                # SATIR
                # =========================
                satir = ctk.CTkFrame(
                    self.personel_frame,
                    height=90,
                    corner_radius=12,
                    fg_color="white",
                    border_width=1,
                    border_color="#E2E8F0"
                )
                satir.pack(fill="x", pady=5, padx=5)
                satir.pack_propagate(False)

                # =========================
                # HOVER EFEKTİ
                # =========================
                def on_enter(e, w=satir):
                    w.configure(fg_color="#F1F5F9")

                def on_leave(e, w=satir):
                    if cb.get() != 1:  # Seçili değilse beyaza dön
                        w.configure(fg_color="white")
                    else:
                        w.configure(fg_color="#EFF6FF")

                satir.bind("<Enter>", on_enter)
                satir.bind("<Leave>", on_leave)

                # =========================
                # ÜST KATMAN
                # =========================
                ust_katman = ctk.CTkFrame(satir, fg_color="transparent", height=35)
                ust_katman.pack(fill="x", side="top", padx=5, pady=(5, 0))
                ust_katman.pack_propagate(False)

                # Checkbox
                cb = ctk.CTkCheckBox(
                    ust_katman,
                    text="",
                    width=20,
                    checkbox_width=16,
                    checkbox_height=16
                )
                cb.pack(side="left", padx=(5, 10))
                cb.personel_data = p

                # seçim highlight
                def toggle_select():
                    if cb.get() == 1:
                        satir.configure(border_color="#2563EB", fg_color="#EFF6FF")
                    else:
                        satir.configure(border_color="#E2E8F0", fg_color="white")

                cb.configure(command=toggle_select)

                # ==========================================
                # GERİ GETİRİLEN İŞLEM BUTONLARI Panelİ
                # ==========================================
                btn_frame = ctk.CTkFrame(ust_katman, fg_color="transparent")
                btn_frame.pack(side="right", padx=5)

                # 1. Düzenle Butonu (✏)
                ctk.CTkButton(
                    btn_frame,
                    text="✏ Düzenle",
                    width=75,
                    height=26,
                    fg_color="#E3F2FD",
                    text_color="#1976D2",
                    font=("Segoe UI", 10, "bold"),
                    command=lambda data=p: self.verileri_yukari_aktar(data)
                ).pack(side="left", padx=2)
                
                # 2. Sil Butonu (🗑)
                ctk.CTkButton(
                    btn_frame,
                    text="🗑 Sil",
                    width=55,
                    height=26,
                    fg_color="#FFEBEE",
                    text_color="#D32F2F",
                    font=("Segoe UI", 10, "bold"),
                    command=lambda data=p: self.personeli_sil_onayli(data)
                ).pack(side="left", padx=2)

                # 3. Pasife Al / Pasif Durum Butonu
                if is_aktif:
                    ctk.CTkButton(
                        btn_frame,
                        text="⛔ Pasife Al",
                        width=85,
                        height=26,
                        fg_color="#FEE2E2",
                        text_color="#B91C1C",
                        font=("Segoe UI", 10, "bold"),
                        command=lambda data=p: self.pasife_al_tarih_penceresi(data)
                    ).pack(side="left", padx=2)
                else:
                    ctk.CTkButton(
                        btn_frame,
                        text="✓ Pasif",
                        width=75,
                        height=26,
                        fg_color="#F3F4F6",
                        text_color="#9CA3AF",
                        font=("Segoe UI", 10, "bold"),
                        state="disabled"
                    ).pack(side="left", padx=2)

                # =========================
                # ALT KATMAN
                # =========================
                alt_katman = ctk.CTkFrame(satir, fg_color="transparent", height=40)
                alt_katman.pack(fill="x", side="bottom", padx=5, pady=(0, 5))
                alt_katman.pack_propagate(False)

                # 👤 AD SOYAD
                ctk.CTkLabel(
                    alt_katman,
                    text=f"👤 {p.get('ad','').upper()} {p.get('soyad','').upper()}",
                    font=("Segoe UI", 11, "bold"),
                    text_color="#0F172A"
                ).pack(side="left", padx=(20, 10))

                # 🪪 TC
                ctk.CTkLabel(
                    alt_katman,
                    text=f"🪪 {p.get('tc_no', '-')}",
                    font=("Segoe UI", 10),
                    text_color="#475569"
                ).pack(side="left", padx=10)

                # 💰 MAAŞ
                ctk.CTkLabel(
                    alt_katman,
                    text=f"💰 {p.get('maas', '0')} ₺",
                    font=("Segoe UI", 11, "bold"),
                    text_color="#16A34A"
                ).pack(side="right", padx=10)

                # =========================
                # STATUS BADGE
                # =========================
                status_text = "Aktif" if is_aktif else "Pasif"
                status_color = "#16A34A" if is_aktif else "#DC2626"

                ctk.CTkLabel(
                    alt_katman,
                    text=status_text,
                    width=65,
                    height=22,
                    corner_radius=10,
                    fg_color=status_color,
                    text_color="white",
                    font=("Segoe UI", 10, "bold")
                ).pack(side="right", padx=8)

        except Exception as e:
            print(f"Tablo güncelleme hatası: {e}")


    def verileri_yukari_aktar(self, p):
        """Seçilen satırdaki veriyi üstteki giriş kutularına taşır."""
        self.secili_personel_id = p.get('id')
        # 1. TÜM ENTRY ALANLARINI TEMİZLE
        entry_listesi = [
            self.tc_entry, self.ad_entry, self.soyad_entry, self.baba_entry, 
            self.tel_entry, self.email_entry, self.adres_entry, self.il_entry, 
            self.ilce_entry, self.maas_entry, self.isten_cikis_entry, 
            self.banka_adi_entry, self.sube_adi_entry, self.iban_no_entry,
            self.ise_giris_entry, self.sigorta_giris_entry, self.dogum_entry
        ]
            
        for entry in entry_listesi:
            if hasattr(entry, 'delete'):
                entry.delete(0, 'end')

        # 2. VERİLERİ YERLEŞTİR
        self.tc_entry.insert(0, str(p.get('tc_no', '')))
        self.ad_entry.insert(0, str(p.get('ad', '')))
        self.soyad_entry.insert(0, str(p.get('soyad', '')))
        self.baba_entry.insert(0, str(p.get('baba_adi', '')))
        self.dogum_entry.insert(0, str(p.get('dogum_tarihi', '')))
        self.tel_entry.insert(0, str(p.get('telefon_no', '')))
        self.email_entry.insert(0, str(p.get('eposta', '')))
        self.adres_entry.insert(0, str(p.get('adres', '')))
        self.il_entry.insert(0, str(p.get('adres_il', '')))
        self.ilce_entry.insert(0, str(p.get('adres_ilce', '')))
        self.maas_entry.insert(0, str(p.get('maas', '')))
        self.isten_cikis_entry.insert(0, str(p.get('isten_cikis_tarihi', '')))
        self.ise_giris_entry.insert(0, str(p.get('ise_giris_tarihi', '')))
        self.sigorta_giris_entry.insert(0, str(p.get('sigorta_giris_tarihi', '')))
        self.banka_adi_entry.insert(0, str(p.get('banka_adi', '')))
        self.sube_adi_entry.insert(0, str(p.get('sube_adi', '')))
        self.iban_no_entry.insert(0, str(p.get('iban_no', '')))

        # --- FOTOĞRAF YÜKLEME (GÜNCEL HATA GİDERİCİ) ---
        # Önce eski referansı serbest bırak
        self.photo_img = None
        # image="" ile bağlantıyı kesiyoruz (None yerine boş string kullanın)
        self.photo_label.configure(image="", text="Fotoğraf Yok")
        
        fotograf_yolu = p.get('fotograf_url') or p.get('fotograf')
        
        if fotograf_yolu and str(fotograf_yolu).strip() != "" and str(fotograf_yolu) != "None":
            try:
                from PIL import Image
                import os
                if os.path.exists(fotograf_yolu):
                    img = Image.open(fotograf_yolu)
                    img = img.resize((140, 140))
                    
                    # Resmi sınıfın bir parçası yapıyoruz (Garbage Collector'a takılmasın diye)
                    self.photo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(140, 140))
                    self.photo_label.configure(image=self.photo_img, text="")
                else:
                    self.photo_label.configure(image="", text="Dosya Yok")
            except Exception as e:
                print(f"Fotoğraf yüklenemedi: {e}")
                self.photo_label.configure(image="", text="Fotoğraf Yok")
        else:
            self.photo_label.configure(image="", text="Fotoğraf Yok")

        # 3. GÜVENLİ COMBOBOX ATAMALARI
        self.combobox_set_guvenli(self.cinsiyet_combo, p.get('cinsiyet', 'Erkek'))
        self.combobox_set_guvenli(self.gorev_combo, p.get('gorev', 'Düz İşçi'))
        self.combobox_set_guvenli(self.dept_combo, p.get('departman', 'Şantiye'))
        self.combobox_set_guvenli(self.sgk_combo, p.get('sgk_durumu', 'SGK\'lı'))
        self.combobox_set_guvenli(self.ucret_tipi_combo, p.get('ucret_tipi', 'Aylık'))

        # --- ESKİ SATIRIN YERİNE GELECEK GÜNCEL KOD ---
        durum = p.get('durum')
        is_aktif = (durum == True or durum == 1 or str(durum).lower() == 'true')

        if is_aktif:
            self.durum_switch.select()   # Anahtarı sağa çek (Aktif konumu)
        else:
            self.durum_switch.deselect() # Anahtarı sola çek (Pasif konumu)
        
        # Switch konumu değiştikten sonra renk ve metni (Yeşil/Kırmızı) güncelliyoruz
        self.durum_degistir()

    def combobox_set_guvenli(self, combo_widget, deger):
        """Combobox'a güvenli veri atama fonksiyonu."""
        try:
            mevcut_degerler = list(combo_widget.cget("values"))
            deger = str(deger) if deger is not None else ""
                
            if deger and deger not in mevcut_degerler:
                mevcut_degerler.append(deger)
                combo_widget.configure(values=mevcut_degerler)
                    
            combo_widget.set(deger)
        except Exception as e:
            print(f"Set hatası: {e}")

    def pasife_al_tarih_penceresi(self, p):
        """Pasife almadan önce tarih seçtiren küçük pencere."""
        tarih_penceresi = ctk.CTkToplevel(self)
        tarih_penceresi.title("İşten Çıkış Tarihi")
        tarih_penceresi.geometry("300x200")
        tarih_penceresi.attributes("-topmost", True)

        ctk.CTkLabel(tarih_penceresi, text="Lütfen çıkış tarihini seçin:").pack(pady=10)
        
        # Tarih girişi (Varsayılan olarak bugünün tarihi)
        tarih_entry = ctk.CTkEntry(tarih_penceresi, placeholder_text="YYYY-MM-DD")
        tarih_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        tarih_entry.pack(pady=10)

        def kaydet_ve_pasif_yap():
            secilen_tarih = tarih_entry.get()
            # Supabase güncelleme fonksiyonunu çağırıyoruz
            # Not: 'personel_pasif_yap' fonksiyonunun db_manager'da olduğunu varsaydım
            from db_manager import personel_pasif_yap 
            if personel_pasif_yap(p.get('id'), secilen_tarih):
                messagebox.showinfo("Başarılı", "Personel pasife alındı.")
                tarih_penceresi.destroy()
                self.tabloyu_guncelle() # Listeyi yenile
            else:
                messagebox.showerror("Hata", "Veritabanı güncellenemedi.")

        ctk.CTkButton(tarih_penceresi, text="Pasife Al", fg_color="#c0392b", command=kaydet_ve_pasif_yap).pack(pady=10)


    def personeli_sil_onayli(self, personel_data):
        # Ensure 'id' key exists and matches your Supabase column name exactly
        p_id = personel_data.get('id') 
    
        if p_id is None:
            print(f"CRITICAL ERROR: 'id' key missing. Data: {personel_data}")
            messagebox.showerror("Hata", "Personel ID bilgisi alınamadı!")
            return

        if messagebox.askyesno("Silme Onayı", "Bu personeli kalıcı olarak silmek istiyor musunuz?"):
            try:
                # Call the imported function
                response = personel_sil(p_id) 
            
                # Check if Supabase actually returned data (or acknowledged the delete)
                # Depending on your supabase-py version, checking if it crashed is usually enough
                self.after(200, self.tabloyu_guncelle)
                messagebox.showinfo("Başarılı", "Personel sistemden silindi.")
            except Exception as e:
                messagebox.showerror("Hata", f"Silme işlemi başarısız: {e}")



    def personeli_guncelle_islem(self):
        if not hasattr(self, 'secili_personel_id') or self.secili_personel_id is None:
            messagebox.showwarning("Uyarı", "Lütfen önce listeden bir personel seçin!")
            return

        # Formdan güncel verileri topla
        # Not: Entry isimlerinin `self.ad_entry` vb. ile aynı olduğundan emin ol
        guncel_data = {
        "tc_no": self.tc_entry.get(),
        "ad": self.ad_entry.get(),
        "soyad": self.soyad_entry.get(),
        "baba_adi": self.baba_entry.get(),
        # TARİH ALANLARINI TEMİZLE
        "dogum_tarihi": self.temizle_tarih(self.dogum_entry.get()),
        "telefon_no": self.tel_entry.get(),
        "eposta": self.email_entry.get(),
        "adres": self.adres_entry.get(),
        "adres_il": self.il_entry.get(),
        "adres_ilce": self.ilce_entry.get(),
        "gorev": self.gorev_combo.get(),
        "departman": self.dept_combo.get(),
        "ise_giris_tarihi": self.temizle_tarih(self.ise_giris_entry.get()),
        "maas": float(self.maas_entry.get()) if self.maas_entry.get() else 0, # Maaş sayısal olmalı
        "sigorta_giris_tarihi": self.temizle_tarih(self.sigorta_giris_entry.get()),
        "isten_cikis_tarihi": self.temizle_tarih(self.isten_cikis_entry.get()),
        "banka_adi": self.banka_adi_entry.get(),
        "sube_adi": self.sube_adi_entry.get(),
        "iban_no": self.iban_no_entry.get(),
        "durum": True if self.durum_switch.get() == 1 else False
    }

        if messagebox.askyesno("Güncelleme Onayı", "Personel bilgilerini kaydetmek istiyor musunuz?"):
            # db_manager'daki fonksiyonu çağırıyoruz
            basarili, sonuc = personel_guncelle(self.secili_personel_id, guncel_data)
        
            if basarili:
                messagebox.showinfo("Başarılı", "Personel bilgileri güncellendi.")
                self.tabloyu_guncelle() # Listeyi yenile
            else:
                messagebox.showerror("Hata", f"Güncelleme başarısız: {sonuc}")

    def temizle_tarih(self, value):
        # Eğer değer boşsa veya "None" stringi ise None döndür (Supabase bunu NULL yapar)
        if not value or str(value).strip() == "" or str(value).lower() == "none":
            return None
        return value


    def formu_ve_listeyi_sifirla(self):
        # 1. Seçimi sıfırla
        self.secili_personel_id = None
    
        # 2. Formdaki tüm giriş alanlarını temizle (verileri_yukari_aktar'da kullandığın liste ile aynı)
        entry_listesi = [
            self.tc_entry, self.ad_entry, self.soyad_entry, self.baba_entry, 
            self.tel_entry, self.email_entry, self.adres_entry, self.il_entry, 
            self.ilce_entry, self.maas_entry, self.isten_cikis_entry, 
            self.banka_adi_entry, self.sube_adi_entry, self.iban_no_entry,
            self.ise_giris_entry, self.sigorta_giris_entry, self.dogum_entry
        ]
    
        for entry in entry_listesi:
            if hasattr(entry, 'delete'):
                entry.delete(0, 'end')
            
        # 3. Combobox'ları varsayılan değerine çek (veya boşalt)
        self.gorev_combo.set("Kalıp Ustası") 
        # ... diğer comboboxlar için de benzeri ...
    
        # 4. Fotoğraf alanını temizle
        self.photo_label.configure(image="", text="Fotoğraf Yok")
        self.photo_img = None
    
        # 5. Tabloyu en güncel haliyle veritabanından tekrar çek
        self.tabloyu_guncelle()
    
        print("Form sıfırlandı ve tablo yenilendi.")