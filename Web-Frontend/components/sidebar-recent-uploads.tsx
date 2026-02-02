'use client';

import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { HistoryIcon, FileIcon } from '@/components/chemistry-icons';
import { listDatasets, type Dataset } from '@/lib/api';

interface SidebarRecentUploadsProps {
  onDatasetClick?: (datasetId: number, datasetName: string) => void;
  currentDatasetId?: number | null;
}

export function SidebarRecentUploads({ onDatasetClick, currentDatasetId }: SidebarRecentUploadsProps) {
  const [uploads, setUploads] = useState<Dataset[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadRecentUploads();
  }, [currentDatasetId]);

  const loadRecentUploads = async () => {
    setIsLoading(true);
    try {
      const result = await listDatasets();
      if (result.success) {
        // Get the most recent 5 completed datasets
        const recentUploads = result.data.datasets
          .filter((d: Dataset) => d.status === 'completed')
          .slice(0, 5);
        setUploads(recentUploads);
      }
    } catch (error) {
      console.error('Error loading recent uploads:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleDatasetClick = (dataset: Dataset) => {
    if (onDatasetClick) {
      onDatasetClick(dataset.id, dataset.file_name);
    }
  };

  if (isLoading) {
    return (
      <div className="text-sm text-muted-foreground text-center py-4 font-semibold">
        Loading...
      </div>
    );
  }

  // Find current dataset by ID, or use most recent if none specified
  let currentDataset = uploads.find(u => u.id === currentDatasetId) || (uploads.length > 0 ? uploads[0] : null);
  // Get other datasets excluding the current one
  const olderDatasets = uploads.filter(u => u.id !== currentDataset?.id).slice(0, 4);

  return (
    <div className="space-y-4">
      {uploads.length > 0 ? (
        <>
          {/* Current Dataset */}
          {currentDataset && (
            <div>
              <h4 className="text-xs font-black text-primary uppercase tracking-wider mb-2 flex items-center gap-2">
                <span className="w-2 h-2 bg-primary rounded-full animate-pulse"></span>
                Current Dataset
              </h4>
              <button
                onClick={() => handleDatasetClick(currentDataset)}
                className="w-full p-3 rounded-xl bg-gradient-to-br from-primary/20 to-accent/10 border-2 border-primary/50 hover:border-primary hover:from-primary/30 hover:to-accent/15 transition-all cursor-pointer shadow-lg hover:shadow-xl text-left"
              >
                <div className="flex items-start gap-2 mb-2">
                  <FileIcon size={16} className="text-primary flex-shrink-0 mt-0.5" />
                  <p className="text-sm font-bold text-foreground truncate flex-1">{currentDataset.file_name}</p>
                </div>
                <p className="text-xs text-muted-foreground ml-6 font-semibold">
                  {formatDate(currentDataset.uploaded_at)}
                </p>
              </button>
            </div>
          )}

          {/* Older Datasets */}
          {olderDatasets.length > 0 && (
            <div>
              <h4 className="text-xs font-black text-muted-foreground uppercase tracking-wider mb-2">
                Previous Datasets
              </h4>
              <div className="space-y-2">
                {olderDatasets.map((upload) => (
                  <button
                    key={upload.id}
                    onClick={() => handleDatasetClick(upload)}
                    className="w-full p-3 rounded-xl bg-gradient-to-br from-muted/30 to-background border-2 border-muted hover:border-primary/40 hover:from-primary/10 hover:to-accent/5 transition-all cursor-pointer shadow-md hover:shadow-lg text-left"
                  >
                    <div className="flex items-start gap-2 mb-2">
                      <FileIcon size={14} className="text-muted-foreground flex-shrink-0 mt-0.5" />
                      <p className="text-xs font-bold text-foreground truncate flex-1">{upload.file_name}</p>
                    </div>
                    <p className="text-[10px] text-muted-foreground ml-5 font-semibold">
                      {formatDate(upload.uploaded_at)}
                    </p>
                  </button>
                ))}
              </div>
            </div>
          )}
        </>
      ) : (
        <p className="text-xs text-muted-foreground text-center py-4 font-semibold">No recent uploads</p>
      )}
    </div>
  );
}
