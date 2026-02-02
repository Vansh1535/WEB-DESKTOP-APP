'use client';

import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { HistoryIcon, FileIcon } from '@/components/chemistry-icons';

interface HistoryItem {
  id: string;
  filename: string;
  timestamp: string;
  recordCount: number;
}

interface HistoryPanelProps {
  filename: string;
  data: any[];
}

export function HistoryPanel({ filename, data }: HistoryPanelProps) {
  const [history, setHistory] = useState<HistoryItem[]>([]);

  useEffect(() => {
    // Load history from localStorage on mount
    const storedHistory = localStorage.getItem('uploadHistory');
    if (storedHistory) {
      setHistory(JSON.parse(storedHistory));
    }

    // Add current upload to history (limited to last 5)
    if (filename && data.length > 0) {
      const newItem: HistoryItem = {
        id: Date.now().toString(),
        filename,
        timestamp: new Date().toLocaleString(),
        recordCount: data.length,
      };

      const updatedHistory = [newItem, ...history].slice(0, 5);
      setHistory(updatedHistory);
      localStorage.setItem('uploadHistory', JSON.stringify(updatedHistory));
    }
  }, [filename, data.length]);

  const handleClearHistory = () => {
    if (confirm('Are you sure you want to clear all history?')) {
      setHistory([]);
      localStorage.removeItem('uploadHistory');
    }
  };

  const handleDownload = (item: HistoryItem) => {
    // This would typically fetch and download the historical data
    const data = localStorage.getItem(`history_${item.id}`);
    if (data) {
      const blob = new Blob([data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = item.filename;
      a.click();
    }
  };

  return (
    <Card className="border-primary/20 p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center">
            <HistoryIcon size={18} className="text-primary" />
          </div>
          <h3 className="text-lg font-semibold">Recent Uploads</h3>
        </div>
        {history.length > 0 && (
          <Button
            variant="ghost"
            size="sm"
            onClick={handleClearHistory}
            className="text-destructive hover:bg-destructive/10"
          >
            Clear
          </Button>
        )}
      </div>

      {history.length > 0 ? (
        <div className="space-y-3">
          {history.map((item) => (
            <div
              key={item.id}
              className="flex items-start justify-between p-3 rounded-lg border border-primary/10 hover:border-primary/30 hover:bg-primary/5 transition-colors"
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <FileIcon size={16} className="text-primary flex-shrink-0" />
                  <p className="font-medium text-sm truncate">{item.filename}</p>
                </div>
                <p className="text-xs text-muted-foreground">
                  {item.recordCount} types • {item.timestamp}
                </p>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => handleDownload(item)}
                className="ml-2 text-primary hover:bg-primary/10 flex-shrink-0"
              >
                Re-use
              </Button>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-8">
          <p className="text-muted-foreground">No upload history yet</p>
          <p className="text-xs text-muted-foreground mt-2">Your recent uploads will appear here</p>
        </div>
      )}

      <div className="mt-6 p-4 bg-primary/5 rounded-lg border border-primary/10">
        <p className="text-xs text-muted-foreground">
          <span className="font-semibold text-foreground">Note:</span> History is stored locally in your browser. Recent uploads are limited to the last 5 files.
        </p>
      </div>
    </Card>
  );
}
