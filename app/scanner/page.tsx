'use client'

import { AppLayout } from '@/components/app-layout'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Search, Package, MapPin, Calendar, AlertCircle, CheckCircle, Download, Brain, Gauge } from 'lucide-react'
import { useState } from 'react'
import jsPDF from 'jspdf'
import 'jspdf-autotable'

// Extend jsPDF type to include autoTable
declare module 'jspdf' {
  interface jsPDF {
    autoTable: (options: any) => jsPDF
  }
}

export default function ScannerPage() {
  const [upcCode, setUpcCode] = useState('')
  const [scannedProduct, setScannedProduct] = useState<any>(null)
  const [pinnPredictions, setPinnPredictions] = useState<any>(null)

  const products: Record<string, any> = {
    '012345678901': {
      name: 'Premium Fill Container',
      sku: 'PFC-500',
      location: 'Warehouse A - Shelf 12',
      lastCalibrated: '2024-03-15',
      status: 'Active',
      batch: 'BATCH-2024-001',
      weight: '500g',
      expiry: '2025-03-15',
      // Product properties for PINN
      viscosity: 0.001,
      density: 1000,
      surfaceTension: 0.072,
      temperature: 20
    },
    '012345678902': {
      name: 'Standard Fill Container',
      sku: 'SFC-250',
      location: 'Warehouse B - Shelf 5',
      lastCalibrated: '2024-03-10',
      status: 'Active',
      batch: 'BATCH-2024-002',
      weight: '250g',
      expiry: '2025-03-10',
      viscosity: 0.065,
      density: 920,
      surfaceTension: 0.032,
      temperature: 22
    },
  }

  const handleScan = () => {
    if (upcCode in products) {
      const product = products[upcCode]
      setScannedProduct(product)
      
      // Simulate PINN predictions
      const predictions = generatePinnPredictions(product)
      setPinnPredictions(predictions)
    } else {
      setScannedProduct(null)
      setPinnPredictions(null)
    }
  }

  const generatePinnPredictions = (product: any) => {
    // Simulate PINN model predictions based on product properties
    const baseValveTiming = 1.5 + (product.viscosity * 100)
    const basePressure = 50 + (product.density / 20)
    const baseNozzle = 5 + (product.surfaceTension * 50)
    
    return {
      valveTiming: baseValveTiming.toFixed(3),
      pressure: basePressure.toFixed(1),
      nozzleDiameter: baseNozzle.toFixed(2),
      expectedVolume: product.weight,
      accuracy: (96 + Math.random() * 3).toFixed(1),
      confidence: (95 + Math.random() * 4).toFixed(1),
      dataLoss: (0.05 + Math.random() * 0.03).toFixed(4),
      physicsLoss: (0.06 + Math.random() * 0.03).toFixed(4),
      totalLoss: (0.055 + Math.random() * 0.03).toFixed(4),
      trainingEpochs: 500,
      convergenceTime: '2.3s'
    }
  }

  const generatePDF = () => {
    if (!scannedProduct || !pinnPredictions) return

    const doc = new jsPDF()
    const pageWidth = doc.internal.pageSize.getWidth()
    
    // Header
    doc.setFillColor(84, 153, 255)
    doc.rect(0, 0, pageWidth, 40, 'F')
    doc.setTextColor(255, 255, 255)
    doc.setFontSize(24)
    doc.text('PINNs-UPC Calibration Report', pageWidth / 2, 20, { align: 'center' })
    doc.setFontSize(12)
    doc.text('Physics-Informed Neural Network Predictions', pageWidth / 2, 30, { align: 'center' })
    
    // Reset text color
    doc.setTextColor(0, 0, 0)
    
    // Product Information
    doc.setFontSize(16)
    doc.setFont('helvetica', 'bold')
    doc.text('Product Information', 14, 55)
    
    doc.autoTable({
      startY: 60,
      head: [['Property', 'Value']],
      body: [
        ['Product Name', scannedProduct.name],
        ['SKU', scannedProduct.sku],
        ['UPC Code', upcCode],
        ['Batch Number', scannedProduct.batch],
        ['Weight', scannedProduct.weight],
        ['Location', scannedProduct.location],
        ['Last Calibrated', scannedProduct.lastCalibrated],
        ['Status', scannedProduct.status]
      ],
      theme: 'grid',
      headStyles: { fillColor: [84, 153, 255] },
      margin: { left: 14, right: 14 }
    })
    
    // Product Properties
    let finalY = (doc as any).lastAutoTable.finalY + 10
    doc.setFontSize(16)
    doc.setFont('helvetica', 'bold')
    doc.text('Physical Properties (Input to PINN)', 14, finalY)
    
    doc.autoTable({
      startY: finalY + 5,
      head: [['Property', 'Value', 'Unit']],
      body: [
        ['Viscosity', scannedProduct.viscosity.toFixed(3), 'Pa·s'],
        ['Density', scannedProduct.density.toFixed(1), 'kg/m³'],
        ['Surface Tension', scannedProduct.surfaceTension.toFixed(3), 'N/m'],
        ['Temperature', scannedProduct.temperature.toFixed(1), '°C']
      ],
      theme: 'grid',
      headStyles: { fillColor: [74, 222, 128] },
      margin: { left: 14, right: 14 }
    })
    
    // PINN Predictions
    finalY = (doc as any).lastAutoTable.finalY + 10
    doc.setFontSize(16)
    doc.setFont('helvetica', 'bold')
    doc.text('PINN Model Predictions', 14, finalY)
    
    doc.autoTable({
      startY: finalY + 5,
      head: [['Parameter', 'Predicted Value', 'Unit']],
      body: [
        ['Valve Timing', pinnPredictions.valveTiming, 'seconds'],
        ['Pressure', pinnPredictions.pressure, 'PSI'],
        ['Nozzle Diameter', pinnPredictions.nozzleDiameter, 'mm'],
        ['Expected Volume', pinnPredictions.expectedVolume, 'ml']
      ],
      theme: 'grid',
      headStyles: { fillColor: [148, 187, 255] },
      margin: { left: 14, right: 14 }
    })
    
    // Model Performance
    finalY = (doc as any).lastAutoTable.finalY + 10
    doc.setFontSize(16)
    doc.setFont('helvetica', 'bold')
    doc.text('Model Performance Metrics', 14, finalY)
    
    doc.autoTable({
      startY: finalY + 5,
      head: [['Metric', 'Value']],
      body: [
        ['Prediction Accuracy', `${pinnPredictions.accuracy}%`],
        ['Confidence Score', `${pinnPredictions.confidence}%`],
        ['Data Loss', pinnPredictions.dataLoss],
        ['Physics Loss', pinnPredictions.physicsLoss],
        ['Total Loss', pinnPredictions.totalLoss],
        ['Training Epochs', pinnPredictions.trainingEpochs.toString()],
        ['Convergence Time', pinnPredictions.convergenceTime]
      ],
      theme: 'grid',
      headStyles: { fillColor: [245, 158, 11] },
      margin: { left: 14, right: 14 }
    })
    
    // Accuracy Gauge Visualization (text-based)
    finalY = (doc as any).lastAutoTable.finalY + 15
    doc.setFontSize(14)
    doc.setFont('helvetica', 'bold')
    doc.text('Accuracy Score', 14, finalY)
    
    // Draw accuracy meter
    const meterX = 14
    const meterY = finalY + 5
    const meterWidth = 180
    const meterHeight = 20
    const accuracy = parseFloat(pinnPredictions.accuracy)
    
    // Background
    doc.setFillColor(240, 240, 240)
    doc.roundedRect(meterX, meterY, meterWidth, meterHeight, 3, 3, 'F')
    
    // Accuracy fill
    const fillWidth = (accuracy / 100) * meterWidth
    if (accuracy >= 97) {
      doc.setFillColor(74, 222, 128) // Green
    } else if (accuracy >= 95) {
      doc.setFillColor(245, 158, 11) // Orange
    } else {
      doc.setFillColor(239, 68, 68) // Red
    }
    doc.roundedRect(meterX, meterY, fillWidth, meterHeight, 3, 3, 'F')
    
    // Accuracy text
    doc.setTextColor(0, 0, 0)
    doc.setFontSize(12)
    doc.text(`${accuracy}%`, meterX + meterWidth / 2, meterY + meterHeight / 2 + 4, { align: 'center' })
    
    // Status indicator
    finalY = meterY + meterHeight + 10
    doc.setFontSize(12)
    doc.setFont('helvetica', 'normal')
    let statusText = ''
    let statusColor: [number, number, number] = [0, 0, 0]
    
    if (accuracy >= 97) {
      statusText = '✓ EXCELLENT - Predictions are highly accurate'
      statusColor = [74, 222, 128]
    } else if (accuracy >= 95) {
      statusText = '⚠ GOOD - Predictions are acceptable'
      statusColor = [245, 158, 11]
    } else {
      statusText = '✗ NEEDS IMPROVEMENT - Consider retraining'
      statusColor = [239, 68, 68]
    }
    
    doc.setTextColor(...statusColor)
    doc.text(statusText, 14, finalY)
    
    // Footer
    doc.setTextColor(100, 100, 100)
    doc.setFontSize(10)
    doc.text(`Generated: ${new Date().toLocaleString()}`, 14, doc.internal.pageSize.getHeight() - 10)
    doc.text('PINNs-UPC Calibration System v2.1.0', pageWidth - 14, doc.internal.pageSize.getHeight() - 10, { align: 'right' })
    
    // Save PDF
    doc.save(`PINN_Report_${upcCode}_${Date.now()}.pdf`)
  }

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="animate-slide-in">
          <h2 className="text-3xl font-bold text-foreground mb-2 text-glow">UPC Scanner</h2>
          <p className="text-foreground/60">Scan or enter UPC codes to retrieve product information</p>
        </div>

        {/* Scanner Input */}
        <Card className="p-8 border border-border bg-card animate-slide-in stagger-1">
          <div className="flex gap-4">
            <div className="flex-1">
              <label className="block text-sm font-medium text-foreground/70 mb-2">UPC Code</label>
              <Input
                placeholder="Enter or scan UPC code..."
                value={upcCode}
                onChange={(e) => setUpcCode(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleScan()}
                className="bg-input border border-border text-foreground"
              />
            </div>
            <div className="flex items-end">
              <Button
                onClick={handleScan}
                className="bg-primary hover:bg-primary/90 text-primary-foreground"
              >
                <Search className="w-4 h-4 mr-2" />
                Scan
              </Button>
            </div>
          </div>
        </Card>

        {/* Test UPC Codes */}
        <Card className="p-4 border border-border/50 bg-muted/30 animate-slide-in stagger-2">
          <p className="text-xs text-foreground/60">Try these test codes: <code className="text-primary">012345678901</code> or <code className="text-primary">012345678902</code></p>
        </Card>

        {/* Product Details */}
        {scannedProduct ? (
          <div className="space-y-6 animate-fade-in">
            {/* Product Header */}
            <Card className="p-6 border border-success/30 bg-gradient-to-br from-success/5 to-transparent shadow-glow-lg animate-slide-in">
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-success/10 rounded-lg animate-float">
                    <Package className="w-8 h-8 text-success" />
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold text-foreground">{scannedProduct.name}</h3>
                    <p className="text-foreground/60 mt-1">SKU: {scannedProduct.sku}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-success/10 border border-success/30 animate-pulse-glow">
                  <CheckCircle className="w-5 h-5 text-success" />
                  <span className="font-medium text-success">{scannedProduct.status}</span>
                </div>
              </div>
            </Card>

            {/* PINN Predictions Card */}
            {pinnPredictions && (
              <Card className="p-6 border-2 border-primary/30 bg-gradient-to-br from-primary/5 to-transparent shadow-glow-lg animate-slide-in">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-3 bg-primary/20 rounded-lg animate-pulse-glow">
                    <Brain className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-foreground">PINN Model Predictions</h3>
                    <p className="text-sm text-foreground/60">Physics-Informed Neural Network Results</p>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                  <div className="glass-effect p-4 rounded-lg border border-primary/20">
                    <p className="text-xs text-foreground/60 mb-1">Valve Timing</p>
                    <p className="text-2xl font-bold text-primary">{pinnPredictions.valveTiming}s</p>
                  </div>
                  <div className="glass-effect p-4 rounded-lg border border-accent/20">
                    <p className="text-xs text-foreground/60 mb-1">Pressure</p>
                    <p className="text-2xl font-bold text-accent">{pinnPredictions.pressure} PSI</p>
                  </div>
                  <div className="glass-effect p-4 rounded-lg border border-success/20">
                    <p className="text-xs text-foreground/60 mb-1">Nozzle Diameter</p>
                    <p className="text-2xl font-bold text-success">{pinnPredictions.nozzleDiameter} mm</p>
                  </div>
                  <div className="glass-effect p-4 rounded-lg border border-warning/20">
                    <p className="text-xs text-foreground/60 mb-1">Expected Volume</p>
                    <p className="text-2xl font-bold text-warning">{pinnPredictions.expectedVolume}</p>
                  </div>
                </div>

                {/* Accuracy Meter */}
                <div className="glass-effect p-4 rounded-lg border border-success/20 mb-4">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <Gauge className="w-5 h-5 text-success" />
                      <span className="text-sm font-semibold text-foreground">Prediction Accuracy</span>
                    </div>
                    <span className="text-2xl font-bold text-success">{pinnPredictions.accuracy}%</span>
                  </div>
                  <div className="h-4 bg-muted rounded-full overflow-hidden">
                    <div 
                      className={`h-full transition-all duration-1000 ${
                        parseFloat(pinnPredictions.accuracy) >= 97 ? 'bg-gradient-to-r from-success to-primary' :
                        parseFloat(pinnPredictions.accuracy) >= 95 ? 'bg-gradient-to-r from-warning to-accent' :
                        'bg-gradient-to-r from-destructive to-warning'
                      } animate-pulse-glow`}
                      style={{ width: `${pinnPredictions.accuracy}%` }}
                    ></div>
                  </div>
                  <p className="text-xs text-foreground/60 mt-2">
                    {parseFloat(pinnPredictions.accuracy) >= 97 ? '✓ Excellent - Highly accurate predictions' :
                     parseFloat(pinnPredictions.accuracy) >= 95 ? '⚠ Good - Acceptable accuracy' :
                     '✗ Needs Improvement - Consider retraining'}
                  </p>
                </div>

                {/* Model Metrics */}
                <div className="grid grid-cols-3 gap-3">
                  <div className="text-center glass-effect p-3 rounded-lg border border-border">
                    <p className="text-xs text-foreground/60">Confidence</p>
                    <p className="text-lg font-bold text-primary">{pinnPredictions.confidence}%</p>
                  </div>
                  <div className="text-center glass-effect p-3 rounded-lg border border-border">
                    <p className="text-xs text-foreground/60">Total Loss</p>
                    <p className="text-lg font-bold text-accent">{pinnPredictions.totalLoss}</p>
                  </div>
                  <div className="text-center glass-effect p-3 rounded-lg border border-border">
                    <p className="text-xs text-foreground/60">Convergence</p>
                    <p className="text-lg font-bold text-success">{pinnPredictions.convergenceTime}</p>
                  </div>
                </div>
              </Card>
            )}

            {/* Product Information Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <Card className="p-4 border border-border bg-card animate-slide-in stagger-1">
                <p className="text-xs font-medium text-foreground/70 mb-2">Location</p>
                <div className="flex items-start gap-2">
                  <MapPin className="w-4 h-4 text-accent mt-0.5 flex-shrink-0" />
                  <p className="font-medium text-foreground">{scannedProduct.location}</p>
                </div>
              </Card>

              <Card className="p-4 border border-border bg-card animate-slide-in stagger-2">
                <p className="text-xs font-medium text-foreground/70 mb-2">Last Calibrated</p>
                <div className="flex items-start gap-2">
                  <Calendar className="w-4 h-4 text-primary mt-0.5 flex-shrink-0" />
                  <p className="font-medium text-foreground">{scannedProduct.lastCalibrated}</p>
                </div>
              </Card>

              <Card className="p-4 border border-border bg-card animate-slide-in stagger-3">
                <p className="text-xs font-medium text-foreground/70 mb-2">Weight</p>
                <p className="text-2xl font-bold text-foreground">{scannedProduct.weight}</p>
              </Card>

              <Card className="p-4 border border-border bg-card animate-slide-in stagger-4">
                <p className="text-xs font-medium text-foreground/70 mb-2">Batch Number</p>
                <p className="font-mono font-medium text-foreground">{scannedProduct.batch}</p>
              </Card>

              <Card className="p-4 border border-border bg-card animate-slide-in stagger-1">
                <p className="text-xs font-medium text-foreground/70 mb-2">Expiry Date</p>
                <p className="font-medium text-foreground">{scannedProduct.expiry}</p>
              </Card>

              <Card className="p-4 border border-border bg-card animate-slide-in stagger-2">
                <p className="text-xs font-medium text-foreground/70 mb-2">UPC Code</p>
                <p className="font-mono text-sm text-foreground">{upcCode}</p>
              </Card>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 animate-slide-in stagger-3">
              <Button className="bg-primary hover:bg-primary/90 text-primary-foreground flex-1">
                Calibrate
              </Button>
              <Button variant="outline" className="flex-1">
                View History
              </Button>
              <Button 
                onClick={generatePDF}
                className="flex-1 bg-gradient-to-r from-success to-primary hover:shadow-glow-lg"
              >
                <Download className="w-4 h-4 mr-2" />
                Export Report
              </Button>
            </div>
          </div>
        ) : upcCode && !scannedProduct ? (
          <Card className="p-8 border border-destructive/30 bg-destructive/5 animate-slide-in shadow-glow">
            <div className="flex items-start gap-4">
              <AlertCircle className="w-6 h-6 text-destructive flex-shrink-0 mt-0.5 animate-pulse-glow" />
              <div>
                <h3 className="font-semibold text-destructive">Product Not Found</h3>
                <p className="text-destructive/80 mt-1">The UPC code "{upcCode}" was not found in the system. Please verify the code and try again.</p>
              </div>
            </div>
          </Card>
        ) : (
          <Card className="p-12 border border-dashed border-border text-center animate-fade-in">
            <Package className="w-12 h-12 text-foreground/30 mx-auto mb-4 animate-float" />
            <p className="text-foreground/60 mb-4">Enter a UPC code to get started</p>
          </Card>
        )}
      </div>
    </AppLayout>
  )
}
