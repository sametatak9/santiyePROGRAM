import { Banknote, ArrowDownLeft, ArrowUpRight, Wallet, Plus } from 'lucide-react'
import { ModulePage, Badge, type Column } from '@/components/module-page'

const columns: Column[] = [
  { key: 'tarih', label: 'Tarih', mono: true },
  { key: 'aciklama', label: 'Açıklama' },
  { key: 'tur', label: 'Tür' },
  { key: 'giris', label: 'Giriş', align: 'right' },
  { key: 'cikis', label: 'Çıkış', align: 'right' },
  { key: 'durum', label: 'Tip', align: 'right' },
]

const rows = [
  ['2026-06-16', 'Hakediş tahsilatı', 'Tahsilat', '₺340.000', '—', <Badge key="1" tone="success">Giriş</Badge>],
  ['2026-06-15', 'Demir A.Ş. ödeme', 'Tedarikçi', '—', '₺50.000', <Badge key="2" tone="destructive">Çıkış</Badge>],
  ['2026-06-14', 'Personel maaş ödemesi', 'Maaş', '—', '₺684.000', <Badge key="3" tone="destructive">Çıkış</Badge>],
  ['2026-06-13', 'Yakıt ve bakım', 'Araç', '—', '₺18.400', <Badge key="4" tone="destructive">Çıkış</Badge>],
  ['2026-06-12', 'Avans iadesi', 'Tahsilat', '₺12.000', '—', <Badge key="5" tone="success">Giriş</Badge>],
]

export default function KasaPage() {
  return (
    <ModulePage
      title="Haftalık Kasa"
      subtitle="Nakit giriş/çıkış hareketleri ve haftalık kasa raporu"
      primaryAction="Hareket Ekle"
      primaryIcon={Plus}
      stats={[
        { label: 'Açılış Bakiyesi', value: '₺1.2M', icon: Wallet, iconTone: 'info' },
        { label: 'Haftalık Giriş', value: '₺352K', icon: ArrowDownLeft, iconTone: 'success' },
        { label: 'Haftalık Çıkış', value: '₺752K', icon: ArrowUpRight, iconTone: 'destructive' },
        { label: 'Kapanış Bakiyesi', value: '₺800K', icon: Banknote, iconTone: 'primary' },
      ]}
      columns={columns}
      rows={rows}
    />
  )
}
