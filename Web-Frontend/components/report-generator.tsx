'use client';

import { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { FileIcon } from '@/components/chemistry-icons';
import {
  generateHTMLReport,
  downloadReport,
  calculateStats,
  type ReportData,
} from '@/lib/report-generator';

interface ReportGeneratorProps {
  data: any[];
  filename: string;
}

export function ReportGenerator({ data, filename }: ReportGeneratorProps) {
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerateReport = async () => {
    if (data.length === 0) {
      alert('No data to generate report');
      return;
    }

    setIsGenerating(true);
    try {
      const stats = calculateStats(data);
      const reportData: ReportData = {
        filename,
        timestamp: new Date().toLocaleString(),
        totalRecords: data.length,
        data,
        stats,
      };

      const html = generateHTMLReport(reportData);
      downloadReport(html, filename);
    } catch (error) {
      alert('Error generating report');
      console.error(error);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <Card className="p-6 border-primary/20">
      <div className="flex items-start justify-between">
        <div className="flex items-start gap-4">
          <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center flex-shrink-0">
            <FileIcon size={20} className="text-primary" />
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-2">Generate Report</h3>
            <p className="text-sm text-muted-foreground">
              Create a comprehensive HTML report with statistics and data analysis. Perfect for presentations and documentation.
            </p>
          </div>
        </div>

        <Button
          onClick={handleGenerateReport}
          disabled={isGenerating || data.length === 0}
          className="bg-primary hover:bg-primary/90 flex-shrink-0 ml-4"
        >
          {isGenerating ? 'Generating...' : 'Generate Report'}
        </Button>
      </div>

      <div className="mt-6 pt-6 border-t border-primary/10 space-y-3">
        <p className="text-sm font-medium text-foreground">Report Includes:</p>
        <ul className="text-sm text-muted-foreground space-y-2">
          <li className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-accent rounded-full flex-shrink-0" />
            Summary statistics (min, max, average)
          </li>
          <li className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-accent rounded-full flex-shrink-0" />
            Data table with first 20 records
          </li>
          <li className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-accent rounded-full flex-shrink-0" />
            Professional formatting and branding
          </li>
          <li className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-accent rounded-full flex-shrink-0" />
            Print-ready HTML document
          </li>
        </ul>
      </div>
    </Card>
  );
}
