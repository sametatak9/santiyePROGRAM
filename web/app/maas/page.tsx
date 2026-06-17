import { Wallet, Calculator, TrendingUp, Clock, FileText } from 'lucide-react'
import { ModulePage, Badge, type Column } from '@/components/module-page'

const columns: Column[] = [
  { key: 'ad', label: 'Ad Soyad' },
  { key: 'gun', label: 'Çalışılan Gün', align: 'right' },
  { key: 'mesai', label: 'Mesai (saat)', align: 'right' },
  { key: 'brut', label: 'Brüt', align: 'right' },
  { key: 'net', label: 'Net Maaş', align: 'right', mono: true },
  { key: 'durum', label: 'Durum', align: 'right' },
]

const rows = [
  ['Ahmet Yılmaz', '30', '12', '₺58.000', '₺48.200', <Badge key="1" tone="success">Ödendi</Badge>],
  ['Mehmet Demir', '28', '20', '₺42.000', '₺36.800', <Badge key="2" tone="success">Ödendi</Badge>],
  ['Ayşe Kaya', '30', '4', '₺48.000', '₺40.100', <Badge key="3" tone="warning">Beklemede</Badge>],
  ['Fatma Şahin', '26', '16', '₺45.000', '₺38.400', <Badge key="4" tone="warning">Beklemede</Badge>],
  ['Ali Çelik', '22', '0', '₺38.000', '₺30.900', <Badge key="5" tone="neutral">Taslak</Badge>],
]

export default function MaasPage() {
  return (
    <ModulePage
      title="Maaş Hesaplama"
      subtitle="Puantaj bazlı maaş, mesai ve kesinti hesaplama"
      primaryAction="Bordro Oluştur"
      primaryIcon={FileText}
      stats={[
        { label: 'Toplam Bordro', value: '₺6.84M', icon: Wallet, iconTone: 'primary' },
        { label: 'Hesaplanan', value: '142', icon: Calculator, iconTone: 'info' },
        { label: 'Ort. Net Maaş', value: '₺41.300', icon: TrendingUp, iconTone: 'success' },
        { label: 'Bekleyen', value: '14', icon: Clock, iconTone: 'warning' },
      ]}
      columns={columns}
      rows={rows}
    />
  )
}
