'use client';

import { useState } from 'react';
import { DashboardLayout } from '@/components/dashboard-layout';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { SettingsIcon } from '@/components/chemistry-icons';

export default function SettingsPage() {
  const [email, setEmail] = useState('scientist@example.com');
  const [displayName, setDisplayName] = useState('Dr. Researcher');
  const [theme, setTheme] = useState('light');
  const [notifications, setNotifications] = useState(true);
  const [isSaving, setIsSaving] = useState(false);

  const handleSaveProfile = () => {
    setIsSaving(true);
    setTimeout(() => {
      setIsSaving(false);
      alert('Profile updated successfully');
    }, 500);
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 bg-primary/20 rounded-lg flex items-center justify-center">
            <SettingsIcon size={24} className="text-primary" />
          </div>
          <div>
            <h1 className="text-3xl font-bold">Settings</h1>
            <p className="text-muted-foreground">Manage your account and preferences</p>
          </div>
        </div>

        <Tabs defaultValue="profile" className="w-full">
          <TabsList className="grid w-full max-w-md grid-cols-3">
            <TabsTrigger value="profile">Profile</TabsTrigger>
            <TabsTrigger value="preferences">Preferences</TabsTrigger>
            <TabsTrigger value="advanced">Advanced</TabsTrigger>
          </TabsList>

          {/* Profile Tab */}
          <TabsContent value="profile" className="mt-6 space-y-4">
            <Card className="p-6 border-primary/20">
              <h3 className="text-lg font-semibold mb-6">Account Information</h3>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="displayName" className="mb-2 block">
                    Display Name
                  </Label>
                  <Input
                    id="displayName"
                    value={displayName}
                    onChange={(e) => setDisplayName(e.target.value)}
                    className="border-primary/30"
                  />
                </div>

                <div>
                  <Label htmlFor="email" className="mb-2 block">
                    Email Address
                  </Label>
                  <Input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="border-primary/30"
                  />
                </div>

                <Button onClick={handleSaveProfile} disabled={isSaving} className="bg-primary hover:bg-primary/90 mt-4">
                  {isSaving ? 'Saving...' : 'Save Changes'}
                </Button>
              </div>
            </Card>

            <Card className="p-6 border-primary/20">
              <h3 className="text-lg font-semibold mb-4">Password</h3>
              <p className="text-sm text-muted-foreground mb-4">Change your password regularly to keep your account secure</p>
              <Button variant="outline" className="border-primary/30 bg-transparent">
                Change Password
              </Button>
            </Card>
          </TabsContent>

          {/* Preferences Tab */}
          <TabsContent value="preferences" className="mt-6 space-y-4">
            <Card className="p-6 border-primary/20">
              <h3 className="text-lg font-semibold mb-6">Display Settings</h3>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="theme" className="mb-2 block">
                    Theme
                  </Label>
                  <select
                    id="theme"
                    value={theme}
                    onChange={(e) => setTheme(e.target.value)}
                    className="w-full px-3 py-2 border border-primary/30 rounded-lg bg-background text-foreground"
                  >
                    <option value="light">Light</option>
                    <option value="dark">Dark</option>
                    <option value="auto">Auto (System)</option>
                  </select>
                </div>
              </div>
            </Card>

            <Card className="p-6 border-primary/20">
              <h3 className="text-lg font-semibold mb-6">Notifications</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Email Notifications</p>
                    <p className="text-sm text-muted-foreground">Receive updates about uploads and analysis</p>
                  </div>
                  <Switch checked={notifications} onCheckedChange={setNotifications} />
                </div>
              </div>
            </Card>
          </TabsContent>

          {/* Advanced Tab */}
          <TabsContent value="advanced" className="mt-6 space-y-4">
            <Card className="p-6 border-primary/20">
              <h3 className="text-lg font-semibold mb-4">Data Management</h3>
              <div className="space-y-4">
                <div>
                  <p className="font-medium mb-2">Export Data</p>
                  <p className="text-sm text-muted-foreground mb-4">Download all your uploaded files and analysis results</p>
                  <Button variant="outline" className="border-primary/30 bg-transparent">
                    Export All Data
                  </Button>
                </div>

                <div className="border-t border-primary/10 pt-4">
                  <p className="font-medium mb-2">Clear Cache</p>
                  <p className="text-sm text-muted-foreground mb-4">Remove locally stored data and history</p>
                  <Button
                    variant="outline"
                    className="border-primary/30 bg-transparent"
                    onClick={() => {
                      localStorage.removeItem('uploadHistory');
                      alert('Cache cleared');
                    }}
                  >
                    Clear Cache
                  </Button>
                </div>
              </div>
            </Card>

            <Card className="p-6 border-destructive/30 bg-destructive/5">
              <h3 className="text-lg font-semibold mb-4 text-destructive">Danger Zone</h3>
              <div>
                <p className="font-medium mb-2">Delete Account</p>
                <p className="text-sm text-muted-foreground mb-4">Permanently delete your account and all associated data</p>
                <Button variant="destructive">Delete Account</Button>
              </div>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  );
}
