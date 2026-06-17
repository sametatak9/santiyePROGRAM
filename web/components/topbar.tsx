'use client'

import { usePathname } from 'next/navigation'
import { Search, Bell, ChevronRight } from 'lucide-react'
import { findModuleByHref } from '@/lib/navigation'

export function Topbar() {
  const pathname = usePathname()
  const current = findModuleByHref(pathname)

  return (
    <header className="sticky top-0 z-20 flex h-16 shrink-0 items-center justify-between gap-4 border-b border-border bg-card/80 px-6 backdrop-blur-md">
      {/* Breadcrumb */}
      <div className="flex min-w-0 items-center gap-2 text-sm">
        <span className="font-medium text-muted-foreground">KIBRITCI ERP</span>
        <ChevronRight className="size-4 text-muted-foreground/50" />
        <span className="truncate font-semibold text-foreground">
          {current?.label ?? 'Genel Bakış'}
        </span>
      </div>

      <div className="flex items-center gap-2">
        {/* Search */}
        <div className="relative hidden md:block">
          <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
          <input
            type="search"
            placeholder="Ara..."
            className="h-9 w-56 rounded-lg border border-border bg-secondary/60 pl-9 pr-3 text-sm outline-none transition-colors placeholder:text-muted-foreground focus:border-ring focus:bg-card focus:ring-2 focus:ring-ring/20"
          />
        </div>

        {/* Notifications */}
        <button
          className="relative flex size-9 items-center justify-center rounded-lg border border-border bg-card text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
          aria-label="Bildirimler"
        >
          <Bell className="size-[18px]" />
          <span className="absolute right-2 top-2 size-2 rounded-full bg-destructive ring-2 ring-card" />
        </button>

        {/* Status */}
        <div className="flex h-9 items-center gap-2 rounded-lg border border-success/30 bg-success/10 px-3">
          <span className="size-2 rounded-full bg-success" />
          <span className="text-[13px] font-medium text-success">Aktif</span>
        </div>
      </div>
    </header>
  )
}
