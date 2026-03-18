'use client'

import { AppLayout } from '@/components/app-layout'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ScatterChart, Scatter, Cell } from 'recharts'
import { Activity, Zap, Droplets, TrendingUp, BookOpen, X, Brain, Target, Layers, Sparkles, ChevronDown, ChevronUp, CheckCircle2, Circle, ArrowRight, Barcode, Camera, Wrench, BarChart3, Database } from 'lucide-react'
import { useState } from 'react'
import { useRouter } from 'next/navigation'

const metricsData = [
  { time: '00:00', temperature: 72.5, pressure: 98.2, flow: 45.3 },
  { time: '04:00', temperature: 71.8, pressure: 97.9, flow: 46.1 },
  { time: '08:00', temperature: 73.2, pressure: 99.1, flow: 44.8 },
  { time: '12:00', temperature: 74.1, pressure: 99.8, flow: 43.5 },
  { time: '16:00', temperature: 72.9, pressure: 98.5, flow: 45.2 },
  { time: '20:00', temperature: 71.5, pressure: 97.3, flow: 47.1 },
]

const calibrationData = [
  { point: 'Cal 1', expected: 100, actual: 98.5, deviation: -1.5 },
  { point: 'Cal 2', expected: 100, actual: 101.2, deviation: 1.2 },
  { point: 'Cal 3', expected: 100, actual: 99.8, deviation: -0.2 },
  { point: 'Cal 4', expected: 100, actual: 100.5, deviation: 0.5 },
  { point: 'Cal 5', expected: 100, actual: 99.2, deviation: -0.8 },
]

// PINN Neural Network Visualization Data
const pinnLayersData = [
  { layer: 'Input', neurons: 4, activation: 0.85, color: '#5499FF' },
  { layer: 'Hidden 1', neurons: 32, activation: 0.72, color: '#94BBFF' },
  { layer: 'Hidden 2', neurons: 32, activation: 0.68, color: '#94BBFF' },
  { layer: 'Physics', neurons: 16, activation: 0.91, color: '#4ADE80' },
  { layer: 'Output', neurons: 2, activation: 0.88, color: '#F59E0B' },
]

// PINN Training Loss Data
const pinnLossData = [
  { epoch: 0, dataLoss: 0.95, physicsLoss: 0.88, totalLoss: 0.92 },
  { epoch: 100, dataLoss: 0.45, physicsLoss: 0.52, totalLoss: 0.48 },
  { epoch: 200, dataLoss: 0.22, physicsLoss: 0.28, totalLoss: 0.25 },
  { epoch: 300, dataLoss: 0.12, physicsLoss: 0.15, totalLoss: 0.13 },
  { epoch: 400, dataLoss: 0.08, physicsLoss: 0.09, totalLoss: 0.08 },
  { epoch: 500, dataLoss: 0.05, physicsLoss: 0.06, totalLoss: 0.05 },
]

// Prediction vs Actual Heatmap Data
const predictionAccuracyData = [
  { viscosity: 0.001, density: 1000, accuracy: 98.5 },
  { viscosity: 0.001, density: 1020, accuracy: 97.8 },
  { viscosity: 0.065, density: 920, accuracy: 96.2 },
  { viscosity: 0.065, density: 940, accuracy: 95.8 },
  { viscosity: 6.0, density: 1420, accuracy: 94.5 },
  { viscosity: 6.0, density: 1400, accuracy: 93.2 },
  { viscosity: 2.5, density: 1350, accuracy: 97.1 },
  { viscosity: 0.002, density: 1030, accuracy: 98.9 },
]

export default function Dashboard() {
  const [showGuide, setShowGuide] = useState(false)
  const [completedSteps, setCompletedSteps] = useState<number[]>([])
  const router = useRouter()

  const toggleStep = (stepNumber: number) => {
    setCompletedSteps(prev => 
      prev.includes(stepNumber) 
        ? prev.filter(s => s !== stepNumber)
        : [...prev, stepNumber]
    )
  }

  const navigateToPage = (path: string) => {
    router.push(path)
  }

  const workflowSteps = [
    {
      number: 1,
      title: "Understand the Problem",
      description: "Traditional filling machines need manual calibration for each product type",
      details: [
        "Manual calibration wastes 2-3 hours per product switch",
        "Different liquids (viscosity, density) require different parameters",
        "Human error causes overfill/underfill (±5% variance)",
        "No way to predict settings for new products"
      ],
      icon: Target,
      color: "destructive",
      action: null
    },
    {
      number: 2,
      title: "Scan Product UPC",
      description: "Use UPC scanner to identify product and retrieve properties",
      details: [
        "Navigate to Scanner page",
        "Enter UPC code: 1234567890001 (Water)",
        "System retrieves: viscosity, density, surface tension",
        "Product database stores physical properties"
      ],
      icon: Barcode,
      color: "primary",
      action: { label: "Go to Scanner", path: "/scanner" }
    },
    {
      number: 3,
      title: "PINN Model Prediction",
      description: "AI calculates optimal calibration parameters using physics laws",
      details: [
        "Scanner automatically feeds product properties to PINN model",
        "PINN combines neural networks + fluid dynamics equations",
        "Calculates: Valve timing, pressure, nozzle diameter",
        "Prediction accuracy: 96-99% (see charts below)",
        "Try it: Go to Scanner → Enter UPC → See instant predictions"
      ],
      icon: Brain,
      color: "success",
      action: { label: "Go to Scanner", path: "/scanner" }
    },
    {
      number: 4,
      title: "Monitor Fill Operations",
      description: "Computer vision tracks real-time fill levels with 30 FPS",
      details: [
        "YOLOv8 model detects container and fill level",
        "Real-time accuracy: ±2ml (99.2% success rate)",
        "Automatic anomaly detection",
        "12ms latency for instant feedback"
      ],
      icon: Camera,
      color: "accent",
      action: { label: "Go to Fill Monitor", path: "/fill-monitor" }
    },
    {
      number: 5,
      title: "Track Equipment Health",
      description: "Predictive maintenance prevents downtime",
      details: [
        "Monitor valve wear, pressure drift, nozzle clogging",
        "Predict maintenance needs 7 days in advance",
        "Reduce unplanned downtime by 80%",
        "Track equipment performance trends"
      ],
      icon: Wrench,
      color: "warning",
      action: { label: "Go to Equipment Health", path: "/equipment-health" }
    },
    {
      number: 6,
      title: "Quality Control (SPC)",
      description: "Statistical process control ensures consistent quality",
      details: [
        "Real-time control charts (X-bar, R-chart)",
        "Automatic out-of-control detection",
        "Cpk calculation for process capability",
        "Compliance with industry standards"
      ],
      icon: BarChart3,
      color: "chart-1",
      action: { label: "Go to SPC Control", path: "/spc-control" }
    },
    {
      number: 7,
      title: "Learn from Anomalies",
      description: "System improves by analyzing deviations",
      details: [
        "Classify anomalies: equipment, product, or parameter",
        "Root cause analysis with AI",
        "Automatic model retraining",
        "Continuous accuracy improvement"
      ],
      icon: Database,
      color: "secondary",
      action: { label: "Go to Anomaly Database", path: "/anomaly-database" }
    }
  ]

  const getColorClasses = (color: string) => {
    const colors: Record<string, { bg: string, border: string, text: string, icon: string }> = {
      destructive: { bg: 'bg-destructive/10', border: 'border-destructive/30', text: 'text-destructive', icon: 'bg-destructive/20' },
      primary: { bg: 'bg-primary/10', border: 'border-primary/30', text: 'text-primary', icon: 'bg-primary/20' },
      success: { bg: 'bg-success/10', border: 'border-success/30', text: 'text-success', icon: 'bg-success/20' },
      accent: { bg: 'bg-accent/10', border: 'border-accent/30', text: 'text-accent', icon: 'bg-accent/20' },
      warning: { bg: 'bg-warning/10', border: 'border-warning/30', text: 'text-warning', icon: 'bg-warning/20' },
      'chart-1': { bg: 'bg-chart-1/10', border: 'border-chart-1/30', text: 'text-chart-1', icon: 'bg-chart-1/20' },
      secondary: { bg: 'bg-secondary/10', border: 'border-secondary/30', text: 'text-secondary', icon: 'bg-secondary/20' }
    }
    return colors[color] || colors.primary
  }

  return (
    <AppLayout>
      <div className="space-y-6">
        {/* Header with Guide Toggle */}
        <div className="flex items-start justify-between animate-slide-in">
          <div>
            <h2 className="text-3xl font-bold text-foreground mb-2 text-glow">System Overview</h2>
            <p className="text-foreground/60">Real-time monitoring and PINN-powered calibration</p>
          </div>
          <Button
            onClick={() => setShowGuide(!showGuide)}
            className="bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 shadow-glow-lg"
          >
            <BookOpen className="w-4 h-4 mr-2" />
            {showGuide ? 'Hide Guide' : 'Show Guide'}
          </Button>
        </div>

        {/* Interactive Timeline Guide */}
        {showGuide && (
          <Card className="p-6 border-2 border-primary/30 bg-gradient-to-br from-primary/5 via-accent/5 to-success/5 shadow-glow-lg animate-slide-in">
            <div className="flex items-start justify-between mb-6">
              <div className="flex items-center gap-3">
                <div className="p-3 bg-primary/20 rounded-lg animate-pulse-glow">
                  <Brain className="w-6 h-6 text-primary" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-foreground">Interactive Workflow Guide</h3>
                  <p className="text-sm text-foreground/60">Step-by-step solution to the Technopack challenge</p>
                </div>
              </div>
              <Button variant="ghost" size="icon" onClick={() => setShowGuide(false)}>
                <X className="w-4 h-4" />
              </Button>
            </div>

            {/* Progress Bar */}
            <div className="mb-8">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-foreground">Progress</span>
                <span className="text-sm font-bold text-primary">
                  {completedSteps.length} / {workflowSteps.length} completed
                </span>
              </div>
              <div className="h-3 bg-muted rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-success via-primary to-accent transition-all duration-500 animate-pulse-glow"
                  style={{ width: `${(completedSteps.length / workflowSteps.length) * 100}%` }}
                ></div>
              </div>
            </div>

            {/* Timeline Steps */}
            <div className="relative space-y-6">
              {/* Vertical Timeline Line */}
              <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gradient-to-b from-primary via-accent to-success opacity-30"></div>

              {workflowSteps.map((step, index) => {
                const isCompleted = completedSteps.includes(step.number)
                const colors = getColorClasses(step.color)
                const Icon = step.icon

                return (
                  <div 
                    key={step.number}
                    className={`relative pl-16 animate-slide-in`}
                    style={{ animationDelay: `${index * 0.1}s` }}
                  >
                    {/* Step Number Circle */}
                    <div className={`absolute left-0 top-0 w-12 h-12 rounded-full border-2 ${colors.border} ${colors.bg} flex items-center justify-center transition-all duration-300 ${
                      isCompleted ? 'scale-110 shadow-glow' : ''
                    }`}>
                      {isCompleted ? (
                        <CheckCircle2 className={`w-6 h-6 ${colors.text} animate-pulse-glow`} />
                      ) : (
                        <span className={`text-lg font-bold ${colors.text}`}>{step.number}</span>
                      )}
                    </div>

                    {/* Step Content Card */}
                    <Card className={`p-5 border-2 ${colors.border} ${colors.bg} hover-lift hover-glow transition-all duration-300 ${
                      isCompleted ? 'opacity-75' : ''
                    }`}>
                      <div className="flex items-start gap-4 mb-3">
                        <div className={`p-2.5 ${colors.icon} rounded-lg flex-shrink-0`}>
                          <Icon className={`w-5 h-5 ${colors.text}`} />
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-start justify-between gap-3">
                            <div className="flex-1">
                              <h4 className="text-lg font-bold text-foreground">{step.title}</h4>
                              <p className="text-sm text-foreground/70 mt-1">{step.description}</p>
                            </div>
                            <button
                              onClick={() => toggleStep(step.number)}
                              className={`flex-shrink-0 w-6 h-6 rounded border-2 ${colors.border} flex items-center justify-center transition-all duration-300 hover:scale-110 ${
                                isCompleted ? colors.bg : 'bg-transparent'
                              }`}
                            >
                              {isCompleted && <CheckCircle2 className={`w-4 h-4 ${colors.text}`} />}
                            </button>
                          </div>
                        </div>
                      </div>

                      {/* Step Details */}
                      <ul className="space-y-2 mb-4 ml-14">
                        {step.details.map((detail, idx) => (
                          <li key={idx} className="flex items-start gap-2 text-sm text-foreground/80">
                            <span className={`${colors.text} mt-1 flex-shrink-0`}>•</span>
                            <span>{detail}</span>
                          </li>
                        ))}
                      </ul>

                      {/* Action Button */}
                      {step.action && (
                        <div className="ml-14">
                          <Button
                            onClick={() => navigateToPage(step.action.path)}
                            className={`w-full bg-gradient-to-r from-${step.color} to-${step.color}/80 hover:shadow-glow-lg`}
                            variant="default"
                          >
                            {step.action.label}
                            <ArrowRight className="w-4 h-4 ml-2" />
                          </Button>
                        </div>
                      )}
                    </Card>
                  </div>
                )
              })}
            </div>

            {/* Completion Message */}
            {completedSteps.length === workflowSteps.length && (
              <Card className="mt-6 p-6 border-2 border-success/30 bg-gradient-to-br from-success/10 to-transparent shadow-glow-lg animate-slide-in">
                <div className="flex items-center gap-4">
                  <div className="p-4 bg-success/20 rounded-full animate-success-pulse">
                    <CheckCircle2 className="w-8 h-8 text-success" />
                  </div>
                  <div>
                    <h4 className="text-xl font-bold text-success">Congratulations!</h4>
                    <p className="text-foreground/80 mt-1">
                      You've completed the full workflow. Your system is now calibrated and ready for production!
                    </p>
                  </div>
                </div>
              </Card>
            )}
          </Card>
        )}

        {/* KPI Cards with Enhanced Colors */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="p-6 glass-effect shadow-glow hover-lift hover-glow animate-slide-in stagger-1 rounded-xl cursor-pointer bg-gradient-to-br from-primary/10 to-transparent border-primary/30">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-foreground/70">Temperature</p>
                <p className="text-3xl font-bold text-foreground mt-2">72.5°C</p>
                <p className="text-xs text-success mt-1">+0.3° from target</p>
              </div>
              <div className="p-3 bg-primary/20 rounded-lg animate-pulse-glow">
                <Zap className="w-6 h-6 text-primary" />
              </div>
            </div>
          </Card>

          <Card className="p-6 glass-effect shadow-glow hover-lift hover-glow animate-slide-in stagger-2 rounded-xl cursor-pointer bg-gradient-to-br from-accent/10 to-transparent border-accent/30">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-foreground/70">Pressure</p>
                <p className="text-3xl font-bold text-foreground mt-2">98.2 kPa</p>
                <p className="text-xs text-success mt-1">Within tolerance</p>
              </div>
              <div className="p-3 bg-accent/20 rounded-lg animate-pulse-glow">
                <Activity className="w-6 h-6 text-accent" />
              </div>
            </div>
          </Card>

          <Card className="p-6 glass-effect shadow-glow hover-lift hover-glow animate-slide-in stagger-3 rounded-xl cursor-pointer bg-gradient-to-br from-success/10 to-transparent border-success/30">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-foreground/70">Flow Rate</p>
                <p className="text-3xl font-bold text-foreground mt-2">45.3 L/min</p>
                <p className="text-xs text-success mt-1">Optimal range</p>
              </div>
              <div className="p-3 bg-success/20 rounded-lg animate-pulse-glow">
                <Droplets className="w-6 h-6 text-success" />
              </div>
            </div>
          </Card>

          <Card className="p-6 glass-effect shadow-glow hover-lift hover-glow animate-slide-in stagger-4 rounded-xl cursor-pointer bg-gradient-to-br from-chart-1/10 to-transparent border-chart-1/30">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-foreground/70">Uptime</p>
                <p className="text-3xl font-bold text-foreground mt-2">99.8%</p>
                <p className="text-xs text-success mt-1">Last 7 days</p>
              </div>
              <div className="p-3 bg-chart-1/20 rounded-lg animate-pulse-glow">
                <TrendingUp className="w-6 h-6 text-chart-1" />
              </div>
            </div>
          </Card>
        </div>

        {/* PINN Visualization Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* PINN Training Loss */}
          <Card className="p-6 border-2 border-primary/30 bg-gradient-to-br from-primary/5 to-transparent shadow-glow-lg animate-slide-in">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-primary/20 rounded-lg">
                <Brain className="w-5 h-5 text-primary" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-foreground">PINN Training Loss</h3>
                <p className="text-xs text-foreground/60">Physics + Data Loss Convergence</p>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={pinnLossData}>
                <defs>
                  <linearGradient id="dataLoss" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#5499FF" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#5499FF" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="physicsLoss" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#4ADE80" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#4ADE80" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="epoch" stroke="var(--foreground)" />
                <YAxis stroke="var(--foreground)" />
                <Tooltip contentStyle={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)' }} />
                <Legend />
                <Area type="monotone" dataKey="dataLoss" stroke="#5499FF" fillOpacity={1} fill="url(#dataLoss)" />
                <Area type="monotone" dataKey="physicsLoss" stroke="#4ADE80" fillOpacity={1} fill="url(#physicsLoss)" />
              </AreaChart>
            </ResponsiveContainer>
          </Card>

          {/* PINN Accuracy Heatmap */}
          <Card className="p-6 border-2 border-success/30 bg-gradient-to-br from-success/5 to-transparent shadow-glow-lg animate-slide-in">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-success/20 rounded-lg">
                <Target className="w-5 h-5 text-success" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-foreground">Prediction Accuracy Map</h3>
                <p className="text-xs text-foreground/60">Viscosity vs Density Performance</p>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <ScatterChart>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis type="number" dataKey="viscosity" name="Viscosity" stroke="var(--foreground)" label={{ value: 'Viscosity (Pa·s)', position: 'bottom' }} />
                <YAxis type="number" dataKey="density" name="Density" stroke="var(--foreground)" label={{ value: 'Density (kg/m³)', angle: -90, position: 'left' }} />
                <Tooltip 
                  cursor={{ strokeDasharray: '3 3' }}
                  contentStyle={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)' }}
                  formatter={(value: any, name: string) => {
                    if (name === 'accuracy') return [`${value}%`, 'Accuracy']
                    return [value, name]
                  }}
                />
                <Scatter data={predictionAccuracyData} fill="#8884d8">
                  {predictionAccuracyData.map((entry, index) => (
                    <Cell 
                      key={`cell-${index}`} 
                      fill={entry.accuracy > 97 ? '#4ADE80' : entry.accuracy > 95 ? '#F59E0B' : '#EF4444'} 
                    />
                  ))}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>
          </Card>
        </div>

        {/* System Metrics and Calibration */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card className="p-6 border border-accent/30 bg-gradient-to-br from-accent/5 to-transparent shadow-glow animate-slide-in">
            <h3 className="text-lg font-semibold text-foreground mb-4">System Metrics (24h)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={metricsData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="time" stroke="var(--foreground)" />
                <YAxis stroke="var(--foreground)" />
                <Tooltip contentStyle={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)' }} />
                <Legend />
                <Line type="monotone" dataKey="temperature" stroke="#F59E0B" strokeWidth={3} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="pressure" stroke="#5499FF" strokeWidth={3} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </Card>

          <Card className="p-6 border border-warning/30 bg-gradient-to-br from-warning/5 to-transparent shadow-glow animate-slide-in">
            <h3 className="text-lg font-semibold text-foreground mb-4">Calibration Status</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={calibrationData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="point" stroke="var(--foreground)" />
                <YAxis stroke="var(--foreground)" />
                <Tooltip contentStyle={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)' }} />
                <Bar dataKey="expected" fill="#F59E0B" radius={[8, 8, 0, 0]} />
                <Bar dataKey="actual" fill="#5499FF" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="p-6 border border-success/30 bg-gradient-to-br from-success/10 to-transparent shadow-glow hover-lift animate-slide-in">
            <h3 className="text-sm font-medium text-foreground/70 mb-3">Last Calibration</h3>
            <p className="text-2xl font-bold text-foreground">2 hrs ago</p>
            <p className="text-xs text-success mt-2">All points within tolerance</p>
          </Card>

          <Card className="p-6 border border-primary/30 bg-gradient-to-br from-primary/10 to-transparent shadow-glow hover-lift animate-slide-in">
            <h3 className="text-sm font-medium text-foreground/70 mb-3">System Health</h3>
            <div className="flex items-center gap-2">
              <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
                <div className="h-full w-[95%] bg-gradient-to-r from-success to-primary rounded-full animate-pulse-glow"></div>
              </div>
              <span className="text-lg font-bold text-success">95%</span>
            </div>
          </Card>

          <Card className="p-6 border border-warning/30 bg-gradient-to-br from-warning/10 to-transparent shadow-glow hover-lift animate-slide-in">
            <h3 className="text-sm font-medium text-foreground/70 mb-3">Active Anomalies</h3>
            <p className="text-2xl font-bold text-warning">1</p>
            <p className="text-xs text-warning mt-2">Minor drift detected</p>
          </Card>
        </div>
      </div>
    </AppLayout>
  )
}
