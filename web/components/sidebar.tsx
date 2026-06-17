'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Flame, LogOut, ChevronsUpDown } from 'lucide-react'
import { navGroups } from '@/lib/navigation'
import { cn } from '@/lib/utils'

export function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="flex h-full w-[264px] shrink-0 flex-col bg-sidebar text-sidebar-foreground">
      {/* Brand */}
      <div className="flex items-center gap-3 px-5 py-5">
        <div className="flex size-10 items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-lg shadow-primary/20">
          <Flame className="size-5" strokeWidth={2.5} />
        </div>
        <div className="min-w-0">
          <p className="truncate text-[15px] font-semibold leading-tight tracking-tight">
            KIBRITCI ERP
          </p>
          <p className="truncate text-xs text-sidebar-muted">Şantiye Yönetim Sistemi</p>
        </div>
      </div>

      {/* Project switcher */}
      <div className="px-3 pb-3">
        <button className="flex w-full items-center justify-between rounded-lg border border-sidebar-border bg-sidebar-accent/40 px-3 py-2 text-left transition-colors hover:bg-sidebar-accent">
          <div className="min-w-0">
            <p className="truncate text-[13px] font-medium">Merkez Şantiye</p>
            <p className="truncate text-[11px] text-sidebar-muted">Kıbrıtçı İnşaat</p>
          </div>
          <ChevronsUpDown className="size-4 shrink-0 text-sidebar-muted" />
        </button>
      </div>

      {/* Nav */}
      <nav className="scroll-thin flex-1 overflow-y-auto px-3 pb-4">
        {navGroups.map((group) => (
          <div key={group.key} className="mb-1">
            <p className="px-3 pb-1.5 pt-4 text-[10px] font-semibold uppercase tracking-wider text-sidebar-muted">
              {group.label}
            </p>
            <ul className="space-y-0.5">
              {group.items.map((item) => {
                const active = pathname === item.href
                const Icon = item.icon
                return (
                  <li key={item.key}>
                    <Link
                      href={item.href}
                      className={cn(
                        'group flex items-center gap-3 rounded-lg px-3 py-2 text-[13px] font-medium transition-colors',
                        active
                          ? 'bg-primary text-primary-foreground shadow-sm shadow-primary/20'
                          : 'text-sidebar-foreground/80 hover:bg-sidebar-accent hover:text-sidebar-foreground',
                      )}
                    >
                      <Icon
                        className={cn(
                          'size-[18px] shrink-0',
                          active ? 'text-primary-foreground' : 'text-sidebar-muted group-hover:text-sidebar-foreground',
                        )}
                        strokeWidth={2}
                      />
                      <span className="truncate">{item.label}</span>
                    </Link>
                  </li>
                )
              })}
            </ul>
          </div>
        ))}
      </nav>

      {/* User footer */}
      <div className="border-t border-sidebar-border p-3">
        <div className="flex items-center gap-3 rounded-lg px-2 py-2">
          <div className="flex size-9 shrink-0 items-center justify-center rounded-full bg-primary/15 text-sm font-semibold text-primary">
            YK
          </div>
          <div className="min-w-0 flex-1">
            <p className="truncate text-[13px] font-medium">Yönetici</p>
            <p className="truncate text-[11px] text-sidebar-muted">v1.0 · Supabase bağlı</p>
          </div>
          <button
            className="rounded-md p-1.5 text-sidebar-muted transition-colors hover:bg-sidebar-accent hover:text-sidebar-foreground"
            aria-label="Çıkış yap"
          >
            <LogOut className="size-4" />
          </button>
        </div>
      </div>
    </aside>
  )
}
