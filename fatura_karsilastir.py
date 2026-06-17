"""Satin alma - irsaliye - fatura 3'lu kontrol mantigi."""

def _norm(value):
    return (value or "").strip().lower()

def _birim(value):
    return (value or "").strip().upper()

def _num(value):
    try:
        return float(value or 0)
    except Exception:
        return 0.0

def _ozet(kalemler, urun_key, miktar_key, birim_key):
    sonuc = {}
    for kalem in kalemler or []:
        key = (_norm(kalem.get(urun_key)), _birim(kalem.get(birim_key)))
        if not key[0]:
            continue
        if key not in sonuc:
            sonuc[key] = {"urun_adi": kalem.get(urun_key, ""), "birim": kalem.get(birim_key, ""), "toplam": 0.0}
        sonuc[key]["toplam"] += _num(kalem.get(miktar_key))
    return sonuc

def _esit(a, b, tolerans=0.001):
    return abs(_num(a) - _num(b)) <= tolerans

def karsilastir(satin_alma_kalemleri, irsaliye_kalemleri, fatura_kalemleri):
    sa = _ozet(satin_alma_kalemleri, "urun_adi", "talep_edilen_miktar", "talep_birimi")
    ir = _ozet(irsaliye_kalemleri, "urun_adi", "miktar", "birim")
    ft = _ozet(fatura_kalemleri, "urun_adi", "miktar", "birim")
    kalemler = []
    genel_uyumlu = True

    for key in sorted(set(sa) | set(ir) | set(ft), key=lambda x: (x[0], x[1])):
        kaynak = sa.get(key) or ir.get(key) or ft.get(key) or {}
        talep = sa.get(key, {}).get("toplam", 0.0)
        teslim = ir.get(key, {}).get("toplam", 0.0)
        fatura = ft.get(key, {}).get("toplam", 0.0)
        durumlar = []

        if key not in sa:
            durumlar.append("Talep disi kalem")
        if key not in ir:
            durumlar.append("Irsaliyede yok")
        if key not in ft:
            durumlar.append("Faturada yok")
        if key in sa and key in ir and not _esit(talep, teslim):
            durumlar.append("Siparis-teslim farki")
        if key in ir and key in ft and not _esit(teslim, fatura):
            durumlar.append("Teslim-fatura farki")
        if key in sa and key in ft and not _esit(talep, fatura):
            durumlar.append("Siparis-fatura farki")

        uyumlu = len(durumlar) == 0
        genel_uyumlu = genel_uyumlu and uyumlu
        kalemler.append({
            "urun_adi": kaynak.get("urun_adi", key[0]),
            "birim": kaynak.get("birim", key[1]),
            "talep_miktar": round(talep, 3),
            "teslim_miktar": round(teslim, 3),
            "fatura_miktar": round(fatura, 3),
            "teslim_fatura_farki": round(fatura - teslim, 3),
            "siparis_fatura_farki": round(fatura - talep, 3),
            "uyumlu": uyumlu,
            "durum": ", ".join(durumlar) if durumlar else "UYUMLU",
        })

    toplam_talep = sum(v["toplam"] for v in sa.values())
    toplam_teslim = sum(v["toplam"] for v in ir.values())
    toplam_fatura = sum(v["toplam"] for v in ft.values())
    return {
        "genel_uyumlu": genel_uyumlu,
        "kalemler": kalemler,
        "ozet": {
            "toplam_talep": round(toplam_talep, 3),
            "toplam_teslim": round(toplam_teslim, 3),
            "toplam_fatura": round(toplam_fatura, 3),
            "teslim_fatura_farki": round(toplam_fatura - toplam_teslim, 3),
            "siparis_fatura_farki": round(toplam_fatura - toplam_talep, 3),
        },
        "odeme_onayi": "ODEME ONAYI" if genel_uyumlu else "SORUNLU ODEME ONAYI",
        "ozet_mesaj": "Fatura, teslim ve siparis miktarlari uyumlu." if genel_uyumlu else "Fatura kontrolunde fark var.",
    }

def rapor_metni_olustur(sa_id, irsaliye_id, fatura_kodu, sonuc):
    satirlar = [
        "KIBRITCI FATURA KONTROL RAPORU",
        "=" * 34,
        f"Satin Alma ID : {sa_id or '-'}",
        f"Irsaliye ID   : {irsaliye_id or 'Tum irsaliyeler'}",
        f"Fatura ID     : {fatura_kodu or '-'}",
        "",
        "TOPLAM OZET",
        f"Talep miktari        : {sonuc['ozet']['toplam_talep']}",
        f"Teslim miktari       : {sonuc['ozet']['toplam_teslim']}",
        f"Fatura miktari       : {sonuc['ozet']['toplam_fatura']}",
        f"Teslim-Fatura farki  : {sonuc['ozet']['teslim_fatura_farki']}",
        f"Siparis-Fatura farki : {sonuc['ozet']['siparis_fatura_farki']}",
        "",
        "KALEM KONTROLU",
    ]
    for kalem in sonuc["kalemler"]:
        satirlar.append(
            f"- {kalem['urun_adi']} ({kalem['birim']}): "
            f"Talep={kalem['talep_miktar']} | Teslim={kalem['teslim_miktar']} | "
            f"Fatura={kalem['fatura_miktar']} | Durum={kalem['durum']}"
        )
    satirlar.extend(["", sonuc["ozet_mesaj"], f"Finans sonucu: {sonuc['odeme_onayi']}"])
    return "\n".join(satirlar)
