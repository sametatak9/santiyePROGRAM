import customtkinter as ctk
from tkinter import messagebox, StringVar
from tkcalendar import DateEntry
from db_manager import personel_kaydet
from tkinter import filedialog
import os


class PersonelEklePenceresi(ctk.CTkToplevel):
    def __init__(self, parent, refresh_callback):
        super().__init__(parent)

        self.title("Yeni Personel Kaydı")
        self.geometry("820x780")

        self.attributes("-topmost", True)
        self.grab_set()

        self.refresh_callback = refresh_callback
        self.fotograf_yolu = ""

        # ======================
        # STYLE
        # ======================
        self.BG = "#F1F5F9"
        self.CARD = "#FFFFFF"
        self.BORDER = "#E2E8F0"
        self.TEXT = "#0F172A"
        self.PRIMARY = "#2563EB"

        self.configure(fg_color=self.BG)

        self.tc_var = StringVar()
        self.tc_var.trace_add("write", lambda *args: self.kisitla(self.tc_var, 11, True))

        self.iban_var = StringVar(value="TR")
        self.iban_var.trace_add("write", lambda *args: self.iban_kisitla())

        # ======================
        # HEADER
        # ======================
        header = ctk.CTkFrame(
            self,
            fg_color=self.CARD,
            corner_radius=14,
            border_width=1,
            border_color=self.BORDER
        )
        header.pack(fill="x", padx=15, pady=12)

        ctk.CTkLabel(
            header,
            text="👤 Yeni Personel Kayıt Formu",
            font=("Segoe UI", 18, "bold"),
            text_color=self.TEXT
        ).pack(side="left", padx=15, pady=12)

        # ======================
        # SCROLL
        # ======================
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        form_card = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=self.CARD,
            corner_radius=16,
            border_width=1,
            border_color=self.BORDER
        )
        form_card.pack(fill="x", padx=5, pady=10)

        form_inner = ctk.CTkFrame(form_card, fg_color="transparent")
        form_inner.pack(fill="x", padx=15, pady=15)

        self.fields = {}

        columns = [
            ("TC KİMLİK NO", "tc_no"),
            ("ADI", "ad"),
            ("SOYADI", "soyad"),
            ("BABA ADI", "baba_adi"),
            ("DOĞUM TARİHİ", "dogum_tarihi"),
            ("TELEFON", "telefon_no"),
            ("E-POSTA", "eposta"),
            ("ADRES", "adres"),
            ("İL", "adres_il"),
            ("İLÇE", "adres_ilce"),
            ("DEPARTMAN", "departman"),
            ("İSE GİRİŞ TARİHİ", "ise_giris_tarihi"),
            ("IBAN", "iban_no"),
            ("BANKA ADI", "banka_adi"),
            ("ŞUBE ADI", "sube_adi"),
            ("MAAŞ", "maas")
        ]

        for i, (label_text, key) in enumerate(columns):

            row = ctk.CTkFrame(form_inner, fg_color="transparent")
            row.pack(fill="x", pady=6)

            ctk.CTkLabel(
                row,
                text=label_text,
                width=160,
                anchor="w",
                text_color="#334155",
                font=("Segoe UI", 11, "bold")
            ).pack(side="left")

            # ======================
            # DATE FIX (NEW STYLE)
            # ======================
            if key in ["dogum_tarihi", "ise_giris_tarihi"]:

                wrapper = ctk.CTkFrame(row, fg_color="transparent")
                wrapper.pack(side="left", fill="x", expand=True)

                entry = DateEntry(
                    wrapper,
                    width=30,
                    date_pattern="yyyy-mm-dd",
                    background="white",
                    foreground="black",
                    borderwidth=0
                )
                entry.pack(fill="x", ipady=6)

            elif key == "tc_no":
                entry = ctk.CTkEntry(row, width=300, textvariable=self.tc_var)

            elif key == "iban_no":
                entry = ctk.CTkEntry(row, width=300, textvariable=self.iban_var)
                entry.bind("<FocusOut>", self.iban_cozumle)

            else:
                entry = ctk.CTkEntry(row, width=300)
                if key == "telefon_no":
                    entry.insert(0, "+90 ")

            entry.pack(side="left", fill="x", expand=True, ipady=5)
            self.fields[key] = entry

        # ======================
        # EXTRA CARD
        # ======================
        extra_card = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=self.CARD,
            corner_radius=16,
            border_width=1,
            border_color=self.BORDER
        )
        extra_card.pack(fill="x", padx=5, pady=10)

        extra_inner = ctk.CTkFrame(extra_card, fg_color="transparent")
        extra_inner.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(extra_inner, text="GÖREV", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w")
        self.gorev_combo = ctk.CTkComboBox(extra_inner,
            values=["Düz İşçi", "Usta", "Mühendis", "Mimar", "Şöför", "Güvenlik", "İdari", "Depocu", "Kampcı", "Formen", "Ofis", "Şenör"])
        self.gorev_combo.grid(row=1, column=0, padx=10, pady=5)

        ctk.CTkLabel(extra_inner, text="CİNSİYET", font=("Segoe UI", 11, "bold")).grid(row=0, column=1, sticky="w")
        self.cinsiyet_combo = ctk.CTkComboBox(extra_inner, values=["Erkek", "Kadın"])
        self.cinsiyet_combo.grid(row=1, column=1, padx=10, pady=5)

        self.lbl_foto = ctk.CTkLabel(extra_inner, text="📷 Fotoğraf seçilmedi", text_color="#64748B")
        self.lbl_foto.grid(row=2, column=0, columnspan=2, pady=10)

        ctk.CTkButton(
            extra_inner,
            text="Fotoğraf Seç",
            fg_color=self.PRIMARY,
            hover_color="#1D4ED8",
            command=self.foto_sec
        ).grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)

        # ======================
        # SAVE
        # ======================
        ctk.CTkButton(
            self,
            text="KAYDI TAMAMLA",
            height=45,
            fg_color="#16A34A",
            hover_color="#15803D",
            font=("Segoe UI", 14, "bold"),
            command=self.kaydet
        ).pack(fill="x", padx=20, pady=15)

    # ======================
    # LOGIC (AYNI)
    # ======================
    def iban_cozumle(self, event):
        iban = self.iban_var.get().replace(" ", "").upper()
        if len(iban) >= 10:
            banka_kodu = iban[4:9]
            bankalar = {
                "00062": "Garanti BBVA",
                "00015": "Vakıfbank",
                "00012": "Halkbank",
                "00064": "İş Bankası"
            }
            if banka_kodu in bankalar:
                self.fields["banka_adi"].delete(0, 'end')
                self.fields["banka_adi"].insert(0, bankalar[banka_kodu])

    def kisitla(self, var, limit, numeric_only):
        value = var.get()
        if numeric_only and not value.isdigit() and value != "":
            var.set(value[:-1])
        if len(value) > limit:
            var.set(value[:limit])

    def iban_kisitla(self):
        val = self.iban_var.get()
        if not val.startswith("TR"):
            self.iban_var.set("TR" + val.replace("TR", ""))
        if len(val) > 26:
            self.iban_var.set(val[:26])

    def foto_sec(self):
        self.attributes("-topmost", False)
        dosya = filedialog.askopenfilename(filetypes=[("Resimler", "*.png;*.jpg;*.jpeg")])
        if dosya:
            self.fotograf_yolu = dosya
            self.lbl_foto.configure(text=os.path.basename(dosya), text_color="white")
        self.attributes("-topmost", True)

    def kaydet(self):
        self.attributes("-topmost", False)

        data = {
            k: v.get_date().strftime('%Y-%m-%d') if isinstance(v, DateEntry) else v.get().strip()
            for k, v in self.fields.items()
        }

        data["gorev"] = self.gorev_combo.get()
        data["cinsiyet"] = self.cinsiyet_combo.get()
        data["fotograf_url"] = self.fotograf_yolu
        data["durum"] = True

        if len(data["iban_no"]) != 26:
            messagebox.showerror("Hata", "IBAN tam 26 karakter olmalıdır!")
            self.attributes("-topmost", True)
            return

        success, res = personel_kaydet(data)

        if success:
            messagebox.showinfo("Başarılı", "Kayıt başarıyla oluşturuldu.")
            self.refresh_callback()
            self.destroy()
        else:
            messagebox.showerror("Hata", str(res))
            self.attributes("-topmost", True)