'use client'

import { AppLayout } from '@/components/app-layout'
import { Card } from '@/components/ui/card'
import { LineChart, Line, ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ComposedChart, Bar } from 'recharts'
import { TrendingUp, AlertCircle, CheckCircle } from 'lucide-react'

const spcData = [
  { sample: 1, value: 100.2, ucl: 105, lcl: 95, mean: 100 },
  { sample: 2, value: 99.8, ucl: 105, lcl: 95, mean: 100 },
  { sample: 3, value: 101.1, ucl: 105, lcl: 95, mean: 100 },
  { sample: 4, value: 98.9, ucl: 105, lcl: 95, mean: 100 },
  { sample: 5, value: 100.5, ucl: 105, lcl: 95, mean: 100 },
  { sample: 6, value: 102.3, ucl: 105, lcl: 95, mean: 100 },
  { sample: 7, value: 99.2, ucl: 105, lcl: 95, mean: 100 },
  { sample: 8, value: 101.6, ucl: 105, lcl: 95, mean: 100 },
  { sample: 9, value: 100.1, ucl: 105, lcl: 95, mean: 100 },
  { sample: 10, value: 99.7, ucl: 105, lcl: 95, mean: 100 },
  { sample: 11, value: 100.8, ucl: 105, lcl: 95, mean: 100 },
  { sample: 12, value: 101.4, ucl: 105, lcl: 95, mean: 100 },
]

const capabilityData = [
  { capability: 'Cp', value: 1.45, target: 1.33, status: 'pass' },
  { capability: 'Cpk', value: 1.38, target: 1.33, status: 'pass' },
  { capability: 'Pp', value: 1.42, target: 1.33, status: 'pass' },
  { capability: 'Ppk', value: 1.35, target: 1.33, status: 'pass' },
]

const processMetrics = [
  { metric: 'Mean', value: '100.08', unit: 'g' },
  { metric: 'Std Dev', value: '0.92', unit: 'g' },
  { metric: 'Min', value: '98.9', unit: 'g' },
  { metric: 'Max', value: '102.3', unit: 'g' },
  { metric: 'Range', value: '3.4', unit: 'g' },
  { metric: 'USL', value: '105', unit: 'g' },
  { metric: 'LSL', value: '95', unit: 'g' },
]

export default function SPCControlPage() {
  return (
    <AppLayout>
      <div className="space-y-6">
        <div>
          <h2 className="text-3xl font-bold text-foreground mb-2">SPC Control Charts</h2>
          <p className="text-foreground/60">Statistical process control and quality metrics</p>
        </div>

        {/* Key Indicators */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="p-6 border border-success/30 bg-success/5">
            <div className="flex items-start gap-4">
              <div className="p-3 bg-success/10 rounded-lg">
                <CheckCircle className="w-6 h-6 text-success" />
              </div>
              <div>
                <p className="text-sm font-medium text-foreground/70">Process Capability</p>
                <p className="text-3xl font-bold text-success mt-2">Cpk 1.38</p>
                <p className="text-xs text-success/80 mt-1">Capable & stable</p>
              </div>
            </div>
          </Card>

          <Card className="p-6 border border-border bg-card">
            <div className="flex items-start gap-4">
              <div className="p-3 bg-primary/10 rounded-lg">
                <TrendingUp className="w-6 h-6 text-primary" />
              </div>
              <div>
                <p className="text-sm font-medium text-foreground/70">Last 30 Samples</p>
                <p className="text-3xl font-bold text-primary mt-2">100%</p>
                <p className="text-xs text-primary/80 mt-1">In control</p>
              </div>
            </div>
          </Card>

          <Card className="p-6 border border-border bg-card">
            <div className="flex items-start gap-4">
              <div className="p-3 bg-accent/10 rounded-lg">
                <AlertCircle className="w-6 h-6 text-accent" />
              </div>
              <div>
                <p className="text-sm font-medium text-foreground/70">Out of Control Points</p>
                <p className="text-3xl font-bold text-accent mt-2">0</p>
                <p className="text-xs text-accent/80 mt-1">No violations</p>
              </div>
            </div>
          </Card>
        </div>

        {/* SPC Chart */}
        <Card className="p-6 border border-border bg-card">
          <h3 className="text-lg font-semibold text-foreground mb-4">Control Chart - Fill Weight</h3>
          <ResponsiveContainer width="100%" height={350}>
            <ComposedChart data={spcData} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="sample" stroke="var(--foreground)" />
              <YAxis stroke="var(--foreground)" domain={[90, 110]} />
              <Tooltip contentStyle={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)' }} />
              <Legend />
              <Line type="monotone" dataKey="ucl" stroke="var(--destructive)" strokeWidth={2} strokeDasharray="5 5" name="UCL (105)" isAnimationActive={false} />
              <Line type="monotone" dataKey="mean" stroke="var(--chart-2)" strokeWidth={2} name="Mean (100)" isAnimationActive={false} />
              <Line type="monotone" dataKey="lcl" stroke="var(--destructive)" strokeWidth={2} strokeDasharray="5 5" name="LCL (95)" isAnimationActive={false} />
              <Line type="monotone" dataKey="value" stroke="var(--primary)" strokeWidth={2.5} name="Sample Value" isAnimationActive={false} />
            </ComposedChart>
          </ResponsiveContainer>
        </Card>

        {/* Capability Analysis */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card className="p-6 border border-border bg-card">
            <h3 className="text-lg font-semibold text-foreground mb-4">Process Capability Analysis</h3>
            <div className="space-y-4">
              {capabilityData.map((item, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 border border-border/50 rounded-lg">
                  <div>
                    <p className="font-medium text-foreground">{item.capability}</p>
                    <p className="text-xs text-foreground/60">Target: {item.target}</p>
                  </div>
                  <div className="text-right">
                    <p className={`text-2xl font-bold ${item.value >= item.target ? 'text-success' : 'text-warning'}`}>
                      {item.value}
                    </p>
                    {item.value >= item.target ? (
                      <span className="text-xs text-success">✓ Capable</span>
                    ) : (
                      <span className="text-xs text-warning">⚠ Review</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card className="p-6 border border-border bg-card">
            <h3 className="text-lg font-semibold text-foreground mb-4">Process Metrics</h3>
            <div className="grid grid-cols-2 gap-3">
              {processMetrics.map((item, idx) => (
                <div key={idx} className="p-3 border border-border/50 rounded-lg">
                  <p className="text-xs font-medium text-foreground/60">{item.metric}</p>
                  <div className="flex items-baseline gap-1 mt-2">
                    <p className="text-xl font-bold text-foreground">{item.value}</p>
                    <p className="text-xs text-foreground/50">{item.unit}</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* SPC Rules Analysis */}
        <Card className="p-6 border border-border bg-card">
          <h3 className="text-lg font-semibold text-foreground mb-4">SPC Rules Validation</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              { rule: 'Rule 1', desc: '1 point > 3σ from mean', status: 'pass' },
              { rule: 'Rule 2', desc: '9 consecutive > mean', status: 'pass' },
              { rule: 'Rule 3', desc: '6 consecutive trend', status: 'pass' },
              { rule: 'Rule 4', desc: '14 alternating', status: 'pass' },
            ].map((item, idx) => (
              <div key={idx} className="p-4 border border-border/50 rounded-lg">
                <div className="flex items-start justify-between mb-2">
                  <p className="font-semibold text-foreground">{item.rule}</p>
                  <div className="w-2 h-2 rounded-full bg-success"></div>
                </div>
                <p className="text-sm text-foreground/70">{item.desc}</p>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </AppLayout>
  )
}
