export interface ReportData {
  filename: string;
  timestamp: string;
  totalRecords: number;
  data: any[];
  stats: {
    flowrateMin: number;
    flowrateMax: number;
    flowrateAvg: number;
    pressureMin: number;
    pressureMax: number;
    pressureAvg: number;
    temperatureMin: number;
    temperatureMax: number;
    temperatureAvg: number;
  };
}

export function generateHTMLReport(report: ReportData): string {
  const css = `
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      body {
        font-family: 'Geist', sans-serif;
        color: #2d3748;
        background: white;
        padding: 40px;
      }
      .header {
        border-bottom: 3px solid #1f3a5f;
        padding-bottom: 24px;
        margin-bottom: 32px;
      }
      .logo {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
      }
      .logo-icon {
        width: 32px;
        height: 32px;
        background: rgba(31, 58, 95, 0.1);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #1f3a5f;
      }
      .company-name {
        font-size: 24px;
        font-weight: bold;
        color: #1f3a5f;
      }
      h1 { font-size: 32px; color: #1f3a5f; margin-bottom: 8px; }
      .metadata {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-bottom: 32px;
      }
      .metadata-item {
        padding: 12px;
        background: #f7fafc;
        border-radius: 8px;
        border-left: 3px solid #4ec5e6;
      }
      .metadata-label {
        font-size: 12px;
        color: #718096;
        font-weight: 500;
        text-transform: uppercase;
      }
      .metadata-value {
        font-size: 16px;
        font-weight: 600;
        color: #1f3a5f;
        margin-top: 4px;
      }
      .section {
        margin-bottom: 32px;
      }
      .section-title {
        font-size: 18px;
        font-weight: 600;
        color: #1f3a5f;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid #e2e8f0;
      }
      .stats-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 16px;
        margin-bottom: 24px;
      }
      .stat-card {
        padding: 16px;
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        text-align: center;
      }
      .stat-label {
        font-size: 12px;
        color: #718096;
        text-transform: uppercase;
        font-weight: 500;
      }
      .stat-value {
        font-size: 24px;
        font-weight: bold;
        color: #4ec5e6;
        margin-top: 8px;
      }
      table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 16px;
      }
      thead {
        background: #f7fafc;
      }
      th {
        padding: 12px;
        text-align: left;
        font-weight: 600;
        color: #1f3a5f;
        font-size: 12px;
        text-transform: uppercase;
        border-bottom: 2px solid #e2e8f0;
      }
      td {
        padding: 12px;
        border-bottom: 1px solid #e2e8f0;
      }
      tr:hover { background: #f7fafc; }
      .footer {
        margin-top: 48px;
        padding-top: 24px;
        border-top: 1px solid #e2e8f0;
        text-align: center;
        color: #718096;
        font-size: 12px;
      }
      @media print {
        body { padding: 20px; }
        .page-break { page-break-after: always; }
      }
    </style>
  `;

  const getStatRows = () => {
    if (report.data.length === 0) return '';
    const rows = report.data.slice(0, 20).map((row: any, idx: number) => `
      <tr>
        <td>${idx + 1}</td>
        <td>${row['equipment name'] || row['name'] || '-'}</td>
        <td>${row.type || '-'}</td>
        <td>${parseFloat(row.flowrate || 0).toFixed(2)}</td>
        <td>${parseFloat(row.pressure || 0).toFixed(2)}</td>
        <td>${parseFloat(row.temperature || 0).toFixed(2)}</td>
      </tr>
    `).join('');
    return rows;
  };

  return `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>ChemData Analysis Report</title>
      ${css}
    </head>
    <body>
      <div class="header">
        <div class="logo">
          <div class="logo-icon">⚛️</div>
          <div class="company-name">ChemData</div>
        </div>
        <h1>Equipment Data Analysis Report</h1>
      </div>

      <div class="metadata">
        <div class="metadata-item">
          <div class="metadata-label">File Name</div>
          <div class="metadata-value">${report.filename}</div>
        </div>
        <div class="metadata-item">
          <div class="metadata-label">Total Records</div>
          <div class="metadata-value">${report.totalRecords}</div>
        </div>
        <div class="metadata-item">
          <div class="metadata-label">Report Date</div>
          <div class="metadata-value">${report.timestamp}</div>
        </div>
        <div class="metadata-item">
          <div class="metadata-label">Generated By</div>
          <div class="metadata-value">ChemData Platform</div>
        </div>
      </div>

      <div class="section">
        <h2 class="section-title">Key Statistics</h2>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-label">Flowrate (L/min)</div>
            <div style="font-size: 12px; color: #718096; margin-top: 12px;">
              <div>Min: ${report.stats.flowrateMin.toFixed(2)}</div>
              <div>Max: ${report.stats.flowrateMax.toFixed(2)}</div>
              <div style="color: #4ec5e6; font-weight: 600; margin-top: 8px;">Avg: ${report.stats.flowrateAvg.toFixed(2)}</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Pressure (bar)</div>
            <div style="font-size: 12px; color: #718096; margin-top: 12px;">
              <div>Min: ${report.stats.pressureMin.toFixed(2)}</div>
              <div>Max: ${report.stats.pressureMax.toFixed(2)}</div>
              <div style="color: #f59e0b; font-weight: 600; margin-top: 8px;">Avg: ${report.stats.pressureAvg.toFixed(2)}</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-label">Temperature (°C)</div>
            <div style="font-size: 12px; color: #718096; margin-top: 12px;">
              <div>Min: ${report.stats.temperatureMin.toFixed(2)}</div>
              <div>Max: ${report.stats.temperatureMax.toFixed(2)}</div>
              <div style="color: #ef4444; font-weight: 600; margin-top: 8px;">Avg: ${report.stats.temperatureAvg.toFixed(2)}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="section">
        <h2 class="section-title">Data Sample (First 20 Records)</h2>
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Equipment Name</th>
              <th>Type</th>
              <th>Flowrate (L/min)</th>
              <th>Pressure (bar)</th>
              <th>Temperature (°C)</th>
            </tr>
          </thead>
          <tbody>
            ${getStatRows()}
          </tbody>
        </table>
      </div>

      <div class="footer">
        <p>This report was generated by ChemData Equipment Analysis Platform</p>
        <p>© ${new Date().getFullYear()} ChemData. All rights reserved.</p>
      </div>
    </body>
    </html>
  `;
}

export function downloadReport(reportHtml: string, filename: string) {
  const blob = new Blob([reportHtml], { type: 'text/html' });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${filename.replace('.csv', '')}_report.html`;
  link.click();
  window.URL.revokeObjectURL(url);
}

export function calculateStats(data: any[]) {
  const flowrates = data.map((d) => parseFloat(d.flowrate) || 0).filter((v) => !isNaN(v));
  const pressures = data.map((d) => parseFloat(d.pressure) || 0).filter((v) => !isNaN(v));
  const temps = data.map((d) => parseFloat(d.temperature) || 0).filter((v) => !isNaN(v));

  return {
    flowrateMin: Math.min(...flowrates),
    flowrateMax: Math.max(...flowrates),
    flowrateAvg: flowrates.length > 0 ? flowrates.reduce((a, b) => a + b) / flowrates.length : 0,
    pressureMin: Math.min(...pressures),
    pressureMax: Math.max(...pressures),
    pressureAvg: pressures.length > 0 ? pressures.reduce((a, b) => a + b) / pressures.length : 0,
    temperatureMin: Math.min(...temps),
    temperatureMax: Math.max(...temps),
    temperatureAvg: temps.length > 0 ? temps.reduce((a, b) => a + b) / temps.length : 0,
  };
}
