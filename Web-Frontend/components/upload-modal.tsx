'use client';

import { UploadSection } from '@/components/upload-section';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { XIcon } from '@/components/chemistry-icons';

interface UploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onFileUpload: (data: any[], filename: string, datasetId?: number, statistics?: any) => void;
}

export function UploadModal({ isOpen, onClose, onFileUpload }: UploadModalProps) {
  if (!isOpen) return null;

  const handleFileUpload = (data: any[], filename: string, datasetId?: number, statistics?: any) => {
    onFileUpload(data, filename, datasetId, statistics);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <Card className="w-full max-w-2xl border-2 border-primary/40 shadow-2xl bg-card">
        <div className="flex items-center justify-between p-6 border-b-2 border-primary/30">
          <div>
            <h2 className="text-2xl font-black text-foreground uppercase tracking-wider">Upload Equipment Data</h2>
            <p className="text-sm text-muted-foreground mt-1">Select or drag your CSV file</p>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={onClose}
            className="font-black hover:bg-destructive/10"
          >
            <XIcon size={24} />
          </Button>
        </div>

        <div className="p-8">
          <UploadSection onFileUpload={handleFileUpload} />
        </div>
      </Card>
    </div>
  );
}
