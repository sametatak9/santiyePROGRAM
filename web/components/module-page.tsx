import type { ReactNode } from 'react'
import { Search, Filter, Download, Plus, type LucideIcon } from 'lucide-react'
import { AppShell } from '@/components/app-shell'
import { PageHeader, Card, Badge, Button } from '@/components/ui'
import { StatCard } from '@/components/stat-card'

export type Column = {
  key: string
  label: string
  align?: 'left' | 'right' | 'center'
  mono?: boolean
}

export type Stat = {
  label: string
  value: string
  icon: LucideIcon
  iconTone?: 'primary' | 'info' | 'success' | 'warning'
}

export type RowCell = ReactNode

export function ModulePage({
  title,
  subtitle,
  stats,
  columns,
  rows,
  primaryAction = 'Yeni Ekle',
  primaryIcon: PrimaryIcon = Plus,
}: {
  title: string
  subtitle: string
  stats?: Stat[]
  columns: Column[]
  rows: RowCell[][]
  primaryAction?: string
  primaryIcon?: LucideIcon
}) {
  return (
    <AppShell>
      <PageHeader
        title={title}
        subtitle={subtitle}
        actions={
          <>
            <Button variant="outline">
              <Download className="size-4" />
              Dışa Aktar
            </Button>
            <Button>
              <PrimaryIcon className="size-4" />
              {primaryAction}
            </Button>
          </>
        }
      />

      {stats && stats.length > 0 && (
        <div className="mt-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
          {stats.map((s) => (
            <StatCard
              key={s.label}
              label={s.label}
              value={s.value}
              icon={s.icon}
              iconTone={s.iconTone}
            />
          ))}
        </div>
      )}

      <Card className="mt-6 overflow-hidden">
        {/* Toolbar */}
        <div className="flex flex-col gap-3 border-b border-border p-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="relative max-w-sm flex-1">
            <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
            <input
              type="search"
              placeholder="Bu modülde ara..."
              className="h-9 w-full rounded-lg border border-border bg-secondary/60 pl-9 pr-3 text-sm outline-none transition-colors placeholder:text-muted-foreground focus:border-ring focus:bg-card focus:ring-2 focus:ring-ring/20"
            />
          </div>
          <Button variant="outline" className="self-start sm:self-auto">
            <Filter className="size-4" />
            Filtrele
          </Button>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border text-xs uppercase tracking-wide text-muted-foreground">
                {columns.map((c) => (
                  <th
                    key={c.key}
                    className={`px-5 py-3 font-medium ${
                      c.align === 'right'
                        ? 'text-right'
                        : c.align === 'center'
                          ? 'text-center'
                          : 'text-left'
                    }`}
                  >
                    {c.label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, ri) => (
                <tr
                  key={ri}
                  className="border-b border-border/60 last:border-0 transition-colors hover:bg-secondary/50"
                >
                  {row.map((cell, ci) => {
                    const c = columns[ci]
                    return (
                      <td
                        key={ci}
                        className={`px-5 py-3.5 ${
                          c?.align === 'right'
                            ? 'text-right'
                            : c?.align === 'center'
                              ? 'text-center'
                              : 'text-left'
                        } ${c?.mono ? 'font-mono text-[13px] font-medium text-foreground' : 'text-foreground'}`}
                      >
                        {cell}
                      </td>
                    )
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between border-t border-border px-5 py-3 text-xs text-muted-foreground">
          <span>{rows.length} kayıt gösteriliyor</span>
          <div className="flex items-center gap-1">
            <button className="rounded-md border border-border px-2.5 py-1 transition-colors hover:bg-secondary">
              Önceki
            </button>
            <button className="rounded-md border border-border bg-secondary px-2.5 py-1 font-medium text-foreground">
              1
            </button>
            <button className="rounded-md border border-border px-2.5 py-1 transition-colors hover:bg-secondary">
              Sonraki
            </button>
          </div>
        </div>
      </Card>
    </AppShell>
  )
}

export { Badge }
