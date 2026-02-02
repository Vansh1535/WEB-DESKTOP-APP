# Vibrant Neon Comic Chemistry Theme Guide

## Overview
ChemData now features a vibrant neon color palette with full light/dark mode support. The theme emphasizes bold, energetic colors while maintaining professional credibility for scientific work.

## Color Palette

### Light Mode
- **Background**: Clean white with minimal saturation
- **Foreground**: Deep navy/purple text
- **Primary (Neon Blue)**: `oklch(0.50 0.30 250)` - Main action elements, buttons, accents
- **Secondary (Neon Purple/Magenta)**: `oklch(0.55 0.32 290)` - Alternative accent
- **Accent (Neon Lime Green)**: `oklch(0.80 0.28 110)` - Analysis highlights, data emphasis
- **Destructive (Neon Red)**: `oklch(0.60 0.28 30)` - Alerts, warnings

### Dark Mode
- **Background**: Very dark navy `oklch(0.08 0.05 270)` - High contrast
- **Foreground**: Near white text `oklch(0.97 0.01 0)`
- **Primary (Bright Cyan)**: `oklch(0.70 0.32 250)` - Vibrant on dark background
- **Secondary (Bright Magenta)**: `oklch(0.72 0.35 290)` - Energetic accent
- **Accent (Bright Lime)**: `oklch(0.88 0.32 110)` - Neon highlighting
- **Destructive (Neon Red)**: `oklch(0.78 0.32 30)` - High contrast warnings

## Chart Colors
Enhanced vibrant colors for data visualization:
- **Chart 1**: Neon Red/Orange
- **Chart 2**: Neon Yellow/Gold
- **Chart 3**: Neon Blue
- **Chart 4**: Neon Lime Green
- **Chart 5**: Neon Magenta

## Features

### Theme Toggle
- Located in top navbar next to user info
- Sun icon for light mode
- Moon icon for dark mode
- Persists user preference in localStorage
- Respects system preference on first visit

### Responsive Application
- All components automatically adapt to selected theme
- Smooth transitions between light and dark modes
- Consistent saturation and vibrance in both modes
- Professional appearance while maintaining comic energy

### Typography
- **Headings**: Font-black (900 weight), uppercase, wide letter spacing
- **Body**: Semi-bold to bold weights
- **Accents**: All-caps for emphasis in secondary text

### Visual Elements
- 2-3px borders for comic book feel
- Gradient backgrounds on cards and containers
- Bold, energetic hover states with scale transforms
- Neon glow effects in dark mode

## Implementation

### Using the Theme
All Tailwind classes work with the theme:
```tsx
<div className="bg-primary text-primary-foreground">
  Primary button
</div>

<div className="bg-accent text-accent-foreground">
  Accent text
</div>

<div className="border-primary/30">
  Border with opacity
</div>
```

### Dark Mode
The `.dark` class on `<html>` element automatically applies dark mode:
```tsx
// User clicks theme toggle
// ThemeToggle component adds/removes 'dark' class
// CSS variables automatically switch
```

### Custom Colors
Additional variables available:
- `--sidebar`: Sidebar background
- `--border`: Border colors
- `--input`: Input backgrounds
- `--muted`: Muted backgrounds
- `--destructive`: Error/delete actions

## Files Modified
- `/app/globals.css` - Updated color definitions
- `/components/theme-toggle.tsx` - New theme toggle component
- `/components/top-navbar.tsx` - Added theme toggle to navbar
- `/app/layout.tsx` - Added theme initialization script

## Performance
- Theme toggle uses localStorage (no database calls)
- Initialization script prevents flash of wrong theme
- CSS variables for instant theme switching
- No re-renders required for theme changes

## Accessibility
- Color contrast meets WCAG AA standards
- Both modes provide readable text on backgrounds
- Theme preference respects system settings
- Clear visual indicators for interactive elements

## Future Enhancements
- Additional theme presets (e.g., monochrome, high contrast)
- Custom color picker for team branding
- Per-user theme preferences in database
- Theme scheduling (auto-switch based on time)
