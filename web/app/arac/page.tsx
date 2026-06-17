import { Car, Wrench, Fuel, AlertTriangle, Plus } from 'lucide-react'
import { ModulePage, Badge, type Column } from '@/components/module-page'

const columns: Column[] = [
  { key: 'plaka', label: 'Plaka', mono: true },
  { key: 'arac', label: 'Araç / Marka' },
  { key: 'tip', label: 'Tip' },
  { key: 'surucu', label: 'Zimmetli' },
  { key: 'km', label: 'KM', align: 'right' },
  { key: 'durum', label: 'Durum', align: 'right' },
]

const rows = [
  ['34 ABC 123', 'Ford Transit', 'Panelvan', 'A. Yılmaz', '142.500', <Badge key="1" tone="success">Aktif</Badge>],
  ['34 XYZ 456', 'Caterpillar 320', 'İş Makinesi', 'Şantiye', '8.200 saat', <Badge key="2" tone="success">Aktif</Badge>],
  ['06 KLM 789', 'Fiat Doblo', 'Hafif Ticari', 'M. Demir', '98.300', <Badge key="3" tone="warning">Bakımda</Badge>],
  ['16 DEF 012', 'Mercedes Actros', 'Kamyon', 'H. Aydın', '320.100', <Badge key="4" tone="destructive">Muayene Gecikti</Badge>],
]

export default function AracPage() {
  return (
    <ModulePage
      title="Araç ve Bakım"
      subtitle="Araç filosu, bakım planı, yakıt ve muayene takibi"
      primaryAction="Araç Ekle"
      primaryIcon={Plus}
      stats={[
        { label: 'Toplam Araç', value: '38', icon: Car, iconTone: 'info' },
        { label: 'Bakımda', value: '4', icon: Wrench, iconTone: 'warning' },
        { label: 'Aylık Yakıt', value: '₺248K', icon: Fuel, iconTone: 'primary' },
        { label: 'Muayene Yaklaşan', value: '5', icon: AlertTriangle, iconTone: 'destructive' },
      ]}
      columns={columns}
      rows={rows}
    />
  )
}
