'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { BarChart3, Barcode, Beaker, AlertTriangle, TrendingUp, Gauge } from 'lucide-react'
import { cn } from '@/lib/utils'

export function Sidebar() {
  const pathname = usePathname()

  const menuItems = [
    { href: '/dashboard', label: 'Dashboard', icon: BarChart3 },
    { href: '/scanner', label: 'Scanner', icon: Barcode },
    { href: '/fill-monitor', label: 'Fill Monitor', icon: Beaker },
    { href: '/equipment-health', label: 'Equipment Health', icon: Gauge },
    { href: '/spc-control', label: 'SPC Control', icon: TrendingUp },
    { href: '/anomaly-database', label: 'Anomaly Database', icon: AlertTriangle },
  ]

  return (
    <aside className="fixed left-0 top-0 bottom-0 w-60 bg-sidebar border-r border-sidebar-border pt-20 flex flex-col glass-effect-strong shadow-glow-lg">
      <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
        {menuItems.map((item, index) => {
          const Icon = item.icon
          const isActive = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                'flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-300 animate-slide-in',
                `stagger-${index + 1}`,
                isActive
                  ? 'bg-sidebar-primary text-sidebar-primary-foreground shadow-glow scale-105'
                  : 'text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground hover:scale-105 hover:shadow-sm-glow'
              )}
            >
              <Icon className={cn("w-5 h-5 transition-transform duration-300", isActive && "animate-pulse-glow")} />
              <span className="font-medium">{item.label}</span>
            </Link>
          )
        })}
      </nav>

      {/* Status Footer */}
      <div className="p-4 border-t border-sidebar-border glass-effect">
        <div className="space-y-2 text-sm animate-fade-in">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-success animate-pulse-glow"></div>
            <span className="text-sidebar-foreground">System Online</span>
          </div>
          <div className="text-xs text-sidebar-foreground/60">CalibratePro v2.1</div>
        </div>
      </div>
    </aside>
  )
}
