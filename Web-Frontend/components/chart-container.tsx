'use client';

import { useMemo } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from 'recharts';
import { Card } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

interface ChartContainerProps {
  data: any[];
}

export function ChartContainer({ data }: ChartContainerProps) {
  // Prepare data for charts
  const chartData = useMemo(() => {
    return data.map((row, idx) => ({
      name: row['equipment name'] || row['name'] || `Item ${idx + 1}`,
      flowrate: parseFloat(row.flowrate) || 0,
      pressure: parseFloat(row.pressure) || 0,
      temperature: parseFloat(row.temperature) || 0,
      type: row.type || 'Unknown',
    }));
  }, [data]);

  // Aggregated data for type analysis
  const typeData = useMemo(() => {
    const types: Record<string, any> = {};
    chartData.forEach((item) => {
      if (!types[item.type]) {
        types[item.type] = {
          type: item.type,
          count: 0,
          avgFlowrate: 0,
          avgPressure: 0,
          avgTemp: 0,
        };
      }
      types[item.type].count += 1;
      types[item.type].avgFlowrate += item.flowrate;
      types[item.type].avgPressure += item.pressure;
      types[item.type].avgTemp += item.temperature;
    });

    return Object.values(types).map((t: any) => ({
      type: t.type,
      count: t.count,
      avgFlowrate: (t.avgFlowrate / t.count).toFixed(2),
      avgPressure: (t.avgPressure / t.count).toFixed(2),
      avgTemp: (t.avgTemp / t.count).toFixed(2),
    }));
  }, [chartData]);

  const chartColors = {
    flowrate: '#0EA5E9',
    pressure: '#FBBF24',
    temperature: '#FF6B6B',
  };

  // Pie chart colors
  const PIE_COLORS = ['#FF6B1A', '#D94452', '#7B2C9E', '#0EA5E9', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899'];

  // Distribution data for pie chart
  const distributionData = useMemo(() => {
    const typeCounts: Record<string, number> = {};
    chartData.forEach((item) => {
      typeCounts[item.type] = (typeCounts[item.type] || 0) + 1;
    });
    return Object.entries(typeCounts).map(([name, value]) => ({ name, value }));
  }, [chartData]);

  // Radar data for multi-dimensional view
  const radarData = useMemo(() => {
    return typeData.map(t => ({
      type: t.type,
      flowrate: parseFloat(t.avgFlowrate),
      pressure: parseFloat(t.avgPressure),
      temperature: parseFloat(t.avgTemp),
    }));
  }, [typeData]);

  return (
    <div className="w-full space-y-4">
      <Tabs defaultValue="trend" className="w-full">
        <TabsList className="grid w-full grid-cols-2 md:grid-cols-5 bg-background border-2 border-primary/30 p-1 shadow-md">
          <TabsTrigger value="trend" className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-primary data-[state=active]:to-primary/80 data-[state=active]:text-white data-[state=active]:shadow-xl font-bold text-sm">📈 Trends</TabsTrigger>
          <TabsTrigger value="types" className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-accent data-[state=active]:to-accent/80 data-[state=active]:text-white data-[state=active]:shadow-xl font-bold text-sm">📊 Equipment</TabsTrigger>
          <TabsTrigger value="distribution" className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-secondary data-[state=active]:to-secondary/80 data-[state=active]:text-white data-[state=active]:shadow-xl font-bold text-sm">🥧 Distribution</TabsTrigger>
          <TabsTrigger value="radar" className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-[#10B981] data-[state=active]:to-[#059669] data-[state=active]:text-white data-[state=active]:shadow-xl font-bold text-sm">📡 Radar</TabsTrigger>
          <TabsTrigger value="correlation" className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-[#8B5CF6] data-[state=active]:to-[#7C3AED] data-[state=active]:text-white data-[state=active]:shadow-xl font-bold text-sm">🔬 Analysis</TabsTrigger>
        </TabsList>

        {/* Line Chart - Trends over data */}
        <TabsContent value="trend" className="mt-4">
          <Card className="p-6 border-2 border-primary/30 bg-gradient-to-br from-card to-background/50 shadow-lg">
            <h3 className="text-xl font-black mb-6 text-foreground uppercase tracking-wider">Equipment Parameter Trends</h3>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={chartData}>
                <defs>
                  <linearGradient id="flowrateGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#4EC5E6" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#4EC5E6" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                <XAxis
                  dataKey="name"
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  tick={{ fill: '#666', fontSize: 12 }}
                />
                <YAxis tick={{ fill: '#666', fontSize: 12 }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(255, 255, 255, 0.95)',
                    border: '1px solid #E5E7EB',
                    borderRadius: '8px',
                  }}
                />
                <Legend
                  wrapperStyle={{ paddingTop: '20px' }}
                  iconType="line"
                />
                <Line
                  type="monotone"
                  dataKey="flowrate"
                  stroke={chartColors.flowrate}
                  dot={{ fill: chartColors.flowrate, r: 4 }}
                  activeDot={{ r: 6 }}
                  name="Flowrate (L/min)"
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey="pressure"
                  stroke={chartColors.pressure}
                  dot={{ fill: chartColors.pressure, r: 4 }}
                  activeDot={{ r: 6 }}
                  name="Pressure (bar)"
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey="temperature"
                  stroke={chartColors.temperature}
                  dot={{ fill: chartColors.temperature, r: 4 }}
                  activeDot={{ r: 6 }}
                  name="Temperature (°C)"
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </Card>
        </TabsContent>

        {/* Bar Chart - Type Analysis */}
        <TabsContent value="types" className="mt-4">
          <Card className="p-6 border-2 border-primary/30 bg-gradient-to-br from-card to-background/50 shadow-2xl">
            <h3 className="text-2xl font-black mb-6 text-foreground uppercase tracking-wider">Average by Equipment Type</h3>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={typeData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                <XAxis
                  dataKey="type"
                  tick={{ fill: '#666', fontSize: 14, fontWeight: 600 }}
                />
                <YAxis tick={{ fill: '#666', fontSize: 14, fontWeight: 600 }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(255, 255, 255, 0.98)',
                    border: '2px solid #FF6B1A',
                    borderRadius: '12px',
                    boxShadow: '0 10px 30px rgba(0,0,0,0.2)',
                    padding: '12px',
                    fontSize: '14px',
                    fontWeight: 600,
                  }}
                />
                <Legend
                  wrapperStyle={{ paddingTop: '20px', fontSize: '14px', fontWeight: 600 }}
                />
                <Bar
                  dataKey="avgFlowrate"
                  fill={chartColors.flowrate}
                  name="Avg Flowrate"
                  radius={[8, 8, 0, 0]}
                />
                <Bar
                  dataKey="avgPressure"
                  fill={chartColors.pressure}
                  name="Avg Pressure"
                  radius={[8, 8, 0, 0]}
                />
                <Bar
                  dataKey="avgTemp"
                  fill={chartColors.temperature}
                  name="Avg Temperature"
                  radius={[8, 8, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </TabsContent>

        {/* Pie Chart - Distribution */}
        <TabsContent value="distribution" className="mt-4">
          <div className="grid md:grid-cols-2 gap-4">
            <Card className="p-6 border-2 border-primary/30 bg-gradient-to-br from-card to-background/50 shadow-2xl">
              <h3 className="text-2xl font-black mb-6 text-foreground uppercase tracking-wider">Equipment Type Distribution</h3>
              <ResponsiveContainer width="100%" height={350}>
                <PieChart>
                  <Pie
                    data={distributionData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {distributionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'rgba(255, 255, 255, 0.98)',
                      border: '2px solid #D94452',
                      borderRadius: '12px',
                      boxShadow: '0 10px 30px rgba(0,0,0,0.2)',
                      fontSize: '14px',
                      fontWeight: 600,
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </Card>

            {/* Area Chart for Trends */}
            <Card className="p-6 border-2 border-primary/30 bg-gradient-to-br from-card to-background/50 shadow-2xl">
              <h3 className="text-2xl font-black mb-6 text-foreground uppercase tracking-wider">Parameter Distribution Areas</h3>
              <ResponsiveContainer width="100%" height={350}>
                <AreaChart data={chartData.slice(0, 10)}>
                  <defs>
                    <linearGradient id="colorFlowrate" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#0EA5E9" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#0EA5E9" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="colorPressure" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#FBBF24" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#FBBF24" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="colorTemperature" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#FF6B6B" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#FF6B6B" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                  <XAxis dataKey="name" tick={{ fill: '#666', fontSize: 12 }} />
                  <YAxis tick={{ fill: '#666', fontSize: 12 }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'rgba(255, 255, 255, 0.98)',
                      border: '2px solid #7B2C9E',
                      borderRadius: '12px',
                      boxShadow: '0 10px 30px rgba(0,0,0,0.2)',
                      fontSize: '14px',
                      fontWeight: 600,
                    }}
                  />
                  <Area type="monotone" dataKey="flowrate" stroke="#0EA5E9" fillOpacity={1} fill="url(#colorFlowrate)" />
                  <Area type="monotone" dataKey="pressure" stroke="#FBBF24" fillOpacity={1} fill="url(#colorPressure)" />
                  <Area type="monotone" dataKey="temperature" stroke="#FF6B6B" fillOpacity={1} fill="url(#colorTemperature)" />
                </AreaChart>
              </ResponsiveContainer>
            </Card>
          </div>
        </TabsContent>

        {/* Radar Chart - Multi-dimensional view */}
        <TabsContent value="radar" className="mt-4">
          <Card className="p-6 border-2 border-primary/30 bg-gradient-to-br from-card to-background/50 shadow-2xl">
            <h3 className="text-2xl font-black mb-6 text-foreground uppercase tracking-wider">Multi-Dimensional Equipment Analysis</h3>
            <ResponsiveContainer width="100%" height={450}>
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                <PolarGrid stroke="#E5E7EB" />
                <PolarAngleAxis dataKey="type" tick={{ fill: '#666', fontSize: 14, fontWeight: 600 }} />
                <PolarRadiusAxis tick={{ fill: '#666', fontSize: 12 }} />
                <Radar name="Flowrate" dataKey="flowrate" stroke="#0EA5E9" fill="#0EA5E9" fillOpacity={0.6} />
                <Radar name="Pressure" dataKey="pressure" stroke="#FBBF24" fill="#FBBF24" fillOpacity={0.6} />
                <Radar name="Temperature" dataKey="temperature" stroke="#FF6B6B" fill="#FF6B6B" fillOpacity={0.6} />
                <Legend wrapperStyle={{ fontSize: '14px', fontWeight: 600 }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(255, 255, 255, 0.98)',
                    border: '2px solid #10B981',
                    borderRadius: '12px',
                    boxShadow: '0 10px 30px rgba(0,0,0,0.2)',
                    fontSize: '14px',
                    fontWeight: 600,
                  }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </Card>
        </TabsContent>

        {/* Scatter Chart - Correlations */}
        <TabsContent value="correlation" className="mt-4">
          <Card className="p-6 border-2 border-primary/30 bg-gradient-to-br from-card to-background/50 shadow-2xl">
            <h3 className="text-2xl font-black mb-6 text-foreground uppercase tracking-wider">Pressure vs Temperature Correlation</h3>
            <ResponsiveContainer width="100%" height={400}>
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                <XAxis
                  type="number"
                  dataKey="pressure"
                  name="Pressure (bar)"
                  tick={{ fill: '#666', fontSize: 14, fontWeight: 600 }}
                  label={{ value: 'Pressure (bar)', position: 'bottom', style: { fontSize: 16, fontWeight: 700, fill: '#333' } }}
                />
                <YAxis
                  type="number"
                  dataKey="temperature"
                  name="Temperature (°C)"
                  tick={{ fill: '#666', fontSize: 14, fontWeight: 600 }}
                  label={{ value: 'Temperature (°C)', angle: -90, position: 'insideLeft', style: { fontSize: 16, fontWeight: 700, fill: '#333' } }}
                />
                <Tooltip
                  cursor={{ strokeDasharray: '3 3' }}
                  contentStyle={{
                    backgroundColor: 'rgba(255, 255, 255, 0.98)',
                    border: '2px solid #8B5CF6',
                    borderRadius: '12px',
                    boxShadow: '0 10px 30px rgba(0,0,0,0.2)',
                    fontSize: '14px',
                    fontWeight: 600,
                  }}
                />
                <Scatter
                  name="Equipment"
                  data={chartData}
                  fill={chartColors.flowrate}
                  fillOpacity={0.8}
                />
              </ScatterChart>
            </ResponsiveContainer>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Summary Statistics - Enhanced Comic Style */}
      <Card className="p-6 border-2 border-accent/40 bg-gradient-to-r from-accent/8 to-primary/8 shadow-lg">
        <h3 className="text-lg font-black mb-6 text-foreground uppercase tracking-wider">📊 Dataset Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-gradient-to-br from-primary/10 to-transparent border-2 border-primary/30 rounded-lg p-4 shadow-md">
            <p className="text-sm font-black text-primary mb-3 uppercase tracking-wider">Flowrate Stats</p>
            <div className="space-y-2 font-mono">
              <p className="text-xs font-bold"><span className="text-accent">MIN:</span> {Math.min(...chartData.map((d) => d.flowrate)).toFixed(2)} L/min</p>
              <p className="text-xs font-bold"><span className="text-accent">MAX:</span> {Math.max(...chartData.map((d) => d.flowrate)).toFixed(2)} L/min</p>
              <p className="text-xs font-bold"><span className="text-primary">AVG:</span> {(chartData.reduce((a, d) => a + d.flowrate, 0) / chartData.length).toFixed(2)} L/min</p>
            </div>
          </div>
          <div className="bg-gradient-to-br from-accent/10 to-transparent border-2 border-accent/30 rounded-lg p-4 shadow-md">
            <p className="text-sm font-black text-accent mb-3 uppercase tracking-wider">Pressure Stats</p>
            <div className="space-y-2 font-mono">
              <p className="text-xs font-bold"><span className="text-accent">MIN:</span> {Math.min(...chartData.map((d) => d.pressure)).toFixed(2)} bar</p>
              <p className="text-xs font-bold"><span className="text-accent">MAX:</span> {Math.max(...chartData.map((d) => d.pressure)).toFixed(2)} bar</p>
              <p className="text-xs font-bold"><span className="text-primary">AVG:</span> {(chartData.reduce((a, d) => a + d.pressure, 0) / chartData.length).toFixed(2)} bar</p>
            </div>
          </div>
          <div className="bg-gradient-to-br from-secondary/10 to-transparent border-2 border-secondary/30 rounded-lg p-4 shadow-md">
            <p className="text-sm font-black text-secondary mb-3 uppercase tracking-wider">Temperature Stats</p>
            <div className="space-y-2 font-mono">
              <p className="text-xs font-bold"><span className="text-accent">MIN:</span> {Math.min(...chartData.map((d) => d.temperature)).toFixed(2)} °C</p>
              <p className="text-xs font-bold"><span className="text-accent">MAX:</span> {Math.max(...chartData.map((d) => d.temperature)).toFixed(2)} °C</p>
              <p className="text-xs font-bold"><span className="text-primary">AVG:</span> {(chartData.reduce((a, d) => a + d.temperature, 0) / chartData.length).toFixed(2)} °C</p>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}
