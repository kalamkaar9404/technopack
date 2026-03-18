'use client'

import { AppLayout } from '@/components/app-layout'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ScatterChart, Scatter } from 'recharts'
import { AlertCircle, CheckCircle, TrendingUp, Zap, Camera, Play, Pause, Eye, Scan } from 'lucide-react'
import { useState, useEffect } from 'react'

const operationalData = [
  { time: '00:00', target: 500, actual: 502, variance: 0.4 },
  { time: '02:00', target: 500, actual: 499, variance: -0.2 },
  { time: '04:00', target: 500, actual: 503, variance: 0.6 },
  { time: '06:00', target: 500, actual: 498, variance: -0.4 },
  { time: '08:00', target: 500, actual: 501, variance: 0.2 },
  { time: '10:00', target: 500, actual: 504, variance: 0.8 },
  { time: '12:00', target: 500, actual: 500, variance: 0.0 },
  { time: '14:00', target: 500, actual: 497, variance: -0.6 },
  { time: '16:00', target: 500, actual: 502, variance: 0.4 },
]

const predictionData = [
  { hour: 0, predicted: 500, confidence: 98 },
  { hour: 2, predicted: 501, confidence: 97 },
  { hour: 4, predicted: 499, confidence: 96 },
  { hour: 6, predicted: 502, confidence: 95 },
  { hour: 8, predicted: 500, confidence: 98 },
  { hour: 10, predicted: 503, confidence: 94 },
  { hour: 12, predicted: 501, confidence: 99 },
]

const fillSessionData = [
  { session: 'Session 1', avgFill: 501, variance: 0.2, status: 'Pass' },
  { session: 'Session 2', avgFill: 498, variance: -0.4, status: 'Pass' },
  { session: 'Session 3', avgFill: 504, variance: 0.8, status: 'Warning' },
  { session: 'Session 4', avgFill: 499, variance: -0.2, status: 'Pass' },
  { session: 'Session 5', avgFill: 502, variance: 0.4, status: 'Pass' },
]

export default function FillMonitorPage() {
  const [isMonitoring, setIsMonitoring] = useState(true)
  const [currentFillLevel, setCurrentFillLevel] = useState(85)
  const [detectionConfidence, setDetectionConfidence] = useState(98.5)
  const [fillStatus, setFillStatus] = useState<'filling' | 'complete' | 'checking'>('filling')

  // Simulate real-time fill level changes
  useEffect(() => {
    if (!isMonitoring) return
    
    const interval = setInterval(() => {
      setCurrentFillLevel(prev => {
        const newLevel = prev + Math.random() * 3
        if (newLevel >= 100) {
          setFillStatus('complete')
          return 100
        }
        setFillStatus('filling')
        return newLevel
      })
      setDetectionConfidence(95 + Math.random() * 4)
    }, 500)

    return () => clearInterval(interval)
  }, [isMonitoring])

  // Reset fill level when complete
  useEffect(() => {
    if (currentFillLevel >= 100) {
      setTimeout(() => {
        setCurrentFillLevel(0)
        setFillStatus('checking')
        setTimeout(() => setFillStatus('filling'), 500)
      }, 2000)
    }
  }, [currentFillLevel])

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex items-start justify-between animate-slide-in">
          <div>
            <h2 className="text-3xl font-bold text-foreground mb-2 text-glow">Fill Monitor</h2>
            <p className="text-foreground/60">Real-time computer vision monitoring with AI predictions</p>
          </div>
          <Button
            onClick={() => setIsMonitoring(!isMonitoring)}
            variant={isMonitoring ? 'destructive' : 'default'}
            className="shadow-glow"
          >
            {isMonitoring ? (
              <>
                <Pause className="w-4 h-4 mr-2" />
                Pause Monitoring
              </>
            ) : (
              <>
                <Play className="w-4 h-4 mr-2" />
                Start Monitoring
              </>
            )}
          </Button>
        </div>

        {/* Computer Vision Live Feed */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Camera Feed */}
          <Card className="lg:col-span-2 p-6 border-2 border-primary/30 bg-gradient-to-br from-primary/5 to-transparent shadow-glow-lg animate-slide-in">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-primary/20 rounded-lg animate-pulse-glow">
                  <Camera className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-foreground">Computer Vision Feed</h3>
                  <p className="text-xs text-foreground/60">Real-time fill level detection</p>
                </div>
              </div>
              <div className={`flex items-center gap-2 px-3 py-1.5 rounded-lg ${
                isMonitoring ? 'bg-success/10 border border-success/30' : 'bg-muted/30 border border-border'
              }`}>
                <div className={`w-2 h-2 rounded-full ${isMonitoring ? 'bg-success animate-pulse-glow' : 'bg-muted'}`}></div>
                <span className="text-xs font-medium">{isMonitoring ? 'LIVE' : 'PAUSED'}</span>
              </div>
            </div>

            {/* Simulated Camera View */}
            <div className="relative aspect-video bg-gradient-to-br from-slate-900 to-slate-800 rounded-lg overflow-hidden border-2 border-primary/20">
              {/* Scan lines effect */}
              {isMonitoring && <div className="scan-line"></div>}
              
              {/* Container outline */}
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="relative w-48 h-80 border-4 border-primary/40 rounded-lg">
                  {/* Fill level visualization */}
                  <div 
                    className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-accent via-primary to-success transition-all duration-500 rounded-b-lg"
                    style={{ height: `${currentFillLevel}%` }}
                  >
                    <div className="absolute inset-0 bg-white/10 animate-shimmer"></div>
                  </div>
                  
                  {/* Detection box */}
                  {isMonitoring && (
                    <div className="absolute inset-0 border-2 border-success animate-pulse-border rounded-lg">
                      {/* Corner markers */}
                      <div className="absolute top-0 left-0 w-4 h-4 border-t-4 border-l-4 border-success"></div>
                      <div className="absolute top-0 right-0 w-4 h-4 border-t-4 border-r-4 border-success"></div>
                      <div className="absolute bottom-0 left-0 w-4 h-4 border-b-4 border-l-4 border-success"></div>
                      <div className="absolute bottom-0 right-0 w-4 h-4 border-b-4 border-r-4 border-success"></div>
                    </div>
                  )}
                  
                  {/* Fill level indicator line */}
                  <div 
                    className="absolute left-0 right-0 h-0.5 bg-warning shadow-glow transition-all duration-500"
                    style={{ bottom: `${currentFillLevel}%` }}
                  >
                    <div className="absolute -right-16 -top-6 bg-warning/90 px-2 py-1 rounded text-xs font-mono font-bold whitespace-nowrap">
                      {currentFillLevel.toFixed(1)}%
                    </div>
                  </div>
                </div>
              </div>

              {/* Status overlay */}
              <div className="absolute top-4 left-4 space-y-2">
                <div className="glass-effect px-3 py-1.5 rounded-lg border border-primary/30">
                  <p className="text-xs text-foreground/70">Confidence</p>
                  <p className="text-lg font-bold text-primary">{detectionConfidence.toFixed(1)}%</p>
                </div>
                <div className={`glass-effect px-3 py-1.5 rounded-lg border ${
                  fillStatus === 'complete' ? 'border-success/30' : 
                  fillStatus === 'checking' ? 'border-warning/30' : 'border-primary/30'
                }`}>
                  <p className="text-xs text-foreground/70">Status</p>
                  <p className={`text-sm font-bold ${
                    fillStatus === 'complete' ? 'text-success' : 
                    fillStatus === 'checking' ? 'text-warning' : 'text-primary'
                  }`}>
                    {fillStatus === 'complete' ? 'COMPLETE' : 
                     fillStatus === 'checking' ? 'CHECKING' : 'FILLING'}
                  </p>
                </div>
              </div>

              {/* Detection info overlay */}
              <div className="absolute bottom-4 left-4 right-4 glass-effect p-3 rounded-lg border border-primary/30">
                <div className="grid grid-cols-3 gap-4 text-center">
                  <div>
                    <p className="text-xs text-foreground/60">Target</p>
                    <p className="text-sm font-bold text-foreground">500ml</p>
                  </div>
                  <div>
                    <p className="text-xs text-foreground/60">Current</p>
                    <p className="text-sm font-bold text-primary">{(currentFillLevel * 5).toFixed(0)}ml</p>
                  </div>
                  <div>
                    <p className="text-xs text-foreground/60">Accuracy</p>
                    <p className="text-sm font-bold text-success">±2ml</p>
                  </div>
                </div>
              </div>
            </div>

            {/* CV Model Info */}
            <div className="mt-4 grid grid-cols-3 gap-3">
              <div className="glass-effect p-3 rounded-lg border border-primary/20 text-center">
                <Eye className="w-4 h-4 text-primary mx-auto mb-1" />
                <p className="text-xs text-foreground/60">Model</p>
                <p className="text-sm font-bold text-foreground">YOLOv8</p>
              </div>
              <div className="glass-effect p-3 rounded-lg border border-success/20 text-center">
                <Scan className="w-4 h-4 text-success mx-auto mb-1" />
                <p className="text-xs text-foreground/60">FPS</p>
                <p className="text-sm font-bold text-foreground">30</p>
              </div>
              <div className="glass-effect p-3 rounded-lg border border-accent/20 text-center">
                <Zap className="w-4 h-4 text-accent mx-auto mb-1" />
                <p className="text-xs text-foreground/60">Latency</p>
                <p className="text-sm font-bold text-foreground">12ms</p>
              </div>
            </div>
          </Card>

          {/* Detection Stats */}
          <Card className="p-6 border border-success/30 bg-gradient-to-br from-success/5 to-transparent shadow-glow animate-slide-in">
            <h3 className="text-lg font-semibold text-foreground mb-4">Detection Stats</h3>
            <div className="space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-foreground/70">Fill Level</span>
                  <span className="text-sm font-bold text-primary">{currentFillLevel.toFixed(1)}%</span>
                </div>
                <div className="h-2 bg-muted rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-gradient-to-r from-success via-primary to-accent transition-all duration-500 animate-pulse-glow"
                    style={{ width: `${currentFillLevel}%` }}
                  ></div>
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-foreground/70">Confidence</span>
                  <span className="text-sm font-bold text-success">{detectionConfidence.toFixed(1)}%</span>
                </div>
                <div className="h-2 bg-muted rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-success transition-all duration-300"
                    style={{ width: `${detectionConfidence}%` }}
                  ></div>
                </div>
              </div>

              <div className="pt-4 border-t border-border">
                <h4 className="text-sm font-semibold text-foreground mb-3">Recent Detections</h4>
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-foreground/60">Container #1</span>
                    <span className="text-success font-medium">✓ 502ml</span>
                  </div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-foreground/60">Container #2</span>
                    <span className="text-success font-medium">✓ 498ml</span>
                  </div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-foreground/60">Container #3</span>
                    <span className="text-success font-medium">✓ 501ml</span>
                  </div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-foreground/60">Container #4</span>
                    <span className="text-warning font-medium">⚠ 495ml</span>
                  </div>
                </div>
              </div>

              <div className="pt-4 border-t border-border">
                <div className="glass-effect p-3 rounded-lg border border-success/20">
                  <p className="text-xs text-foreground/60 mb-1">Success Rate (24h)</p>
                  <p className="text-2xl font-bold text-success">99.2%</p>
                  <p className="text-xs text-success mt-1">4,752 / 4,790 fills</p>
                </div>
              </div>
            </div>
          </Card>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="p-6 border border-border bg-card">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-foreground/70">Avg Fill Weight</p>
                <p className="text-3xl font-bold text-foreground mt-2">500.4g</p>
                <p className="text-xs text-success mt-1">±0.08% variance</p>
              </div>
            </div>
          </Card>

          <Card className="p-6 border border-border bg-card">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-foreground/70">Fill Rate</p>
                <p className="text-3xl font-bold text-foreground mt-2">48/min</p>
                <p className="text-xs text-success mt-1">Optimal speed</p>
              </div>
            </div>
          </Card>

          <Card className="p-6 border border-border bg-card">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-foreground/70">Line Efficiency</p>
                <p className="text-3xl font-bold text-foreground mt-2">99.2%</p>
                <p className="text-xs text-success mt-1">All lines operational</p>
              </div>
            </div>
          </Card>

          <Card className="p-6 border border-border bg-card">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-foreground/70">Model Accuracy</p>
                <p className="text-3xl font-bold text-foreground mt-2">96.8%</p>
                <p className="text-xs text-success mt-1">Latest training</p>
              </div>
            </div>
          </Card>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card className="p-6 border border-border bg-card">
            <h3 className="text-lg font-semibold text-foreground mb-4">Fill Operations (24h)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={operationalData}>
                <defs>
                  <linearGradient id="colorTarget" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--chart-1)" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="var(--chart-1)" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorActual" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--chart-2)" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="var(--chart-2)" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="time" stroke="var(--foreground)" />
                <YAxis stroke="var(--foreground)" />
                <Tooltip contentStyle={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)' }} />
                <Area type="monotone" dataKey="target" stroke="var(--chart-1)" fillOpacity={1} fill="url(#colorTarget)" isAnimationActive={false} />
                <Area type="monotone" dataKey="actual" stroke="var(--chart-2)" fillOpacity={1} fill="url(#colorActual)" isAnimationActive={false} />
              </AreaChart>
            </ResponsiveContainer>
          </Card>

          <Card className="p-6 border border-border bg-card">
            <h3 className="text-lg font-semibold text-foreground mb-4">AI Predictions (Next 12h)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={predictionData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="hour" stroke="var(--foreground)" />
                <YAxis stroke="var(--foreground)" />
                <Tooltip contentStyle={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)' }} />
                <Line type="monotone" dataKey="predicted" stroke="var(--primary)" strokeWidth={2} isAnimationActive={false} name="Predicted" />
                <Line type="monotone" dataKey="confidence" stroke="var(--success)" strokeWidth={2} strokeDasharray="5 5" isAnimationActive={false} name="Confidence %" />
              </LineChart>
            </ResponsiveContainer>
          </Card>
        </div>

        {/* Session Performance */}
        <Card className="p-6 border border-border bg-card">
          <h3 className="text-lg font-semibold text-foreground mb-4">Fill Session Performance</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={fillSessionData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="session" stroke="var(--foreground)" />
              <YAxis stroke="var(--foreground)" yAxisId="left" />
              <YAxis stroke="var(--foreground)" yAxisId="right" orientation="right" />
              <Tooltip contentStyle={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)' }} />
              <Legend />
              <Bar yAxisId="left" dataKey="avgFill" fill="var(--chart-1)" name="Avg Fill (g)" />
              <Bar yAxisId="right" dataKey="variance" fill="var(--chart-3)" name="Variance (%)" />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* Prediction Summary */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="p-6 border border-border bg-card">
            <div className="flex items-start gap-3">
              <div className="p-2 bg-success/10 rounded-lg">
                <CheckCircle className="w-5 h-5 text-success" />
              </div>
              <div>
                <p className="text-sm font-medium text-foreground/70">Drift Prediction</p>
                <p className="text-lg font-bold text-foreground mt-1">No drift</p>
                <p className="text-xs text-success mt-1">System stable</p>
              </div>
            </div>
          </Card>

          <Card className="p-6 border border-border bg-card">
            <div className="flex items-start gap-3">
              <div className="p-2 bg-warning/10 rounded-lg">
                <AlertCircle className="w-5 h-5 text-warning" />
              </div>
              <div>
                <p className="text-sm font-medium text-foreground/70">Maintenance Alert</p>
                <p className="text-lg font-bold text-warning mt-1">In 168h</p>
                <p className="text-xs text-warning mt-1">Preventive schedule</p>
              </div>
            </div>
          </Card>

          <Card className="p-6 border border-border bg-card">
            <div className="flex items-start gap-3">
              <div className="p-2 bg-primary/10 rounded-lg">
                <TrendingUp className="w-5 h-5 text-primary" />
              </div>
              <div>
                <p className="text-sm font-medium text-foreground/70">Throughput Forecast</p>
                <p className="text-lg font-bold text-primary mt-1">↑ 2.3%</p>
                <p className="text-xs text-primary mt-1">Next week projection</p>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </AppLayout>
  )
}
