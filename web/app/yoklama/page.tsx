import { CalendarCheck, UserCheck, UserX, Clock } from 'lucide-react'
import { ModulePage, Badge, type Column } from '@/components/module-page'

const columns: Column[] = [
  { key: 'ad', label: 'Personel' },
  { key: 'gorev', label: 'Görev' },
  { key: 'durum', label: 'Durum' },
  { key: 'giris', label: 'Giriş', align: 'center' },
  { key: 'cikis', label: 'Çıkış', align: 'center' },
  { key: 'mesai', label: 'Mesai (saat)', align: 'right' },
]

const rows = [
  ['Ahmet Yılmaz', 'Şantiye Şefi', <Badge key="1" tone="success">Geldi</Badge>, '08:00', '18:00', '2,0'],
  ['Mehmet Demir', 'Usta', <Badge key="2" tone="success">Geldi</Badge>, '07:30', '17:30', '1,5'],
  ['Ayşe Kaya', 'Muhasebe', <Badge key="3" tone="success">Geldi</Badge>, '09:00', '18:00', '0,0'],
  ['Ali Çelik', 'İşçi', <Badge key="4" tone="warning">İzin</Badge>, '—', '—', '0,0'],
  ['Hasan Aydın', 'Bekçi', <Badge key="5" tone="destructive">Yok</Badge>, '—', '—', '0,0'],
  ['Fatma Şahin', 'Operatör', <Badge key="6" tone="info">Rapor</Badge>, '—', '—', '0,0'],
]

export default function YoklamaPage() {
  return (
    <ModulePage
      title="Yoklama ve Puantaj"
      subtitle="Günlük yoklama, mesai ve aylık puantaj takibi"
      primaryAction="Yoklama Al"
      primaryIcon={CalendarCheck}
      stats={[
        { label: 'Bugün Gelen', value: '128', icon: UserCheck, iconTone: 'success' },
        { label: 'Gelmeyen', value: '6', icon: UserX, iconTone: 'warning' },
        { label: 'Toplam Mesai', value: '184 sa', icon: Clock, iconTone: 'info' },
        { label: 'Devam Oranı', value: '%95', icon: CalendarCheck, iconTone: 'primary' },
      ]}
      columns={columns}
      rows={rows}
    />
  )
}
