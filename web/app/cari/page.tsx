import { Building2, ArrowDownLeft, ArrowUpRight, Scale, Plus } from 'lucide-react'
import { ModulePage, Badge, type Column } from '@/components/module-page'

const columns: Column[] = [
  { key: 'kod', label: 'Cari Kod', mono: true },
  { key: 'unvan', label: 'Ünvan' },
  { key: 'tur', label: 'Tür' },
  { key: 'tel', label: 'Telefon' },
  { key: 'bakiye', label: 'Bakiye', align: 'right', mono: true },
  { key: 'durum', label: 'Durum', align: 'right' },
]

const rows = [
  ['CR-0001', 'Demir A.Ş.', 'Tedarikçi', '0212 555 0101', '₺125.400', <Badge key="1" tone="destructive">Borç</Badge>],
  ['CR-0002', 'ABC Malzeme Ltd.', 'Tedarikçi', '0216 444 0202', '₺48.900', <Badge key="2" tone="destructive">Borç</Badge>],
  ['CR-0003', 'XYZ Tedarik', 'Tedarikçi', '0312 333 0303', '₺0', <Badge key="3" tone="neutral">Kapalı</Badge>],
  ['CR-0010', 'Beton Sanayi A.Ş.', 'Tedarikçi', '0224 222 0404', '₺212.000', <Badge key="4" tone="destructive">Borç</Badge>],
  ['CR-0021', 'Kibritçi İnşaat', 'Müşteri', '0212 555 9090', '₺340.500', <Badge key="5" tone="success">Alacak</Badge>],
]

export default function CariPage() {
  return (
    <ModulePage
      title="Cari Kartlar"
      subtitle="Müşteri ve tedarikçi hesapları, bakiye takibi"
      primaryAction="Cari Ekle"
      primaryIcon={Plus}
      stats={[
        { label: 'Toplam Cari', value: '284', icon: Building2, iconTone: 'info' },
        { label: 'Toplam Borç', value: '₺1.24M', icon: ArrowUpRight, iconTone: 'destructive' },
        { label: 'Toplam Alacak', value: '₺860K', icon: ArrowDownLeft, iconTone: 'success' },
        { label: 'Net Bakiye', value: '-₺380K', icon: Scale, iconTone: 'warning' },
      ]}
      columns={columns}
      rows={rows}
    />
  )
}
