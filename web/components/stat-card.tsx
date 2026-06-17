import { cn } from '@/lib/utils'
import { ArrowUpRight, ArrowDownRight, type LucideIcon } from 'lucide-react'

export function StatCard({
  label,
  value,
  delta,
  deltaPositive,
  icon: Icon,
  iconTone = 'primary',
}: {
  label: string
  value: string
  delta?: string
  deltaPositive?: boolean
  icon: LucideIcon
  iconTone?: 'primary' | 'info' | 'success' | 'warning'
}) {
  const toneBg: Record<string, string> = {
    primary: 'bg-primary/10 text-primary',
    info: 'bg-info/10 text-info',
    success: 'bg-success/10 text-success',
    warning: 'bg-warning/15 text-warning-foreground',
  }

  return (
    <div className="rounded-xl border border-border bg-card p-5 shadow-sm transition-shadow hover:shadow-md">
      <div className="flex items-start justify-between">
        <div className={cn('flex size-10 items-center justify-center rounded-lg', toneBg[iconTone])}>
          <Icon className="size-5" strokeWidth={2} />
        </div>
        {delta && (
          <span
            className={cn(
              'inline-flex items-center gap-0.5 text-xs font-medium',
              deltaPositive ? 'text-success' : 'text-destructive',
            )}
          >
            {deltaPositive ? (
              <ArrowUpRight className="size-3.5" />
            ) : (
              <ArrowDownRight className="size-3.5" />
            )}
            {delta}
          </span>
        )}
      </div>
      <p className="mt-4 text-2xl font-semibold tracking-tight text-foreground tabular-nums">
        {value}
      </p>
      <p className="mt-1 text-sm text-muted-foreground">{label}</p>
    </div>
  )
}
