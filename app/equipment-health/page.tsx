'use client'

import { AppLayout } from '@/components/app-layout'
import { Card } from '@/components/ui/card'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from 'recharts'
import { AlertCircle, CheckCircle, AlertTriangle, Wrench } from 'lucide-react'

const temperatureData = [
  { time: '00:00', nozzle1: 72, nozzle2: 71, nozzle3: 73, pump: 65 },
  { time: '04:00', nozzle1: 71, nozzle2: 72, nozzle3: 71, pump: 64 },
  { time: '08:00', nozzle1: 73, nozzle2: 73, nozzle3: 74, pump: 66 },
  { time: '12:00', nozzle1: 74, nozzle2: 74, nozzle3: 75, pump: 67 },
  { time: '16:00', nozzle1: 72, nozzle2: 71, nozzle3: 73, pump: 65 },
  { time: '20:00', nozzle1: 70, nozzle2: 70, nozzle3: 71, pump: 64 },
]

const vibrationData = [
  { component: 'Motor', value: 45, critical: 100 },
  { component: 'Pump', value: 32, critical: 80 },
  { component: 'Conveyor', value: 28, critical: 75 },
  { component: 'Nozzle Array', value: 18, critical: 50 },
  { component: 'Valve Block', value: 22, critical: 60 },
]

const healthRadarData = [
  { subject: 'Motor Health', A: 92, fullMark: 100 },
  { subject: 'Pump Condition', A: 88, fullMark: 100 },
  { subject: 'Thermal Status', A: 95, fullMark: 100 },
  { subject: 'Vibration', A: 85, fullMark: 100 },
  { subject: 'Pressure', A: 91, fullMark: 100 },
  { subject: 'Flow Rate', A: 89, fullMark: 100 },
]

const equipmentItems = [
  { name: 'Primary Pump', status: 'healthy', health: 94, uptime: '2156h', maintenance: '168h' },
  { name: 'Nozzle Assembly 1', status: 'healthy', health: 89, uptime: '1850h', maintenance: '240h' },
  { name: 'Nozzle Assembly 2', status: 'healthy', health: 92, uptime: '1850h', maintenance: '240h' },
  { name: 'Nozzle Assembly 3', status: 'warning', health: 78, uptime: '1850h', maintenance: '48h' },
  { name: 'Pressure Valve', status: 'healthy', health: 91, uptime: '2156h', maintenance: '336h' },
  { name: 'Conveyor Motor', status: 'healthy', health: 87, uptime: '1950h', maintenance: '120h' },
]

export default function EquipmentHealthPage() {
  return (
    <AppLayout>
      <div className="space-y-6">
        <div>
          <h2 className="text-3xl font-bold text-foreground mb-2">Equipment Health</h2>
          <p className="text-foreground/60">Real-time monitoring and predictive maintenance</p>
        </div>

        {/* Overall Health Summary */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="p-6 border border-success/30 bg-success/5">
            <div className="flex items-start gap-4">
              <div className="p-3 bg-success/10 rounded-lg">
                <CheckCircle className="w-6 h-6 text-success" />
              </div>
              <div>
                <p className="text-sm font-medium text-foreground/70">Overall Health</p>
                <p className="text-3xl font-bold text-success mt-2">90.2%</p>
                <p className="text-xs text-success/80 mt-1">All systems operational</p>
              </div>
            </div>
          </Card>

          <Card className="p-6 border border-warning/30 bg-warning/5">
            <div className="flex items-start gap-4">
              <div className="p-3 bg-warning/10 rounded-lg">
                <AlertTriangle className="w-6 h-6 text-warning" />
              </div>
              <div>
                <p className="text-sm font-medium text-foreground/70">Scheduled Maintenance</p>
                <p className="text-3xl font-bold text-warning mt-2">5</p>
                <p className="text-xs text-warning/80 mt-1">Next in 48 hours</p>
              </div>
            </div>
          </Card>

          <Card className="p-6 border border-primary/30 bg-primary/5">
            <div className="flex items-start gap-4">
              <div className="p-3 bg-primary/10 rounded-lg">
                <Wrench className="w-6 h-6 text-primary" />
              </div>
              <div>
                <p className="text-sm font-medium text-foreground/70">Mean Time to Failure</p>
                <p className="text-3xl font-bold text-primary mt-2">2847h</p>
                <p className="text-xs text-primary/80 mt-1">Estimated</p>
              </div>
            </div>
          </Card>
        </div>

        {/* Monitoring Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card className="p-6 border border-border bg-card">
            <h3 className="text-lg font-semibold text-foreground mb-4">Component Temperature (24h)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={temperatureData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="time" stroke="var(--foreground)" />
                <YAxis stroke="var(--foreground)" />
                <Tooltip contentStyle={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)' }} />
                <Legend />
                <Line type="monotone" dataKey="nozzle1" stroke="var(--chart-1)" strokeWidth={2} isAnimationActive={false} name="Nozzle 1" />
                <Line type="monotone" dataKey="nozzle2" stroke="var(--chart-2)" strokeWidth={2} isAnimationActive={false} name="Nozzle 2" />
                <Line type="monotone" dataKey="nozzle3" stroke="var(--chart-3)" strokeWidth={2} isAnimationActive={false} name="Nozzle 3" />
                <Line type="monotone" dataKey="pump" stroke="var(--warning)" strokeWidth={2} isAnimationActive={false} name="Pump" />
              </LineChart>
            </ResponsiveContainer>
          </Card>

          <Card className="p-6 border border-border bg-card">
            <h3 className="text-lg font-semibold text-foreground mb-4">System Health Radar</h3>
            <ResponsiveContainer width="100%" height={300}>
              <RadarChart data={healthRadarData}>
                <PolarGrid stroke="var(--border)" />
                <PolarAngleAxis dataKey="subject" stroke="var(--foreground)" />
                <PolarRadiusAxis stroke="var(--foreground)" />
                <Radar name="Health Score" dataKey="A" stroke="var(--primary)" fill="var(--primary)" fillOpacity={0.6} isAnimationActive={false} />
              </RadarChart>
            </ResponsiveContainer>
          </Card>
        </div>

        {/* Vibration Analysis */}
        <Card className="p-6 border border-border bg-card">
          <h3 className="text-lg font-semibold text-foreground mb-4">Vibration Analysis</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={vibrationData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="component" stroke="var(--foreground)" />
              <YAxis stroke="var(--foreground)" />
              <Tooltip contentStyle={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)' }} />
              <Bar dataKey="value" fill="var(--chart-1)" name="Current Level" />
              <Bar dataKey="critical" fill="var(--destructive)" name="Critical Threshold" />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* Equipment Status List */}
        <Card className="p-6 border border-border bg-card">
          <h3 className="text-lg font-semibold text-foreground mb-4">Equipment Status</h3>
          <div className="space-y-3">
            {equipmentItems.map((item, idx) => (
              <div key={idx} className="flex items-center justify-between p-4 border border-border/50 rounded-lg hover:bg-muted/30 transition-colors">
                <div className="flex items-center gap-4 flex-1">
                  {item.status === 'healthy' ? (
                    <div className="p-2 bg-success/10 rounded">
                      <CheckCircle className="w-5 h-5 text-success" />
                    </div>
                  ) : (
                    <div className="p-2 bg-warning/10 rounded">
                      <AlertTriangle className="w-5 h-5 text-warning" />
                    </div>
                  )}
                  <div className="flex-1">
                    <p className="font-medium text-foreground">{item.name}</p>
                    <div className="flex gap-4 text-xs text-foreground/60 mt-1">
                      <span>Uptime: {item.uptime}</span>
                      <span>Maintenance: {item.maintenance}</span>
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <p className={`text-2xl font-bold ${item.health >= 85 ? 'text-success' : 'text-warning'}`}>
                    {item.health}%
                  </p>
                  <p className="text-xs text-foreground/60">Health Score</p>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </AppLayout>
  )
}
