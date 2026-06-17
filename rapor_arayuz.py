import customtkinter as ctk
import calendar

from datetime import datetime, date

from tkinter import filedialog, messagebox

from openpyxl import Workbook

from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment,
    Border,
    Side
)

from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter
from excel_rapor import excel_bos_puantaj, excel_dolu_puantaj
from pdf_rapor import pdf_dolu_puantaj
class RaporArayuz(ctk.CTkFrame):

    def __init__(self, master, veri_getir_func):
        super().__init__(master, fg_color="#f6f7fb")

        self.veri_getir = veri_getir_func
        self.personeller = []

        self.cell_w = 28
        self.row_h = 30

        self.gun_sayisi = 0
        self.resmi_tatiller = {
            "2026-01-01",
            "2026-04-23",
            "2026-05-01",
            "2026-05-19",
            "2026-07-15",
            "2026-08-30",
            "2026-10-29",
        }

        self.bayram_gunleri = {
            "2026-03-20",
            "2026-03-21",
            "2026-03-22",
            "2026-03-23",
        }

        self._build()

    # ================= UI =================
    def _build(self):

        # ================= TOP BAR =================
        ust = ctk.CTkFrame(self, fg_color="white", corner_radius=12)
        ust.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(ust, text="📅 Ay").pack(side="left", padx=5)

        self.ay = ctk.CTkComboBox(
            ust,
            values=[str(i) for i in range(1, 13)],
            width=70
        )
        self.ay.set(str(datetime.now().month))
        self.ay.pack(side="left")

        ctk.CTkLabel(ust, text="📆 Yıl").pack(side="left", padx=5)

        self.yil = ctk.CTkComboBox(
            ust,
            values=["2024", "2025", "2026", "2027", "2028"],
            width=90
        )
        self.yil.set(str(datetime.now().year))
        self.yil.pack(side="left")

        ctk.CTkButton(
            ust,
            text="🔎 Filtrele",
            fg_color="#2563eb",
            command=self.yukle
        ).pack(side="left", padx=10)

        # ================= EXPORT BUTTONS =================
        ctk.CTkButton(
            ust,
            text="📄 PDF",
            fg_color="#16a34a",
            command=self.export_pdf
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            ust,
            text="📊 Excel",
            fg_color="#f59e0b",
            command=self.export_menu
        ).pack(side="right", padx=5)
        self.kpi_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.kpi_frame.pack(fill="x", padx=10, pady=(0, 5))

        self.kpi_personel = ctk.CTkLabel(
            self.kpi_frame,
            text="👥 Personel: 0",
            fg_color="#2563eb",
            corner_radius=10,
            height=40
        )
        self.kpi_personel.pack(side="left", padx=5)

        self.kpi_gun = ctk.CTkLabel(
            self.kpi_frame,
            text="📅 Gün: 0",
            fg_color="#16a34a",
            corner_radius=10,
            height=40
        )
        self.kpi_gun.pack(side="left", padx=5)

        self.kpi_mesai = ctk.CTkLabel(
            self.kpi_frame,
            text="⏱ Mesai: 0",
            fg_color="#f59e0b",
            corner_radius=10,
            height=40
        )
        self.kpi_mesai.pack(side="left", padx=5)
        # ================= TABLE FRAME =================
        self.table_frame = ctk.CTkScrollableFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # ================= DATA =================
    def set_personeller(self, personeller):
        self.personeller = personeller

    # ================= LOAD =================
    def yukle(self):
        print(self.personeller[0])
        print(self.personeller[0].keys())
        if self.personeller:

            veri = self.veri_getir(
                self.personeller[0]["id"],
                int(self.yil.get()),
                int(self.ay.get())
            )

            print(veri[:5])
        genel_gun = 0
        genel_mesai = 0
        
        # Önceki arayüz elemanlarını temizle
        for w in self.table_frame.winfo_children():
            w.destroy()

        ay = int(self.ay.get())
        yil = int(self.yil.get())

        self.gun_sayisi = calendar.monthrange(yil, ay)[1]

        # ================= HEADER (BAŞLIK SATIRI) =================
        header = ctk.CTkFrame(self.table_frame, fg_color="#e5e7eb")
        header.pack(fill="x")

        # Sol Başlık: Personel Bilgisi Bölümü
        ctk.CTkLabel(
            header,
            text="Personel Adı / Detay",
            width=180,
            font=("Segoe UI", 11, "bold")
        ).pack(side="left", padx=5)

        gunler = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]

        # Günlük Sütun Başlıklarını Çiz
        for g in range(1, self.gun_sayisi + 1):
            tarih = date(yil, ay, g)
            hafta_gunu = tarih.weekday()
            tarih_str = f"{yil}-{ay:02d}-{g:02d}"

            renk = "#e5e7eb"
            if hafta_gunu == 5:
                renk = "#fef3c7"  # Cumartesi
            elif hafta_gunu == 6:
                renk = "#fee2e2"  # Pazar

            if tarih_str in self.resmi_tatiller:
                renk = "#fde68a"
            if tarih_str in self.bayram_gunleri:
                renk = "#ddd6fe"

            ctk.CTkLabel(
                header,
                text=f"{g:02d}\n{gunler[hafta_gunu]}",
                width=self.cell_w,  # cell_w ile senkronize edildi
                height=40,
                corner_radius=6,
                fg_color=renk,
                font=("Segoe UI", 10, "bold")
            ).pack(side="left", padx=1)

        # Sağ Başlık: Toplamlar Bölümü
        ctk.CTkLabel(
            header,
            text="Toplam",
            width=120,
            font=("Segoe UI", 11, "bold")
        ).pack(side="left", padx=5)

        # ================= PERSONELLER (VERİ SATIRLARI) =================
        for p in self.personeller:
            # Veritabanından çalışanın ilgili ay/yıl verisini çek
            veri = self.veri_getir(p["id"], yil, ay)

            gun_map = {}
            mesai_map = {}

            for v in veri:
                # Tarih formatından gün bilgisini güvenle al
                gun = int(str(v["tarih"]).split("-")[2])
                gun_map[gun] = v.get("durum")
                mesai_map[gun] = float(v.get("mesai_saati") or 0)

            # ================= YOKLAMA SATIRI çerçevesi =================
            row1 = ctk.CTkFrame(
                self.table_frame,
                fg_color="white",
                corner_radius=10,
                border_width=1,
                border_color="#dbeafe"
            )
            row1.pack(fill="x", pady=(2, 0))

            # Satırın soluna Personel İsmini yazdırıyoruz
            ctk.CTkLabel(
                row1,
                text=p.get("ad_soyad", f"Personel (ID: {p['id']})"),
                width=180,
                anchor="w",
                font=("Segoe UI", 11, "bold")
            ).pack(side="left", padx=5)

            # ================= MESAİ SATIRI çerçevesi =================
            row2 = ctk.CTkFrame(
                self.table_frame,
                fg_color="#f8fafc",
                corner_radius=10,
                border_width=1,
                border_color="#e5e7eb"
            )
            row2.pack(fill="x", pady=(0, 4))

            # Alt satırın soluna "Mesai" ibaresini koyuyoruz
            ctk.CTkLabel(
                row2,
                text=" ⏱ Mesai Saati",
                width=180,
                anchor="w",
                text_color="#64748b",
                font=("Segoe UI", 10, "italic")
            ).pack(side="left", padx=5)

            toplam_gun = 0
            toplam_mesai = 0

            # bg_map içine "P" durumu için açık turuncu arka plan rengi eklendi
            bg_map = {
                "G": "#dcfce7",
                "P": "#ffedd5",  # Pazar günü gelenler için soft turuncu arka plan
                "Y": "#fee2e2",
                "İ": "#dbeafe",
                "R": "#fed7aa",
                "-": "#f3f4f6"
            }

            # ================= HÜCRELERİ DÖNGÜDE YAN YANA DİZİYORUZ =================
            for g in range(1, self.gun_sayisi + 1):
                durum = gun_map.get(g)
                
                # Hatanın önlenmesi için txt ve col değişkenlerine varsayılan başlangıç değeri atıyoruz
                txt = "-"
                col = "#9ca3af"
                
                # İlgili günün haftanın hangi günü olduğunu buluyoruz (6 = Pazar)
                hafta_gunu = date(yil, ay, g).weekday()

                # PAZAR GÜNÜ KONTROLÜ VE RENKLENDİRME MANTIĞI
                if durum == "Geldi" and hafta_gunu == 6:
                    txt = "P"
                    col = "#f59e0b"  # Turuncu metin rengi
                    toplam_gun += 1
                    genel_gun += 1
                elif durum == "Geldi":
                    txt = "G"
                    col = "#22c55e"
                    toplam_gun += 1
                    genel_gun += 1
                elif durum == "Yok":
                    txt = "Y"
                    col = "#ef4444"
                elif durum == "İzinli":
                    txt = "İ"
                    col = "#3b82f6"
                elif durum == "Raporlu":
                    txt = "R"
                    col = "#f59e0b"
                else:
                    txt = "-"
                    col = "#9ca3af"

                # YOKLAMA HÜCRESİ (Renkli ve yuvarlatılmış kutu düzeni)
                ctk.CTkLabel(
                    row1,
                    text=txt,
                    width=self.cell_w,
                    height=24,
                    corner_radius=5,
                    fg_color=bg_map.get(txt, "#f3f4f6"),
                    text_color=col,
                    font=("Segoe UI", 10, "bold")
                ).pack(side="left", padx=1)

                # MESAİ HÜCRESİ
                mesai = float(mesai_map.get(g) or 0)
                toplam_mesai += mesai
                genel_mesai += mesai

                ctk.CTkLabel(
                    row2,
                    text=str(mesai) if mesai > 0 else "-",
                    width=self.cell_w,
                    text_color="#475569" if mesai > 0 else "#94a3b8",
                    font=("Segoe UI", 10)
                ).pack(side="left", padx=1)

            # ================= SATIR SONU TOPLAMLARI =================
            ctk.CTkLabel(
                row1,
                text=f"{toplam_gun} Gün",
                width=120,
                font=("Segoe UI", 10, "bold"),
                text_color="#16a34a"
            ).pack(side="left", padx=5)

            ctk.CTkLabel(
                row2,
                text=f"{round(toplam_mesai, 1)} Saat",
                width=120,
                font=("Segoe UI", 10, "bold"),
                text_color="#ea580c"
            ).pack(side="left", padx=5)

        # ================= ÜST KPI PANELİNİ GÜNCELLEME =================
        self.kpi_personel.configure(text=f"👥 Personel: {len(self.personeller)}")
        self.kpi_gun.configure(text=f"📅 Toplam Gün: {genel_gun}")
        self.kpi_mesai.configure(text=f"⏱ Mesai: {round(genel_mesai, 1)}")

    # ================= EXPORT (placeholder) =================

    def export_menu(self):
        secim = ctk.CTkToplevel(self)
        secim.title("Puantaj Türü")
        secim.geometry("300x180")

        secim.transient(self.winfo_toplevel())
        secim.grab_set()
        secim.focus_force()
        secim.lift()
        secim.attributes("-topmost", True)

        ctk.CTkLabel(
            secim,
            text="Oluşturulacak raporu seçiniz",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=20)

        # Aktif seçili ay ve yıl verilerini alıyoruz
        secilen_ay = int(self.ay.get())
        secilen_yil = int(self.yil.get())

        ctk.CTkButton(
            secim,
            text="📄 Boş Puantaj",
            command=lambda: [
                secim.destroy(),
                excel_bos_puantaj(
                    secilen_yil=secilen_yil,
                    secilen_ay=secilen_ay,
                    personeller=self.personeller
                )
            ]
        ).pack(pady=5)

        ctk.CTkButton(
            secim,
            text="📊 Dolu Puantaj (Maaş Evrakı)",
            fg_color="#16a34a",
            command=lambda: [
                secim.destroy(),
                excel_dolu_puantaj(
                    secilen_yil=secilen_yil,
                    secilen_ay=secilen_ay,
                    personeller=self.personeller,
                    veri_getir_func=self.veri_getir
                )
            ]
        ).pack(pady=5)
    def export_pdf(self):
        """Arayüzdeki seçili yıla, aya ve listelenen personellere göre kurumsal PDF çıktısını üretir."""
        # 1. Arayüzdeki ComboBox veya giriş alanlarından seçili ay ve yılı alıyoruz
        secilen_ay = int(self.ay.get())
        secilen_yil = int(self.yil.get())
        
        # 2. Eğer ekranda listelenmiş hiç personel yoksa boşuna işlem yapmaması için uyarı veriyoruz
        if not self.personeller:
            from tkinter import messagebox
            messagebox.showwarning("Uyarı", "Lütfen önce raporu yenileyip personelleri listeleyin.")
            return

        # 3. pdf_rapor.py içindeki fonksiyonu tetikliyoruz. 
        # self.veri_getir fonksiyonunu parametre olarak gönderiyoruz ki PDF modülü arka planda 
        # her personel için db_manager'a gidip yoklama verilerini çekebilsin.
        pdf_dolu_puantaj(
            secilen_yil=secilen_yil,
            secilen_ay=secilen_ay,
            personeller=self.personeller,
            veri_getir_func=self.veri_getir
        )