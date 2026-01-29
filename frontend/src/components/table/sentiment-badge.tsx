import type { FC } from 'react';
import type { SentimentLabel } from '../../types/sentiment';

interface SentimentBadgeProps {
  /** Sentiment classification */
  sentiment: SentimentLabel;
}

const badgeStyles: Record<SentimentLabel, string> = {
  positive: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
  negative: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
  neutral: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
};

/**
 * Color-coded badge for sentiment labels.
 */
export const SentimentBadge: FC<SentimentBadgeProps> = ({ sentiment }) => {
  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${badgeStyles[sentiment]}`}
    >
      {sentiment}
    </span>
  );
};
