'use client'

import { AppLayout } from '@/components/app-layout'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Search, Package, Droplets, Gauge, Waves, CheckCircle, AlertCircle } from 'lucide-react'
import { useState } from 'react'
import { api, type Product, type CalibrationProfile } from '@/lib/api'
import { useToast } from '@/hooks/use-toast'

export default function ScannerPage() {
  const [upcCode, setUpcCode] = useState('')
  const [loading, setLoading] = useState(false)
  const [scannedProduct, setScannedProduct] = useState<Product | null>(null)
  const [profile, setProfile] = useState<CalibrationProfile | null>(null)
  const { toast } = useToast()

  const handleScan = async () => {
    if (!upcCode) {
      toast({
        title: "Error",
        description: "Please enter a UPC code",
        variant: "destructive"
      })
      return
    }

    setLoading(true)
    try {
      const response = await api.scanUPC(upcCode)
      setScannedProduct(response.product)
      setProfile(response.profile)
      
      toast({
        title: "Success",
        description: `Product ${response.product.product_name} loaded successfully`,
      })
    } catch (error: any) {
      setScannedProduct(null)
      setProfile(null)
      toast({
        title: "Product Not Found",
        description: error.message || "UPC code not found in database",
        variant: "destructive"
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <AppLayout>
      <div className="space-y-6">
        <div>
          <h2 className="text-3xl font-bold text-foreground mb-2">Product Scanner</h2>
          <p className="text-foreground/60">Scan UPC code for instant product recognition and calibration</p>
        </div>

        {/* Scanner Input */}
        <Card className="p-8 glass-effect shadow-glow">
          <div className="flex gap-4">
            <div className="flex-1">
              <label className="block text-sm font-medium text-foreground/70 mb-2">UPC Code</label>
              <Input
                placeholder="Enter or scan UPC code..."
                value={upcCode}
                onChange={(e) => setUpcCode(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleScan()}
                className="bg-input border border-border text-foreground text-lg h-12"
                disabled={loading}
              />
            </div>
            <div className="flex items-end">
              <Button
                onClick={handleScan}
                disabled={loading}
                className="bg-primary hover:bg-primary/90 text-primary-foreground h-12 px-8"
              >
                <Search className="w-5 h-5 mr-2" />
                {loading ? 'Scanning...' : 'Scan'}
              </Button>
            </div>
          </div>
        </Card>

        {/* Sample UPC Codes */}
        <Card className="p-4 border border-border/50 bg-muted/30">
          <p className="text-sm text-foreground/60 mb-2">Sample UPC codes:</p>
          <div className="flex gap-2 flex-wrap">
            {['1234567890001', '1234567890002', '1234567890003'].map((code) => (
              <Button
                key={code}
                variant="outline"
                size="sm"
                onClick={() => {
                  setUpcCode(code)
                  setTimeout(() => handleScan(), 100)
                }}
                className="font-mono"
              >
                {code}
              </Button>
            ))}
          </div>
        </Card>

        {/* Product Details */}
        {scannedProduct ? (
          <div className="space-y-6 animate-slide-in">
            {/* Product Header */}
            <Card className="p-6 border border-success/30 bg-gradient-to-br from-success/5 to-transparent glass-effect shadow-glow">
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-success/10 rounded-lg animate-pulse-glow">
                    <Package className="w-8 h-8 text-success" />
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold text-foreground">{scannedProduct.product_name}</h3>
                    <p className="text-foreground/60 mt-1 font-mono">UPC: {scannedProduct.upc_code}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-success/10 border border-success/30">
                  <CheckCircle className="w-5 h-5 text-success" />
                  <span className="font-medium text-success">Active</span>
                </div>
              </div>
            </Card>

            {/* Product Properties */}
            <div>
              <h4 className="text-lg font-semibold text-foreground mb-3">Product Properties</h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card className="p-4 border border-border bg-card hover-lift">
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-primary/10 rounded-lg">
                      <Droplets className="w-5 h-5 text-primary" />
                    </div>
                    <div>
                      <p className="text-xs font-medium text-foreground/70">Viscosity</p>
                      <p className="text-xl font-bold text-foreground mt-1">{scannedProduct.viscosity}</p>
                      <p className="text-xs text-foreground/60 mt-0.5">Pa·s</p>
                    </div>
                  </div>
                </Card>

                <Card className="p-4 border border-border bg-card hover-lift">
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-accent/10 rounded-lg">
                      <Gauge className="w-5 h-5 text-accent" />
                    </div>
                    <div>
                      <p className="text-xs font-medium text-foreground/70">Density</p>
                      <p className="text-xl font-bold text-foreground mt-1">{scannedProduct.density}</p>
                      <p className="text-xs text-foreground/60 mt-0.5">kg/m³</p>
                    </div>
                  </div>
                </Card>

                <Card className="p-4 border border-border bg-card hover-lift">
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-chart-1/10 rounded-lg">
                      <Waves className="w-5 h-5 text-chart-1" />
                    </div>
                    <div>
                      <p className="text-xs font-medium text-foreground/70">Surface Tension</p>
                      <p className="text-xl font-bold text-foreground mt-1">{scannedProduct.surface_tension}</p>
                      <p className="text-xs text-foreground/60 mt-0.5">N/m</p>
                    </div>
                  </div>
                </Card>
              </div>
            </div>

            {/* Calibration Profile */}
            {profile && (
              <div>
                <h4 className="text-lg font-semibold text-foreground mb-3">Calibration Profile</h4>
                <Card className="p-6 border border-primary/30 bg-gradient-to-br from-primary/5 to-transparent">
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                    <div>
                      <p className="text-xs font-medium text-foreground/70 mb-1">Valve Timing</p>
                      <p className="text-2xl font-bold text-primary">{profile.valve_timing.toFixed(2)}s</p>
                    </div>
                    <div>
                      <p className="text-xs font-medium text-foreground/70 mb-1">Pressure</p>
                      <p className="text-2xl font-bold text-primary">{profile.pressure.toFixed(0)} PSI</p>
                    </div>
                    <div>
                      <p className="text-xs font-medium text-foreground/70 mb-1">Nozzle Diameter</p>
                      <p className="text-2xl font-bold text-primary">{profile.nozzle_diameter.toFixed(1)} mm</p>
                    </div>
                    <div>
                      <p className="text-xs font-medium text-foreground/70 mb-1">Target Volume</p>
                      <p className="text-2xl font-bold text-primary">{profile.target_volume.toFixed(0)} mL</p>
                    </div>
                    <div>
                      <p className="text-xs font-medium text-foreground/70 mb-1">Accuracy</p>
                      <p className="text-2xl font-bold text-success">{profile.accuracy.toFixed(2)}%</p>
                    </div>
                  </div>
                </Card>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex gap-3">
              <Button 
                className="bg-primary hover:bg-primary/90 text-primary-foreground flex-1"
                onClick={() => window.location.href = '/fill-monitor'}
              >
                Start Fill Operation
              </Button>
              <Button variant="outline" className="flex-1">
                View History
              </Button>
            </div>
          </div>
        ) : upcCode && !loading && !scannedProduct ? (
          <Card className="p-8 border border-destructive/30 bg-destructive/5 animate-slide-in">
            <div className="flex items-start gap-4">
              <AlertCircle className="w-6 h-6 text-destructive flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-semibold text-destructive">Product Not Found</h3>
                <p className="text-destructive/80 mt-1">
                  The UPC code "{upcCode}" was not found in the system. Please verify the code or add a new product.
                </p>
              </div>
            </div>
          </Card>
        ) : (
          <Card className="p-12 border border-dashed border-border text-center">
            <Package className="w-12 h-12 text-foreground/30 mx-auto mb-4" />
            <p className="text-foreground/60 mb-4">Enter a UPC code to get started</p>
            <p className="text-sm text-foreground/40">Instant product recognition with AI-powered calibration</p>
          </Card>
        )}
      </div>
    </AppLayout>
  )
}
