-- =====================================================
-- EKSIK KOLONLARı MEVCUT TABLOLARA EKLE
-- =====================================================

-- irsaliyeler tablosuna eksik kolonlar
ALTER TABLE irsaliyeler 
ADD COLUMN IF NOT EXISTS cari_kart_id BIGINT,
ADD COLUMN IF NOT EXISTS onay_durumu TEXT DEFAULT 'ONAY BEKLİYOR',
ADD COLUMN IF NOT EXISTS imzali_evrak_url TEXT,
ADD COLUMN IF NOT EXISTS karsilastirma_raporu TEXT,
ADD COLUMN IF NOT EXISTS gonderim_tarihi TIMESTAMPTZ;

-- satin_alma_formlari tablosuna eksik kolonlar
ALTER TABLE satin_alma_formlari
ADD COLUMN IF NOT EXISTS imzali_evrak_url TEXT,
ADD COLUMN IF NOT EXISTS gonderim_tarihi TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS stok_kart_id BIGINT;

-- =====================================================
-- CARİ KARTLAR
-- =====================================================

CREATE TABLE IF NOT EXISTS cari_kartlar (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    kart_tipi TEXT NOT NULL, -- CARI, TEDARIKCI, TASERON, MUSTERI
    kod TEXT,
    unvan TEXT NOT NULL,
    yetkili TEXT,
    telefon TEXT,
    eposta TEXT,
    vergi_no TEXT,
    vergi_dairesi TEXT,
    adres TEXT,
    iban TEXT,
    durum TEXT DEFAULT 'AKTIF',
    notlar TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cari_kartlar_unvan ON cari_kartlar(unvan);
CREATE INDEX IF NOT EXISTS idx_cari_kartlar_kart_tipi ON cari_kartlar(kart_tipi);

-- =====================================================
-- STOK KARTLARI
-- =====================================================

CREATE TABLE IF NOT EXISTS stok_kartlari (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    stok_kodu TEXT UNIQUE,
    stok_adi TEXT NOT NULL,
    kategori TEXT,
    birim TEXT DEFAULT 'ADET',
    kritik_seviye NUMERIC(15,3),
    durum TEXT DEFAULT 'AKTIF',
    aciklama TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_stok_kartlari_stok_adi ON stok_kartlari(stok_adi);
CREATE INDEX IF NOT EXISTS idx_stok_kartlari_stok_kodu ON stok_kartlari(stok_kodu);

-- =====================================================
-- KART İŞLEM GEÇMİŞİ
-- =====================================================

CREATE TABLE IF NOT EXISTS kart_islem_gecmisi (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    kart_tipi TEXT NOT NULL, -- CARI, STOK, ARAC, DEMIRBAS
    kart_id BIGINT NOT NULL,
    islem_tipi TEXT NOT NULL,
    belge_no TEXT,
    aciklama TEXT,
    tutar NUMERIC(15,2),
    tarih DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_kart_gecmisi_kart_tipi ON kart_islem_gecmisi(kart_tipi);
CREATE INDEX IF NOT EXISTS idx_kart_gecmisi_kart_id ON kart_islem_gecmisi(kart_id);
CREATE INDEX IF NOT EXISTS idx_kart_gecmisi_tarih ON kart_islem_gecmisi(tarih);

-- =====================================================
-- ARAÇ KARTLARI
-- =====================================================

CREATE TABLE IF NOT EXISTS arac_kartlari (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    plaka TEXT NOT NULL UNIQUE,
    arac_tipi TEXT, -- ARAC, IS MAKINESI, EKIPMAN
    marka_model TEXT,
    sorumlu_personel_id BIGINT,
    mevcut_km NUMERIC(15,2),
    km_bakim_araligi NUMERIC(15,2),
    sonraki_bakim_km NUMERIC(15,2),
    yag_bakim_km NUMERIC(15,2),
    muayene_tarihi DATE,
    sigorta_tarihi DATE,
    durum TEXT DEFAULT 'AKTIF',
    notlar TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_arac_personel
        FOREIGN KEY (sorumlu_personel_id)
        REFERENCES personel(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_arac_kartlari_plaka ON arac_kartlari(plaka);
CREATE INDEX IF NOT EXISTS idx_arac_kartlari_sorumlu_personel ON arac_kartlari(sorumlu_personel_id);

-- =====================================================
-- DEMİRBAŞ KARTLARI
-- =====================================================

CREATE TABLE IF NOT EXISTS demirbas_kartlari (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    demirbas_kodu TEXT NOT NULL UNIQUE,
    demirbas_adi TEXT NOT NULL,
    kategori TEXT,
    seri_no TEXT,
    durum TEXT DEFAULT 'MUSAIT', -- MUSAIT, TAHSIS EDILDI, BAKIMDA, PASIF
    notlar TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_demirbas_kartlari_demirbas_adi ON demirbas_kartlari(demirbas_adi);
CREATE INDEX IF NOT EXISTS idx_demirbas_kartlari_demirbas_kodu ON demirbas_kartlari(demirbas_kodu);

-- =====================================================
-- TAHSİS KAYITLARI
-- =====================================================

CREATE TABLE IF NOT EXISTS tahsis_kayitlari (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tahsis_tipi TEXT NOT NULL, -- ARAC, DEMIRBAS
    kaynak_id BIGINT NOT NULL,
    personel_id BIGINT,
    cari_kart_id BIGINT,
    tahsis_tarihi DATE DEFAULT CURRENT_DATE,
    iade_tarihi DATE,
    durum TEXT DEFAULT 'TAHSIS EDILDI', -- TAHSIS EDILDI, IADE EDILDI, HASARLI, KAYIP
    tutanak_url TEXT,
    aciklama TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_tahsis_personel
        FOREIGN KEY (personel_id)
        REFERENCES personel(id) ON DELETE SET NULL,
    CONSTRAINT fk_tahsis_cari
        FOREIGN KEY (cari_kart_id)
        REFERENCES cari_kartlar(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_tahsis_kayitlari_tahsis_tipi ON tahsis_kayitlari(tahsis_tipi);
CREATE INDEX IF NOT EXISTS idx_tahsis_kayitlari_personel_id ON tahsis_kayitlari(personel_id);
CREATE INDEX IF NOT EXISTS idx_tahsis_kayitlari_durum ON tahsis_kayitlari(durum);

-- =====================================================
-- HAZIR TUTANAKLAR
-- =====================================================

CREATE TABLE IF NOT EXISTS hazir_tutanaklar (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tutanak_tipi TEXT NOT NULL, -- TAHSIS, TESLIM, SEVK, HASAR, GENEL
    belge_no TEXT NOT NULL UNIQUE,
    personel_id BIGINT,
    cari_kart_id BIGINT,
    konu TEXT,
    tarih DATE DEFAULT CURRENT_DATE,
    pdf_url TEXT,
    aciklama TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_tutanak_personel
        FOREIGN KEY (personel_id)
        REFERENCES personel(id) ON DELETE SET NULL,
    CONSTRAINT fk_tutanak_cari
        FOREIGN KEY (cari_kart_id)
        REFERENCES cari_kartlar(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_tutanak_tutanak_tipi ON hazir_tutanaklar(tutanak_tipi);
CREATE INDEX IF NOT EXISTS idx_tutanak_belge_no ON hazir_tutanaklar(belge_no);
CREATE INDEX IF NOT EXISTS idx_tutanak_personel_id ON hazir_tutanaklar(personel_id);

-- =====================================================
-- KASA HAREKETLERİ
-- =====================================================

CREATE TABLE IF NOT EXISTS kasa_hareketleri (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tarih DATE DEFAULT CURRENT_DATE,
    hafta TEXT,
    hareket_tipi TEXT NOT NULL, -- GELIR, GIDER
    cari_kart_id BIGINT,
    fis_no TEXT,
    tutar NUMERIC(15,2),
    fis_evrak_url TEXT,
    aciklama TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_kasa_hareketleri_cari
        FOREIGN KEY (cari_kart_id)
        REFERENCES cari_kartlar(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_kasa_hareketleri_tarih ON kasa_hareketleri(tarih);
CREATE INDEX IF NOT EXISTS idx_kasa_hareketleri_hareket_tipi ON kasa_hareketleri(hareket_tipi);
CREATE INDEX IF NOT EXISTS idx_kasa_hareketleri_cari_kart_id ON kasa_hareketleri(cari_kart_id);

-- =====================================================
-- EPOSTA GÖNDERİMLERİ
-- =====================================================

CREATE TABLE IF NOT EXISTS eposta_gonderimleri (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    konu TEXT NOT NULL,
    alicilar TEXT,
    modul TEXT, -- PERSONEL, FINANS, IDARI, RAPOR
    rapor_tipi TEXT,
    dosya_url TEXT,
    durum TEXT DEFAULT 'HAZIR', -- HAZIR, GONDERILDI, HATA
    notlar TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_eposta_gonderimleri_durum ON eposta_gonderimleri(durum);
CREATE INDEX IF NOT EXISTS idx_eposta_gonderimleri_modul ON eposta_gonderimleri(modul);

-- =====================================================
-- POLİCİLER (RLS)
-- =====================================================

-- Cari Kartlar Policies
CREATE POLICY "cari_kartlar_insert"
ON public.cari_kartlar FOR INSERT WITH CHECK (true);

CREATE POLICY "cari_kartlar_select"
ON public.cari_kartlar FOR SELECT USING (true);

CREATE POLICY "cari_kartlar_update"
ON public.cari_kartlar FOR UPDATE USING (true) WITH CHECK (true);

CREATE POLICY "cari_kartlar_delete"
ON public.cari_kartlar FOR DELETE USING (true);

-- Stok Kartları Policies
CREATE POLICY "stok_kartlari_insert"
ON public.stok_kartlari FOR INSERT WITH CHECK (true);

CREATE POLICY "stok_kartlari_select"
ON public.stok_kartlari FOR SELECT USING (true);

CREATE POLICY "stok_kartlari_update"
ON public.stok_kartlari FOR UPDATE USING (true) WITH CHECK (true);

CREATE POLICY "stok_kartlari_delete"
ON public.stok_kartlari FOR DELETE USING (true);

-- Kart İşlem Geçmişi Policies
CREATE POLICY "kart_islem_gecmisi_insert"
ON public.kart_islem_gecmisi FOR INSERT WITH CHECK (true);

CREATE POLICY "kart_islem_gecmisi_select"
ON public.kart_islem_gecmisi FOR SELECT USING (true);

-- Araç Kartları Policies
CREATE POLICY "arac_kartlari_insert"
ON public.arac_kartlari FOR INSERT WITH CHECK (true);

CREATE POLICY "arac_kartlari_select"
ON public.arac_kartlari FOR SELECT USING (true);

CREATE POLICY "arac_kartlari_update"
ON public.arac_kartlari FOR UPDATE USING (true) WITH CHECK (true);

-- Demirbas Kartları Policies
CREATE POLICY "demirbas_kartlari_insert"
ON public.demirbas_kartlari FOR INSERT WITH CHECK (true);

CREATE POLICY "demirbas_kartlari_select"
ON public.demirbas_kartlari FOR SELECT USING (true);

CREATE POLICY "demirbas_kartlari_update"
ON public.demirbas_kartlari FOR UPDATE USING (true) WITH CHECK (true);

-- Tahsis Kayıtları Policies
CREATE POLICY "tahsis_kayitlari_insert"
ON public.tahsis_kayitlari FOR INSERT WITH CHECK (true);

CREATE POLICY "tahsis_kayitlari_select"
ON public.tahsis_kayitlari FOR SELECT USING (true);

CREATE POLICY "tahsis_kayitlari_update"
ON public.tahsis_kayitlari FOR UPDATE USING (true) WITH CHECK (true);

-- Hazır Tutanaklar Policies
CREATE POLICY "hazir_tutanaklar_insert"
ON public.hazir_tutanaklar FOR INSERT WITH CHECK (true);

CREATE POLICY "hazir_tutanaklar_select"
ON public.hazir_tutanaklar FOR SELECT USING (true);

CREATE POLICY "hazir_tutanaklar_update"
ON public.hazir_tutanaklar FOR UPDATE USING (true) WITH CHECK (true);

-- Kasa Hareketleri Policies
CREATE POLICY "kasa_hareketleri_insert"
ON public.kasa_hareketleri FOR INSERT WITH CHECK (true);

CREATE POLICY "kasa_hareketleri_select"
ON public.kasa_hareketleri FOR SELECT USING (true);

CREATE POLICY "kasa_hareketleri_update"
ON public.kasa_hareketleri FOR UPDATE USING (true) WITH CHECK (true);

-- Eposta Gonderimleri Policies
CREATE POLICY "eposta_gonderimleri_insert"
ON public.eposta_gonderimleri FOR INSERT WITH CHECK (true);

CREATE POLICY "eposta_gonderimleri_select"
ON public.eposta_gonderimleri FOR SELECT USING (true);

CREATE POLICY "eposta_gonderimleri_update"
ON public.eposta_gonderimleri FOR UPDATE USING (true) WITH CHECK (true);

-- İrsaliyeler için eksik policies
CREATE POLICY "irsaliyeler_update"
ON public.irsaliyeler FOR UPDATE USING (true) WITH CHECK (true);

CREATE POLICY "irsaliyeler_delete"
ON public.irsaliyeler FOR DELETE USING (true);

-- Satin Alma Formlari için eksik policies
CREATE POLICY "satin_alma_formlari_delete"
ON public.satin_alma_formlari FOR DELETE USING (true);

-- =====================================================
-- TAMAMLANDI
-- =====================================================
