import { ShoppingCart, Clock, CheckCircle2, XCircle, Plus } from 'lucide-react'
import { ModulePage, Badge, type Column } from '@/components/module-page'

const columns: Column[] = [
  { key: 'kod', label: 'Talep No', mono: true },
  { key: 'malzeme', label: 'Malzeme / Açıklama' },
  { key: 'talep', label: 'Talep Eden' },
  { key: 'tarih', label: 'Tarih' },
  { key: 'tutar', label: 'Tahmini Tutar', align: 'right' },
  { key: 'durum', label: 'Durum', align: 'right' },
]

const rows = [
  ['SAT-2026-041', 'Çimento + Demir takviyesi', 'A. Yılmaz', '2026-06-14', '₺85.000', <Badge key="1" tone="warning">Onay Bekliyor</Badge>],
  ['SAT-2026-040', 'Elektrik malzemeleri', 'M. Demir', '2026-06-12', '₺22.400', <Badge key="2" tone="success">Onaylandı</Badge>],
  ['SAT-2026-039', 'İskele ekipmanı', 'A. Kaya', '2026-06-10', '₺140.000', <Badge key="3" tone="success">Onaylandı</Badge>],
  ['SAT-2026-038', 'Ofis sarf malzemesi', 'F. Şahin', '2026-06-08', '₺3.800', <Badge key="4" tone="destructive">Reddedildi</Badge>],
]

export default function SatinAlmaPage() {
  return (
    <ModulePage
      title="Satın Alma Talep"
      subtitle="Malzeme talepleri, onay akışı ve tedarik takibi"
      primaryAction="Talep Oluştur"
      primaryIcon={Plus}
      stats={[
        { label: 'Toplam Talep', value: '186', icon: ShoppingCart, iconTone: 'info' },
        { label: 'Onay Bekleyen', value: '9', icon: Clock, iconTone: 'warning' },
        { label: 'Onaylanan', value: '162', icon: CheckCircle2, iconTone: 'success' },
        { label: 'Reddedilen', value: '15', icon: XCircle, iconTone: 'destructive' },
      ]}
      columns={columns}
      rows={rows}
    />
  )
}
