'use client';

import React, { useState, useEffect } from 'react';
import { TopNavbar } from '@/components/top-navbar';
import { SidebarRecentUploads } from '@/components/sidebar-recent-uploads';
import { Button } from '@/components/ui/button';
import { UploadIcon, HistoryIcon } from '@/components/chemistry-icons';
import type { UserProfile } from '@/lib/api';

interface DashboardLayoutProps {
  children: React.ReactNode;
  onUploadClick?: () => void;
  onDatasetClick?: (datasetId: number, datasetName: string) => void;
  currentDatasetId?: number | null;
  userProfile?: UserProfile | null;
}

export function DashboardLayout({ children, onUploadClick, onDatasetClick, currentDatasetId, userProfile }: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isDesktop, setIsDesktop] = useState(true);

  useEffect(() => {
    const checkScreenSize = () => {
      const desktop = window.innerWidth >= 1024;
      setIsDesktop(desktop);
      if (!desktop) {
        setSidebarOpen(false);
      }
    };

    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);
    return () => window.removeEventListener('resize', checkScreenSize);
  }, []);

  return (
    <div className="min-h-screen bg-background">
      {/* Top Navbar */}
      <TopNavbar onMenuClick={() => setSidebarOpen(!sidebarOpen)} userProfile={userProfile} />

      {/* Main Layout with Sidebar */}
      <div className="flex pt-16">
        {/* Mobile overlay */}
        {sidebarOpen && !isDesktop && (
          <div 
            className="fixed inset-0 bg-black/50 z-30 lg:hidden" 
            onClick={() => setSidebarOpen(false)}
          />
        )}
        
        <aside
          className={`fixed left-0 top-16 h-[calc(100vh-64px)] bg-gradient-to-b from-card to-background/50 border-r-2 border-primary/30 transition-all duration-300 flex flex-col shadow-xl z-40 ${
            isDesktop 
              ? (sidebarOpen ? 'w-64' : 'w-20')
              : (sidebarOpen ? 'w-64 translate-x-0' : 'w-64 -translate-x-full')
          }`}
        >
          {/* Sidebar Header */}
          <div className="p-4 lg:p-6 border-b-2 border-primary/30 bg-gradient-to-r from-primary/10 to-accent/10">
            {sidebarOpen ? (
              <div>
                <h2 className="text-base lg:text-lg font-black text-foreground uppercase tracking-wider">Analysis Hub</h2>
                <p className="text-xs text-muted-foreground font-semibold mt-1">Data Tools</p>
              </div>
            ) : (
              <div className="w-8 h-8 bg-gradient-to-br from-primary to-accent rounded-lg flex items-center justify-center">
                <span className="font-black text-xs text-primary-foreground">A</span>
              </div>
            )}
          </div>

          {/* Sidebar Actions */}
          <nav className="flex-1 p-3 lg:p-4 space-y-3 overflow-y-auto">
            {/* Upload Button */}
            <Button
              onClick={onUploadClick}
              className="w-full justify-start gap-2 lg:gap-3 text-sm lg:text-base bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary/70 text-primary-foreground font-black transition-all duration-200 hover:shadow-lg"
            >
              <UploadIcon size={18} />
              {sidebarOpen && <span>Upload File</span>}
            </Button>

            {/* Recent Uploads Section */}
            {sidebarOpen && (
              <div className="mt-4 lg:mt-6 pt-4 border-t-2 border-primary/20">
                <h3 className="text-xs font-black text-foreground uppercase tracking-wider mb-3 flex items-center gap-2">
                  <HistoryIcon size={14} />
                  Recent Uploads
                </h3>
                <div className="max-h-60 lg:max-h-80 overflow-y-auto pr-1">
                  <SidebarRecentUploads onDatasetClick={onDatasetClick} currentDatasetId={currentDatasetId} />
                </div>
              </div>
            )}
          </nav>
        </aside>

        {/* Main Content */}
        <main
          className={`transition-all duration-300 flex-1 w-full ${
            isDesktop 
              ? (sidebarOpen ? 'lg:ml-64' : 'lg:ml-20')
              : 'lg:ml-20'
          }`}
        >
          <div className="p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
