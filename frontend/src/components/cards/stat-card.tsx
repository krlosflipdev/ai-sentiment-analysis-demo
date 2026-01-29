import type { FC, ReactNode } from 'react';

interface StatCardProps {
  /** Card title */
  title: string;
  /** Main value to display */
  value: string | number;
  /** Optional subtitle or secondary info */
  subtitle?: string;
  /** Optional icon */
  icon?: ReactNode;
  /** Color variant */
  variant?: 'positive' | 'negative' | 'neutral' | 'default';
  /** Loading state */
  isLoading?: boolean;
}

const variantStyles = {
  positive: {
    bg: 'bg-green-50 dark:bg-green-900/20',
    text: 'text-green-700 dark:text-green-400',
    border: 'border-green-200 dark:border-green-800',
  },
  negative: {
    bg: 'bg-red-50 dark:bg-red-900/20',
    text: 'text-red-700 dark:text-red-400',
    border: 'border-red-200 dark:border-red-800',
  },
  neutral: {
    bg: 'bg-gray-50 dark:bg-gray-800',
    text: 'text-gray-700 dark:text-gray-300',
    border: 'border-gray-200 dark:border-gray-700',
  },
  default: {
    bg: 'bg-blue-50 dark:bg-blue-900/20',
    text: 'text-blue-700 dark:text-blue-400',
    border: 'border-blue-200 dark:border-blue-800',
  },
};

/**
 * Displays a single metric in a styled card.
 */
export const StatCard: FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  icon,
  variant = 'default',
  isLoading = false,
}) => {
  const styles = variantStyles[variant];

  return (
    <div
      className={`rounded-lg border p-6 ${styles.bg} ${styles.border} ${styles.text}`}
    >
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium opacity-75">{title}</p>
          {isLoading ? (
            <div className="h-9 w-20 animate-pulse bg-current opacity-20 rounded mt-1" />
          ) : (
            <p className="text-3xl font-bold mt-1">{value}</p>
          )}
          {subtitle && (
            <p className="text-sm mt-1 opacity-75">{subtitle}</p>
          )}
        </div>
        {icon && <div className="text-4xl opacity-50 ml-4">{icon}</div>}
      </div>
    </div>
  );
};
