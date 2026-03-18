# v0 Prompt: PINNs-UPC Calibration System UI

Create a modern, professional web application UI for an AI-powered liquid filling calibration system used in industrial manufacturing. This is for the Technopack Hackathon 2026.

## Application Overview

**Name**: PINNs-UPC Calibration System  
**Purpose**: Intelligent liquid filling machine calibration combining Physics-Informed Neural Networks (PINNs) with UPC product database for instant, accurate fills with advanced monitoring.

**Core Innovation**: Scan product UPC → Get instant calibration → AI predicts fill parameters → Computer vision verifies → Real-time quality monitoring

## Design Requirements

### Brand & Style
- **Theme**: Industrial tech meets modern AI
- **Colors**: 
  - Primary: Deep blue (#1e3a8a) - trust, precision
  - Secondary: Cyan (#06b6d4) - technology, innovation
  - Accent: Orange (#f97316) - alerts, warnings
  - Success: Green (#10b981)
  - Error: Red (#ef4444)
- **Typography**: Clean, technical sans-serif (Inter or similar)
- **Style**: Modern dashboard with glassmorphism effects, subtle gradients
- **Icons**: Use Lucide React icons throughout

### Layout Structure
- **Sidebar Navigation** (left, 240px wide, collapsible on mobile)
- **Main Content Area** (responsive, max-width 1400px)
- **Header Bar** (top, 64px, with logo and status indicators)


## Page 1: Scanner (Home/Landing)

### Purpose
Product recognition via UPC scanning - the entry point for all operations.

### Layout
```
┌─────────────────────────────────────────────────┐
│ Header: "Product Scanner" + Quick Stats        │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────────┐  ┌─────────────────────┐ │
│  │  UPC Input      │  │  Current Product    │ │
│  │  [Scan Icon]    │  │  Card               │ │
│  │  Large input    │  │  - Name             │ │
│  │  field          │  │  - UPC              │ │
│  │  "Scan Product" │  │  - Properties       │ │
│  │  button         │  │  - Profile preview  │ │
│  └─────────────────┘  └─────────────────────┘ │
│                                                 │
│  Recent Products (horizontal scroll)           │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐                 │
│  │Card│ │Card│ │Card│ │Card│                 │
│  └────┘ └────┘ └────┘ └────┘                 │
│                                                 │
│  Add New Product (expandable section)          │
│  Form with: UPC, Name, Viscosity, Density,     │
│  Surface Tension fields                        │
└─────────────────────────────────────────────────┘
```

### Components
1. **UPC Input Card** (centered, elevated)
   - Large text input with barcode icon
   - "Scan Product" primary button
   - Sample UPC codes shown below as chips
   - Loading state with spinner

2. **Current Product Card** (right side)
   - Product name (large, bold)
   - UPC code (monospace font)
   - Property badges (viscosity, density, surface tension)
   - Calibration profile preview (valve timing, pressure, nozzle)
   - "Start Fill" CTA button

3. **Recent Products** (horizontal carousel)
   - Small cards with product name + UPC
   - Click to load
   - Max 10 items

4. **Add Product Form** (collapsible)
   - All input fields with validation
   - Helper text for each field
   - "Add Product" button

### Sample Data
- UPC: 1234567890001 → Water (0.001 Pa·s)
- UPC: 1234567890002 → Vegetable Oil (0.065 Pa·s)
- UPC: 1234567890003 → Honey (6.0 Pa·s)


## Page 2: Fill Monitor (Main Operations)

### Purpose
Execute fills with AI prediction, vision verification, and real-time monitoring.

### Layout
```
┌─────────────────────────────────────────────────┐
│ Header: "Fill Monitor" + Active Product        │
├──────────────────┬──────────────────────────────┤
│ Parameters       │  Prediction & Results        │
│ (Left Panel)     │  (Right Panel)               │
│                  │                              │
│ Valve Timing     │  ┌─────────────────────┐    │
│ [Slider] 1.0s    │  │ AI Prediction       │    │
│                  │  │ Volume: 498.5 mL    │    │
│ Pressure         │  │ Time: 2.1s          │    │
│ [Slider] 50 PSI  │  │ Confidence: 95%     │    │
│                  │  │ Accuracy: 99.7%     │    │
│ Nozzle Diameter  │  └─────────────────────┘    │
│ [Slider] 5.0mm   │                              │
│                  │  ⚠️ Similar Issues Found     │
│ Target Volume    │  [Expandable warnings]       │
│ [Input] 500 mL   │                              │
│                  │  ┌─────────────────────┐    │
│ [Predict Fill]   │  │ Vision Detection    │    │
│                  │  │ 📷 Detected: 499mL  │    │
│ ─────────────    │  │ Confidence: 92%     │    │
│                  │  │ ✓ No foam           │    │
│ Actual Volume    │  └─────────────────────┘    │
│ [Input] 498.5 mL │                              │
│                  │  Fill History (table)        │
│ Actual Time      │  Recent 10 fills             │
│ [Input] 2.1s     │                              │
│                  │                              │
│ ☑ Vision Check   │                              │
│                  │                              │
│ [Log Fill]       │                              │
└──────────────────┴──────────────────────────────┘
```

### Components
1. **Parameter Controls** (left panel, sticky)
   - 3 sliders with live values
   - Target volume input
   - "Predict Fill" primary button
   - Actual values section (appears after prediction)
   - Vision detection checkbox
   - "Log Fill Result" button

2. **Prediction Card** (top right)
   - Large metrics display
   - Color-coded accuracy indicator:
     - Green: >99% (Excellent)
     - Yellow: 98-99% (Acceptable)
     - Red: <98% (Poor)
   - Confidence score with progress bar
   - Physics validation badge

3. **Similar Issues Alert** (expandable)
   - Warning icon + count
   - Expandable list showing:
     - Issue type badge
     - Solution preview
     - Effectiveness % + upvotes
     - "View Details" link

4. **Vision Detection Card**
   - Camera icon
   - Detected volume (large)
   - Confidence meter
   - Foam detection indicator
   - Image quality status

5. **Fill History Table**
   - Columns: Time, Target, Actual, Error%, Status
   - Color-coded status (success/warning/error)
   - Sortable
   - Last 10 fills


## Page 3: Equipment Health

### Purpose
Monitor equipment health, predict failures, schedule maintenance.

### Layout
```
┌─────────────────────────────────────────────────┐
│ Header: "Equipment Health" + Overall Score     │
├─────────────────────────────────────────────────┤
│                                                 │
│  Active Alerts (if any)                        │
│  ┌─────────────────────────────────────────┐  │
│  │ 🔴 CRITICAL: Nozzle health 92%         │  │
│  │ Action: IMMEDIATE replacement needed    │  │
│  └─────────────────────────────────────────┘  │
│                                                 │
│  Component Health (4-column grid)              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───┐│
│  │ Nozzle   │ │ Valve    │ │ Pump     │ │...││
│  │ ━━━━━━━  │ │ ━━━━━━━━ │ │ ━━━━━━━━ │ │   ││
│  │ 92%      │ │ 98%      │ │ 99%      │ │   ││
│  │ ⚠️ Warning│ │ ✓ Good   │ │ ✓ Good   │ │   ││
│  │          │ │          │ │          │ │   ││
│  │ Trend ↓  │ │ Trend →  │ │ Trend ↑  │ │   ││
│  │ 15 days  │ │ No issues│ │ No issues│ │   ││
│  └──────────┘ └──────────┘ └──────────┘ └───┘│
│                                                 │
│  Maintenance Schedule                          │
│  ┌─────────────────────────────────────────┐  │
│  │ 🔴 HIGH: Nozzle inspection - Due: 3/20 │  │
│  │ 🟡 MED: Valve service - Due: 4/15      │  │
│  │ 🟢 LOW: Pump check - Due: 5/1          │  │
│  └─────────────────────────────────────────┘  │
│                                                 │
│  Accuracy Trend Chart (7 days)                 │
│  [Line chart showing accuracy over time]       │
└─────────────────────────────────────────────────┘
```

### Components
1. **Overall Health Score** (header)
   - Large circular progress indicator
   - Color-coded (green/yellow/red)
   - System status text

2. **Alert Banner** (conditional)
   - Severity icon + color
   - Component name
   - Message
   - Recommended action
   - Days until failure (if applicable)

3. **Component Cards** (4-column grid)
   - Component name + icon
   - Health score (large, bold)
   - Circular progress bar
   - Status badge (Good/Warning/Critical)
   - Trend indicator (↑↓→)
   - Failure prediction or "No issues"
   - Mini sparkline chart

4. **Maintenance Schedule** (list)
   - Priority indicator (colored dot)
   - Component name
   - Action required
   - Due date
   - "Schedule" button

5. **Accuracy Trend Chart**
   - Line chart (7-30 days)
   - Warning/critical thresholds shown
   - Hover tooltips with details


## Page 4: SPC Control Chart

### Purpose
Statistical Process Control monitoring with Western Electric rules.

### Layout
```
┌─────────────────────────────────────────────────┐
│ Header: "Quality Control" + Process Status     │
├─────────────────────────────────────────────────┤
│                                                 │
│  Process Status (3 metrics)                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ Cpk      │ │ In Control│ │ Violations│      │
│  │ 1.45     │ │ ✓ Yes    │ │ 0         │      │
│  │ Excellent│ │          │ │           │      │
│  └──────────┘ └──────────┘ └──────────┘       │
│                                                 │
│  SPC Rule Violations (if any)                  │
│  ┌─────────────────────────────────────────┐  │
│  │ ⚠️ Rule 4: 7 consecutive above center  │  │
│  │ Action: Reduce pressure or timing      │  │
│  └─────────────────────────────────────────┘  │
│                                                 │
│  Control Chart (large, interactive)            │
│  ┌─────────────────────────────────────────┐  │
│  │     UCL ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─     │  │
│  │     UWL ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄     │  │
│  │  ●  ●     ●  ●  ●     ●  ●  ●  ●  ●   │  │
│  │ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │  │
│  │     LWL ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄ ┄     │  │
│  │     LCL ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─     │  │
│  │                                         │  │
│  │  X-axis: Fill Number                   │  │
│  │  Y-axis: Error %                       │  │
│  └─────────────────────────────────────────┘  │
│                                                 │
│  Process Capability Details                    │
│  ┌──────────────────┬──────────────────────┐  │
│  │ Cp: 1.52         │ Mean Error: 0.12%    │  │
│  │ Cpk: 1.45        │ Std Dev: 0.45%       │  │
│  │ Capability: ⭐⭐⭐│ Range: -1.2% to 1.5% │  │
│  └──────────────────┴──────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### Components
1. **Process Status Cards** (3-column)
   - Cpk value (large) + interpretation
   - In Control status (✓/✗)
   - Violation count

2. **Rule Violation Alerts** (conditional)
   - Rule name + description
   - Severity indicator
   - Recommended action
   - Data points involved

3. **Control Chart** (main feature)
   - Interactive line chart
   - Control limits (UCL, UWL, Center, LWL, LCL)
   - Data points with hover details
   - Violations highlighted in red
   - Zoom/pan controls
   - Legend

4. **Capability Details** (2-column grid)
   - Cp and Cpk values
   - Star rating visualization
   - Mean error and std dev
   - Range information

5. **Western Electric Rules** (info panel)
   - Collapsible section explaining 6 rules
   - Visual examples


## Page 5: Anomaly Database

### Purpose
Search and share solutions to common filling issues globally.

### Layout
```
┌─────────────────────────────────────────────────┐
│ Header: "Anomaly Database" + Stats             │
├─────────────────────────────────────────────────┤
│                                                 │
│  Database Stats (4 metrics)                    │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │
│  │ 1,247  │ │ 94%    │ │ 3,521  │ │ 5      │ │
│  │Anomalies│ │Avg Eff │ │Upvotes │ │Categories││
│  └────────┘ └────────┘ └────────┘ └────────┘ │
│                                                 │
│  Search Solutions                              │
│  ┌─────────────────────────────────────────┐  │
│  │ Issue Type: [Dropdown ▼]               │  │
│  │ ○ Foam Overflow  ○ Clog  ○ Drift       │  │
│  │ ○ Underfill      ○ Overfill            │  │
│  │                                         │  │
│  │ [Search Solutions] button               │  │
│  └─────────────────────────────────────────┘  │
│                                                 │
│  Solutions (card list)                         │
│  ┌─────────────────────────────────────────┐  │
│  │ 🔴 Foam Overflow                        │  │
│  │ Effectiveness: ████████░░ 85%          │  │
│  │ Upvotes: 👍 42                          │  │
│  │                                         │  │
│  │ Solution: Reduce fill speed by 30%     │  │
│  │ and lower temperature to <25°C         │  │
│  │                                         │  │
│  │ Conditions: Carbonated | Low visc |    │  │
│  │ Room temp | 60 PSI                     │  │
│  │                                         │  │
│  │ [👍 Upvote] [View Details]             │  │
│  └─────────────────────────────────────────┘  │
│                                                 │
│  Report New Anomaly (expandable)               │
│  Form: Issue type, Solution, Effectiveness     │
└─────────────────────────────────────────────────┘
```

### Components
1. **Database Stats** (4-column metrics)
   - Total anomalies
   - Average effectiveness
   - Total upvotes
   - Issue categories
   - Each with icon

2. **Search Section**
   - Issue type dropdown
   - Radio buttons for quick selection
   - "Search Solutions" button
   - Loading state

3. **Solution Cards** (list)
   - Issue type badge (colored)
   - Effectiveness progress bar
   - Upvote count with icon
   - Solution text (prominent)
   - Conditions (chips/badges)
   - Similarity score (if from search)
   - Action buttons (Upvote, View Details)

4. **Report Form** (collapsible)
   - Issue type selector
   - Solution textarea
   - Effectiveness slider
   - "Submit to Database" button
   - Success confirmation

5. **Trending Issues** (sidebar)
   - Top 5 most common issues
   - Click to search


## Page 6: Dashboard (Overview)

### Purpose
Executive overview with key metrics and system status.

### Layout
```
┌─────────────────────────────────────────────────┐
│ Header: "System Dashboard" + Time Range        │
├─────────────────────────────────────────────────┤
│                                                 │
│  Key Metrics (4-column)                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───┐│
│  │ Fills    │ │ Accuracy │ │ Uptime   │ │...││
│  │ 1,247    │ │ 99.2%    │ │ 98.5%    │ │   ││
│  │ +12% ↑   │ │ +0.3% ↑  │ │ -0.2% ↓  │ │   ││
│  └──────────┘ └──────────┘ └──────────┘ └───┘│
│                                                 │
│  ┌─────────────────────┬───────────────────┐  │
│  │ System Status       │ Quick Actions     │  │
│  │                     │                   │  │
│  │ ✓ All systems OK    │ [Scan Product]    │  │
│  │ ⚠️ 1 maintenance due│ [Start Fill]      │  │
│  │ ℹ️ Model trained    │ [View Health]     │  │
│  │                     │ [View SPC]        │  │
│  └─────────────────────┴───────────────────┘  │
│                                                 │
│  Recent Activity (timeline)                    │
│  ┌─────────────────────────────────────────┐  │
│  │ 2m ago: Fill completed (Water, 500mL)   │  │
│  │ 5m ago: Product switched (Oil → Water) │  │
│  │ 12m ago: SPC alert resolved             │  │
│  └─────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────┬──────────────────────┐  │
│  │ Accuracy Trend   │ Equipment Health     │  │
│  │ [Line chart]     │ [Radial chart]       │  │
│  └──────────────────┴──────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### Components
1. **Key Metrics Cards**
   - Large number
   - Metric name
   - Trend indicator (↑↓→)
   - Percentage change
   - Color-coded

2. **System Status Panel**
   - Status items with icons
   - Color-coded (green/yellow/red)
   - Clickable to navigate

3. **Quick Actions**
   - Primary action buttons
   - Navigate to key pages

4. **Recent Activity Timeline**
   - Chronological list
   - Icons for activity type
   - Timestamps
   - Clickable items

5. **Charts** (2-column)
   - Accuracy trend (line chart)
   - Equipment health (radial/radar chart)


## Navigation & Header

### Sidebar Navigation
```
┌─────────────────────┐
│ 🔬 PINNs-UPC        │
│    Calibration      │
├─────────────────────┤
│ 📊 Dashboard        │
│ 📱 Scanner          │
│ ⚙️  Fill Monitor    │
│ 🔧 Equipment Health │
│ 📈 SPC Control      │
│ 🌐 Anomaly Database │
├─────────────────────┤
│ ⚙️  Settings        │
│ 📚 Help             │
│ 👤 Profile          │
└─────────────────────┘
```

### Header Bar
```
┌─────────────────────────────────────────────────┐
│ [☰] PINNs-UPC  |  [Product: Water]  |  Status  │
│                                      [🔔] [👤]  │
└─────────────────────────────────────────────────┘
```

**Elements**:
- Hamburger menu (mobile)
- Logo + app name
- Current product indicator
- System status badge
- Notifications bell (with count)
- User avatar


## UI Components Library

### Cards
- **Elevated Card**: White background, subtle shadow, rounded corners (8px)
- **Metric Card**: Large number, label, trend indicator, icon
- **Alert Card**: Colored left border, icon, message, action button
- **Product Card**: Image placeholder, name, properties, CTA

### Buttons
- **Primary**: Blue background, white text, hover effect
- **Secondary**: White background, blue border, blue text
- **Danger**: Red background, white text
- **Icon Button**: Circular, icon only, hover effect

### Form Elements
- **Input**: Border, focus state (blue ring), label above
- **Slider**: Blue track, circular thumb, value display
- **Dropdown**: Chevron icon, smooth animation
- **Checkbox**: Blue when checked, smooth transition

### Status Indicators
- **Badge**: Rounded pill, colored background
  - Success: Green
  - Warning: Yellow
  - Error: Red
  - Info: Blue
- **Progress Bar**: Colored fill, percentage label
- **Health Score**: Circular progress with percentage

### Charts
- **Line Chart**: Smooth curves, grid lines, hover tooltips
- **Control Chart**: Multiple horizontal lines (limits), data points
- **Radial Chart**: Circular, multiple axes, filled area

### Feedback
- **Toast Notifications**: Top-right, auto-dismiss, icon + message
- **Loading States**: Spinner or skeleton screens
- **Empty States**: Icon, message, CTA button


## Responsive Design

### Breakpoints
- **Mobile**: < 640px (single column, stacked)
- **Tablet**: 640px - 1024px (2 columns)
- **Desktop**: > 1024px (full layout)

### Mobile Adaptations
- Sidebar collapses to hamburger menu
- Cards stack vertically
- Charts resize/simplify
- Tables become scrollable
- Sliders become touch-friendly

### Tablet Adaptations
- 2-column grid for cards
- Sidebar remains visible
- Charts scale proportionally


## Interactions & Animations

### Micro-interactions
- **Button Hover**: Scale 1.02, shadow increase
- **Card Hover**: Lift effect (shadow increase)
- **Input Focus**: Blue ring, smooth transition
- **Loading**: Pulse animation on skeleton screens
- **Success**: Checkmark animation, green flash
- **Error**: Shake animation, red flash

### Transitions
- **Page Navigation**: Fade in/out (200ms)
- **Modal Open**: Scale up from center (300ms)
- **Dropdown**: Slide down (200ms)
- **Toast**: Slide in from right (300ms)

### Loading States
- **Initial Load**: Full-page spinner with logo
- **Data Fetch**: Skeleton screens matching content
- **Button Action**: Spinner inside button, disabled state


## Sample Data for Mockup

### Products
```json
[
  {
    "upc": "1234567890001",
    "name": "Purified Water",
    "viscosity": "0.001 Pa·s",
    "density": "1000 kg/m³",
    "surfaceTension": "0.072 N/m",
    "profile": {
      "valveTiming": "0.8s",
      "pressure": "35 PSI",
      "nozzleDiameter": "4.0mm"
    }
  },
  {
    "upc": "1234567890002",
    "name": "Vegetable Oil",
    "viscosity": "0.065 Pa·s",
    "density": "920 kg/m³",
    "surfaceTension": "0.032 N/m",
    "profile": {
      "valveTiming": "1.5s",
      "pressure": "50 PSI",
      "nozzleDiameter": "5.0mm"
    }
  },
  {
    "upc": "1234567890003",
    "name": "Honey",
    "viscosity": "6.0 Pa·s",
    "density": "1420 kg/m³",
    "surfaceTension": "0.056 N/m",
    "profile": {
      "valveTiming": "3.5s",
      "pressure": "75 PSI",
      "nozzleDiameter": "6.0mm"
    }
  }
]
```

### Fill History
```json
[
  {
    "time": "2m ago",
    "target": "500 mL",
    "actual": "498.5 mL",
    "error": "0.3%",
    "status": "success"
  },
  {
    "time": "5m ago",
    "target": "500 mL",
    "actual": "502.1 mL",
    "error": "0.42%",
    "status": "success"
  },
  {
    "time": "8m ago",
    "target": "500 mL",
    "actual": "489.2 mL",
    "error": "2.16%",
    "status": "warning"
  }
]
```

### Equipment Health
```json
{
  "nozzle": {
    "score": 92,
    "status": "warning",
    "trend": "down",
    "prediction": "15 days until failure"
  },
  "valve": {
    "score": 98,
    "status": "good",
    "trend": "stable",
    "prediction": null
  },
  "pump": {
    "score": 99,
    "status": "good",
    "trend": "up",
    "prediction": null
  },
  "sensor": {
    "score": 97,
    "status": "good",
    "trend": "stable",
    "prediction": null
  }
}
```

### Anomalies
```json
[
  {
    "type": "foam_overflow",
    "solution": "Reduce fill speed by 30% and lower temperature to <25°C",
    "effectiveness": 85,
    "upvotes": 42,
    "conditions": ["Carbonated", "Low viscosity", "Room temp"]
  },
  {
    "type": "clog",
    "solution": "Increase nozzle diameter to 5mm or warm product to 25°C",
    "effectiveness": 90,
    "upvotes": 38,
    "conditions": ["High viscosity", "Cold temp", "Small nozzle"]
  }
]
```


## Technical Requirements

### Framework
- **React** with TypeScript
- **Tailwind CSS** for styling
- **Shadcn/ui** components (or similar)
- **Lucide React** for icons
- **Recharts** or **Chart.js** for charts

### State Management
- React hooks (useState, useEffect)
- Context API for global state (current product, system status)

### Routing
- React Router for navigation
- Persistent state across routes

### Accessibility
- ARIA labels on all interactive elements
- Keyboard navigation support
- Focus indicators
- Screen reader friendly
- Color contrast WCAG AA compliant

### Performance
- Lazy loading for charts
- Debounced inputs
- Optimized re-renders
- Code splitting by route


## Key User Flows

### Flow 1: Quick Fill Operation
1. Land on Scanner page
2. Enter UPC or select from recent
3. Product loads with profile
4. Click "Start Fill" → Navigate to Fill Monitor
5. Adjust parameters if needed
6. Click "Predict Fill" → See AI prediction
7. Execute fill → Enter actual values
8. Click "Log Fill Result" → See vision verification
9. Success toast → Data logged

### Flow 2: Health Check
1. Navigate to Equipment Health
2. View component health scores
3. See active alerts (if any)
4. Review maintenance schedule
5. Click component → See detailed trend
6. Schedule maintenance (if needed)

### Flow 3: Quality Investigation
1. Navigate to SPC Control Chart
2. View control chart
3. See rule violations (if any)
4. Click violation → See details
5. Review process capability
6. Take corrective action

### Flow 4: Problem Solving
1. Navigate to Anomaly Database
2. Select issue type
3. Click "Search Solutions"
4. Review solutions sorted by effectiveness
5. Click solution → See full details
6. Upvote if helpful
7. Report new solution if needed


## Special Features

### Real-time Updates
- Live status indicators
- Auto-refresh for monitoring pages
- WebSocket simulation for demo

### Data Visualization
- Interactive charts with zoom/pan
- Hover tooltips with details
- Export chart as image
- Time range selector

### Smart Notifications
- Toast for actions (success/error)
- Badge count on notification bell
- Notification center dropdown
- Persistent alerts on relevant pages

### Search & Filter
- Quick search in anomaly database
- Filter by date range
- Sort tables by column
- Export data to CSV

### Help & Onboarding
- Tooltips on hover (info icons)
- First-time user tour (optional)
- Help modal with documentation
- Sample data for demo mode


## Design Inspiration

### Style References
- **Industrial Dashboard**: Clean, data-dense, professional
- **Modern SaaS**: Glassmorphism, subtle gradients, smooth animations
- **AI/ML Tools**: Confidence scores, prediction displays, model status
- **Manufacturing**: Equipment monitoring, real-time status, alerts

### Color Psychology
- **Blue**: Trust, precision, technology (primary)
- **Cyan**: Innovation, AI, future (secondary)
- **Green**: Success, healthy, operational
- **Yellow/Orange**: Warning, attention needed
- **Red**: Critical, error, immediate action

### Typography Hierarchy
- **H1**: 32px, bold (page titles)
- **H2**: 24px, semibold (section headers)
- **H3**: 20px, semibold (card titles)
- **Body**: 16px, regular (content)
- **Small**: 14px, regular (labels, captions)
- **Tiny**: 12px, regular (metadata)

### Spacing System
- **xs**: 4px
- **sm**: 8px
- **md**: 16px
- **lg**: 24px
- **xl**: 32px
- **2xl**: 48px


## Implementation Priority

### Phase 1: Core Pages (MVP)
1. **Scanner** - Product loading (highest priority)
2. **Fill Monitor** - Main operations
3. **Navigation** - Sidebar + header

### Phase 2: Monitoring
4. **Equipment Health** - Component monitoring
5. **SPC Control Chart** - Quality control

### Phase 3: Advanced
6. **Anomaly Database** - Solution sharing
7. **Dashboard** - Overview

### Phase 4: Polish
8. Animations and transitions
9. Responsive design refinements
10. Accessibility improvements


## Final Notes

### Brand Identity
- **Tagline**: "Intelligent Filling, Powered by Physics & AI"
- **Mission**: Eliminate filling errors through instant calibration and predictive monitoring
- **Target Users**: Manufacturing operators, quality engineers, maintenance teams

### Key Differentiators
1. **Instant Recognition**: UPC scan → immediate calibration
2. **Physics + AI**: Not just machine learning, but physics-informed
3. **Vision Verification**: Camera-based quality assurance
4. **Predictive**: Prevents problems before they occur
5. **Global Learning**: Crowd-sourced solutions

### Success Metrics to Display
- Fill accuracy (target: >99%)
- Equipment uptime (target: >98%)
- Time saved per product switch
- Anomalies prevented
- Community contributions

### Demo Mode Features
- Pre-populated with sample data
- Simulated real-time updates
- All features functional
- No backend required for demo

---

## Summary for v0

Create a modern, professional React + TypeScript web application for an AI-powered liquid filling calibration system. The UI should have:

1. **6 main pages**: Dashboard, Scanner, Fill Monitor, Equipment Health, SPC Control Chart, Anomaly Database
2. **Design**: Industrial tech aesthetic with blue/cyan colors, glassmorphism, smooth animations
3. **Components**: Cards, charts, forms, tables, alerts - all with Tailwind CSS + Shadcn/ui
4. **Features**: Real-time monitoring, interactive charts, smart notifications, responsive design
5. **Data**: Use provided sample JSON data for mockup
6. **Priority**: Start with Scanner and Fill Monitor pages (core functionality)

The application combines UPC product recognition, Physics-Informed Neural Networks, computer vision, predictive maintenance, statistical process control, and global anomaly sharing into one cohesive manufacturing solution.

Build it as a fully functional demo with all interactions working (no backend needed - use mock data and local state).
