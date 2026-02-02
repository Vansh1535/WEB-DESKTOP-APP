'use client';

import React from "react"

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { ChemistryIcon, BeakerIcon, AtomIcon } from '@/components/chemistry-icons';
import { login, register } from '@/lib/api';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [isSignup, setIsSignup] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    const result = await login(username, password);
    
    if (result.success) {
      router.push('/dashboard');
    } else {
      setError(result.error || 'Login failed. Please check your credentials.');
      setIsLoading(false);
    }
  };

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    // Validation
    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      setIsLoading(false);
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters long.');
      setIsLoading(false);
      return;
    }

    const result = await register(username, email, password, firstName, lastName);
    
    if (result.success) {
      router.push('/dashboard');
    } else {
      setError(result.error || 'Registration failed. Please try again.');
      setIsLoading(false);
    }
  };

  const toggleMode = () => {
    setIsSignup(!isSignup);
    setError('');
    setUsername('');
    setEmail('');
    setPassword('');
    setConfirmPassword('');
    setFirstName('');
    setLastName('');
  };

  return (
    <div className="min-h-screen bg-background text-foreground flex items-center justify-center p-3 sm:p-4 overflow-hidden relative">
      {/* Gradient Background */}
      <div className="absolute inset-0 gradient-warm opacity-20" />
      
      {/* Background decorative elements - More chemistry elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-10 right-10 opacity-16">
          <AtomIcon size={140} className="text-primary" />
        </div>
        <div className="absolute bottom-10 left-10 opacity-15">
          <BeakerIcon size={120} className="text-accent" />
        </div>
        <div className="absolute top-40 left-20 opacity-12">
          <AtomIcon size={80} className="text-secondary" />
        </div>
        <div className="absolute bottom-40 right-32 opacity-12">
          <BeakerIcon size={90} className="text-primary" />
        </div>
        <div className="absolute top-1/2 right-10 opacity-10">
          <AtomIcon size={60} className="text-accent" />
        </div>
        {/* Circular decorative elements */}
        <div className="absolute top-1/4 right-1/4 w-32 h-32 rounded-full border-2 border-primary/15" />
        <div className="absolute bottom-1/3 left-1/3 w-24 h-24 rounded-full border-2 border-accent/15" />
        <div className="absolute top-1/3 left-1/4 w-40 h-40 rounded-full border-2 border-secondary/10" />
        <div className="absolute bottom-1/4 right-1/3 w-28 h-28 rounded-full border-2 border-primary/12" />
      </div>

      <div className="w-full max-w-md relative z-10">
        {/* Header - Minimalist Style */}
        <div className="mb-8 sm:mb-12 text-center">
          <div className="flex justify-center mb-6 sm:mb-8">
            <div className="w-16 h-16 sm:w-20 sm:h-20 gradient-primary rounded-2xl flex items-center justify-center shadow-2xl">
              <ChemistryIcon size={40} className="text-white sm:hidden" />
              <ChemistryIcon size={48} className="text-white hidden sm:block" />
            </div>
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-2 sm:mb-3 tracking-tight">ChemData</h1>
          <div className="flex items-center justify-center gap-2 mb-2">
            <div className="w-1 h-1 bg-accent rounded-full" />
            <p className="text-accent font-semibold text-xs sm:text-sm">Analysis Platform</p>
            <div className="w-1 h-1 bg-accent rounded-full" />
          </div>
          <p className="text-muted-foreground text-sm sm:text-base">Professional Equipment Data Insights</p>
        </div>

        {/* Login Card - Minimalist Professional Style */}
        <Card className="p-6 sm:p-8 border border-border shadow-2xl bg-card/90 backdrop-blur-sm relative overflow-hidden group hover:shadow-3xl transition-all duration-300">
          {/* Card subtle gradient effect */}
          <div className="absolute inset-0 gradient-warm opacity-0 group-hover:opacity-5 transition-opacity duration-300" />
          
          {/* Toggle Tabs */}
          <div className="flex gap-2 mb-6 relative z-10">
            <button
              type="button"
              onClick={() => setIsSignup(false)}
              className={`flex-1 py-3 rounded-lg font-semibold text-sm transition-all ${
                !isSignup 
                  ? 'gradient-primary text-white shadow-lg' 
                  : 'bg-muted text-muted-foreground hover:bg-muted/80'
              }`}
            >
              Sign In
            </button>
            <button
              type="button"
              onClick={() => setIsSignup(true)}
              className={`flex-1 py-3 rounded-lg font-semibold text-sm transition-all ${
                isSignup 
                  ? 'gradient-primary text-white shadow-lg' 
                  : 'bg-muted text-muted-foreground hover:bg-muted/80'
              }`}
            >
              Sign Up
            </button>
          </div>

          <form onSubmit={isSignup ? handleSignup : handleLogin} className="space-y-6 relative z-10">
            {error && (
              <div className="p-4 bg-destructive/10 border border-destructive/50 rounded-lg">
                <p className="text-destructive text-sm font-medium">{error}</p>
              </div>
            )}

            {isSignup && (
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label htmlFor="firstName" className="block text-sm font-semibold mb-3 text-foreground">
                    First Name
                  </label>
                  <Input
                    id="firstName"
                    type="text"
                    placeholder="John"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    className="h-12 border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 font-medium bg-background transition-colors"
                  />
                </div>
                <div>
                  <label htmlFor="lastName" className="block text-sm font-semibold mb-3 text-foreground">
                    Last Name
                  </label>
                  <Input
                    id="lastName"
                    type="text"
                    placeholder="Doe"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    className="h-12 border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 font-medium bg-background transition-colors"
                  />
                </div>
              </div>
            )}

            <div>
              <label htmlFor="username" className="block text-sm font-semibold mb-3 text-foreground">
                Username
              </label>
              <Input
                id="username"
                type="text"
                placeholder="Enter your username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="h-12 border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 font-medium bg-background transition-colors"
                required
              />
            </div>

            {isSignup && (
              <div>
                <label htmlFor="email" className="block text-sm font-semibold mb-3 text-foreground">
                  Email
                </label>
                <Input
                  id="email"
                  type="email"
                  placeholder="your.email@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="h-12 border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 font-medium bg-background transition-colors"
                  required
                />
              </div>
            )}

            <div>
              <label htmlFor="password" className="block text-sm font-semibold mb-3 text-foreground">
                Password
              </label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="h-12 border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 font-medium bg-background transition-colors"
                required
              />
            </div>

            {isSignup && (
              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-semibold mb-3 text-foreground">
                  Confirm Password
                </label>
                <Input
                  id="confirmPassword"
                  type="password"
                  placeholder="••••••••"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="h-12 border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 font-medium bg-background transition-colors"
                  required
                />
              </div>
            )}

            <Button
              type="submit"
              disabled={isLoading}
              className="w-full h-12 gradient-primary hover:opacity-90 text-white font-semibold shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-105 active:scale-95 border-0"
            >
              {isLoading 
                ? 'Processing...' 
                : isSignup 
                  ? 'Create Account' 
                  : 'Sign In'
              }
            </Button>
          </form>

          {!isSignup && (
            <div className="mt-8 pt-6 border-t border-border">
              <div className="bg-accent/5 border border-accent/30 rounded-lg p-4">
                <p className="text-xs font-semibold text-accent mb-2">Demo Credentials</p>
                <p className="text-sm text-muted-foreground">
                  Username: <span className="text-foreground font-medium">admin</span><br/>
                  Password: <span className="text-foreground font-medium">admin123</span>
                </p>
              </div>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
