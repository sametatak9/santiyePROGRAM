import { HardHat, Activity, CheckCircle2, AlertTriangle, Plus } from 'lucide-react'
import { ModulePage, Badge, type Column } from '@/components/module-page'

const columns: Column[] = [
  { key: 'kod', label: 'Faaliyet No', mono: true },
  { key: 'saha', label: 'Saha / Bölge' },
  { key: 'is', label: 'Yapılan İş' },
  { key: 'tarih', label: 'Tarih' },
  { key: 'ilerleme', label: 'İlerleme', align: 'right' },
  { key: 'durum', label: 'Durum', align: 'right' },
]

const rows = [
  ['SAH-2026-088', 'A Blok', 'Kalıp ve demir montajı', '2026-06-16', '%75', <Badge key="1" tone="info">Devam Ediyor</Badge>],
  ['SAH-2026-087', 'B Blok', 'Beton döküm', '2026-06-15', '%100', <Badge key="2" tone="success">Tamamlandı</Badge>],
  ['SAH-2026-086', 'Çevre Düzenleme', 'Hafriyat', '2026-06-14', '%40', <Badge key="3" tone="info">Devam Ediyor</Badge>],
  ['SAH-2026-085', 'C Blok', 'Tesisat', '2026-06-12', '%20', <Badge key="4" tone="warning">Gecikmeli</Badge>],
]

export default function SahaPage() {
  return (
    <ModulePage
      title="Saha Faaliyetleri"
      subtitle="Günlük saha raporları, iş ilerlemesi ve İSG takibi"
      primaryAction="Faaliyet Ekle"
      primaryIcon={Plus}
      stats={[
        { label: 'Aktif Saha', value: '8', icon: HardHat, iconTone: 'info' },
        { label: 'Günlük Faaliyet', value: '34', icon: Activity, iconTone: 'primary' },
        { label: 'Tamamlanan', value: '212', icon: CheckCircle2, iconTone: 'success' },
        { label: 'Gecikmeli', value: '5', icon: AlertTriangle, iconTone: 'warning' },
      ]}
      columns={columns}
      rows={rows}
    />
  )
}
