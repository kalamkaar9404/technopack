'use client'

import { Clock, Bell, AlertCircle, X, AlertTriangle, Info, CheckCircle } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

interface Alert {
  id: number
  priority: 'critical' | 'high' | 'medium' | 'low'
  title: string
  message: string
  timestamp: string
  source: string
  acknowledged: boolean
}

export function Header() {
  const [time, setTime] = useState<string>('')
  const [showAlerts, setShowAlerts] = useState(false)
  const [alerts, setAlerts] = useState<Alert[]>([
    {
      id: 1,
      priority: 'high',
      title: 'Pressure Drift Detected',
      message: 'Line 2 pressure has drifted 3% above target. Recommend calibration check.',
      timestamp: '2 minutes ago',
      source: 'Equipment Health Monitor',
      acknowledged: false
    },
    {
      id: 2,
      priority: 'medium',
      title: 'Maintenance Due Soon',
      message: 'Valve replacement scheduled in 7 days. Parts have been ordered.',
      timestamp: '1 hour ago',
      source: 'Predictive Maintenance',
      acknowledged: false
    },
    {
      id: 3,
      priority: 'low',
      title: 'Model Retrained Successfully',
      message: 'PINN model updated with 150 new samples. Accuracy improved to 98.2%.',
      timestamp: '3 hours ago',
      source: 'AI Training System',
      acknowledged: true
    },
    {
      id: 4,
      priority: 'medium',
      title: 'Fill Variance Increasing',
      message: 'Product SKU-250 showing increased variance. SPC control limits approaching.',
      timestamp: '5 hours ago',
      source: 'SPC Monitor',
      acknowledged: false
    }
  ])

  useEffect(() => {
    setTime(new Date().toLocaleTimeString())
    const interval = setInterval(() => {
      setTime(new Date().toLocaleTimeString())
    }, 1000)
    return () => clearInterval(interval)
  }, [])

  const unacknowledgedCount = alerts.filter(a => !a.acknowledged).length

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return { bg: 'bg-destructive/10', border: 'border-destructive/30', text: 'text-destructive', icon: 'bg-destructive/20' }
      case 'high': return { bg: 'bg-warning/10', border: 'border-warning/30', text: 'text-warning', icon: 'bg-warning/20' }
      case 'medium': return { bg: 'bg-primary/10', border: 'border-primary/30', text: 'text-primary', icon: 'bg-primary/20' }
      case 'low': return { bg: 'bg-success/10', border: 'border-success/30', text: 'text-success', icon: 'bg-success/20' }
      default: return { bg: 'bg-muted/10', border: 'border-border', text: 'text-foreground', icon: 'bg-muted/20' }
    }
  }

  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case 'critical': return AlertCircle
      case 'high': return AlertTriangle
      case 'medium': return Info
      case 'low': return CheckCircle
      default: return Info
    }
  }

  const acknowledgeAlert = (id: number) => {
    setAlerts(alerts.map(alert => 
      alert.id === id ? { ...alert, acknowledged: true } : alert
    ))
  }

  const acknowledgeAll = () => {
    setAlerts(alerts.map(alert => ({ ...alert, acknowledged: true })))
  }

  return (
    <>
      <header className="fixed top-0 left-60 right-0 h-16 bg-card border-b border-border flex items-center justify-between px-6 z-40 glass-effect-strong shadow-glow animate-slide-in">
        <div className="flex items-center gap-4">
          <h1 className="text-xl font-semibold text-foreground text-glow">PINNs-UPC Calibration System</h1>
        </div>

        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2 text-sm text-foreground/70 animate-fade-in stagger-1">
            <Clock className="w-4 h-4 animate-pulse-glow" />
            <span className="font-mono">{time}</span>
          </div>

          <div className="flex items-center gap-3 animate-fade-in stagger-2">
            <button 
              onClick={() => setShowAlerts(!showAlerts)}
              className="relative p-2 text-foreground/60 hover:text-foreground transition-all duration-300 hover:scale-110 hover-glow rounded-lg"
            >
              <Bell className="w-5 h-5" />
              {unacknowledgedCount > 0 && (
                <span className="absolute top-1 right-1 w-2 h-2 bg-destructive rounded-full animate-pulse-glow"></span>
              )}
            </button>

            <button
              onClick={() => setShowAlerts(!showAlerts)}
              className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-warning/10 border border-warning/20 shadow-sm-glow hover-scale transition-all duration-300"
            >
              <AlertCircle className="w-4 h-4 text-warning animate-pulse-glow" />
              <span className="text-xs font-medium text-warning">{unacknowledgedCount} Alerts</span>
            </button>
          </div>
        </div>
      </header>

      {/* Alerts Modal */}
      {showAlerts && (
        <>
          {/* Backdrop */}
          <div 
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 animate-fade-in"
            onClick={() => setShowAlerts(false)}
          ></div>

          {/* Modal */}
          <div className="fixed top-20 right-6 w-[500px] max-h-[calc(100vh-120px)] z-50 animate-slide-in">
            <Card className="border-2 border-primary/30 bg-card shadow-glow-lg overflow-hidden">
              {/* Header */}
              <div className="p-4 border-b border-border bg-gradient-to-r from-primary/10 to-accent/10">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-primary/20 rounded-lg">
                      <Bell className="w-5 h-5 text-primary" />
                    </div>
                    <div>
                      <h3 className="text-lg font-bold text-foreground">System Alerts</h3>
                      <p className="text-xs text-foreground/60">{unacknowledgedCount} unacknowledged</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {unacknowledgedCount > 0 && (
                      <Button
                        onClick={acknowledgeAll}
                        size="sm"
                        variant="outline"
                        className="text-xs"
                      >
                        Acknowledge All
                      </Button>
                    )}
                    <button
                      onClick={() => setShowAlerts(false)}
                      className="p-1 hover:bg-muted rounded transition-colors"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>

              {/* Alerts List */}
              <div className="max-h-[calc(100vh-240px)] overflow-y-auto">
                {alerts.length === 0 ? (
                  <div className="p-8 text-center">
                    <CheckCircle className="w-12 h-12 text-success mx-auto mb-3 opacity-50" />
                    <p className="text-foreground/60">No alerts at this time</p>
                  </div>
                ) : (
                  <div className="p-4 space-y-3">
                    {alerts
                      .sort((a, b) => {
                        // Sort by acknowledged status first, then by priority
                        if (a.acknowledged !== b.acknowledged) {
                          return a.acknowledged ? 1 : -1
                        }
                        const priorityOrder = { critical: 0, high: 1, medium: 2, low: 3 }
                        return priorityOrder[a.priority] - priorityOrder[b.priority]
                      })
                      .map((alert) => {
                        const colors = getPriorityColor(alert.priority)
                        const Icon = getPriorityIcon(alert.priority)

                        return (
                          <Card
                            key={alert.id}
                            className={`p-4 border ${colors.border} ${colors.bg} transition-all duration-300 hover-lift ${
                              alert.acknowledged ? 'opacity-60' : ''
                            }`}
                          >
                            <div className="flex items-start gap-3">
                              <div className={`p-2 ${colors.icon} rounded-lg flex-shrink-0 ${
                                !alert.acknowledged ? 'animate-pulse-glow' : ''
                              }`}>
                                <Icon className={`w-4 h-4 ${colors.text}`} />
                              </div>
                              <div className="flex-1 min-w-0">
                                <div className="flex items-start justify-between gap-2 mb-1">
                                  <h4 className="font-semibold text-foreground text-sm">
                                    {alert.title}
                                  </h4>
                                  <span className={`text-xs font-medium px-2 py-0.5 rounded ${colors.bg} ${colors.text} border ${colors.border} whitespace-nowrap`}>
                                    {alert.priority.toUpperCase()}
                                  </span>
                                </div>
                                <p className="text-sm text-foreground/70 mb-2">
                                  {alert.message}
                                </p>
                                <div className="flex items-center justify-between">
                                  <div className="text-xs text-foreground/50">
                                    <span className="font-medium">{alert.source}</span>
                                    <span className="mx-1">•</span>
                                    <span>{alert.timestamp}</span>
                                  </div>
                                  {!alert.acknowledged && (
                                    <Button
                                      onClick={() => acknowledgeAlert(alert.id)}
                                      size="sm"
                                      variant="ghost"
                                      className="text-xs h-6 px-2"
                                    >
                                      Acknowledge
                                    </Button>
                                  )}
                                </div>
                              </div>
                            </div>
                          </Card>
                        )
                      })}
                  </div>
                )}
              </div>
            </Card>
          </div>
        </>
      )}
    </>
  )
}
