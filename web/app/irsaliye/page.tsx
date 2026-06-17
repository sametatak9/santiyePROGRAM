import { Truck, PackageCheck, Clock, FileWarning, Plus } from 'lucide-react'
import { ModulePage, Badge, type Column } from '@/components/module-page'

const columns: Column[] = [
  { key: 'kod', label: 'İrsaliye No', mono: true },
  { key: 'firma', label: 'Firma' },
  { key: 'tarih', label: 'Tarih' },
  { key: 'kalem', label: 'Kalem', align: 'right' },
  { key: 'tutar', label: 'Tutar', align: 'right' },
  { key: 'durum', label: 'Durum', align: 'right' },
]

const rows = [
  ['IRS-2026-112', 'Demir A.Ş.', '2026-06-14', '8', '₺50.000', <Badge key="1" tone="success">Faturalandı</Badge>],
  ['IRS-2026-111', 'ABC Malzeme Ltd.', '2026-06-13', '5', '₺30.000', <Badge key="2" tone="warning">Bekliyor</Badge>],
  ['IRS-2026-110', 'Beton Sanayi A.Ş.', '2026-06-12', '3', '₺120.000', <Badge key="3" tone="warning">Bekliyor</Badge>],
  ['IRS-2026-109', 'XYZ Tedarik', '2026-06-10', '12', '₺18.500', <Badge key="4" tone="success">Faturalandı</Badge>],
]

export default function IrsaliyePage() {
  return (
    <ModulePage
      title="İrsaliye Girişi"
      subtitle="Sevk irsaliyeleri, mal kabul ve fatura eşleştirme"
      primaryAction="İrsaliye Ekle"
      primaryIcon={Plus}
      stats={[
        { label: 'Toplam İrsaliye', value: '342', icon: Truck, iconTone: 'info' },
        { label: 'Faturalanan', value: '298', icon: PackageCheck, iconTone: 'success' },
        { label: 'Bekleyen', value: '44', icon: Clock, iconTone: 'warning' },
        { label: 'Eksik / Hatalı', value: '6', icon: FileWarning, iconTone: 'destructive' },
      ]}
      columns={columns}
      rows={rows}
    />
  )
}
