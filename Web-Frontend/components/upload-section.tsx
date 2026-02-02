'use client';

import React from "react"

import { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { UploadIcon } from '@/components/chemistry-icons';
import { parseSampleData, downloadSampleCSV } from '@/lib/sample-data';
import { uploadCSV } from '@/lib/api';

interface UploadSectionProps {
  onFileUpload: (data: any[], filename: string, datasetId?: number, statistics?: any) => void;
}

export function UploadSection({ onFileUpload }: UploadSectionProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = async (file: File) => {
    if (!file.name.endsWith('.csv')) {
      setError('Please upload a CSV file');
      return;
    }

    setIsLoading(true);
    setError('');
    
    try {
      const result = await uploadCSV(file);
      
      if (result.success && result.data) {
        // Parse statistics to create displayable data
        const displayData = parseStatisticsToData(result.data.statistics);
        onFileUpload(
          displayData, 
          result.data.file_name,
          result.data.dataset_id,
          result.data.statistics
        );
      } else {
        setError(result.error || 'Failed to upload CSV');
      }
    } catch (error) {
      console.error('Upload error:', error);
      setError('Error uploading file. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const parseStatisticsToData = (statistics: any): any[] => {
    if (!statistics || !statistics.by_type) return [];
    
    const data: any[] = [];
    
    // Convert backend statistics to displayable rows
    Object.entries(statistics.by_type).forEach(([type, stats]: [string, any]) => {
      // Create representative rows for each equipment type
      data.push({
        equipment_name: `${type} (Average)`,
        type: type,
        flowrate: stats.flowrate.avg,
        pressure: stats.pressure.avg,
        temperature: stats.temperature.avg,
      });
    });
    
    return data;
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFile(files[0]);
    }
  };

  return (
    <div className="space-y-4">
      {error && (
        <div className="p-4 bg-destructive/10 border-2 border-destructive/50 rounded-lg">
          <p className="text-destructive text-sm font-bold">{error}</p>
        </div>
      )}
      
      <Card
        className={`p-10 border-3 border-dashed transition-all shadow-lg ${
          isDragging
            ? 'border-accent bg-gradient-to-br from-accent/15 to-primary/10 scale-105 shadow-xl'
            : 'border-primary/40 hover:border-primary/70 bg-gradient-to-br from-primary/5 to-accent/5'
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
      <div className="flex flex-col items-center justify-center text-center">
        <div className="w-16 h-16 bg-gradient-to-br from-primary/20 to-accent/20 rounded-2xl flex items-center justify-center mb-6 shadow-lg">
          <UploadIcon size={32} className="text-primary" />
        </div>
        <h3 className="text-2xl font-black mb-3 text-foreground uppercase tracking-wider">Upload Equipment Data</h3>
        <p className="text-sm text-muted-foreground mb-8 max-w-md font-semibold">
          Drag and drop your CSV file here, or click to browse. 
          <br />
          <span className="text-accent font-bold">Columns: Equipment Name, Type, Flowrate, Pressure, Temperature</span>
        </p>

        <div className="flex gap-4 flex-wrap justify-center">
          <Button
            onClick={() => fileInputRef.current?.click()}
            disabled={isLoading}
            className="bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary/70 text-primary-foreground font-bold shadow-lg px-8 py-6 text-base"
          >
            {isLoading ? '⏳ Processing...' : '📤 Select CSV File'}
          </Button>
          <Button
            onClick={() => {
              const sampleData = parseSampleData();
              onFileUpload(sampleData, 'sample_equipment_data.csv');
            }}
            variant="outline"
            className="border-2 border-accent/60 hover:bg-accent/10 text-foreground font-bold px-8 py-6 text-base"
          >
            ⭐ Try Sample Data
          </Button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) handleFile(file);
            }}
            className="hidden"
          />
        </div>

        <div className="mt-8 p-4 bg-background/60 border-2 border-primary/20 rounded-lg max-w-md">
          <p className="text-xs font-mono text-muted-foreground">
            <span className="text-accent font-black">Example CSV Format:</span>
            <br />
            equipment_name, type, flowrate, pressure, temperature
          </p>
        </div>
      </div>
    </Card>
    </div>
  );
}
