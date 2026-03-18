'use client'

import { AppLayout } from '@/components/app-layout'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { AlertCircle, CheckCircle, Clock, ExternalLink, Search } from 'lucide-react'
import { useState } from 'react'

const anomalies = [
  {
    id: 'ANM-001',
    type: 'Pressure Spike',
    severity: 'high',
    detected: '2024-03-18 14:32:15',
    duration: '2.3 min',
    rootCause: 'Nozzle 2 partial blockage',
    solution: 'Clean nozzle with solvent, verify flow',
    status: 'resolved',
    resolution: '2024-03-18 15:45:00',
  },
  {
    id: 'ANM-002',
    type: 'Temperature Drift',
    severity: 'medium',
    detected: '2024-03-18 11:20:45',
    duration: '18.5 min',
    rootCause: 'Heating element aging',
    solution: 'Replace heating element, run calibration',
    status: 'resolved',
    resolution: '2024-03-18 12:15:00',
  },
  {
    id: 'ANM-003',
    type: 'Fill Weight Variance',
    severity: 'medium',
    detected: '2024-03-17 22:15:30',
    duration: '42 min',
    rootCause: 'Pump worn seal causing friction',
    solution: 'Replace pump seal, verify dispense accuracy',
    status: 'resolved',
    resolution: '2024-03-17 23:00:00',
  },
  {
    id: 'ANM-004',
    type: 'Vibration Spike',
    severity: 'low',
    detected: '2024-03-17 10:45:12',
    duration: '5.2 min',
    rootCause: 'Conveyor belt misalignment',
    solution: 'Realign conveyor belt, check bearing wear',
    status: 'resolved',
    resolution: '2024-03-17 11:30:00',
  },
  {
    id: 'ANM-005',
    type: 'Sensor Drift',
    severity: 'medium',
    detected: '2024-03-15 09:22:00',
    duration: 'ongoing',
    rootCause: 'Scale calibration drift',
    solution: 'Perform scale calibration with standard weights',
    status: 'in-progress',
    resolution: 'pending',
  },
]

function getSeverityColor(severity: string) {
  switch (severity) {
    case 'critical': return 'bg-destructive text-destructive-foreground'
    case 'high': return 'bg-warning text-warning-foreground'
    case 'medium': return 'bg-accent text-accent-foreground'
    case 'low': return 'bg-success text-success-foreground'
    default: return 'bg-muted text-muted-foreground'
  }
}

function getStatusIcon(status: string) {
  switch (status) {
    case 'resolved': return <CheckCircle className="w-4 h-4 text-success" />
    case 'in-progress': return <Clock className="w-4 h-4 text-warning" />
    default: return <AlertCircle className="w-4 h-4 text-destructive" />
  }
}

export default function AnomalyDatabasePage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [severityFilter, setSeverityFilter] = useState<string | null>(null)
  const [statusFilter, setStatusFilter] = useState<string | null>(null)

  const filteredAnomalies = anomalies.filter((anomaly) => {
    const matchesSearch = anomaly.id.includes(searchTerm) || anomaly.type.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesSeverity = !severityFilter || anomaly.severity === severityFilter
    const matchesStatus = !statusFilter || anomaly.status === statusFilter
    return matchesSearch && matchesSeverity && matchesStatus
  })

  const stats = {
    total: anomalies.length,
    resolved: anomalies.filter(a => a.status === 'resolved').length,
    inProgress: anomalies.filter(a => a.status === 'in-progress').length,
    highSeverity: anomalies.filter(a => a.severity === 'high' || a.severity === 'critical').length,
  }

  return (
    <AppLayout>
      <div className="space-y-6">
        <div>
          <h2 className="text-3xl font-bold text-foreground mb-2">Anomaly Database</h2>
          <p className="text-foreground/60">Historical anomalies with root cause analysis and solutions</p>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card className="p-4 border border-border bg-card">
            <p className="text-sm font-medium text-foreground/70">Total Anomalies</p>
            <p className="text-3xl font-bold text-foreground mt-2">{stats.total}</p>
          </Card>
          <Card className="p-4 border border-success/30 bg-success/5">
            <p className="text-sm font-medium text-success">Resolved</p>
            <p className="text-3xl font-bold text-success mt-2">{stats.resolved}</p>
          </Card>
          <Card className="p-4 border border-warning/30 bg-warning/5">
            <p className="text-sm font-medium text-warning">In Progress</p>
            <p className="text-3xl font-bold text-warning mt-2">{stats.inProgress}</p>
          </Card>
          <Card className="p-4 border border-destructive/30 bg-destructive/5">
            <p className="text-sm font-medium text-destructive">High Priority</p>
            <p className="text-3xl font-bold text-destructive mt-2">{stats.highSeverity}</p>
          </Card>
        </div>

        {/* Filters */}
        <Card className="p-6 border border-border bg-card">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-foreground/70 mb-2">Search</label>
              <div className="relative">
                <Search className="absolute left-3 top-3 w-4 h-4 text-foreground/40" />
                <input
                  type="text"
                  placeholder="Search by ID or type..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 bg-input border border-border rounded-lg text-foreground placeholder-foreground/40"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-foreground/70 mb-2">Severity</label>
                <div className="flex flex-wrap gap-2">
                  {['critical', 'high', 'medium', 'low'].map((s) => (
                    <button
                      key={s}
                      onClick={() => setSeverityFilter(severityFilter === s ? null : s)}
                      className={`px-3 py-1 rounded text-sm capitalize transition-colors ${
                        severityFilter === s
                          ? getSeverityColor(s)
                          : 'bg-muted text-foreground/70 hover:bg-muted/80'
                      }`}
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-foreground/70 mb-2">Status</label>
                <div className="flex flex-wrap gap-2">
                  {['resolved', 'in-progress', 'open'].map((s) => (
                    <button
                      key={s}
                      onClick={() => setStatusFilter(statusFilter === s ? null : s)}
                      className={`px-3 py-1 rounded text-sm capitalize transition-colors ${
                        statusFilter === s
                          ? 'bg-primary text-primary-foreground'
                          : 'bg-muted text-foreground/70 hover:bg-muted/80'
                      }`}
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </Card>

        {/* Anomalies List */}
        <div className="space-y-3">
          {filteredAnomalies.map((anomaly) => (
            <Card key={anomaly.id} className="p-6 border border-border bg-card hover:bg-muted/50 transition-colors">
              <div className="space-y-4">
                {/* Header */}
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-4 flex-1">
                    <div className="mt-1">
                      {getStatusIcon(anomaly.status)}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-semibold text-foreground">{anomaly.type}</h3>
                        <Badge className={getSeverityColor(anomaly.severity)}>
                          {anomaly.severity}
                        </Badge>
                        <Badge className={anomaly.status === 'resolved' ? 'bg-success/20 text-success' : 'bg-warning/20 text-warning'}>
                          {anomaly.status}
                        </Badge>
                      </div>
                      <p className="text-sm font-mono text-foreground/60">{anomaly.id}</p>
                    </div>
                  </div>
                </div>

                {/* Timeline */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                  <div>
                    <p className="text-foreground/60">Detected</p>
                    <p className="font-medium text-foreground mt-1">{anomaly.detected}</p>
                  </div>
                  <div>
                    <p className="text-foreground/60">Duration</p>
                    <p className="font-medium text-foreground mt-1">{anomaly.duration}</p>
                  </div>
                  <div>
                    <p className="text-foreground/60">Root Cause</p>
                    <p className="font-medium text-foreground mt-1">{anomaly.rootCause}</p>
                  </div>
                  <div>
                    <p className="text-foreground/60">Resolution</p>
                    <p className="font-medium text-foreground mt-1">
                      {anomaly.resolution === 'pending' ? 'Pending' : anomaly.resolution}
                    </p>
                  </div>
                </div>

                {/* Solution */}
                <div className="p-4 bg-primary/10 border border-primary/20 rounded-lg">
                  <p className="text-sm font-medium text-primary mb-1">Recommended Solution</p>
                  <p className="text-sm text-foreground/90">{anomaly.solution}</p>
                </div>

                {/* Action */}
                <div className="flex justify-end">
                  <button className="flex items-center gap-2 text-sm font-medium text-primary hover:text-primary/80 transition-colors">
                    View Details <ExternalLink className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </AppLayout>
  )
}
