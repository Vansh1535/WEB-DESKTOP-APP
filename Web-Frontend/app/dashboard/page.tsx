'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { DashboardLayout } from '@/components/dashboard-layout';
import { UploadModal } from '@/components/upload-modal';
import { ReportModal } from '@/components/report-modal';
import { DataTable } from '@/components/data-table';
import { ChartContainer } from '@/components/chart-container';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { DataIcon, ChartLineIcon, FileIcon, DownloadIcon, ArrowLeftIcon } from '@/components/chemistry-icons';
import { isAuthenticated, listDatasets, getStatistics, deleteDataset, downloadPDF, getDataset, getUserProfile, getUserPreferences, updateUserPreferences, type Dataset, type Statistics, type UserProfile, type UserPreferences } from '@/lib/api';
import { UserHistoryTable, type HistoryEntry } from '@/components/user-history-table';
import { Loader2 } from 'lucide-react';

export default function DashboardPage() {
  const router = useRouter();
  const [data, setData] = useState<any[]>([]);
  const [filename, setFilename] = useState('');
  const [currentDatasetId, setCurrentDatasetId] = useState<number | null>(null);
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [stats, setStats] = useState({
    totalRecords: 0,
    avgFlowrate: 0,
    avgPressure: 0,
    avgTemperature: 0,
  });
  const [uploadModalOpen, setUploadModalOpen] = useState(false);
  const [reportModalOpen, setReportModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isDownloadingPDF, setIsDownloadingPDF] = useState(false);
  const [isLoadingDataset, setIsLoadingDataset] = useState(false);
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [userPreferences, setUserPreferences] = useState<UserPreferences | null>(null);

  useEffect(() => {
    // Check authentication
    if (!isAuthenticated()) {
      router.push('/login');
      return;
    }

    // Load user profile and preferences first
    loadUserData();
    // Load datasets and statistics
    loadDashboardData();
    loadHistory();
  }, [router]);

  const loadUserData = async () => {
    try {
      const profileResult = await getUserProfile();
      if (profileResult.success) {
        setUserProfile(profileResult.data);
        
        // Load preferences
        if (profileResult.data.preferences) {
          setUserPreferences(profileResult.data.preferences);
          
          // Restore last active dataset if available
          const lastDatasetId = profileResult.data.preferences.last_active_dataset_id;
          if (lastDatasetId) {
            const datasetResult = await getDataset(lastDatasetId);
            if (datasetResult.success) {
              setCurrentDatasetId(lastDatasetId);
              setFilename(datasetResult.data.file_name);
              
              if (datasetResult.data.statistics) {
                setStatistics(datasetResult.data.statistics);
                updateStatsFromBackend(datasetResult.data.statistics);
                const displayData = parseStatisticsToData(datasetResult.data.statistics);
                setData(displayData);
              }
            }
          }
        }
      }
    } catch (error) {
      console.error('Error loading user data:', error);
    }
  };

  const loadDashboardData = async () => {
    setIsLoading(true);
    
    try {
      // Fetch datasets list
      const datasetsResult = await listDatasets();
      if (datasetsResult.success) {
        setDatasets(datasetsResult.data.datasets);
      }

      // Fetch latest statistics
      const statsResult = await getStatistics();
      if (statsResult.success) {
        setStatistics(statsResult.data);
        updateStatsFromBackend(statsResult.data);
        
        // Convert statistics to displayable data
        const displayData = parseStatisticsToData(statsResult.data);
        setData(displayData);
        
        // Find the most recent completed dataset
        if (datasetsResult.success && datasetsResult.data.datasets.length > 0) {
          const latestDataset = datasetsResult.data.datasets.find((d: Dataset) => d.status === 'completed');
          if (latestDataset) {
            setFilename(latestDataset.file_name);
            setCurrentDatasetId(latestDataset.id);
          }
        }
      }
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadHistory = () => {
    // Load history from localStorage
    const savedHistory = localStorage.getItem('userHistory');
    if (savedHistory) {
      try {
        const parsedHistory = JSON.parse(savedHistory);
        setHistory(parsedHistory);
      } catch (error) {
        console.error('Error parsing history:', error);
        setHistory([]);
      }
    }
  };

  const addHistoryEntry = (action: HistoryEntry['action'], datasetName: string, status: 'success' | 'failed', details?: string) => {
    const newEntry: HistoryEntry = {
      id: Date.now(),
      action,
      datasetName,
      timestamp: new Date().toISOString(),
      status,
      details,
    };

    const updatedHistory = [newEntry, ...history].slice(0, 50); // Keep last 50 entries
    setHistory(updatedHistory);
    localStorage.setItem('userHistory', JSON.stringify(updatedHistory));
  };

  const updateStatsFromBackend = (backendStats: Statistics) => {
    // Calculate actual displayed rows count from by_type data
    const displayedRowsCount = backendStats.by_type ? Object.keys(backendStats.by_type).length : 0;
    
    setStats({
      totalRecords: displayedRowsCount,
      avgFlowrate: backendStats.overall_averages.flowrate,
      avgPressure: backendStats.overall_averages.pressure,
      avgTemperature: backendStats.overall_averages.temperature,
    });
  };

  const parseStatisticsToData = (statistics: Statistics): any[] => {
    if (!statistics || !statistics.by_type) return [];
    
    const data: any[] = [];
    
    // Convert backend statistics to displayable rows
    Object.entries(statistics.by_type).forEach(([type, stats]) => {
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

  const handleFileUpload = (uploadedData: any[], name: string, datasetId?: number, newStatistics?: any) => {
    setData(uploadedData);
    setFilename(name);
    setCurrentDatasetId(datasetId || null);

    if (newStatistics) {
      setStatistics(newStatistics);
      updateStatsFromBackend(newStatistics);
    }

    // Add to history
    addHistoryEntry('upload', name, 'success', `${uploadedData.length} records`);

    // Reload datasets list
    loadDashboardData();
  };

  const handleDeleteDataset = async (id: number) => {
    if (!confirm('Are you sure you want to delete this dataset?')) {
      return;
    }

    const datasetToDelete = datasets.find(d => d.id === id);
    
    try {
      const result = await deleteDataset(id);
      
      if (result.success) {
        // Add to history
        if (datasetToDelete) {
          addHistoryEntry('delete', datasetToDelete.file_name, 'success');
        }
        
        // If we deleted the current dataset, clear it
        if (currentDatasetId === id) {
          setCurrentDatasetId(null);
          setFilename('');
          setData([]);
        }
        
        // Reload dashboard data
        await loadDashboardData();
      } else {
        if (datasetToDelete) {
          addHistoryEntry('delete', datasetToDelete.file_name, 'failed', result.error);
        }
        alert(result.error || 'Failed to delete dataset');
      }
    } catch (error) {
      console.error('Error deleting dataset:', error);
      if (datasetToDelete) {
        addHistoryEntry('delete', datasetToDelete.file_name, 'failed', 'Network error');
      }
      alert('Failed to delete dataset. Please try again.');
    }
  };

  const handleDownloadPDF = async () => {
    if (!currentDatasetId) {
      alert('No dataset selected');
      return;
    }

    setIsDownloadingPDF(true);
    const pdfFilename = `${filename.replace('.csv', '')}_report.pdf`;
    const result = await downloadPDF(currentDatasetId, pdfFilename);
    setIsDownloadingPDF(false);
    
    if (result.success) {
      addHistoryEntry('download', filename, 'success', 'PDF report');
    } else {
      addHistoryEntry('download', filename, 'failed', result.error);
      alert(result.error || 'Failed to generate PDF');
    }
  };

  // Function to load a specific dataset
  const loadDatasetById = async (datasetId: number, datasetName: string) => {
    setIsLoadingDataset(true);
    try {
      const result = await getDataset(datasetId);
      if (result.success) {
        // Update current dataset
        setCurrentDatasetId(datasetId);
        setFilename(datasetName);
        
        // Use the statistics from the dataset
        if (result.data.statistics) {
          setStatistics(result.data.statistics);
          updateStatsFromBackend(result.data.statistics);
          
          // Convert statistics to displayable data
          const displayData = parseStatisticsToData(result.data.statistics);
          setData(displayData);
        }
        
        addHistoryEntry('upload', datasetName, 'success', 'Loaded from recent uploads');
        
        // Save as last active dataset
        await updateUserPreferences({ last_active_dataset_id: datasetId });
      }
    } catch (error) {
      console.error('Error loading dataset:', error);
      addHistoryEntry('upload', datasetName, 'failed', 'Failed to load dataset');
    } finally {
      setIsLoadingDataset(false);
    }
  };

  const handlePreferenceChange = async (preferences: Partial<UserPreferences>) => {
    try {
      await updateUserPreferences(preferences);
      // Update local state
      if (userPreferences) {
        setUserPreferences({ ...userPreferences, ...preferences });
      }
    } catch (error) {
      console.error('Error updating preferences:', error);
    }
  };

  return (
    <DashboardLayout 
      onUploadClick={() => setUploadModalOpen(true)} 
      onDatasetClick={loadDatasetById} 
      currentDatasetId={currentDatasetId}
      userProfile={userProfile}
    >
      {/* Upload Modal */}
      <UploadModal
        isOpen={uploadModalOpen}
        onClose={() => setUploadModalOpen(false)}
        onFileUpload={handleFileUpload}
      />

      {/* Report Modal */}
      <ReportModal
        isOpen={reportModalOpen}
        onClose={() => setReportModalOpen(false)}
        data={data}
        filename={filename}
      />

      {/* Loading Spinner Overlay */}
      {(isLoadingDataset || isLoading) && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 backdrop-blur-sm">
          <Card className="p-8 shadow-2xl border-2 border-primary">
            <div className="flex flex-col items-center gap-4">
              <Loader2 className="h-12 w-12 animate-spin text-primary" />
              <p className="text-lg font-bold text-foreground">
                {isLoadingDataset ? 'Loading Dataset...' : 'Loading Dashboard...'}
              </p>
            </div>
          </Card>
        </div>
      )}

      <div className="space-y-5">
        {/* Back to Home Button */}
        <Button
          variant="outline"
          onClick={() => router.push('/')}
          className="border-2 border-primary/40 hover:border-primary hover:bg-primary/5 font-bold gap-2 shadow-md"
        >
          <ArrowLeftIcon size={18} />
          Back to Home
        </Button>

        {/* Empty State */}
        {data.length === 0 && !isLoading && (
          <Card className="p-16 border-4 border-primary/30 text-center shadow-2xl bg-gradient-to-br from-card to-background/50">
            <div className="mb-8">
              <div className="w-24 h-24 bg-gradient-to-br from-primary to-accent rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-2xl">
                <FileIcon size={48} className="text-white" />
              </div>
              <h2 className="text-4xl font-black text-foreground uppercase tracking-wider mb-4">No Data Yet</h2>
              <p className="text-lg text-muted-foreground mb-8 font-semibold">Upload a CSV file to get started with analysis</p>
              <Button
                onClick={() => setUploadModalOpen(true)}
                className="gradient-primary text-white font-black px-10 py-6 text-lg shadow-2xl hover:shadow-3xl hover:scale-105 transition-all"
              >
                Upload Equipment Data
              </Button>
            </div>
          </Card>
        )}

        {/* Analysis Hub - Main Focus */}
        {data.length > 0 && !isLoading && (
          <div className="space-y-5">
            {/* File Name & Actions Header */}
            <div className="flex flex-col gap-4 p-4 sm:p-5 gradient-primary rounded-xl shadow-2xl">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                <div className="text-white">
                  <p className="text-xs sm:text-sm font-black uppercase tracking-widest opacity-90">Current Dataset</p>
                  <h2 className="text-xl sm:text-2xl lg:text-3xl font-black uppercase tracking-wider break-all">{filename}</h2>
                </div>
                {userProfile && (
                  <div className="flex gap-2 text-white">
                    <div className="bg-gradient-to-br from-orange-500 to-orange-600 backdrop-blur-sm rounded-lg px-4 py-2.5 border-2 border-orange-400/50 shadow-lg">
                      <p className="text-xs font-bold">Total Uploads</p>
                      <p className="text-3xl font-black">{userProfile.upload_count}</p>
                    </div>
                    <div className="bg-gradient-to-br from-rose-500 to-rose-600 backdrop-blur-sm rounded-lg px-4 py-2.5 border-2 border-rose-400/50 shadow-lg">
                      <p className="text-xs font-bold">Datasets</p>
                      <p className="text-3xl font-black">{datasets.length}</p>
                    </div>
                  </div>
                )}
              </div>
              <div className="flex gap-2 sm:gap-3 flex-wrap">
                <Button
                  onClick={() => setUploadModalOpen(true)}
                  className="flex-1 sm:flex-none bg-card hover:bg-card/80 text-primary font-black gap-2 text-sm sm:text-base shadow-lg hover:scale-105 transition-transform"
                >
                  <FileIcon size={16} className="sm:hidden" />
                  <FileIcon size={18} className="hidden sm:block" />
                  <span className="hidden sm:inline">New Upload</span>
                  <span className="sm:hidden">Upload</span>
                </Button>
                {currentDatasetId && (
                  <>
                    <Button
                      onClick={handleDownloadPDF}
                      disabled={isDownloadingPDF}
                      className="flex-1 sm:flex-none bg-card hover:bg-card/80 text-accent font-black gap-2 text-sm sm:text-base shadow-lg hover:scale-105 transition-transform"
                    >
                      {isDownloadingPDF ? (
                        <>
                          <Loader2 className="h-4 w-4 animate-spin" />
                          Generating Report...
                        </>
                      ) : (
                        <>
                          <DownloadIcon size={18} />
                          Generate Report
                        </>
                      )}
                    </Button>
                    <Button
                      onClick={() => handleDeleteDataset(currentDatasetId)}
                      className="flex-1 sm:flex-none bg-card hover:bg-destructive/90 text-destructive hover:text-destructive-foreground font-black gap-2 text-sm sm:text-base shadow-lg hover:scale-105 transition-all border-2 border-destructive/50"
                    >
                      <span className="text-lg">🗑️</span>
                      <span className="hidden sm:inline">Delete</span>
                      <span className="sm:hidden">Del</span>
                    </Button>
                  </>
                )}
              </div>
            </div>

            {/* Enhanced Statistics Cards with Infographics */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
              <StatCard 
                label="Equipment Types" 
                value={stats.totalRecords} 
                icon="📊"
                highlight 
              />
              <StatCard 
                label="Avg Flowrate" 
                value={stats.avgFlowrate.toFixed(2)} 
                unit="L/min" 
                icon="💧"
              />
              <StatCard 
                label="Avg Pressure" 
                value={stats.avgPressure.toFixed(2)} 
                unit="bar" 
                icon="⚡"
              />
              <StatCard 
                label="Avg Temperature" 
                value={stats.avgTemperature.toFixed(2)} 
                unit="°C" 
                icon="🌡️"
              />
            </div>

            {/* Charts and Data Tabs */}
            <div className="bg-gradient-to-br from-card to-background/50 border-4 border-primary/30 rounded-2xl p-4 sm:p-6 shadow-2xl">
              <h2 className="text-2xl sm:text-3xl font-black text-foreground mb-4 sm:mb-6 uppercase tracking-wider">Analysis Hub</h2>

              <Tabs defaultValue="charts" className="w-full">
                <TabsList className="grid w-full grid-cols-3 mb-4 sm:mb-6 !bg-gradient-to-r from-primary/10 via-accent/10 to-primary/10 border-2 border-primary/30 p-2 sm:p-2.5 shadow-lg rounded-2xl !h-auto">
                  <TabsTrigger value="charts" className="flex items-center justify-center gap-1 sm:gap-2 data-[state=active]:!gradient-primary data-[state=active]:!bg-gradient-to-r data-[state=active]:!from-primary data-[state=active]:!to-accent data-[state=active]:!text-white !bg-transparent hover:!bg-primary/5 font-bold text-sm sm:text-base py-3 sm:py-4 px-4 sm:px-6 rounded-xl transition-all text-foreground">
                    <ChartLineIcon size={18} className="sm:hidden" />
                    <ChartLineIcon size={22} className="hidden sm:block" />
                    <span className="inline">Charts</span>
                  </TabsTrigger>
                  <TabsTrigger value="data" className="flex items-center justify-center gap-1 sm:gap-2 data-[state=active]:!gradient-primary data-[state=active]:!bg-gradient-to-r data-[state=active]:!from-primary data-[state=active]:!to-accent data-[state=active]:!text-white !bg-transparent hover:!bg-primary/5 font-bold text-sm sm:text-base py-3 sm:py-4 px-4 sm:px-6 rounded-xl transition-all text-foreground">
                    <DataIcon size={18} className="sm:hidden" />
                    <DataIcon size={22} className="hidden sm:block" />
                    <span className="inline">Table</span>
                  </TabsTrigger>
                  <TabsTrigger value="history" className="flex items-center justify-center gap-1 sm:gap-2 data-[state=active]:!gradient-primary data-[state=active]:!bg-gradient-to-r data-[state=active]:!from-primary data-[state=active]:!to-accent data-[state=active]:!text-white !bg-transparent hover:!bg-primary/5 font-bold text-sm sm:text-base py-3 sm:py-4 px-4 sm:px-6 rounded-xl transition-all text-foreground">
                    <FileIcon size={18} className="sm:hidden" />
                    <FileIcon size={22} className="hidden sm:block" />
                    <span className="inline">History</span>
                  </TabsTrigger>
                </TabsList>

                <TabsContent value="charts" className="mt-4">
                  <div className="bg-card rounded-xl border-2 border-primary/30 p-6 shadow-2xl">
                    <ChartContainer data={data} />
                  </div>
                </TabsContent>

                <TabsContent value="data" className="mt-4">
                  <div className="bg-card rounded-xl border-2 border-primary/30 shadow-2xl overflow-hidden">
                    <DataTable 
                      data={data} 
                      filename={filename} 
                      userPreferences={userPreferences}
                      onPreferenceChange={handlePreferenceChange}
                    />
                  </div>
                </TabsContent>

                <TabsContent value="history" className="mt-4">
                  <UserHistoryTable history={history} />
                </TabsContent>
              </Tabs>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

function StatCard({ 
  label, 
  value, 
  unit = '', 
  icon = '', 
  trend = '', 
  trendUp = true, 
  highlight = false 
}: { 
  label: string; 
  value: string | number; 
  unit?: string; 
  icon?: string; 
  trend?: string; 
  trendUp?: boolean; 
  highlight?: boolean;
}) {
  return (
    <Card className={`p-5 border-4 transition-all duration-300 hover:shadow-2xl hover:-translate-y-2 relative overflow-hidden ${
      highlight 
        ? 'border-accent bg-gradient-to-br from-accent/20 to-accent/5 hover:border-accent/80' 
        : 'border-primary/30 hover:border-primary/60 bg-gradient-to-br from-card to-background/50'
    }`}>
      {/* Background Icon */}
      <div className="absolute top-2 right-2 text-7xl opacity-30">
        {icon}
      </div>
      
      <div className="relative z-10">
        <p className="text-sm font-bold text-muted-foreground mb-3 uppercase tracking-wide flex items-center gap-2">
          <span className="text-2xl opacity-90">{icon}</span>
          {label}
        </p>
        <div className="flex items-baseline gap-3">
          <p className={`text-4xl font-black ${
            highlight ? 'text-accent' : 'text-primary'
          }`}>
            {value}
            {unit && <span className="text-lg ml-2 font-bold text-muted-foreground">{unit}</span>}
          </p>
          {trend && (
            <span className={`text-sm font-bold px-2 py-1 rounded-md ${
              trendUp 
                ? 'bg-green-100 text-green-700' 
                : 'bg-red-100 text-red-700'
            }`}>
              {trendUp ? '↑' : '↓'} {trend}
            </span>
          )}
        </div>
      </div>
    </Card>
  );
}
