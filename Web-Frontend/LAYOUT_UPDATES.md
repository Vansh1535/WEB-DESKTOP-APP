# New Dashboard Layout Structure

## Overview
The dashboard has been completely restructured for improved UX and focus on data analysis features. The new layout follows a modern navbar + sidebar pattern.

---

## Layout Components

### 1. Top Navbar (`/components/top-navbar.tsx`)
**Fixed at top of screen (height: 64px)**
- **Left**: Hamburger menu icon to toggle sidebar
- **Center**: Empty space (can be used for search or other features)
- **Right**: 
  - User info pill showing logged-in user (avatar + name + status)
  - Logout button

**Styling**: Gradient background, 2px borders, vibrant theme colors

---

### 2. Sidebar - Analysis Hub (`/components/dashboard-layout.tsx`)
**Fixed on left side, toggles between 64px (collapsed) and 256px (expanded)**

#### Structure:
- **Header Section**
  - Title: "Analysis Hub"
  - Subtitle: "Data Tools" (when expanded)
  - Clean brand icon (when collapsed)

- **Main Actions**
  - **Upload File Button** 
    - Primary gradient button
    - Triggers `UploadModal` when clicked
    - Full width when expanded
    
- **Recent Uploads Section** (when sidebar expanded)
  - Shows last 3 uploaded files
  - Displays filename and record count
  - Loaded from localStorage
  - Component: `SidebarRecentUploads`

- **Footer**
  - Collapse/Expand indicator text

---

### 3. Main Content Area
**Takes remaining space after sidebar**
- Responsive padding
- Max-width container for organization
- Full height minus navbar

---

## Dashboard Page Flow (`/app/dashboard/page.tsx`)

### Empty State
When no data is uploaded:
- Large empty state card with icon
- "No Data Yet" heading
- Call-to-action button to upload

### Analysis Hub (Active State)
When data is loaded:

#### 1. **File Header Section**
```
┌─────────────────────────────────────────────────┐
│ Current File                                    │
│ sample_equipment_data.csv          [New Upload] │
│                                  [Generate Report]
└─────────────────────────────────────────────────┘
```
- Displays current filename prominently
- **New Upload** button - opens upload modal
- **Generate Report** button - opens report modal

#### 2. **Statistics Cards Grid** (4 columns)
```
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│  Total │ │  Avg   │ │  Avg   │ │  Avg   │
│Records │ │Flowrate│ │Pressure│ │  Temp  │
│  ####  │ │ ####   │ │ ####   │ │ ####   │
└────────┘ └────────┘ └────────┘ └────────┘
```
- Responsive: 1 col on mobile, 2 on tablet, 4 on desktop
- Hover effects with elevation and color changes
- First card (Total Records) highlighted with accent color

#### 3. **Analysis Hub Section** (Primary Focus)
Contains tabbed interface:

**Tabs:**
- **Charts Tab** (default)
  - ChartContainer component
  - Multiple chart visualizations
  - Dataset summary statistics
  
- **Table Tab**
  - DataTable component
  - Search, sort, pagination
  - All equipment data

---

## Modal Components

### 1. Upload Modal (`/components/upload-modal.tsx`)
- Full-screen overlay with centered card
- Header with close button
- Contains UploadSection component
- Auto-closes on successful upload

### 2. Report Modal (`/components/report-modal.tsx`)
- Full-screen overlay with scrollable content
- Sticky header with:
  - Report title
  - Filename display
  - **Print button** - Triggers browser print dialog
  - Close button
- Report content:
  - Title and timestamp
  - File overview
  - Dataset statistics (4-card grid)
  - Data sample table (first 10 rows)
- Print-friendly styling

---

## Component Hierarchy

```
DashboardPage
├── UploadModal
│   └── UploadSection
├── ReportModal
│   └── Print functionality
└── DashboardLayout
    ├── TopNavbar
    │   ├── MenuIcon (toggle)
    │   ├── User Pill
    │   └── Logout Button
    ├── Sidebar
    │   ├── Header ("Analysis Hub")
    │   ├── Upload Button (triggers modal)
    │   ├── SidebarRecentUploads
    │   └── Footer
    └── Main Content
        ├── File Header + Actions
        ├── Stats Cards (4x)
        ├── Analysis Hub Container
        │   ├── Tabs
        │   ├── Charts Tab
        │   │   └── ChartContainer
        │   └── Table Tab
        │       └── DataTable
        └── (Report section removed - now modal)
```

---

## New Features

### 1. Top Navbar with User Info
- Professional user pill showing logged-in identity
- Quick logout access
- Mobile-responsive (hides user name on small screens)

### 2. Modal-Based Workflows
- **Upload Modal**: Cleaner, focused upload experience
- **Report Modal**: Professional report view with print capability
- Modals overlay entire screen for focus

### 3. Enhanced Sidebar
- "Analysis Hub" branding
- Upload button as primary action
- Recent uploads preview
- Collapsible for more screen space

### 4. Improved Visual Hierarchy
- Filename prominently displayed at top of analysis
- Statistics cards immediately visible
- Analysis section as clear main focus
- Large empty state when no data

### 5. Print Functionality
- Print button in report modal
- Print-friendly styles applied
- Includes all report content
- Browser native print dialog

---

## Responsive Design

### Mobile (< 768px)
- Sidebar collapses by default to icon-only (64px)
- Top navbar shows hamburger menu
- User info pill hidden, logout button icon-only
- Stats cards stack 1 column
- Modals full screen with padding

### Tablet (768px - 1024px)
- Sidebar expandable via hamburger
- Stats cards 2 columns
- Sidebar can expand to full side

### Desktop (> 1024px)
- Sidebar expanded by default
- Stats cards 4 columns
- Full side navigation
- Optimal use of screen space

---

## Color & Styling
- Vibrant comic-style 2D line art theme
- Primary blue for main actions and borders
- Accent yellow/lime for highlights and secondary actions
- Gradient backgrounds for depth
- 2-3px borders for bold comic style
- Smooth transitions and hover effects

---

## Data Flow
1. User lands on dashboard (empty state)
2. Clicks "Upload File" button (in sidebar or empty state)
3. UploadModal opens with UploadSection
4. File uploaded and parsed
5. Statistics calculated
6. Main analysis hub activates
7. User views charts/tables in tabs
8. Can generate report via button
9. ReportModal opens with print option
10. User can print or close modal
11. Return to analysis hub
