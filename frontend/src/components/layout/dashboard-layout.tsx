import type { FC, ReactNode } from 'react';

interface DashboardLayoutProps {
  /** Child content */
  children: ReactNode;
}

/**
 * Main dashboard layout wrapper.
 */
export const DashboardLayout: FC<DashboardLayoutProps> = ({ children }) => {
  return (
    <main className="flex-1 overflow-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </div>
    </main>
  );
};
