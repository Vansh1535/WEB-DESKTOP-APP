'use client';

import React from "react";
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { ChemistryIcon, BeakerIcon, AtomIcon, FlaskIcon } from '@/components/chemistry-icons';
import { ThemeToggle } from '@/components/theme-toggle';
import { useRouter } from 'next/navigation';

export default function LandingPage() {
  const router = useRouter();

  const features = [
    {
      icon: "📊",
      title: "Data Visualization",
      description: "Interactive charts with real-time updates"
    },
    {
      icon: "📤",
      title: "CSV Upload",
      description: "Drag-and-drop with instant processing"
    },
    {
      icon: "📈",
      title: "Statistical Analysis",
      description: "Comprehensive statistics and insights"
    },
    {
      icon: "📄",
      title: "PDF Reports",
      description: "Professional reports with charts"
    },
    {
      icon: "🗃️",
      title: "Dataset Management",
      description: "Organize multiple datasets easily"
    },
    {
      icon: "🎨",
      title: "Modern UI",
      description: "Beautiful dark/light theme support"
    }
  ];

  return (
    <div className="min-h-screen bg-background text-foreground overflow-hidden relative">
      {/* Gradient Background - Darker and more vibrant */}
      <div className="absolute inset-0 gradient-warm opacity-30" />
      
      {/* Background decorative elements - More chemistry elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 right-20 opacity-20">
          <AtomIcon size={160} className="text-primary" />
        </div>
        <div className="absolute bottom-20 left-20 opacity-18">
          <BeakerIcon size={140} className="text-accent" />
        </div>
        <div className="absolute top-40 left-32 opacity-16">
          <FlaskIcon size={100} className="text-secondary" />
        </div>
        <div className="absolute top-1/3 right-40 opacity-15">
          <ChemistryIcon size={90} className="text-accent" />
        </div>
        <div className="absolute bottom-1/4 right-1/4 opacity-16">
          <AtomIcon size={110} className="text-primary" />
        </div>
        <div className="absolute bottom-1/3 left-1/4 opacity-14">
          <FlaskIcon size={85} className="text-accent" />
        </div>
        <div className="absolute top-1/2 left-10 opacity-12">
          <BeakerIcon size={75} className="text-secondary" />
        </div>
        {/* Additional decorative elements */}
        <div className="absolute top-10 left-1/3 opacity-14">
          <AtomIcon size={95} className="text-accent" />
        </div>
        <div className="absolute bottom-40 right-10 opacity-13">
          <FlaskIcon size={80} className="text-primary" />
        </div>
        <div className="absolute top-2/3 right-1/3 opacity-15">
          <BeakerIcon size={110} className="text-secondary" />
        </div>
        <div className="absolute bottom-10 left-1/2 opacity-12">
          <ChemistryIcon size={70} className="text-primary" />
        </div>
        <div className="absolute top-1/4 right-10 opacity-14">
          <FlaskIcon size={90} className="text-accent" />
        </div>
        <div className="absolute bottom-1/2 left-16 opacity-13">
          <AtomIcon size={85} className="text-secondary" />
        </div>
        <div className="absolute top-3/4 left-1/4 opacity-11">
          <BeakerIcon size={65} className="text-accent" />
        </div>
        <div className="absolute top-16 right-1/2 opacity-12">
          <ChemistryIcon size={75} className="text-primary" />
        </div>
        {/* Circular decorative elements */}
        <div className="absolute top-1/4 right-1/4 w-40 h-40 rounded-full border-4 border-primary/20" />
        <div className="absolute bottom-1/3 left-1/3 w-32 h-32 rounded-full border-4 border-accent/20" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full border-2 border-secondary/10" />
        <div className="absolute top-1/4 left-1/4 w-48 h-48 rounded-full border-3 border-primary/15" />
        <div className="absolute bottom-1/4 right-1/3 w-36 h-36 rounded-full border-3 border-accent/18" />
        <div className="absolute top-1/3 left-1/2 w-44 h-44 rounded-full border-3 border-secondary/12" />
        <div className="absolute bottom-1/2 right-1/4 w-52 h-52 rounded-full border-2 border-primary/10" />
        <div className="absolute top-2/3 right-1/2 w-38 h-38 rounded-full border-4 border-accent/15" />
      </div>

      {/* Header */}
      <header className="relative z-10 border-b-2 border-primary/20 bg-card/90 backdrop-blur-md shadow-md">
        <div className="container mx-auto px-3 sm:px-4 lg:px-6 py-5 sm:py-6 flex items-center justify-between">
          <div className="flex items-center gap-3 sm:gap-4">
            <div className="w-12 h-12 sm:w-14 sm:h-14 gradient-primary rounded-xl flex items-center justify-center shadow-lg">
              <ChemistryIcon size={24} className="text-white sm:hidden" />
              <ChemistryIcon size={28} className="text-white hidden sm:block" />
            </div>
            <div className="flex items-baseline gap-2 sm:gap-3">
              <h1 className="text-2xl sm:text-3xl font-bold tracking-tight">ChemData</h1>
              <p className="hidden sm:block text-sm sm:text-base font-semibold text-accent uppercase tracking-wider">Analysis Platform</p>
            </div>
          </div>
          <div className="flex items-center gap-3 sm:gap-4">
            <ThemeToggle />
            <Button 
              onClick={() => router.push('/login')}
              className="gradient-primary hover:opacity-90 text-white font-bold px-5 sm:px-6 py-2.5 h-11 sm:h-12 text-base sm:text-lg shadow-lg hover:shadow-xl hover:scale-105 transition-all border-0"
            >
              Login
            </Button>
          </div>
        </div>
      </header>

      {/* SECTION 1: Hero + Features Combined */}
      <section className="relative z-10 container mx-auto px-3 sm:px-4 lg:px-6 py-6 sm:py-8">
        <div className="max-w-6xl mx-auto">
          {/* Hero Content */}
          <div className="text-center mb-6 sm:mb-8">
            <div className="flex justify-center mb-3 sm:mb-4">
              <div className="w-20 h-20 sm:w-24 sm:h-24 lg:w-28 lg:h-28 gradient-primary rounded-2xl flex items-center justify-center shadow-2xl">
                <ChemistryIcon size={48} className="text-white sm:hidden" />
                <ChemistryIcon size={56} className="text-white hidden sm:block lg:hidden" />
                <ChemistryIcon size={64} className="text-white hidden lg:block" />
              </div>
            </div>
            
            <h2 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold mb-4 sm:mb-5 tracking-tight px-2">
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-[#FF6B1A] via-[#D94452] to-[#7B2C9E]">
                Chemical Equipment Data Visualizer
              </span>
            </h2>
            
            <p className="text-base sm:text-lg md:text-xl text-muted-foreground mb-6 sm:mb-8 max-w-3xl mx-auto px-4 leading-relaxed">
              Upload, analyze, and visualize chemical equipment parameters with powerful statistical tools
            </p>

            <div className="flex gap-2 sm:gap-3 justify-center flex-wrap mb-8 sm:mb-10 px-4">
              <Button 
                size="lg"
                onClick={() => router.push('/login')}
                className="h-12 sm:h-14 px-8 sm:px-10 text-base sm:text-lg font-bold gradient-primary hover:opacity-90 text-white shadow-xl hover:shadow-2xl hover:scale-105 transition-all border-0"
              >
                Get Started →
              </Button>
            </div>
          </div>

          {/* Features Grid - Compact */}
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 sm:gap-4 max-w-4xl mx-auto px-2">
            {features.map((feature, index) => (
              <Card 
                key={index} 
                className="p-3 sm:p-4 border-2 border-primary/20 hover:border-primary/50 transition-all duration-300 bg-card/80 backdrop-blur-sm hover:shadow-lg group"
              >
                <div className="text-3xl sm:text-4xl mb-2 group-hover:scale-110 transition-transform">
                  {feature.icon}
                </div>
                <h4 className="text-sm sm:text-base font-bold mb-1 tracking-tight">
                  {feature.title}
                </h4>
                <p className="text-xs sm:text-sm text-muted-foreground leading-snug">
                  {feature.description}
                </p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* SECTION 2: Stats + Value Proposition */}
      <section className="relative z-10 container mx-auto px-4 py-10 sm:py-14 bg-gradient-to-r from-primary/5 via-accent/5 to-secondary/5">
        <div className="max-w-6xl mx-auto bg-card/95 backdrop-blur-sm rounded-3xl p-6 sm:p-10 md:p-12 border-2 border-accent/30 shadow-2xl">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-10 items-center">
            {/* Stats Cards */}
            <div className="grid grid-cols-3 gap-4 sm:gap-5">
              <Card className="p-5 sm:p-6 border-2 border-primary/30 bg-card shadow-lg text-center hover:scale-105 transition-transform">
                <div className="text-5xl sm:text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[#FF6B1A] to-[#D94452] mb-2">▦</div>
                <p className="text-sm sm:text-base font-semibold text-muted-foreground">Datasets</p>
              </Card>
              <Card className="p-5 sm:p-6 border-2 border-accent/30 bg-card shadow-lg text-center hover:scale-105 transition-transform">
                <div className="text-5xl sm:text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[#D94452] to-[#7B2C9E] mb-2">⚡</div>
                <p className="text-sm sm:text-base font-semibold text-muted-foreground">Fast</p>
              </Card>
              <Card className="p-5 sm:p-6 border-2 border-secondary/30 bg-card shadow-lg text-center hover:scale-105 transition-transform">
                <div className="text-5xl sm:text-6xl mb-2">
                  <span className="bg-clip-text text-transparent bg-gradient-to-r from-[#7B2C9E] to-[#4A1F6B] font-bold">🔍</span>
                </div>
                <p className="text-sm sm:text-base font-semibold text-muted-foreground">Insights</p>
              </Card>
            </div>

            {/* Value Prop */}
            <div>
              <h3 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-5 sm:mb-6 tracking-tight">
                Why Choose ChemData?
              </h3>
              <ul className="space-y-3 sm:space-y-4 text-base sm:text-lg text-muted-foreground">
                <li className="flex items-start gap-3">
                  <span className="text-primary font-bold mt-1 text-xl">✓</span>
                  <span>Instant data processing and visualization</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-accent font-bold mt-1 text-xl">✓</span>
                  <span>Professional PDF reports with one click</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-secondary font-bold mt-1 text-xl">✓</span>
                  <span>Secure data management and history tracking</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-primary font-bold mt-1 text-xl">✓</span>
                  <span>Beautiful, intuitive interface for efficiency</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 3: CTA + Footer */}
      <section className="relative z-10 container mx-auto px-4 py-8">
        <div className="max-w-3xl mx-auto text-center mb-8">
          <h3 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-4 tracking-tight">
            Ready to Analyze Your Data?
          </h3>
          <p className="text-base sm:text-lg text-muted-foreground mb-6">
            Start visualizing your chemical equipment parameters today
          </p>
          <Button 
            size="lg"
            onClick={() => router.push('/login')}
            className="h-12 sm:h-14 px-10 sm:px-12 text-base sm:text-lg font-bold gradient-primary hover:opacity-90 text-white shadow-xl hover:shadow-2xl hover:scale-105 transition-all border-0"
          >
            Launch Platform →
          </Button>
        </div>

        {/* Footer */}
        <footer className="border-t-2 border-primary/20 pt-6 mt-8">
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-3">
              <div className="w-7 h-7 gradient-primary rounded-lg flex items-center justify-center shadow-lg">
                <ChemistryIcon size={14} className="text-white" />
              </div>
              <span className="font-bold tracking-tight">ChemData</span>
            </div>
            <p className="text-muted-foreground text-xs">
              © 2026 ChemData Analysis Platform. Professional Equipment Data Insights.
            </p>
          </div>
        </footer>
      </section>
    </div>
  );
}
