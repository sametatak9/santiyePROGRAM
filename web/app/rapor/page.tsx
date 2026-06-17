import { BarChart3, FileBarChart, Download, TrendingUp, Plus } from 'lucide-react'
import { ModulePage, Badge, type Column } from '@/components/module-page'

const columns: Column[] = [
  { key: 'ad', label: 'Rapor Adı' },
  { key: 'kategori', label: 'Kategori' },
  { key: 'donem', label: 'Dönem' },
  { key: 'olusturan', label: 'Oluşturan' },
  { key: 'format', label: 'Format' },
  { key: 'durum', label: 'Durum', align: 'right' },
]

const rows = [
  ['Aylık Maliyet Raporu', 'Finans', 'Haziran 2026', 'Sistem', 'PDF', <Badge key="1" tone="success">Hazır</Badge>],
  ['Personel Puantaj Özeti', 'Personel', 'Haziran 2026', 'İK', 'Excel', <Badge key="2" tone="success">Hazır</Badge>],
  ['Stok Hareket Raporu', 'Depo', 'Q2 2026', 'Sistem', 'Excel', <Badge key="3" tone="warning">Hazırlanıyor</Badge>],
  ['Araç Yakıt Analizi', 'Filo', 'Mayıs 2026', 'İdari', 'PDF', <Badge key="4" tone="success">Hazır</Badge>],
]

export default function RaporPage() {
  return (
    <ModulePage
      title="Raporlar"
      subtitle="Modül bazlı raporlama, dışa aktarma ve analiz"
      primaryAction="Rapor Oluştur"
      primaryIcon={Plus}
      stats={[
        { label: 'Hazır Rapor', value: '64', icon: FileBarChart, iconTone: 'info' },
        { label: 'Bu Ay Üretilen', value: '28', icon: BarChart3, iconTone: 'primary' },
        { label: 'İndirilen', value: '186', icon: Download, iconTone: 'success' },
        { label: 'Otomatik Rapor', value: '12', icon: TrendingUp, iconTone: 'warning' },
      ]}
      columns={columns}
      rows={rows}
    />
  )
}
