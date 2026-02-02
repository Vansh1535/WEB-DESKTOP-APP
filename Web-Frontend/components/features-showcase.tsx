import {
  UploadIcon,
  DataIcon,
  ChartLineIcon,
  FileIcon,
  HistoryIcon,
} from '@/components/chemistry-icons';
import { Card } from '@/components/ui/card';

export function FeaturesShowcase() {
  const features = [
    {
      icon: UploadIcon,
      title: 'Easy Upload',
      description: 'Drag and drop or select CSV files. Supports all standard equipment data formats.',
    },
    {
      icon: DataIcon,
      title: 'Smart Analysis',
      description: 'Automatic statistics calculation. Filter, search, and sort data with advanced tools.',
    },
    {
      icon: ChartLineIcon,
      title: 'Rich Visualizations',
      description: 'Interactive charts for trends, correlations, and type-based analysis.',
    },
    {
      icon: FileIcon,
      title: 'Report Generation',
      description: 'Create professional HTML reports with statistics and formatted data tables.',
    },
    {
      icon: HistoryIcon,
      title: 'Quick History',
      description: 'Access your last 5 uploads instantly. Never lose your recent work.',
    },
  ];

  return (
    <div className="py-12">
      <div className="max-w-4xl mx-auto text-center mb-12">
        <h2 className="text-3xl font-bold mb-4 text-balance">Powerful Features for Equipment Analysis</h2>
        <p className="text-lg text-muted-foreground text-balance">
          Everything you need to analyze, visualize, and understand your equipment data
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {features.map((feature, idx) => {
          const Icon = feature.icon;
          return (
            <Card
              key={idx}
              className="p-6 border-primary/20 hover:border-primary/50 hover:shadow-lg transition-all group"
            >
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
                <Icon size={24} className="text-primary" />
              </div>
              <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
              <p className="text-sm text-muted-foreground">{feature.description}</p>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
