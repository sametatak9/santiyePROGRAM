import { ClipboardList, ArrowRightLeft, Undo2, Clock, Plus } from 'lucide-react'
import { ModulePage, Badge, type Column } from '@/components/module-page'

const columns: Column[] = [
  { key: 'kod', label: 'Tahsis No', mono: true },
  { key: 'demirbas', label: 'Demirbaş / Ekipman' },
  { key: 'kisi', label: 'Teslim Edilen' },
  { key: 'tarih', label: 'Teslim Tarihi' },
  { key: 'iade', label: 'İade Tarihi' },
  { key: 'durum', label: 'Durum', align: 'right' },
]

const rows = [
  ['THS-0201', 'Dizüstü Bilgisayar', 'A. Kaya', '2026-01-12', '—', <Badge key="1" tone="info">Zimmette</Badge>],
  ['THS-0202', 'Matkap Seti', 'M. Demir', '2026-06-01', '2026-06-15', <Badge key="2" tone="success">İade Edildi</Badge>],
  ['THS-0203', 'Telsiz (4 adet)', 'Saha Ekibi', '2026-05-20', '—', <Badge key="3" tone="info">Zimmette</Badge>],
  ['THS-0204', 'Ölçüm Cihazı', 'A. Yılmaz', '2026-04-10', '—', <Badge key="4" tone="warning">İade Gecikti</Badge>],
]

export default function TahsisPage() {
  return (
    <ModulePage
      title="Tahsisleme"
      subtitle="Ekipman / demirbaş zimmet ve iade işlemleri"
      primaryAction="Tahsis Yap"
      primaryIcon={Plus}
      stats={[
        { label: 'Aktif Tahsis', value: '312', icon: ClipboardList, iconTone: 'info' },
        { label: 'Bu Ay Zimmet', value: '24', icon: ArrowRightLeft, iconTone: 'primary' },
        { label: 'Bu Ay İade', value: '18', icon: Undo2, iconTone: 'success' },
        { label: 'İadesi Geciken', value: '7', icon: Clock, iconTone: 'warning' },
      ]}
      columns={columns}
      rows={rows}
    />
  )
}
