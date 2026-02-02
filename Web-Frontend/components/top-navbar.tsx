'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { MenuIcon, LogoutIcon } from '@/components/chemistry-icons';
import { ThemeToggle } from '@/components/theme-toggle';
import { logout, type UserProfile } from '@/lib/api';

interface TopNavbarProps {
  onMenuClick: () => void;
  userProfile?: UserProfile | null;
}

export function TopNavbar({ onMenuClick, userProfile }: TopNavbarProps) {
  const router = useRouter();
  
  // Determine display name
  let displayName = 'User';
  if (userProfile) {
    if (userProfile.first_name && userProfile.last_name) {
      displayName = `${userProfile.first_name} ${userProfile.last_name}`;
    } else if (userProfile.first_name) {
      displayName = userProfile.first_name;
    } else {
      displayName = userProfile.username;
    }
  }

  const handleLogout = async () => {
    await logout();
    router.push('/');
  };
  return (
    <nav className="fixed top-0 left-0 right-0 h-16 bg-gradient-to-r from-card to-background/50 border-b-2 border-primary/30 flex items-center justify-between px-6 shadow-lg z-40">
      {/* Left - Hamburger */}
      <Button
        variant="ghost"
        size="sm"
        onClick={onMenuClick}
        className="font-black hover:bg-primary/20"
      >
        <MenuIcon size={24} />
      </Button>

      {/* Center - Empty space */}
      <div className="flex-1" />

      {/* Right - Theme Toggle, User Info & Logout */}
      <div className="flex items-center gap-3">
        {/* Theme Toggle */}
        <ThemeToggle />

        {/* User Info Pill */}
        <div className="hidden sm:flex items-center gap-3 px-4 py-2 bg-gradient-to-r from-primary/10 to-accent/10 border-2 border-primary/30 rounded-full">
          <div className="w-8 h-8 bg-gradient-to-br from-primary to-accent rounded-full flex items-center justify-center font-black text-xs text-primary-foreground">
            {displayName.charAt(0).toUpperCase()}
          </div>
          <div className="flex flex-col min-w-0">
            <p className="text-sm font-black text-foreground uppercase tracking-wider">{displayName}</p>
            <p className="text-xs text-muted-foreground">Active</p>
          </div>
        </div>

        {/* Logout Button */}
        <Button
          onClick={handleLogout}
          className="bg-destructive hover:bg-destructive/90 text-destructive-foreground font-bold gap-2"
          size="sm"
        >
          <LogoutIcon size={18} />
          <span className="hidden sm:inline">Logout</span>
        </Button>
      </div>
    </nav>
  );
}
