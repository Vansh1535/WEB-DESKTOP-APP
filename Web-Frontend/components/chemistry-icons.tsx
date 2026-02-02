export function ChemistryIcon({ size = 24, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      {/* Molecule structure - three spheres connected */}
      <circle cx="12" cy="8" r="2" />
      <circle cx="6" cy="14" r="2" />
      <circle cx="18" cy="14" r="2" />
      {/* Connection lines */}
      <line x1="11" y1="9.5" x2="7" y2="13" />
      <line x1="13" y1="9.5" x2="17" y2="13" />
      <line x1="6" y1="16" x2="18" y2="16" />
    </svg>
  );
}

export function BeakerIcon({ size = 24, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      {/* Beaker body */}
      <path d="M 7 4 L 5 6 L 5 20 Q 5 22 7 22 L 17 22 Q 19 22 19 20 L 19 6 L 17 4 Z" fill="none" />
      {/* Beaker mouth */}
      <line x1="7" y1="4" x2="17" y2="4" />
      {/* Liquid inside */}
      <path d="M 6 14 Q 6 16 7 17 L 17 17 Q 18 16 18 14" fill="currentColor" opacity="0.2" />
      <path d="M 6 14 Q 6 16 7 17 L 17 17 Q 18 16 18 14" stroke="currentColor" fill="none" />
    </svg>
  );
}

export function AtomIcon({ size = 24, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      {/* Nucleus */}
      <circle cx="12" cy="12" r="2" />
      {/* Electron orbits */}
      <ellipse cx="12" cy="12" rx="8" ry="3" />
      <ellipse cx="12" cy="12" rx="8" ry="3" transform="rotate(60 12 12)" />
      <ellipse cx="12" cy="12" rx="8" ry="3" transform="rotate(120 12 12)" />
      {/* Electrons */}
      <circle cx="20" cy="12" r="1.5" fill="currentColor" />
      <circle cx="8" cy="17" r="1.5" fill="currentColor" />
      <circle cx="8" cy="7" r="1.5" fill="currentColor" />
    </svg>
  );
}

export function FlaskIcon({ size = 24, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      {/* Flask top */}
      <line x1="9" y1="3" x2="15" y2="3" />
      <path d="M 9 3 L 10 8 Q 10 10 9 12 L 8 18 Q 8 21 10 21 L 14 21 Q 16 21 16 18 L 15 12 Q 14 10 14 8 L 15 3" fill="none" />
      {/* Liquid */}
      <path d="M 9 12 L 8 18 Q 8 21 10 21 L 14 21 Q 16 21 16 18 L 15 12" fill="currentColor" opacity="0.15" />
    </svg>
  );
}

export function DataIcon({ size = 24, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      {/* Grid lines */}
      <line x1="3" y1="6" x2="21" y2="6" />
      <line x1="3" y1="12" x2="21" y2="12" />
      <line x1="3" y1="18" x2="21" y2="18" />
      <line x1="9" y1="3" x2="9" y2="21" />
      <line x1="15" y1="3" x2="15" y2="21" />
    </svg>
  );
}

export function ChartLineIcon({ size = 24, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      {/* Axes */}
      <line x1="3" y1="3" x2="3" y2="21" />
      <line x1="3" y1="21" x2="21" y2="21" />
      {/* Data line */}
      <polyline points="7,16 10,10 13,12 17,5 21,8" fill="none" />
      {/* Data points */}
      <circle cx="7" cy="16" r="1.5" fill="currentColor" />
      <circle cx="10" cy="10" r="1.5" fill="currentColor" />
      <circle cx="13" cy="12" r="1.5" fill="currentColor" />
      <circle cx="17" cy="5" r="1.5" fill="currentColor" />
      <circle cx="21" cy="8" r="1.5" fill="currentColor" />
    </svg>
  );
}

export function UploadIcon({ size = 24, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      {/* Upload arrow */}
      <path d="M 12 3 L 12 15" />
      <path d="M 7 10 L 12 5 L 17 10" fill="none" />
      {/* Document box */}
      <rect x="3" y="15" width="18" height="6" rx="1" />
      <line x1="9" y1="18" x2="15" y2="18" />
    </svg>
  );
}

export function HistoryIcon({ size = 24, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      {/* Clock face */}
      <circle cx="12" cy="13" r="8" />
      {/* Clock hands */}
      <line x1="12" y1="9" x2="12" y2="13" />
      <line x1="12" y1="13" x2="15" y2="13" />
      {/* Arrow indicating history */}
      <path d="M 5 8 Q 5 5 8 5" fill="none" />
    </svg>
  );
}

export function FileIcon({ size = 24, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      {/* File document */}
      <path d="M 4 4 L 4 20 Q 4 22 6 22 L 18 22 Q 20 22 20 20 L 20 9 L 15 4 Z" fill="none" />
      <path d="M 20 9 L 15 4 L 15 9 Z" fill="none" />
      {/* Document lines */}
      <line x1="8" y1="12" x2="16" y2="12" />
      <line x1="8" y1="16" x2="16" y2="16" />
      <line x1="8" y1="20" x2="12" y2="20" />
    </svg>
  );
}

export function SettingsIcon({ size = 24, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      {/* Center gear */}
      <circle cx="12" cy="12" r="3" />
      {/* Outer gear teeth */}
      <circle cx="12" cy="1" r="1" />
      <circle cx="12" cy="23" r="1" />
      <circle cx="1" cy="12" r="1" />
      <circle cx="23" cy="12" r="1" />
      <circle cx="4" cy="4" r="1" />
      <circle cx="20" cy="20" r="1" />
      <circle cx="20" cy="4" r="1" />
      <circle cx="4" cy="20" r="1" />
      {/* Connection lines */}
      <line x1="12" y1="3" x2="12" y2="5" />
      <line x1="12" y1="19" x2="12" y2="21" />
      <line x1="3" y1="12" x2="5" y2="12" />
      <line x1="19" y1="12" x2="21" y2="12" />
    </svg>
  );
}

export function LogoutIcon({ size = 24, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      {/* Door/box */}
      <rect x="3" y="3" width="12" height="18" rx="1" />
      {/* Door handle */}
      <circle cx="16" cy="12" r="1.5" fill="currentColor" />
      {/* Exit arrow */}
      <line x1="14" y1="12" x2="20" y2="12" />
      <path d="M 19 10 L 21 12 L 19 14" fill="none" />
    </svg>
  );
}

export function MenuIcon({ size = 24, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      <line x1="3" y1="6" x2="21" y2="6" />
      <line x1="3" y1="12" x2="21" y2="12" />
      <line x1="3" y1="18" x2="21" y2="18" />
    </svg>
  );
}

export function XIcon({ size = 24, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      <line x1="18" y1="6" x2="6" y2="18" />
      <line x1="6" y1="6" x2="18" y2="18" />
    </svg>
  );
}

export function PrintIcon({ size = 24, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      {/* Printer body */}
      <rect x="3" y="7" width="18" height="12" rx="1" />
      {/* Paper output */}
      <rect x="6" y="3" width="12" height="4" />
      {/* Paper tray bottom */}
      <line x1="3" y1="19" x2="21" y2="19" />
      {/* Dots pattern indicating printed page */}
      <circle cx="8" cy="12" r="0.5" fill="currentColor" />
      <circle cx="12" cy="12" r="0.5" fill="currentColor" />
      <circle cx="16" cy="12" r="0.5" fill="currentColor" />
      <circle cx="8" cy="15" r="0.5" fill="currentColor" />
      <circle cx="12" cy="15" r="0.5" fill="currentColor" />
      <circle cx="16" cy="15" r="0.5" fill="currentColor" />
    </svg>
  );
}

export function DownloadIcon({ size = 24, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      {/* Download arrow */}
      <path d="M 12 3 L 12 15" />
      <path d="M 7 10 L 12 15 L 17 10" fill="none" />
      {/* Document box */}
      <rect x="3" y="17" width="18" height="4" rx="1" />
    </svg>
  );
}

export function ArrowLeftIcon({ size = 24, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      {/* Arrow pointing left */}
      <path d="M 19 12 L 5 12" />
      <path d="M 12 19 L 5 12 L 12 5" />
    </svg>
  );
}
