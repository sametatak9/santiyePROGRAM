import { Users, UserCheck, UserMinus, Building2, UserPlus } from 'lucide-react'
import { ModulePage, Badge, type Column } from '@/components/module-page'

const columns: Column[] = [
  { key: 'tc', label: 'TC No', mono: true },
  { key: 'ad', label: 'Ad Soyad' },
  { key: 'gorev', label: 'Görev' },
  { key: 'departman', label: 'Departman' },
  { key: 'maas', label: 'Maaş', align: 'right' },
  { key: 'durum', label: 'Durum', align: 'right' },
]

const rows = [
  ['12345678901', 'Ahmet Yılmaz', 'Şantiye Şefi', 'Saha', '₺58.000', <Badge key="1" tone="success">Aktif</Badge>],
  ['98765432109', 'Mehmet Demir', 'Usta', 'İnşaat', '₺42.000', <Badge key="2" tone="success">Aktif</Badge>],
  ['45678912345', 'Ayşe Kaya', 'Muhasebe', 'İdari', '₺48.000', <Badge key="3" tone="success">Aktif</Badge>],
  ['32165498712', 'Fatma Şahin', 'Operatör', 'Makine', '₺45.000', <Badge key="4" tone="success">Aktif</Badge>],
  ['78912345678', 'Ali Çelik', 'İşçi', 'İnşaat', '₺38.000', <Badge key="5" tone="warning">İzinde</Badge>],
  ['65498732165', 'Hasan Aydın', 'Bekçi', 'Güvenlik', '₺36.000', <Badge key="6" tone="destructive">Pasif</Badge>],
]

export default function PersonelPage() {
  return (
    <ModulePage
      title="Personel Yönetimi"
      subtitle="Kayıt, düzenleme, durum ve personel raporları"
      primaryAction="Personel Ekle"
      primaryIcon={UserPlus}
      stats={[
        { label: 'Toplam Personel', value: '156', icon: Users, iconTone: 'info' },
        { label: 'Aktif', value: '142', icon: UserCheck, iconTone: 'success' },
        { label: 'İzinli / Raporlu', value: '8', icon: UserMinus, iconTone: 'warning' },
        { label: 'Departman', value: '6', icon: Building2, iconTone: 'primary' },
      ]}
      columns={columns}
      rows={rows}
    />
  )
}
