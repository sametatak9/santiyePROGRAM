'use client'

import { useState } from 'react'
import { Plus, Trash2, FileSearch, Upload, Link2 } from 'lucide-react'
import { Card, CardHeader, Field, Input, Select, Button, Badge } from '@/components/ui'
import { formatTRY } from '@/lib/utils'

type Kalem = {
  id: number
  urun: string
  miktar: number
  birim: string
  birimFiyat: number
  kdv: number
}

let nextId = 2

export function FaturaForm() {
  const [kalemler, setKalemler] = useState<Kalem[]>([
    { id: 1, urun: '', miktar: 0, birim: 'Adet', birimFiyat: 0, kdv: 20 },
  ])

  const addKalem = () =>
    setKalemler((k) => [
      ...k,
      { id: nextId++, urun: '', miktar: 0, birim: 'Adet', birimFiyat: 0, kdv: 20 },
    ])

  const removeKalem = (id: number) =>
    setKalemler((k) => (k.length > 1 ? k.filter((x) => x.id !== id) : k))

  const updateKalem = (id: number, patch: Partial<Kalem>) =>
    setKalemler((k) => k.map((x) => (x.id === id ? { ...x, ...patch } : x)))

  const matrah = kalemler.reduce((s, k) => s + k.miktar * k.birimFiyat, 0)
  const kdvToplam = kalemler.reduce(
    (s, k) => s + k.miktar * k.birimFiyat * (k.kdv / 100),
    0,
  )
  const genelToplam = matrah + kdvToplam

  return (
    <div className="grid grid-cols-1 gap-6 xl:grid-cols-5">
      {/* Sol: Fatura bilgileri */}
      <div className="xl:col-span-2">
        <Card>
          <CardHeader title="Fatura Bilgileri" />
          <div className="flex flex-col gap-4 p-5">
            <Field label="Satın Alma Talebi Bağlantısı" hint="Opsiyonel">
              <Select defaultValue="">
                <option value="">— Seçin —</option>
                <option value="sa-1">SA-20260012 · Demir A.Ş.</option>
                <option value="sa-2">SA-20260018 · ABC Malzeme</option>
              </Select>
            </Field>

            <Field label="Firma / Cari Ünvan" hint="Seçin veya elle yazın">
              <Input placeholder="Firma adı yazın..." />
            </Field>

            <Field label="İrsaliye Bağlantıları">
              <button className="flex h-10 w-full items-center justify-center gap-2 rounded-lg border border-dashed border-border bg-secondary/50 px-3 text-sm font-medium text-muted-foreground transition-colors hover:border-primary/40 hover:text-foreground">
                <Link2 className="size-4" />
                İrsaliyeleri Seç (0 seçildi)
              </button>
            </Field>

            <div className="grid grid-cols-2 gap-4">
              <Field label="Fatura Numarası">
                <Input placeholder="FT-20260012" />
              </Field>
              <Field label="Fatura Tarihi">
                <Input type="date" defaultValue="2026-06-17" />
              </Field>
            </div>

            <div className="grid grid-cols-3 gap-3 rounded-lg border border-border bg-secondary/40 p-4">
              <div>
                <p className="text-xs text-muted-foreground">Matrah</p>
                <p className="mt-1 text-sm font-semibold tabular-nums text-foreground">
                  {formatTRY(matrah)}
                </p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground">KDV</p>
                <p className="mt-1 text-sm font-semibold tabular-nums text-foreground">
                  {formatTRY(kdvToplam)}
                </p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground">Genel Toplam</p>
                <p className="mt-1 text-sm font-semibold tabular-nums text-primary">
                  {formatTRY(genelToplam)}
                </p>
              </div>
            </div>
          </div>
        </Card>
      </div>

      {/* Sağ: Faturalar + Kalemler */}
      <div className="flex flex-col gap-6 xl:col-span-3">
        {/* Sistemdeki faturalar */}
        <Card>
          <CardHeader
            title="Sistemdeki Faturalar"
            action={<span className="text-xs text-muted-foreground">3 kayıt</span>}
          />
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border text-left text-xs uppercase tracking-wide text-muted-foreground">
                  <th className="px-5 py-3 font-medium">Kod</th>
                  <th className="px-5 py-3 font-medium">No</th>
                  <th className="px-5 py-3 font-medium">Firma</th>
                  <th className="px-5 py-3 text-right font-medium">Tutar</th>
                  <th className="px-5 py-3 text-right font-medium">Durum</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { kod: 'FT-20260001', no: '2026/001', firma: 'Demir A.Ş.', tutar: 50000, durum: 'Onaylı', tone: 'success' as const },
                  { kod: 'FT-20260002', no: '2026/045', firma: 'ABC Malzeme', tutar: 30000, durum: 'Bekliyor', tone: 'warning' as const },
                  { kod: 'FT-20260003', no: 'INV-2026-88', firma: 'XYZ Tedarik', tutar: 20000, durum: 'Uyumsuz', tone: 'destructive' as const },
                ].map((f) => (
                  <tr key={f.kod} className="border-b border-border/60 last:border-0 transition-colors hover:bg-secondary/50">
                    <td className="px-5 py-3 font-mono text-[13px] font-medium">{f.kod}</td>
                    <td className="px-5 py-3 text-muted-foreground">{f.no}</td>
                    <td className="px-5 py-3">{f.firma}</td>
                    <td className="px-5 py-3 text-right font-medium tabular-nums">{formatTRY(f.tutar)}</td>
                    <td className="px-5 py-3 text-right">
                      <Badge tone={f.tone}>{f.durum}</Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>

        {/* Malzeme kalemleri */}
        <Card>
          <CardHeader
            title="Fatura Malzeme Kalemleri"
            action={
              <Button variant="secondary" onClick={addKalem} className="h-8 px-2.5">
                <Plus className="size-4" />
                Kalem Ekle
              </Button>
            }
          />
          <div className="p-5">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-xs uppercase tracking-wide text-muted-foreground">
                    <th className="pb-2 pr-2 font-medium">Ürün / Hizmet</th>
                    <th className="pb-2 px-2 font-medium">Miktar</th>
                    <th className="pb-2 px-2 font-medium">Birim</th>
                    <th className="pb-2 px-2 font-medium">Birim Fiyat</th>
                    <th className="pb-2 px-2 font-medium">KDV %</th>
                    <th className="pb-2 pl-2 text-right font-medium">Toplam</th>
                    <th className="pb-2 w-8" />
                  </tr>
                </thead>
                <tbody>
                  {kalemler.map((k) => {
                    const satirToplam = k.miktar * k.birimFiyat * (1 + k.kdv / 100)
                    return (
                      <tr key={k.id}>
                        <td className="py-1.5 pr-2">
                          <Input
                            placeholder="Ürün adı"
                            value={k.urun}
                            onChange={(e) => updateKalem(k.id, { urun: e.target.value })}
                            className="h-9"
                          />
                        </td>
                        <td className="py-1.5 px-2">
                          <Input
                            type="number"
                            min={0}
                            value={k.miktar || ''}
                            onChange={(e) => updateKalem(k.id, { miktar: +e.target.value })}
                            className="h-9 w-20"
                          />
                        </td>
                        <td className="py-1.5 px-2">
                          <Select
                            value={k.birim}
                            onChange={(e) => updateKalem(k.id, { birim: e.target.value })}
                            className="h-9 w-24"
                          >
                            <option>Adet</option>
                            <option>Kg</option>
                            <option>m³</option>
                            <option>Ton</option>
                            <option>Paket</option>
                          </Select>
                        </td>
                        <td className="py-1.5 px-2">
                          <Input
                            type="number"
                            min={0}
                            value={k.birimFiyat || ''}
                            onChange={(e) => updateKalem(k.id, { birimFiyat: +e.target.value })}
                            className="h-9 w-28"
                          />
                        </td>
                        <td className="py-1.5 px-2">
                          <Input
                            type="number"
                            min={0}
                            value={k.kdv}
                            onChange={(e) => updateKalem(k.id, { kdv: +e.target.value })}
                            className="h-9 w-16"
                          />
                        </td>
                        <td className="py-1.5 pl-2 text-right font-medium tabular-nums text-foreground">
                          {formatTRY(satirToplam)}
                        </td>
                        <td className="py-1.5 text-right">
                          <button
                            onClick={() => removeKalem(k.id)}
                            className="rounded-md p-1.5 text-muted-foreground transition-colors hover:bg-destructive/10 hover:text-destructive"
                            aria-label="Kalemi sil"
                          >
                            <Trash2 className="size-4" />
                          </button>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>

            <div className="mt-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex flex-wrap gap-2">
                <Button variant="info">
                  <FileSearch className="size-4" />
                  Fatura / Fiyatları Kontrol Et
                </Button>
                <Button variant="outline">
                  <Upload className="size-4" />
                  Evrak Yükle
                </Button>
              </div>
              <div className="text-right">
                <p className="text-xs text-muted-foreground">Genel Toplam (KDV Dahil)</p>
                <p className="text-xl font-semibold tabular-nums text-foreground">
                  {formatTRY(genelToplam)}
                </p>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}
