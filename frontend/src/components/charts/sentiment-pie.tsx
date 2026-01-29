import type { FC } from 'react';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { useStats } from '../../hooks/use-sentiments';
import { LoadingSpinner } from '../common';

// Register Chart.js components
ChartJS.register(ArcElement, Tooltip, Legend);

/**
 * Doughnut chart showing sentiment distribution.
 */
export const SentimentPie: FC = () => {
  const { data, isLoading, error } = useStats();
  const stats = data?.data;

  if (isLoading) {
    return (
      <div className="h-64 flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-64 flex items-center justify-center text-red-500 dark:text-red-400">
        Failed to load chart data
      </div>
    );
  }

  const chartData = {
    labels: ['Positive', 'Negative', 'Neutral'],
    datasets: [
      {
        data: [
          stats?.positive_count ?? 0,
          stats?.negative_count ?? 0,
          stats?.neutral_count ?? 0,
        ],
        backgroundColor: ['#22c55e', '#ef4444', '#6b7280'],
        borderColor: ['#16a34a', '#dc2626', '#4b5563'],
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          padding: 20,
          usePointStyle: true,
        },
      },
      tooltip: {
        callbacks: {
          label: (context: { label: string; raw: number }) => {
            const total = stats?.total_count ?? 0;
            const percentage = total > 0 ? ((context.raw / total) * 100).toFixed(1) : 0;
            return `${context.label}: ${context.raw.toLocaleString()} (${percentage}%)`;
          },
        },
      },
    },
  };

  return (
    <div className="h-64">
      <Doughnut data={chartData} options={options} />
    </div>
  );
};
