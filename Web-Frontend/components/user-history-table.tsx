'use client';

import React from 'react';
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';

export interface HistoryEntry {
  id: number;
  action: 'upload' | 'delete' | 'download' | 'generate_report';
  datasetName: string;
  timestamp: string;
  status: 'success' | 'failed';
  details?: string;
}

interface UserHistoryTableProps {
  history: HistoryEntry[];
  maxHeight?: string;
}

export function UserHistoryTable({ history, maxHeight = "400px" }: UserHistoryTableProps) {
  const getActionIcon = (action: HistoryEntry['action']) => {
    switch (action) {
      case 'upload':
        return '📤';
      case 'delete':
        return '🗑️';
      case 'download':
        return '💾';
      case 'generate_report':
        return '📄';
      default:
        return '📋';
    }
  };

  const getActionLabel = (action: HistoryEntry['action']) => {
    switch (action) {
      case 'upload':
        return 'CSV Upload';
      case 'delete':
        return 'Deleted Dataset';
      case 'download':
        return 'Downloaded PDF';
      case 'generate_report':
        return 'Generated Report';
      default:
        return action;
    }
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  };

  return (
    <Card className="border-2 border-primary/30 bg-card/50 overflow-hidden">
      <div className="p-4 sm:p-6">
        <div className="flex items-center gap-2 mb-4">
          <h3 className="text-xl sm:text-2xl font-black uppercase tracking-wider">📊 Activity History</h3>
        </div>
        
        <div className="overflow-x-auto">
          <ScrollArea className="w-full" style={{ maxHeight }}>
            <Table>
              <TableHeader>
                <TableRow className="border-primary/20 hover:bg-transparent">
                  <TableHead className="font-black uppercase text-xs tracking-wider min-w-[140px]">Action</TableHead>
                  <TableHead className="font-black uppercase text-xs tracking-wider min-w-[200px]">Dataset</TableHead>
                  <TableHead className="font-black uppercase text-xs tracking-wider min-w-[120px]">Time</TableHead>
                  <TableHead className="font-black uppercase text-xs tracking-wider min-w-[100px]">Status</TableHead>
                  <TableHead className="font-black uppercase text-xs tracking-wider min-w-[150px]">Details</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {history.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center py-8 text-muted-foreground font-semibold">
                      No activity history yet. Start by uploading a dataset!
                    </TableCell>
                  </TableRow>
                ) : (
                  history.map((entry) => (
                    <TableRow 
                      key={entry.id} 
                      className="border-primary/10 hover:bg-primary/5 transition-colors"
                    >
                      <TableCell className="font-semibold">
                        <div className="flex items-center gap-2">
                          <span className="text-xl flex-shrink-0">{getActionIcon(entry.action)}</span>
                          <span className="text-sm whitespace-nowrap">{getActionLabel(entry.action)}</span>
                        </div>
                      </TableCell>
                      <TableCell className="font-semibold text-foreground">
                        <span className="block truncate max-w-[250px]" title={entry.datasetName}>
                          {entry.datasetName}
                        </span>
                      </TableCell>
                      <TableCell className="text-sm text-muted-foreground font-medium whitespace-nowrap">
                        {formatTimestamp(entry.timestamp)}
                      </TableCell>
                      <TableCell>
                        <Badge 
                          variant={entry.status === 'success' ? 'default' : 'destructive'}
                          className={`font-bold uppercase text-xs whitespace-nowrap ${
                            entry.status === 'success' 
                              ? 'bg-accent hover:bg-accent/90' 
                              : ''
                          }`}
                        >
                          {entry.status === 'success' ? '✓ Success' : '✗ Failed'}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-sm text-muted-foreground font-medium">
                        <span className="block truncate max-w-[200px]" title={entry.details || '-'}>
                          {entry.details || '-'}
                        </span>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </ScrollArea>
        </div>
      </div>
    </Card>
  );
}
