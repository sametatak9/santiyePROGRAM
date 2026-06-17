import { FileSignature, FilePlus2, FileCheck2, Archive, Plus } from 'lucide-react'
import { ModulePage, Badge, type Column } from '@/components/module-page'

const columns: Column[] = [
  { key: 'kod', label: 'Tutanak No', mono: true },
  { key: 'konu', label: 'Konu' },
  { key: 'tur', label: 'Tür' },
  { key: 'tarih', label: 'Tarih' },
  { key: 'taraf', label: 'Düzenleyen' },
  { key: 'durum', label: 'Durum', align: 'right' },
]

const rows = [
  ['TTN-2026-018', 'İş kazası bildirim tutanağı', 'İSG', '2026-06-14', 'A. Yılmaz', <Badge key="1" tone="success">İmzalandı</Badge>],
  ['TTN-2026-017', 'Malzeme teslim tutanağı', 'Teslim', '2026-06-12', 'F. Şahin', <Badge key="2" tone="success">İmzalandı</Badge>],
  ['TTN-2026-016', 'Disiplin tutanağı', 'Personel', '2026-06-10', 'İK', <Badge key="3" tone="warning">İmza Bekliyor</Badge>],
  ['TTN-2026-015', 'Sayım tutanağı', 'Envanter', '2026-06-05', 'M. Demir', <Badge key="4" tone="neutral">Taslak</Badge>],
]

export default function TutanakPage() {
  return (
    <ModulePage
      title="Hazır Tutanaklar"
      subtitle="Tutanak şablonları, oluşturma ve arşivleme"
      primaryAction="Tutanak Oluştur"
      primaryIcon={Plus}
      stats={[
        { label: 'Toplam Tutanak', value: '94', icon: FileSignature, iconTone: 'info' },
        { label: 'Bu Ay', value: '12', icon: FilePlus2, iconTone: 'primary' },
        { label: 'İmzalanan', value: '78', icon: FileCheck2, iconTone: 'success' },
        { label: 'Arşivlenen', value: '64', icon: Archive, iconTone: 'neutral' },
      ]}
      columns={columns}
      rows={rows}
    />
  )
}
