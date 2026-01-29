import type { FC } from 'react';
import { useStats } from '../../hooks/use-sentiments';
import { StatCard } from './stat-card';

/**
 * Grid of 4 stat cards showing overall sentiment metrics.
 */
export const StatsGrid: FC = () => {
  const { data, isLoading, error } = useStats();
  const stats = data?.data;

  if (error) {
    return (
      <div className="text-red-500 dark:text-red-400 p-4 bg-red-50 dark:bg-red-900/20 rounded-lg">
        Failed to load statistics
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <StatCard
        title="Total Analyzed"
        value={stats?.total_count.toLocaleString() ?? 0}
        variant="default"
        isLoading={isLoading}
      />
      <StatCard
        title="Positive"
        value={`${stats?.positive_percentage.toFixed(1) ?? 0}%`}
        subtitle={`${stats?.positive_count.toLocaleString() ?? 0} posts`}
        variant="positive"
        isLoading={isLoading}
      />
      <StatCard
        title="Negative"
        value={`${stats?.negative_percentage.toFixed(1) ?? 0}%`}
        subtitle={`${stats?.negative_count.toLocaleString() ?? 0} posts`}
        variant="negative"
        isLoading={isLoading}
      />
      <StatCard
        title="Neutral"
        value={`${stats?.neutral_percentage.toFixed(1) ?? 0}%`}
        subtitle={`${stats?.neutral_count.toLocaleString() ?? 0} posts`}
        variant="neutral"
        isLoading={isLoading}
      />
    </div>
  );
};
