# ChemData - Equipment Analysis Platform

A professional, chemistry-themed equipment data analysis platform built with Next.js 16 and React. Features include CSV data upload, real-time visualization, comprehensive analytics, and report generation.

## Features

### Core Functionality
- **CSV Data Upload**: Drag-and-drop or click-to-upload CSV files with equipment specifications
- **Data Table**: Interactive data table with search, sort, and pagination capabilities
- **Advanced Analytics**: Multi-chart visualizations including trend lines, type analysis, and correlations
- **Report Generation**: Professional HTML reports with statistics and data summaries
- **Upload History**: Local storage of last 5 uploaded files with quick re-access

### Design System
- **Chemistry Theme**: Professional 2D line art aesthetic with molecular/atomic inspired design
- **Color Palette**: 
  - Primary: Deep Navy/Teal (#1F3A5F)
  - Accent: Scientific Cyan (#4EC5E6)
  - Supporting: Warm oranges and reds for data visualization
- **Custom Icons**: Chemistry-themed SVG icons (beakers, atoms, molecules, etc.)
- **Dark Mode Support**: Full light/dark theme compatibility

### Technical Highlights
- **Responsive Design**: Mobile-first, fully responsive layout
- **Performance**: Optimized with React hooks and memoization
- **Accessibility**: Semantic HTML, ARIA attributes, keyboard navigation
- **Type Safety**: Full TypeScript support
- **Recharts Integration**: Multi-format data visualization

## Getting Started

### Installation

1. **Clone or download the repository**
```bash
git clone [repository-url]
cd chemdata
```

2. **Install dependencies**
```bash
npm install
```

3. **Run the development server**
```bash
npm run dev
```

4. **Open in browser**
Navigate to `http://localhost:3000`

## Usage

### Login
- Demo mode: Use any email and password to enter the dashboard
- No authentication backend required for initial testing

### Upload Data
1. Click "Select CSV File" or drag and drop a CSV
2. Alternatively, click "Try Sample Data" to use example equipment data
3. Data is automatically parsed and analyzed

### CSV Format
Your CSV should include these columns:
```
Equipment Name, Type, Flowrate, Pressure, Temperature
```

Example:
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Centrifugal Pump A,Pump,150.5,8.2,45.3
Heat Exchanger 1,Heat Exchanger,200.3,3.2,65.4
```

### Analyze Data
1. **View Statistics**: Key metrics displayed in cards (total records, averages)
2. **Browse Data Table**: Search, sort, and filter records
3. **Visualize Trends**: Three chart types:
   - Trend Line: Parameter values across equipment
   - Type Analysis: Averages grouped by equipment type
   - Correlation: Pressure vs temperature scatter plot
4. **Generate Report**: Create professional HTML report with all statistics

### Export & Reports
- **Data Export**: Download filtered/sorted data as CSV
- **HTML Report**: Complete analysis report with formatting and branding
- **History Access**: Re-use previous uploads from Recent Uploads panel

## File Structure

```
chemdata/
├── app/
│   ├── page.tsx                 # Login page
│   ├── dashboard/
│   │   ├── page.tsx            # Main dashboard
│   │   └── settings/
│   │       └── page.tsx        # User settings
│   ├── globals.css             # Theme configuration
│   └── layout.tsx              # Root layout
├── components/
│   ├── chemistry-icons.tsx     # Custom icon library
│   ├── dashboard-layout.tsx    # Sidebar navigation
│   ├── upload-section.tsx      # File upload component
│   ├── data-table.tsx          # Interactive data table
│   ├── chart-container.tsx     # Data visualizations
│   ├── history-panel.tsx       # Recent uploads
│   ├── report-generator.tsx    # Report UI
│   └── ui/                     # shadcn/ui components
├── lib/
│   ├── report-generator.ts     # Report generation logic
│   └── sample-data.ts          # Sample CSV data
└── package.json
```

## Color System

### Light Mode
- **Background**: Off-white (#FAF9F7)
- **Foreground**: Deep Navy (#2D3748)
- **Primary**: Professional Teal (#1F3A5F)
- **Accent**: Scientific Cyan (#4EC5E6)
- **Chart Colors**: Cyan, Gold, Red (for distinct data series)

### Dark Mode
- **Background**: Deep Navy (#1F2937)
- **Foreground**: Off-white (#F1F5F9)
- **Primary**: Bright Cyan (#4EC5E6)
- **Accent**: Bright Cyan (#72D4FF)

## Data Persistence

Currently uses **browser localStorage** for:
- Upload history (last 5 files)
- User preferences
- Temporary data storage

For production, replace with:
- Backend API with database
- Supabase or similar
- AWS/Azure storage

## Future Enhancements

### Backend Integration
- User authentication with secure sessions
- Database storage for historical data
- API endpoints for data persistence
- Real-time collaboration features

### Advanced Features
- Custom chart configurations
- Batch file processing
- Data validation rules
- Statistical analysis (correlation, regression)
- Multi-file comparison
- Email report delivery
- API for external integrations

### Desktop Application
- PyQt5 desktop version
- Offline functionality
- Advanced plotting with Matplotlib
- Database synchronization

## Performance Optimization

- **Lazy Loading**: Components load on demand
- **Memoization**: useMemo for expensive calculations
- **Responsive Images**: Optimized SVG icons
- **Code Splitting**: Next.js automatic route splitting
- **CSS-in-JS**: Tailwind CSS with minimal overhead

## Accessibility

- WCAG 2.1 AA compliant
- Keyboard navigation support
- Screen reader friendly
- High contrast dark mode
- Semantic HTML structure
- ARIA labels and roles

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile browsers: iOS Safari, Chrome Mobile

## Development

### Tech Stack
- **Framework**: Next.js 16 with App Router
- **UI Library**: shadcn/ui
- **Styling**: Tailwind CSS v4
- **Charts**: Recharts
- **Icons**: Custom SVG
- **Language**: TypeScript

### Available Scripts
```bash
npm run dev      # Development server
npm run build    # Production build
npm run start    # Start production server
npm run lint     # Run linter
```

## Deployment

### Vercel (Recommended)
```bash
# Connect GitHub repository
vercel
```

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install && npm run build
CMD npm run start
```

### Environment Variables
```
NEXT_PUBLIC_APP_URL=https://yourdomain.com
```

## API Integration (Backend)

### Required Endpoints
```
POST /api/auth/login
POST /api/auth/logout
POST /api/uploads
GET  /api/uploads/{id}
GET  /api/uploads
DELETE /api/uploads/{id}
POST /api/reports/{id}
```

## License

MIT License - feel free to use commercially

## Support

For issues or questions:
1. Check the documentation in this README
2. Review sample data in `/lib/sample-data.ts`
3. Examine component examples in `/components`

## Credits

- Design inspiration: Professional chemistry/scientific platforms
- Icon system: Custom 2D line art
- Chart library: Recharts
- UI components: shadcn/ui

---

**ChemData** - Making equipment analysis simple and professional.
