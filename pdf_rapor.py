import os
import calendar
from datetime import date, datetime
from tkinter import messagebox
from collections import Counter

# ReportLab Temel Bileşenleri
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, KeepTogether
from reportlab.platypus import Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

# TÜRKÇE KARAKTER DESTEĞİ İÇİN FONT KAYDI
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

try:
    font_path_regular = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'arial.ttf')
    font_path_bold = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'arialbd.ttf')
    font_path_italic = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'ariali.ttf')
    
    if not os.path.exists(font_path_regular):
        font_path_regular = "/System/Library/Fonts/Supplemental/Arial.ttf"
        font_path_bold = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
        font_path_italic = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"

    pdfmetrics.registerFont(TTFont('Arial', font_path_regular))
    pdfmetrics.registerFont(TTFont('Arial-Bold', font_path_bold))
    pdfmetrics.registerFont(TTFont('Arial-Italic', font_path_italic))
    FONT_REGULAR = 'Arial'
    FONT_BOLD = 'Arial-Bold'
    FONT_ITALIC = 'Arial-Italic'
except Exception:
    FONT_REGULAR = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold'
    FONT_ITALIC = 'Helvetica-Oblique'


def satin_alma_talep_pdf_olustur(form, kalemler, dosya_yolu):
    doc = SimpleDocTemplate(
        dosya_yolu,
        pagesize=A3,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.8 * cm
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "SATitle",
        parent=styles["Normal"],
        fontName=FONT_BOLD,
        fontSize=20,
        leading=24,
        alignment=1,
        textColor=colors.HexColor("#0F172A")
    )
    label_style = ParagraphStyle(
        "SALabel",
        parent=styles["Normal"],
        fontName=FONT_BOLD,
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#334155")
    )
    text_style = ParagraphStyle(
        "SAText",
        parent=styles["Normal"],
        fontName=FONT_REGULAR,
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#0F172A")
    )
    header_style = ParagraphStyle(
        "SAHeader",
        parent=styles["Normal"],
        fontName=FONT_BOLD,
        fontSize=9,
        leading=11,
        alignment=1,
        textColor=colors.white
    )

    story = []
    logo_yolu = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo-kibritci.png")
    kurum_style = ParagraphStyle(
        "SAKurum",
        parent=styles["Normal"],
        fontName=FONT_BOLD,
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#2E5F7F")
    )
    belge_style = ParagraphStyle(
        "SABelge",
        parent=styles["Normal"],
        fontName=FONT_REGULAR,
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#64748B")
    )

    baslik_blok = [
        Paragraph("KİBRİTÇİ İNŞAAT", kurum_style),
        Spacer(1, 4),
        Paragraph("SATIN ALMA TALEP FORMU", title_style),
        Spacer(1, 4),
        Paragraph("1. Onay ve imza süreci için resmi talep evrakı", belge_style),
    ]

    if os.path.exists(logo_yolu):
        logo = RLImage(logo_yolu, width=7.0 * cm, height=2.6 * cm)
        header_table = Table([[logo, baslik_blok]], colWidths=[8.0 * cm, 20.0 * cm])
    else:
        header_table = Table([[baslik_blok]], colWidths=[28.0 * cm])

    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
        ("LINEBELOW", (0, 0), (-1, -1), 2, colors.HexColor("#7F1D2D")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 14))

    bilgi_data = [
        [
            Paragraph("SA ID", label_style),
            Paragraph(str(form.get("sa_id", "")), text_style),
            Paragraph("Tarih", label_style),
            Paragraph(str(form.get("tarih", "")), text_style),
        ],
        [
            Paragraph("Talep Eden / Hazırlayan", label_style),
            Paragraph(str(form.get("talep_eden", "")), text_style),
            Paragraph("Onay Durumu", label_style),
            Paragraph(str(form.get("onay_durumu", "ONAY BEKLİYOR")), text_style),
        ],
    ]

    bilgi_table = Table(bilgi_data, colWidths=[4 * cm, 10 * cm, 4 * cm, 10 * cm])
    bilgi_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F1F5F9")),
        ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#F1F5F9")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(bilgi_table)
    story.append(Spacer(1, 16))

    kalem_data = [[
        Paragraph("No", header_style),
        Paragraph("Ürün", header_style),
        Paragraph("Marka", header_style),
        Paragraph("Miktar", header_style),
        Paragraph("Birim", header_style),
        Paragraph("Kullanılacak Yer", header_style),
        Paragraph("Açıklama", header_style),
    ]]

    for index, kalem in enumerate(kalemler, start=1):
        kalem_data.append([
            Paragraph(str(index), text_style),
            Paragraph(str(kalem.get("urun_adi", "")), text_style),
            Paragraph(str(kalem.get("marka", "")), text_style),
            Paragraph(str(kalem.get("talep_edilen_miktar", "")), text_style),
            Paragraph(str(kalem.get("talep_birimi", "")), text_style),
            Paragraph(str(kalem.get("kullanilacak_yer", "")), text_style),
            Paragraph(str(kalem.get("aciklama", "")), text_style),
        ])

    kalem_table = Table(
        kalem_data,
        colWidths=[1.2 * cm, 6 * cm, 4 * cm, 3 * cm, 2.5 * cm, 5 * cm, 6.3 * cm],
        repeatRows=1
    )
    kalem_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(kalem_table)
    story.append(Spacer(1, 28))

    imza_baslik = ParagraphStyle(
        "SAImzaBaslik",
        parent=styles["Normal"],
        fontName=FONT_BOLD,
        fontSize=11,
        leading=13,
        alignment=1,
        textColor=colors.HexColor("#334155")
    )
    imza_cizgi = ParagraphStyle(
        "SAImzaCizgi",
        parent=styles["Normal"],
        fontName=FONT_REGULAR,
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#64748B")
    )

    imza_rolleri = ["HAZIRLAYAN", "MUHASEBE", "İDARİ İŞLER", "ŞANTİYE ŞEFİ", "PROJE MÜDÜRÜ"]
    imza_data = [
        [Paragraph(rol, imza_baslik) for rol in imza_rolleri],
        [Paragraph("<br/><br/>İmza<br/>................................", imza_cizgi) for _ in imza_rolleri],
    ]
    imza_table = Table(imza_data, colWidths=[5.6 * cm] * 5)
    imza_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F8FAFC")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(KeepTogether([imza_table]))

    doc.build(story)
    return dosya_yolu


class NumberedCanvas(canvas.Canvas):
    """Her sayfanın altına kurumsal bilgi barını ve dinamik sayfa numaralarını basan sınıf."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont(FONT_REGULAR, 10)
        self.setFillColor(colors.HexColor("#475569"))
        
        # A3 Landscape için net genişlik (42.0 cm)
        width, height = landscape(A3)
        
        # Kurumsal Alt Çizgi
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(1.5 * cm, 1.5 * cm, width - (1.5 * cm), 1.5 * cm)
        
        # Sol Alt Bilgi
        simdi_str = datetime.now().strftime("%d.%m.%Y %H:%M")
        self.drawString(1.5 * cm, 1.0 * cm, f"Rapor Oluşturma Tarihi: {simdi_str}  |  KİBRİTÇİ İNŞAAT ERP İSTATİSTİK MODÜLÜ")
        
        # Sağ Alt Bilgi
        page_text = f"Sayfa {self._pageNumber} / {page_count}"
        self.drawRightString(width - (1.5 * cm), 1.0 * cm, page_text)
        
        self.restoreState()


def pdf_dolu_puantaj(secilen_yil, secilen_ay, personeller, veri_getir_func):
    """Masaüstüne geniş A3 formatında, Yönetici Panelli, kurumsal yeşil tonlu ve mesai toplamlı puantaj üretir."""
    try:
        home = os.path.expanduser("~")
        desktop_path = os.path.join(home, "Desktop")
        if not os.path.exists(desktop_path):
            for alt in ["Masaüstü", os.path.join("OneDrive", "Desktop"), os.path.join("OneDrive", "Masaüstü")]:
                p = os.path.join(home, alt)
                if os.path.exists(p):
                    desktop_path = p
                    break

        dosya_adi = f"Kurumsal_A3_Yonetici_Puantaj_{secilen_yil}_{secilen_ay:02d}.pdf"
        kayit_yolu = os.path.join(desktop_path, dosya_adi)

        # Net Kullanılabilir Yatay Alan: 42.0 - (1.5 + 1.5) = 39.0 cm
        doc = SimpleDocTemplate(
            kayit_yolu,
            pagesize=landscape(A3),
            leftMargin=1.5 * cm,
            rightMargin=1.5 * cm,
            topMargin=1.5 * cm,
            bottomMargin=2.2 * cm
        )

        story = []
        styles = getSampleStyleSheet()

        # --- YAZI STİLLERİ ---
        style_baslik = ParagraphStyle('KB', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=24, leading=28, textColor=colors.HexColor("#1F4E78"))
        style_alt_baslik = ParagraphStyle('KAB', parent=styles['Normal'], fontName=FONT_REGULAR, fontSize=12, leading=16, textColor=colors.HexColor("#475569"))
        style_tablo_header = ParagraphStyle('TH', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=10, leading=12, alignment=1, textColor=colors.white)
        style_personel_ad = ParagraphStyle('PA', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=10, leading=12, textColor=colors.HexColor("#0F172A"))
        style_personel_gorev = ParagraphStyle('PG', parent=styles['Normal'], fontName=FONT_ITALIC, fontSize=9, leading=11, textColor=colors.HexColor("#64748B"))
        style_cell_text = ParagraphStyle('CT', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=10, leading=12, alignment=1)
        style_cell_mesai = ParagraphStyle('CM', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=9.5, leading=11, alignment=1)
        
        # Yönetici Paneli Özel Stilleri
        style_kpi_title = ParagraphStyle('KPIT', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=11, leading=14, textColor=colors.HexColor("#1E3A8A"))
        style_kpi_value = ParagraphStyle('KPIV', parent=styles['Normal'], fontName=FONT_REGULAR, fontSize=10, leading=14, textColor=colors.HexColor("#334155"))

        aylar_tr = {
            1: "OCAK", 2: "ŞUBAT", 3: "MART", 4: "NİSAN", 5: "MAYIS", 6: "HAZİRAN",
            7: "TEMMUZ", 8: "AĞUSTOS", 9: "EYLÜL", 10: "EKİM", 11: "KASIM", 12: "ARALIK"
        }
        secili_ay_adi = aylar_tr.get(secilen_ay, "")

        # --- 1. LOGO VE BAŞLIK ALANI (Genişlik Oranı A3 için Sabitlendi: 39.0 cm) ---
        logo_yolu = "logo-kibritci.png"
        header_data = []
        if os.path.exists(logo_yolu):
            from reportlab.platypus import Image as RLImage
            img = RLImage(logo_yolu, width=4.5 * cm, height=1.5 * cm)
            header_data.append([img, [
                Paragraph("KİBRİTÇİ İNŞAAT A.Ş.", style_baslik),
                Spacer(1, 3),
                Paragraph(f"{secili_ay_adi} {secilen_yil} DÖNEMİ YÖNETİCİ ÖZETLİ AKTİF PUANTAJ RAPORU (A3)", style_alt_baslik)
            ]])
            header_table = Table(header_data, colWidths=[5.0 * cm, 34.0 * cm])
        else:
            header_data.append([[
                Paragraph("KİBRİTÇİ İNŞAAT A.Ş.", style_baslik),
                Spacer(1, 3),
                Paragraph(f"{secili_ay_adi} {secilen_yil} DÖNEMİ YÖNETİCİ ÖZETLİ AKTİF PUANTAJ RAPORU (A3)", style_alt_baslik)
            ]])
            header_table = Table(header_data, colWidths=[39.0 * cm])

        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 15))

        # --- 2. VERİ ÖN HESAPLAMA VE YÖNETİCİ BİLGİ PANELİ ---
        gun_sayisi = calendar.monthrange(secilen_yil, secilen_ay)[1]
        
        toplam_santiye_personel = len(personeller)
        toplam_santiye_mesai = 0.0
        gorev_listesi = []
        personel_veri_havuzu = []
        
        for p in personeller:
            p_id = p.get("id")
            p_gorev = p.get("gorev", "İşçi")
            p_ad = p.get("ad_soyad") if "ad_soyad" in p else f"{p.get('ad', '')} {p.get('soyad', '')}".strip()
            gorev_listesi.append(p_gorev)
            
            gun_map = {}
            mesai_map = {}
            p_toplam_mesai = 0.0
            p_toplam_gun = 0
            
            if veri_getir_func:
                veri = veri_getir_func(p_id, secilen_yil, secilen_ay)
                for v in veri:
                    try:
                        tarih_str = v.get("tarih")
                        gun_no = int(tarih_str.split("-")[2])
                        durum_v = v.get("durum")
                        mesai_v = float(v.get("mesai_saati") or 0)
                        
                        gun_map[gun_no] = durum_v
                        mesai_map[gun_no] = mesai_v
                        
                        p_toplam_mesai += mesai_v
                        if durum_v == "Geldi":
                            p_toplam_gun += 1
                    except Exception:
                        continue
            
            toplam_santiye_mesai += p_toplam_mesai
            personel_veri_havuzu.append({
                "ad": p_ad, "gorev": p_gorev, "gun_map": gun_map, "mesai_map": mesai_map,
                "toplam_gun": p_toplam_gun, "toplam_mesai": p_toplam_mesai
            })

        aritmetik_ort_mesai = (toplam_santiye_mesai / toplam_santiye_personel) if toplam_santiye_personel > 0 else 0.0
        gorev_sayaclari = Counter(gorev_listesi)
        gorev_ozet_str = " | ".join([f"{k}: {v} Kişi" for k, v in gorev_sayaclari.items()])

        kpi_data = [
            [
                Paragraph("📊 ŞANTİYE GENEL DURUMU", style_kpi_title),
                Paragraph("⏱ TOPLAM FAZLA MESAİ", style_kpi_title),
                Paragraph("📈 ARİTMETİK MESAİ ORTALAMASI", style_kpi_title),
                Paragraph("👥 AKTİF GÖREV DAĞILIMI", style_kpi_title)
            ],
            [
                Paragraph(f"<b>Toplam Kadro:</b> {toplam_santiye_personel} Personel", style_kpi_value),
                Paragraph(f"<b>Brüt Fazla Mesai:</b> {round(toplam_santiye_mesai, 1)} Saat", style_kpi_value),
                Paragraph(f"<b>Personel Başına:</b> {round(aritmetik_ort_mesai, 2)} Saat/Ay", style_kpi_value),
                Paragraph(gorev_ozet_str if gorev_ozet_str else "Kayıt Yok", style_kpi_value)
            ]
        ]
        
        # Toplam: 7.0 + 7.5 + 8.5 + 16.0 = 39.0 cm (A3 ile Birebir Uyumlu)
        kpi_table = Table(kpi_data, colWidths=[7.0 * cm, 7.5 * cm, 8.5 * cm, 16.0 * cm])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFF6FF")),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 20))

        # --- 3. PUANTAJ TABLOSU SÜTUN AYARLARI (A3 MİLİMETRİK MATEMATİKSEL SIĞDIRMA) ---
        gunler_kisa = ["Pz", "Sa", "Ça", "Pe", "Cu", "Ct", "Pa"]
        
        # İsim Sütun Genişliği: 6.5 cm
        col_widths = [6.5 * cm]
        
        # Gün hücreleri (Maksimum 31 gün için: 31 * 0.9 cm = 27.9 cm)
        for _ in range(gun_sayisi):
            col_widths.append(0.9 * cm)
            
        # Kalan alan (39.0 - 6.5 - 27.9 = 4.6 cm) Kalan iki sütuna paylaştırılıyor:
        # Toplam Gün: 2.2 cm, Toplam Mesai: 2.4 cm
        col_widths.append(2.2 * cm)
        col_widths.append(2.4 * cm)

        table_data = []
        
        header_row = [Paragraph("Personel Bilgileri / Günler", ParagraphStyle('H1', parent=style_tablo_header, alignment=0))]
        for g in range(1, gun_sayisi + 1):
            hafta_gunu = date(secilen_yil, secilen_ay, g).weekday()
            header_row.append(Paragraph(f"{g:02d}<br/>{gunler_kisa[hafta_gunu]}", style_tablo_header))
        header_row.append(Paragraph("Top. Gün", style_tablo_header))
        header_row.append(Paragraph("Top. Mesai", style_tablo_header))
        table_data.append(header_row)

        t_styles = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]

        row_idx = 1
        
        # --- 4. TABLO SATIRLARINI BASMA DÖNGÜSÜ ---
        for pdata in personel_veri_havuzu:
            gun_map = pdata["gun_map"]
            mesai_map = pdata["mesai_map"]

            # --- A) YOKLAMA SATIRI ---
            yoklama_row = [[Paragraph(pdata["ad"], style_personel_ad), Paragraph(pdata["gorev"], style_personel_gorev)]]
            
            for g in range(1, gun_sayisi + 1):
                hafta_gunu = date(secilen_yil, secilen_ay, g).weekday()
                durum = gun_map.get(g)
                
                cell_txt = "-"
                cell_color = "#FFFFFF"
                text_hex = "#9CA3AF"

                if durum == "Geldi" and hafta_gunu == 6:
                    cell_txt = "P"
                    cell_color = "#FFEDD5"
                    text_hex = "#F59E0B"
                elif durum == "Geldi":
                    cell_txt = "G"
                    cell_color = "#DCFCE7"
                    text_hex = "#16A34A"
                elif durum == "Yok":
                    cell_txt = "Y"
                    cell_color = "#FEE2E2"
                    text_hex = "#EF4444"
                elif durum == "İzinli":
                    cell_txt = "İ"
                    cell_color = "#DBEAFE"
                    text_hex = "#3B82F6"
                elif durum == "Raporlu":
                    cell_txt = "R"
                    cell_color = "#FED7AA"
                    text_hex = "#EA580C"
                else:
                    if hafta_gunu == 5: cell_color = "#FFF2CC"
                    elif hafta_gunu == 6: cell_color = "#FCE4D6"

                style_p_durum = ParagraphStyle(f'Durum_{row_idx}_{g}', parent=style_cell_text, textColor=colors.HexColor(text_hex))
                yoklama_row.append(Paragraph(cell_txt, style_p_durum))
                t_styles.append(('BACKGROUND', (g, row_idx), (g, row_idx), colors.HexColor(cell_color)))

            # Toplam Gün Hücresi
            yoklama_row.append(Paragraph(f"{pdata['toplam_gun']} Gün", style_personel_ad))
            t_styles.append(('BACKGROUND', (gun_sayisi + 1, row_idx), (gun_sayisi + 1, row_idx), colors.HexColor("#F8FAFC")))
            
            # Toplam Mesai Değeri
            yoklama_row.append(Paragraph(f"{round(pdata['toplam_mesai'], 1)} Saat", style_personel_ad))
            t_styles.append(('BACKGROUND', (gun_sayisi + 2, row_idx), (gun_sayisi + 2, row_idx + 1), colors.HexColor("#F1F5F9")))
            
            t_styles.append(('SPAN', (0, row_idx), (0, row_idx + 1))) 
            t_styles.append(('SPAN', (gun_sayisi + 2, row_idx), (gun_sayisi + 2, row_idx + 1))) 
            
            table_data.append(yoklama_row)
            row_idx += 1

            # --- B) MESAİ SATIRI ---
            style_mesai_etiket = ParagraphStyle(f'ME_{row_idx}', parent=styles['Normal'], fontName=FONT_ITALIC, fontSize=8.5, textColor=colors.HexColor("#047857"))
            mesai_row = [Paragraph("⏱ Fazla Mesai (Saat)", style_mesai_etiket)]
            
            for g in range(1, gun_sayisi + 1):
                hafta_gunu = date(secilen_yil, secilen_ay, g).weekday()
                mesai = mesai_map.get(g, 0.0)
                
                cell_m_txt = ""
                m_bg_color = "#FFFFFF"
                m_text_color = "#047857"
                
                if mesai > 0:
                    cell_m_txt = str(mesai)
                    if mesai <= 2.0:
                        m_bg_color = "#E6F4EA"
                    elif mesai <= 4.0:
                        m_bg_color = "#CEEAD6"
                    else:
                        m_bg_color = "#A8DADC"
                        m_text_color = "#1D3557"
                else:
                    if hafta_gunu == 5: m_bg_color = "#FFF2CC"
                    elif hafta_gunu == 6: m_bg_color = "#FCE4D6"

                style_m_dyn = ParagraphStyle(f'Mesai_{row_idx}_{g}', parent=style_cell_mesai, textColor=colors.HexColor(m_text_color))
                mesai_row.append(Paragraph(cell_m_txt, style_m_dyn))
                t_styles.append(('BACKGROUND', (g, row_idx), (g, row_idx), colors.HexColor(m_bg_color)))

            mesai_row.append("")
            t_styles.append(('BACKGROUND', (gun_sayisi + 1, row_idx), (gun_sayisi + 1, row_idx), colors.HexColor("#F8FAFC")))
            mesai_row.append("")

            table_data.append(mesai_row)
            row_idx += 1

        # Tabloyu İnşa Etme
        puantaj_table = Table(table_data, colWidths=col_widths, repeatRows=1)
        puantaj_table.setStyle(TableStyle(t_styles))
        story.append(puantaj_table)
        story.append(Spacer(1, 30))

        # --- 5. İMZA BLOKLARI ALANI (4 Sütun * 9.75 cm = 39.0 cm Tam A3 Sığdırma) ---
        imza_unvanlar = ["HAZIRLAYAN", "MUHASEBE", "ŞANTİYE ŞEFİ", "PROJE MÜDÜRÜ"]
        imza_data = []
        row_unvanlar = []
        row_cizgiler = []
        
        for unvan in imza_unvanlar:
            style_unvan = ParagraphStyle(f'U_{unvan}', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=12, alignment=1, textColor=colors.HexColor("#334155"))
            style_cizgi = ParagraphStyle(f'C_{unvan}', parent=styles['Normal'], fontName=FONT_REGULAR, fontSize=10, alignment=1, textColor=colors.HexColor("#94A3B8"))
            
            row_unvanlar.append(Paragraph(unvan, style_unvan))
            row_cizgiler.append([Paragraph("<br/><br/>...................................", style_cizgi)])

        imza_data.append(row_unvanlar)
        imza_data.append(row_cizgiler)

        imza_table = Table(imza_data, colWidths=[9.75 * cm] * 4)
        imza_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        
        story.append(KeepTogether([imza_table]))

        doc.build(story, canvasmaker=NumberedCanvas)
        messagebox.showinfo("Başarılı", f"Kurumsal Yönetici Raporu (A3 PDF) başarıyla masaüstüne kaydedildi:\n{dosya_adi}")

    except Exception as e:
        messagebox.showerror("Hata", f"PDF raporu oluşturulurken teknik bir hata meydana geldi:\n{str(e)}")
