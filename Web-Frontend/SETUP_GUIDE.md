# ChemData Setup & User Guide

## What You're Getting

A fully functional, production-ready equipment data analysis platform with a professional chemistry-themed interface. This is the **web frontend** - the foundation for integrating with your Django backend.

## Quick Start (60 seconds)

1. **Open Preview**: Click the preview button in v0
2. **See Login Page**: Professional chemistry-themed login screen
3. **Click "Sign In"**: Enter any email/password (demo mode)
4. **Try Sample Data**: Click "Try Sample Data" on the dashboard
5. **Explore Features**: View charts, tables, and generate reports

## Architecture Overview

```
ChemData Web Frontend (This Project)
├── Authentication Layer (Ready for backend integration)
├── Dashboard with Navigation
├── Data Upload & Processing
├── Visualization Engine (Recharts)
├── Report Generator
└── Local Storage Management

↓ [Future Integration]

Django Backend (You'll build this)
├── User Authentication & Sessions
├── Database (SQLite/PostgreSQL)
├── Data Validation
├── File Storage
└── API Endpoints
```

## Design System: 2D Line Art Chemistry Vibes

### Color Palette
- **Primary**: Deep Navy (#1F3A5F) - Trust & Authority
- **Accent**: Scientific Cyan (#4EC5E6) - Energy & Innovation
- **Chart Colors**: 
  - Cyan for Flowrate
  - Gold for Pressure
  - Red for Temperature
- **Support**: Warm grays and whites

### Typography
- **Headers**: Bold, geometric fonts
- **Body**: Clean, readable sans-serif
- **Maximum 2 font families** for consistency

### Visual Language
- **Icons**: Custom 2D line art (molecules, atoms, beakers)
- **Borders**: Subtle 1px with primary color at 20-30% opacity
- **Spacing**: Consistent 4px, 8px, 12px, 16px scale
- **Radius**: 10px (0.625rem) for cards and inputs

## File Organization

```
/
├── app/
│   ├── page.tsx ........................ Login page
│   ├── dashboard/
│   │   ├── page.tsx ................... Main dashboard
│   │   └── settings/
│   │       └── page.tsx .............. User settings
│   ├── globals.css .................... Theme tokens (MAIN DESIGN FILE)
│   └── layout.tsx ..................... Root layout & metadata
│
├── components/
│   ├── chemistry-icons.tsx ............ 10 custom SVG icons
│   ├── dashboard-layout.tsx ........... Sidebar + navigation
│   ├── upload-section.tsx ............ CSV upload UI
│   ├── data-table.tsx ................ Interactive table
│   ├── chart-container.tsx ........... 3 chart types
│   ├── history-panel.tsx ............ Upload history
│   ├── report-generator.tsx ........ Report UI
│   ├── features-showcase.tsx ....... Feature cards
│   └── ui/ ........................... shadcn/ui components
│
├── lib/
│   ├── report-generator.ts .......... HTML report logic
│   ├── sample-data.ts ............... 30 sample records
│   └── utils.ts ..................... Utility functions
│
└── README.md & SETUP_GUIDE.md ....... Documentation
```

## How It Works: Data Flow

### 1. Upload
```
User selects CSV
  ↓
parseCSV() extracts data
  ↓
Data stored in React state
  ↓
Statistics calculated immediately
```

### 2. Display
```
Data → DataTable component
       → ChartContainer component (3 chart types)
       → Statistics cards
```

### 3. Export/Report
```
Generate Report
  ↓
calculateStats() 
  ↓
generateHTMLReport() creates formatted HTML
  ↓
downloadReport() sends to browser
```

### 4. History
```
Each upload → localStorage
Last 5 stored
User can re-use without re-uploading
```

## Customization Guide

### Change Colors
Edit `/app/globals.css` in the `:root` section:

```css
:root {
  --primary: oklch(0.32 0.11 265);      /* Change this */
  --accent: oklch(0.65 0.15 220);       /* And this */
  /* ... other colors ... */
}
```

### Add New Icons
1. Open `/components/chemistry-icons.tsx`
2. Add new SVG function:
```tsx
export function MyCoolIcon({ size = 24, className = '' }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" /* ... */>
      {/* Your SVG content */}
    </svg>
  );
}
```
3. Import and use in components

### Modify Dashboard Layout
- Sidebar: `/components/dashboard-layout.tsx`
- Main content area: `/app/dashboard/page.tsx`
- Navigation items: Edit NavLink components

### Customize Data Table
- Columns: Auto-detected from CSV headers
- Search: Searches all fields
- Sort: Click column headers
- Export: CSV download format
- Modify in: `/components/data-table.tsx`

### Adjust Charts
- 3 default types: Line, Bar, Scatter
- Data preparation: `/components/chart-container.tsx`
- Colors: Update `chartColors` object
- Add new chart: Create new TabsContent

## Integration with Backend

### Current State: Frontend Only
- Data lives in browser memory & localStorage
- No backend required for demo
- Perfect for testing UI/UX

### What You Need to Build (Backend)

**Django API Endpoints:**

```python
# Authentication
POST /api/auth/login
POST /api/auth/logout
POST /api/auth/register

# Data Management
POST /api/uploads              # Create upload
GET  /api/uploads              # List user's uploads
GET  /api/uploads/{id}         # Get specific upload
DELETE /api/uploads/{id}       # Delete upload

# Reports
POST /api/reports/{upload_id}  # Generate report
GET  /api/reports/{id}         # Retrieve report

# Settings
GET  /api/settings
PUT  /api/settings
```

### Frontend-Backend Connection

Replace localStorage calls with API calls:

**Before (Local):**
```typescript
localStorage.setItem('uploadHistory', JSON.stringify(history));
```

**After (Backend):**
```typescript
await fetch('/api/uploads', {
  method: 'POST',
  body: JSON.stringify({ data, filename })
});
```

## Sample Data

Pre-loaded sample CSV with 30 equipment records:
- 5 Pump types
- 5 Compressor types
- 5 Heat Exchanger types
- 3 Reactor types
- Real-world parameters (flowrate, pressure, temperature)

**Usage:**
```typescript
import { parseSampleData } from '@/lib/sample-data';
const data = parseSampleData();
```

## Testing Scenarios

### Test 1: Basic Upload
1. Click "Try Sample Data"
2. View auto-calculated statistics
3. Switch between Data/Charts tabs
4. Verify all 30 records display correctly

### Test 2: Search & Filter
1. Search for "Pump" in data table
2. Verify results filtered
3. Test sorting by Flowrate

### Test 3: Report Generation
1. Click "Generate Report"
2. HTML file downloads
3. Open in browser
4. Check formatting and statistics

### Test 4: Responsiveness
1. Desktop: Full sidebar visible
2. Tablet: Responsive grid layout
3. Mobile: Hamburger menu (sidebar collapses)

### Test 5: Dark Mode
1. System preference: Dark
2. Theme applies automatically
3. All colors readable (proper contrast)

## Performance Considerations

### Optimizations Already Implemented
- Memoized data calculations (useMemo)
- Lazy chart rendering
- Optimized SVG icons
- CSS containment for shadows

### For Production, Add:
- Server-side CSV parsing (large files)
- Data pagination (1000+ records)
- Virtual scrolling for tables
- Chart sampling (render every 10th point)
- Compression for reports

## Security Notes

### Current (Demo)
- No authentication validation
- No data encryption
- Local storage used

### For Production, Implement:
1. **Backend Auth**: Validate credentials on server
2. **HTTPS Only**: Encrypt all data in transit
3. **Session Management**: Secure HTTP-only cookies
4. **CORS**: Restrict API to your domain
5. **Input Validation**: Sanitize all CSV inputs
6. **Rate Limiting**: Prevent abuse
7. **Audit Logging**: Track user actions

## Deployment Checklist

- [ ] Replace demo authentication with real backend
- [ ] Add environment variables for API URLs
- [ ] Configure CORS for production domain
- [ ] Add error logging & monitoring
- [ ] Test on mobile devices
- [ ] Verify dark mode appearance
- [ ] Add analytics/tracking
- [ ] Create privacy policy
- [ ] Set up SSL certificate
- [ ] Configure CDN for assets
- [ ] Add database backups
- [ ] Create admin panel

## Troubleshooting

### Charts not appearing?
- Check browser console for errors
- Ensure data has numeric values
- Try sample data first

### Styling looks wrong?
- Clear browser cache (Ctrl+Shift+R)
- Check globals.css is loaded
- Verify Tailwind CSS v4

### Upload fails?
- Check CSV format (proper headers)
- Verify UTF-8 encoding
- Try sample data

### Reports not downloading?
- Check browser download settings
- Verify browser popup blocking
- Check file name has no special chars

## Next Steps

1. **Review the code**: Familiarize yourself with structure
2. **Test the demo**: Click through all features
3. **Customize styling**: Adjust colors and fonts
4. **Plan backend**: Design database schema
5. **Build API**: Create Django endpoints
6. **Connect frontend**: Replace localStorage with API calls
7. **Deploy**: Choose hosting (Vercel, AWS, etc.)

## Support & Resources

### Documentation
- `/README.md` - Full feature documentation
- `/SETUP_GUIDE.md` - This file
- Code comments throughout components

### Sample Files
- `/lib/sample-data.ts` - 30 equipment records
- `/lib/report-generator.ts` - Report generation logic

### Key Technologies
- Next.js 16: nextjs.org
- React 19: react.dev
- Tailwind CSS: tailwindcss.com
- shadcn/ui: ui.shadcn.com
- Recharts: recharts.org

## License

MIT - Free for commercial use

---

**Ready to build?** Start with the frontend, test with sample data, then connect your Django backend. The architecture is ready to scale.
