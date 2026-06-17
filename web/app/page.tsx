import Link from 'next/link'
import {
  Users,
  Banknote,
  Truck,
  Car,
  TrendingUp,
  CircleAlert,
  CircleCheck,
  Clock,
  ArrowRight,
} from 'lucide-react'
import { AppShell } from '@/components/app-shell'
import { PageHeader, Card, CardHeader, Badge, Button } from '@/components/ui'
import { StatCard } from '@/components/stat-card'
import { navGroups } from '@/lib/navigation'
import { formatTRY } from '@/lib/utils'

const recentInvoices = [
  { code: 'FT-20260001', firma: 'Demir A.Ş.', tarih: '10.06.2026', tutar: 50000, durum: 'Onaylı' },
  { code: 'FT-20260002', firma: 'ABC Malzeme', tarih: '12.06.2026', tutar: 30000, durum: 'Bekliyor' },
  { code: 'FT-20260003', firma: 'XYZ Tedarik', tarih: '14.06.2026', tutar: 20000, durum: 'Uyumsuz' },
  { code: 'FT-20260004', firma: 'Beton San.', tarih: '15.06.2026', tutar: 78500, durum: 'Onaylı' },
]

const tasks = [
  { icon: CircleAlert, tone: 'destructive' as const, text: '3 araç muayene tarihi bu ay doluyor', meta: 'Araç ve Bakım' },
  { icon: Clock, tone: 'warning' as const, text: '5 fatura onay bekliyor', meta: 'Fatura Girişi' },
  { icon: CircleAlert, tone: 'warning' as const, text: '2 satın alma talebi imzalı evrak bekliyor', meta: 'Satın Alma' },
  { icon: CircleCheck, tone: 'success' as const, text: 'Haziran puantajı tamamlandı', meta: 'Yoklama' },
]

const durumTone = {
  Onaylı: 'success',
  Bekliyor: 'warning',
  Uyumsuz: 'destructive',
} as const

export default function DashboardPage() {
  const today = new Date().toLocaleDateString('tr-TR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })

  // Quick-access: skip the dashboard group itself
  const quickModules = navGroups
    .filter((g) => g.key !== 'genel')
    .flatMap((g) => g.items)
    .slice(0, 8)

  return (
    <AppShell>
      <PageHeader
        title="Genel Bakış"
        subtitle={`Kıbrıtçı şantiye operasyonları · ${today}`}
        actions={
          <>
            <Button variant="outline">Rapor Al</Button>
            <Button>Yeni Kayıt</Button>
          </>
        }
      />

      {/* Stats */}
      <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Aktif Personel" value="142" delta="%4,2" deltaPositive icon={Users} iconTone="info" />
        <StatCard label="Aylık Kasa Hareketi" value={formatTRY(1284000)} delta="%8,1" deltaPositive icon={Banknote} iconTone="success" />
        <StatCard label="Bekleyen İrsaliye" value="18" delta="%2,0" deltaPositive={false} icon={Truck} iconTone="warning" />
        <StatCard label="Araç ve İş Makinesi" value="37" delta="%1,1" deltaPositive icon={Car} iconTone="primary" />
      </div>

      {/* Main grid */}
      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Recent invoices */}
        <Card className="lg:col-span-2">
          <CardHeader
            title="Son Faturalar"
            action={
              <Link
                href="/fatura"
                className="inline-flex items-center gap-1 text-[13px] font-medium text-primary hover:underline"
              >
                Tümünü gör <ArrowRight className="size-3.5" />
              </Link>
            }
          />
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border text-left text-xs uppercase tracking-wide text-muted-foreground">
                  <th className="px-5 py-3 font-medium">Fatura Kodu</th>
                  <th className="px-5 py-3 font-medium">Firma</th>
                  <th className="px-5 py-3 font-medium">Tarih</th>
                  <th className="px-5 py-3 text-right font-medium">Tutar</th>
                  <th className="px-5 py-3 text-right font-medium">Durum</th>
                </tr>
              </thead>
              <tbody>
                {recentInvoices.map((inv) => (
                  <tr
                    key={inv.code}
                    className="border-b border-border/60 last:border-0 transition-colors hover:bg-secondary/50"
                  >
                    <td className="px-5 py-3.5 font-mono text-[13px] font-medium text-foreground">
                      {inv.code}
                    </td>
                    <td className="px-5 py-3.5 text-foreground">{inv.firma}</td>
                    <td className="px-5 py-3.5 text-muted-foreground">{inv.tarih}</td>
                    <td className="px-5 py-3.5 text-right font-medium tabular-nums text-foreground">
                      {formatTRY(inv.tutar)}
                    </td>
                    <td className="px-5 py-3.5 text-right">
                      <Badge tone={durumTone[inv.durum as keyof typeof durumTone]}>
                        {inv.durum}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>

        {/* Tasks */}
        <Card>
          <CardHeader title="Dikkat Gerektirenler" />
          <ul className="divide-y divide-border/60">
            {tasks.map((task, i) => {
              const Icon = task.icon
              const toneColor = {
                destructive: 'text-destructive bg-destructive/10',
                warning: 'text-warning-foreground bg-warning/15',
                success: 'text-success bg-success/10',
              }[task.tone]
              return (
                <li key={i} className="flex items-start gap-3 px-5 py-3.5">
                  <span className={`mt-0.5 flex size-7 shrink-0 items-center justify-center rounded-lg ${toneColor}`}>
                    <Icon className="size-4" />
                  </span>
                  <div className="min-w-0">
                    <p className="text-[13px] font-medium leading-snug text-foreground">{task.text}</p>
                    <p className="mt-0.5 text-xs text-muted-foreground">{task.meta}</p>
                  </div>
                </li>
              )
            })}
          </ul>
        </Card>
      </div>

      {/* Quick access modules */}
      <div className="mt-6">
        <h2 className="mb-3 text-[13px] font-semibold uppercase tracking-wide text-muted-foreground">
          Hızlı Erişim
        </h2>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
          {quickModules.map((mod) => {
            const Icon = mod.icon
            return (
              <Link
                key={mod.key}
                href={mod.href}
                className="group flex items-center gap-3 rounded-xl border border-border bg-card p-4 shadow-sm transition-all hover:border-primary/30 hover:shadow-md"
              >
                <span className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-secondary text-muted-foreground transition-colors group-hover:bg-primary/10 group-hover:text-primary">
                  <Icon className="size-5" />
                </span>
                <div className="min-w-0">
                  <p className="truncate text-[13px] font-medium text-foreground">{mod.label}</p>
                  <p className="truncate text-xs text-muted-foreground">{mod.desc}</p>
                </div>
              </Link>
            )
          })}
        </div>
      </div>
    </AppShell>
  )
}
