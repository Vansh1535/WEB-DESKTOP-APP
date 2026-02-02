'use client';

import { useState, useMemo } from 'react';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import type { UserPreferences } from '@/lib/api';

interface DataTableProps {
  data: any[];
  filename: string;
  userPreferences?: UserPreferences | null;
  onPreferenceChange?: (preferences: Partial<UserPreferences>) => void;
}

export function DataTable({ data, filename, userPreferences, onPreferenceChange }: DataTableProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState(userPreferences?.default_sort_column || '');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>(userPreferences?.default_sort_order || 'asc');
  const [itemsPerPage, setItemsPerPage] = useState(userPreferences?.items_per_page || 10);
  const [currentPage, setCurrentPage] = useState(1);

  const columns = data.length > 0 ? Object.keys(data[0]) : [];

  const filteredData = useMemo(() => {
    return data.filter((row) =>
      Object.values(row).some((value) =>
        String(value).toLowerCase().includes(searchTerm.toLowerCase())
      )
    );
  }, [data, searchTerm]);

  const sortedData = useMemo(() => {
    if (!sortBy) return filteredData;

    return [...filteredData].sort((a, b) => {
      const aVal = a[sortBy] || '';
      const bVal = b[sortBy] || '';

      // Numeric sort
      const aNum = parseFloat(aVal);
      const bNum = parseFloat(bVal);

      if (!isNaN(aNum) && !isNaN(bNum)) {
        return sortOrder === 'asc' ? aNum - bNum : bNum - aNum;
      }

      // String sort
      const aStr = String(aVal).toLowerCase();
      const bStr = String(bVal).toLowerCase();
      return sortOrder === 'asc'
        ? aStr.localeCompare(bStr)
        : bStr.localeCompare(aStr);
    });
  }, [filteredData, sortBy, sortOrder]);

  const paginatedData = useMemo(() => {
    const start = (currentPage - 1) * itemsPerPage;
    return sortedData.slice(start, start + itemsPerPage);
  }, [sortedData, currentPage, itemsPerPage]);

  const totalPages = Math.ceil(sortedData.length / itemsPerPage);

  const handleSort = (column: string) => {
    let newSortOrder: 'asc' | 'desc' = 'asc';
    if (sortBy === column) {
      newSortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
      setSortOrder(newSortOrder);
    } else {
      setSortBy(column);
      setSortOrder('asc');
    }
    setCurrentPage(1);
    
    // Save preferences
    if (onPreferenceChange) {
      onPreferenceChange({
        default_sort_column: sortBy === column ? column : column,
        default_sort_order: newSortOrder
      });
    }
  };

  const handleExportCSV = () => {
    const csvContent = [
      columns.join(','),
      ...sortedData.map((row) => columns.map((col) => `"${row[col] || ''}"`).join(',')),
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${filename.replace('.csv', '')}_export.csv`;
    a.click();
  };

  return (
    <div className="space-y-6">
      {/* Filters Section */}
      <div className="bg-gradient-to-r from-primary/5 to-accent/5 border-2 border-primary/30 rounded-lg p-6 shadow-md">
        <h3 className="text-lg font-black mb-4 text-foreground uppercase tracking-wider">Search & Filter</h3>
        
        <div className="space-y-4">
          <div>
            <Input
              placeholder="🔍 Search equipment data..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="border-2 border-primary/40 focus-visible:ring-primary focus-visible:border-primary font-semibold"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="border-2 border-primary/30 font-semibold">
                <SelectValue placeholder="↕ Sort by..." />
              </SelectTrigger>
              <SelectContent>
                {columns.map((col) => (
                  <SelectItem key={col} value={col} className="font-semibold">
                    {col}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={sortOrder} onValueChange={(v) => setSortOrder(v as any)}>
              <SelectTrigger className="border-2 border-primary/30 font-semibold">
                <SelectValue placeholder="Order" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="asc" className="font-semibold">Ascending</SelectItem>
                <SelectItem value="desc" className="font-semibold">Descending</SelectItem>
              </SelectContent>
            </Select>

            <Select value={itemsPerPage.toString()} onValueChange={(v) => {
              const newValue = parseInt(v);
              setItemsPerPage(newValue);
              if (onPreferenceChange) {
                onPreferenceChange({ items_per_page: newValue });
              }
            }}>
              <SelectTrigger className="border-2 border-primary/30 font-semibold">
                <SelectValue placeholder="Items per page" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="5" className="font-semibold">5 per page</SelectItem>
                <SelectItem value="10" className="font-semibold">10 per page</SelectItem>
                <SelectItem value="25" className="font-semibold">25 per page</SelectItem>
                <SelectItem value="50" className="font-semibold">50 per page</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>

      {/* Table Section */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
          <p className="text-sm font-bold text-muted-foreground uppercase">
            Showing {paginatedData.length} of {sortedData.length} records
          </p>
          <Button 
            onClick={handleExportCSV}
            className="gradient-primary hover:opacity-90 text-white font-black gap-2 shadow-lg hover:scale-105 transition-transform"
          >
            📥 Export CSV
          </Button>
        </div>

        <div className="overflow-x-auto border-2 border-primary/30 rounded-lg shadow-lg bg-gradient-to-b from-card via-card to-background/30">
          <Table>
            <TableHeader className="bg-gradient-to-r from-primary/15 to-accent/15 border-b-2 border-primary/40 sticky top-0 z-10">
              <TableRow className="hover:bg-transparent">
                {columns.map((col) => (
                  <TableHead 
                    key={col} 
                    className="font-black text-foreground uppercase text-xs tracking-wider cursor-pointer hover:bg-primary/10 transition-colors"
                    onClick={() => handleSort(col)}
                  >
                    <div className="flex items-center gap-2">
                      {col}
                      {sortBy === col && (
                        <span className="text-accent font-black">
                          {sortOrder === 'asc' ? '↑' : '↓'}
                        </span>
                      )}
                    </div>
                  </TableHead>
                ))}
              </TableRow>
            </TableHeader>
            <TableBody>
              {paginatedData.length > 0 ? (
                paginatedData.map((row, idx) => (
                  <TableRow 
                    key={idx} 
                    className="border-primary/15 hover:bg-primary/8 transition-colors duration-150 hover:shadow-md"
                  >
                    {columns.map((col) => (
                      <TableCell 
                        key={`${idx}-${col}`} 
                        className="font-medium py-3"
                      >
                        {row[col]}
                      </TableCell>
                    ))}
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={columns.length} className="text-center py-8 text-muted-foreground font-semibold">
                    No data found
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex justify-center items-center gap-2 mt-6">
            <Button
              onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
              disabled={currentPage === 1}
              variant="outline"
              className="border-2 border-primary/30 hover:bg-primary/10 font-bold"
            >
              ← Previous
            </Button>
            <div className="flex gap-1">
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                <Button
                  key={page}
                  onClick={() => setCurrentPage(page)}
                  variant={currentPage === page ? 'default' : 'outline'}
                  className={`w-10 h-10 font-bold ${
                    currentPage === page
                      ? 'bg-primary text-primary-foreground shadow-lg'
                      : 'border-2 border-primary/30 hover:bg-primary/10'
                  }`}
                >
                  {page}
                </Button>
              ))}
            </div>
            <Button
              onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
              disabled={currentPage === totalPages}
              variant="outline"
              className="border-2 border-primary/30 hover:bg-primary/10 font-bold"
            >
              Next →
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
