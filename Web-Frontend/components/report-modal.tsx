'use client';

import { useRef } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { XIcon, PrintIcon } from '@/components/chemistry-icons';
import { generateHTMLReport } from '@/lib/report-generator';

interface ReportModalProps {
  isOpen: boolean;
  onClose: () => void;
  data: any[];
  filename: string;
}

export function ReportModal({ isOpen, onClose, data, filename }: ReportModalProps) {
  const reportRef = useRef<HTMLDivElement>(null);

  if (!isOpen) return null;

  const handlePrint = () => {
    if (reportRef.current) {
      const printWindow = window.open('', '', 'height=800,width=900');
      if (printWindow) {
        printWindow.document.write('<html><head><title>Equipment Report</title>');
        printWindow.document.write('<style>');
        printWindow.document.write(`
          body { font-family: system-ui, -apple-system, sans-serif; padding: 30px; background: #fff; color: #1a1a1a; }
          h1 { color: #FF6B1A; font-size: 32px; font-weight: 900; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }
          h2 { color: #333; font-size: 20px; font-weight: 800; margin-top: 30px; margin-bottom: 15px; padding-bottom: 8px; border-bottom: 3px solid #FF6B1A; text-transform: uppercase; }
          table { width: 100%; border-collapse: collapse; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
          th, td { border: 1px solid #e5e7eb; padding: 14px; text-align: left; }
          th { background: linear-gradient(135deg, #FF6B1A 0%, #D94452 100%); color: white; font-weight: 800; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; }
          tr:nth-child(even) { background-color: #fef3f0; }
          tr:hover { background-color: #fce8e0; }
          .stat-box { display: inline-block; margin: 10px 15px 10px 0; padding: 18px 24px; background: linear-gradient(135deg, #fff5f0 0%, #ffe8e0 100%); border: 2px solid #FF6B1A; border-radius: 12px; box-shadow: 0 2px 6px rgba(255,107,26,0.15); }
          .stat-label { font-size: 11px; color: #666; margin-bottom: 6px; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; }
          .stat-value { font-size: 26px; font-weight: 900; background: linear-gradient(135deg, #FF6B1A 0%, #D94452 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
          .report-header { margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #e5e7eb; }
          .timestamp { color: #888; font-size: 13px; font-weight: 500; }
        `);        
        printWindow.document.write('</style></head><body>');
        printWindow.document.write(reportRef.current.innerHTML);
        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.print();
      }
    }
  };

  const stats = {
    totalRecords: data.length,
    avgFlowrate: data.length > 0 ? data.reduce((sum: number, d: any) => sum + parseFloat(d.flowrate || 0), 0) / data.length : 0,
    avgPressure: data.length > 0 ? data.reduce((sum: number, d: any) => sum + parseFloat(d.pressure || 0), 0) / data.length : 0,
    avgTemperature: data.length > 0 ? data.reduce((sum: number, d: any) => sum + parseFloat(d.temperature || 0), 0) / data.length : 0,
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50 overflow-y-auto">
      <Card className="w-full max-w-4xl border-2 border-primary/40 shadow-2xl bg-card my-8">
        <div className="flex items-center justify-between p-6 border-b-2 border-primary/30 sticky top-0 bg-card">
          <div>
            <h2 className="text-2xl font-black text-foreground uppercase tracking-wider">Equipment Analysis Report</h2>
            <p className="text-sm text-muted-foreground mt-1">File: {filename}</p>
          </div>
          <div className="flex gap-2">
            <Button
              onClick={handlePrint}
              className="bg-primary hover:bg-primary/90 text-primary-foreground font-bold gap-2"
            >
              <PrintIcon size={18} />
              <span>Print</span>
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={onClose}
              className="font-black hover:bg-destructive/10"
            >
              <XIcon size={24} />
            </Button>
          </div>
        </div>

        <div ref={reportRef} className="p-8 space-y-8">
          <div className="report-header">
            <h1 className="text-4xl font-black uppercase tracking-wider mb-2 bg-gradient-to-r from-primary via-accent to-secondary bg-clip-text text-transparent">ChemData Analysis Report</h1>
            <p className="text-muted-foreground text-sm timestamp">Generated on {new Date().toLocaleString()}</p>
          </div>

          <div>
            <h2 className="text-xl font-black text-foreground uppercase tracking-wider mb-4 pb-2 border-b-3 border-primary">Dataset Overview</h2>
            <div className="space-y-3 mb-6">
              <p className="text-foreground">
                <span className="font-black text-primary">File Name:</span> <span className="font-semibold">{filename}</span>
              </p>
              <p className="text-foreground">
                <span className="font-black text-primary">Total Records:</span> <span className="font-semibold">{stats.totalRecords}</span>
              </p>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-primary/10 border-2 border-primary/30 rounded-lg p-4">
                <p className="text-xs font-black text-primary uppercase">Total Records</p>
                <p className="text-2xl font-black text-foreground">{stats.totalRecords}</p>
              </div>
              <div className="bg-accent/10 border-2 border-accent/30 rounded-lg p-4">
                <p className="text-xs font-black text-accent uppercase">Avg Flowrate</p>
                <p className="text-2xl font-black text-foreground">{stats.avgFlowrate.toFixed(2)}</p>
                <p className="text-xs text-muted-foreground">L/min</p>
              </div>
              <div className="bg-secondary/10 border-2 border-secondary/30 rounded-lg p-4">
                <p className="text-xs font-black text-secondary uppercase">Avg Pressure</p>
                <p className="text-2xl font-black text-foreground">{stats.avgPressure.toFixed(2)}</p>
                <p className="text-xs text-muted-foreground">bar</p>
              </div>
              <div className="bg-primary/10 border-2 border-primary/30 rounded-lg p-4">
                <p className="text-xs font-black text-primary uppercase">Avg Temp</p>
                <p className="text-2xl font-black text-foreground">{stats.avgTemperature.toFixed(2)}</p>
                <p className="text-xs text-muted-foreground">°C</p>
              </div>
            </div>
          </div>

          <div>
            <h2 className="text-xl font-black text-foreground uppercase tracking-wider mb-4 pb-2 border-b-3 border-primary">Data Sample</h2>
            <div className="overflow-x-auto rounded-lg border-2 border-primary/20">
              <table className="w-full text-sm">
                <thead>
                  <tr className="gradient-primary text-white">
                    <th className="px-4 py-3 text-left font-black uppercase tracking-wide text-xs">Equipment Name</th>
                    <th className="px-4 py-3 text-left font-black uppercase tracking-wide text-xs">Type</th>
                    <th className="px-4 py-3 text-left font-black uppercase tracking-wide text-xs">Flowrate</th>
                    <th className="px-4 py-3 text-left font-black uppercase tracking-wide text-xs">Pressure</th>
                    <th className="px-4 py-3 text-left font-black uppercase tracking-wide text-xs">Temperature</th>
                  </tr>
                </thead>
                <tbody>
                  {data.slice(0, 10).map((row: any, idx: number) => (
                    <tr key={idx} className="border-b border-primary/10 hover:bg-primary/5">
                      <td className="px-4 py-2">{row.equipmentName}</td>
                      <td className="px-4 py-2">{row.type}</td>
                      <td className="px-4 py-2 font-semibold">{parseFloat(row.flowrate || 0).toFixed(2)} L/min</td>
                      <td className="px-4 py-2 font-semibold">{parseFloat(row.pressure || 0).toFixed(2)} bar</td>
                      <td className="px-4 py-2 font-semibold">{parseFloat(row.temperature || 0).toFixed(2)} °C</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {data.length > 10 && (
              <p className="text-xs text-muted-foreground mt-2">
                Showing 10 of {data.length} records. Full dataset available in analysis hub.
              </p>
            )}
          </div>
        </div>
      </Card>
    </div>
  );
}
