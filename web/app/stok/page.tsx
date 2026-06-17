import { Package, AlertTriangle, Boxes, TrendingDown, Plus } from 'lucide-react'
import { ModulePage, Badge, type Column } from '@/components/module-page'

const columns: Column[] = [
  { key: 'kod', label: 'Stok Kodu', mono: true },
  { key: 'ad', label: 'Malzeme' },
  { key: 'kategori', label: 'Kategori' },
  { key: 'miktar', label: 'Miktar', align: 'right' },
  { key: 'birim', label: 'Birim Fiyat', align: 'right' },
  { key: 'durum', label: 'Durum', align: 'right' },
]

const rows = [
  ['STK-001', 'Çimento (50kg)', 'İnşaat', '1.240 adet', '₺185', <Badge key="1" tone="success">Yeterli</Badge>],
  ['STK-002', 'İnşaat Demiri Ø12', 'Demir', '8.500 kg', '₺28', <Badge key="2" tone="success">Yeterli</Badge>],
  ['STK-014', 'Tuğla', 'İnşaat', '420 adet', '₺12', <Badge key="3" tone="warning">Azalıyor</Badge>],
  ['STK-022', 'Boya (Beyaz)', 'Sarf', '18 kova', '₺640', <Badge key="4" tone="destructive">Kritik</Badge>],
  ['STK-030', 'Kablo NYA 2.5', 'Elektrik', '3.200 m', '₺18', <Badge key="5" tone="success">Yeterli</Badge>],
]

export default function StokPage() {
  return (
    <ModulePage
      title="Stok Kartları"
      subtitle="Malzeme stok takibi, giriş/çıkış ve kritik seviye uyarıları"
      primaryAction="Stok Kartı Ekle"
      primaryIcon={Plus}
      stats={[
        { label: 'Toplam Kalem', value: '512', icon: Package, iconTone: 'info' },
        { label: 'Stok Değeri', value: '₺4.2M', icon: Boxes, iconTone: 'primary' },
        { label: 'Kritik Seviye', value: '12', icon: AlertTriangle, iconTone: 'destructive' },
        { label: 'Azalan', value: '28', icon: TrendingDown, iconTone: 'warning' },
      ]}
      columns={columns}
      rows={rows}
    />
  )
}
