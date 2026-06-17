import { Tent, Users, BedDouble, UtensilsCrossed, Plus } from 'lucide-react'
import { ModulePage, Badge, type Column } from '@/components/module-page'

const columns: Column[] = [
  { key: 'oda', label: 'Oda / Konteyner', mono: true },
  { key: 'kamp', label: 'Kamp' },
  { key: 'kapasite', label: 'Kapasite', align: 'right' },
  { key: 'dolu', label: 'Dolu', align: 'right' },
  { key: 'sorumlu', label: 'Sorumlu' },
  { key: 'durum', label: 'Durum', align: 'right' },
]

const rows = [
  ['A-101', 'Merkez Kamp', '4', '4', 'A. Yılmaz', <Badge key="1" tone="destructive">Dolu</Badge>],
  ['A-102', 'Merkez Kamp', '4', '3', 'A. Yılmaz', <Badge key="2" tone="success">Müsait</Badge>],
  ['B-205', 'Saha-2 Kamp', '6', '5', 'M. Demir', <Badge key="3" tone="warning">Az Yer</Badge>],
  ['C-301', 'Saha-3 Kamp', '2', '0', 'H. Aydın', <Badge key="4" tone="success">Boş</Badge>],
]

export default function KampPage() {
  return (
    <ModulePage
      title="Kamp Yönetimi"
      subtitle="Şantiye kampı konaklama, kapasite ve yemek takibi"
      primaryAction="Konaklama Ekle"
      primaryIcon={Plus}
      stats={[
        { label: 'Toplam Kamp', value: '4', icon: Tent, iconTone: 'info' },
        { label: 'Konaklayan', value: '186', icon: Users, iconTone: 'primary' },
        { label: 'Doluluk', value: '%82', icon: BedDouble, iconTone: 'warning' },
        { label: 'Günlük Öğün', value: '558', icon: UtensilsCrossed, iconTone: 'success' },
      ]}
      columns={columns}
      rows={rows}
    />
  )
}
