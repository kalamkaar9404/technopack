/**
 * API client for PINNs-UPC Calibration System
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface Product {
  upc_code: string
  product_name: string
  viscosity: number
  density: number
  surface_tension: number
}

export interface CalibrationProfile {
  valve_timing: number
  pressure: number
  nozzle_diameter: number
  target_volume: number
  accuracy: number
}

export interface ScanResponse {
  status: string
  product: Product
  profile: CalibrationProfile | null
}

export interface PredictionResponse {
  prediction: {
    predicted_volume: number
    predicted_time: number
    confidence: number
    physics_valid: boolean
    similar_anomalies?: Array<{
      anomaly_id: string
      similarity_score: number
      issue_type: string
      solution: string
      effectiveness: number
      upvotes: number
    }>
  }
  alert: string | null
  recommendation: any
}

export interface ExecutionResponse {
  actual_volume: number
  actual_time: number
  anomaly_detected: boolean
  vision?: {
    detected_volume: number
    confidence: number
    liquid_height: number
    has_foam: boolean
    image_quality: string
  }
}

export interface HealthStatus {
  components: Record<string, {
    health_score: number
    accuracy_trend: number[]
    predicted_failure_date: string | null
    maintenance_recommended: boolean
  }>
  alerts: Array<{
    severity: string
    component: string
    message: string
    recommended_action: string
    days_until_failure: number | null
  }>
  maintenance_schedule: Array<{
    component: string
    priority: string
    health_score: number
    recommended_date: string
    action: string
  }>
}

export interface SPCStatus {
  alerts: Array<{
    rule_name: string
    severity: string
    message: string
    recommended_action: string
  }>
  chart_data: {
    status: string
    timestamps?: string[]
    errors?: number[]
    ucl?: number
    uwl?: number
    center?: number
    lwl?: number
    lcl?: number
    num_points?: number
  }
  capability: {
    status: string
    cp?: number
    cpk?: number
    capability?: string
    mean_error?: number
    std_error?: number
    interpretation?: string
  }
}

export interface AnomalyStatistics {
  total_anomalies: number
  issue_types: Record<string, number>
  product_categories: Record<string, number>
  average_effectiveness: number
  total_upvotes: number
}

class APIClient {
  private baseURL: string

  constructor(baseURL: string = API_URL) {
    this.baseURL = baseURL
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`
    
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }))
      throw new Error(error.detail || `HTTP ${response.status}`)
    }

    return response.json()
  }

  // Products
  async getProducts(): Promise<{ products: Product[] }> {
    return this.request('/api/products')
  }

  async scanUPC(upcCode: string): Promise<ScanResponse> {
    return this.request('/api/scan', {
      method: 'POST',
      body: JSON.stringify({ upc_code: upcCode }),
    })
  }

  async addProduct(product: {
    upc_code: string
    product_name: string
    viscosity: number
    density: number
    surface_tension: number
  }): Promise<{ status: string; message: string }> {
    return this.request('/api/products', {
      method: 'POST',
      body: JSON.stringify(product),
    })
  }

  // Fill operations
  async predictFill(params: {
    valve_timing: number
    pressure: number
    nozzle_diameter: number
    target_volume: number
    temperature?: number
  }): Promise<PredictionResponse> {
    return this.request('/api/predict', {
      method: 'POST',
      body: JSON.stringify(params),
    })
  }

  async executeFill(params: {
    valve_timing: number
    pressure: number
    nozzle_diameter: number
    target_volume: number
    actual_volume: number
    actual_time: number
    temperature?: number
    use_vision?: boolean
  }): Promise<ExecutionResponse> {
    return this.request('/api/execute', {
      method: 'POST',
      body: JSON.stringify(params),
    })
  }

  // Health monitoring
  async getHealthStatus(): Promise<HealthStatus> {
    return this.request('/api/health')
  }

  // SPC monitoring
  async getSPCStatus(): Promise<SPCStatus> {
    return this.request('/api/spc')
  }

  // Anomaly database
  async getAnomalies(issueType?: string): Promise<any> {
    const query = issueType ? `?issue_type=${issueType}` : ''
    return this.request(`/api/anomalies${query}`)
  }

  async reportAnomaly(params: {
    issue_type: string
    solution: string
    effectiveness: number
  }): Promise<{ status: string; anomaly_id: string }> {
    return this.request('/api/anomalies', {
      method: 'POST',
      body: JSON.stringify(params),
    })
  }

  // Dashboard
  async getDashboardStats(): Promise<{
    total_fills: number
    avg_accuracy: number
    uptime: number
    current_product: Product | null
  }> {
    return this.request('/api/dashboard')
  }
}

export const api = new APIClient()
