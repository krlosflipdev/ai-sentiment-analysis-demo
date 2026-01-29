import type { FC } from 'react';
import { Header, DashboardLayout } from '../components/layout';
import { StatsGrid } from '../components/cards';
import { SentimentPie, TimelineChart } from '../components/charts';
import { SentimentsTable } from '../components/table';
import { useDarkMode } from '../hooks/use-dark-mode';

/**
 * Main dashboard page showing sentiment analysis metrics and data.
 */
export const Dashboard: FC = () => {
  const [isDark, toggleDark] = useDarkMode();

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      <Header isDark={isDark} onToggleDark={toggleDark} />

      <DashboardLayout>
        {/* Stats Cards */}
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Overview
          </h2>
          <StatsGrid />
        </section>

        {/* Charts */}
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Analytics
          </h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-4">
                Sentiment Distribution
              </h3>
              <SentimentPie />
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-4">
                Sentiment Over Time
              </h3>
              <TimelineChart granularity="day" />
            </div>
          </div>
        </section>

        {/* Sentiments Table */}
        <section>
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Recent Sentiments
          </h2>
          <SentimentsTable />
        </section>
      </DashboardLayout>
    </div>
  );
};
