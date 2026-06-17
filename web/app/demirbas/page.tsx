import { Box, UserCheck, Warehouse, Wrench, Plus } from 'lucide-react'
import { ModulePage, Badge, type Column } from '@/components/module-page'

const columns: Column[] = [
  { key: 'kod', label: 'Demirbaş No', mono: true },
  { key: 'ad', label: 'Demirbaş' },
  { key: 'kategori', label: 'Kategori' },
  { key: 'zimmet', label: 'Zimmetli' },
  { key: 'deger', label: 'Değer', align: 'right' },
  { key: 'durum', label: 'Durum', align: 'right' },
]

const rows = [
  ['DMB-0012', 'Dizüstü Bilgisayar', 'Elektronik', 'A. Kaya', '₺32.000', <Badge key="1" tone="info">Zimmetli</Badge>],
  ['DMB-0034', 'Matkap Seti', 'El Aleti', 'Saha Deposu', '₺8.400', <Badge key="2" tone="success">Depoda</Badge>],
  ['DMB-0051', 'Jeneratör 15kVA', 'Ekipman', 'Şantiye-2', '₺145.000', <Badge key="3" tone="info">Zimmetli</Badge>],
  ['DMB-0078', 'Ofis Masası', 'Mobilya', 'İdari Bina', '₺6.200', <Badge key="4" tone="warning">Bakımda</Badge>],
]

export default function DemirbasPage() {
  return (
    <ModulePage
      title="Demirbaş Kartları"
      subtitle="Demirbaş envanteri, zimmet ve amortisman takibi"
      primaryAction="Demirbaş Ekle"
      primaryIcon={Plus}
      stats={[
        { label: 'Toplam Demirbaş', value: '428', icon: Box, iconTone: 'info' },
        { label: 'Zimmetli', value: '312', icon: UserCheck, iconTone: 'primary' },
        { label: 'Depoda', value: '98', icon: Warehouse, iconTone: 'success' },
        { label: 'Bakım / Arıza', value: '18', icon: Wrench, iconTone: 'warning' },
      ]}
      columns={columns}
      rows={rows}
    />
  )
}
