import type { FC } from 'react';
import type { SentimentFilters, SentimentLabel } from '../../types/sentiment';

interface FiltersProps {
  /** Current filter values */
  filters: SentimentFilters;
  /** Filter change callback */
  onChange: (filters: SentimentFilters) => void;
}

/**
 * Filter controls for the sentiments table.
 */
export const Filters: FC<FiltersProps> = ({ filters, onChange }) => {
  const handleSentimentChange = (value: string) => {
    onChange({
      ...filters,
      sentiment: value ? (value as SentimentLabel) : undefined,
    });
  };

  const handleSourceChange = (value: string) => {
    onChange({
      ...filters,
      source: value || undefined,
    });
  };

  const handleClear = () => {
    onChange({});
  };

  const hasFilters = filters.sentiment || filters.source;

  return (
    <div className="flex flex-wrap items-center gap-4">
      <div>
        <label
          htmlFor="sentiment-filter"
          className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
        >
          Sentiment
        </label>
        <select
          id="sentiment-filter"
          value={filters.sentiment ?? ''}
          onChange={(e) => handleSentimentChange(e.target.value)}
          className="block w-32 px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600
                     rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-white
                     focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="">All</option>
          <option value="positive">Positive</option>
          <option value="negative">Negative</option>
          <option value="neutral">Neutral</option>
        </select>
      </div>

      <div>
        <label
          htmlFor="source-filter"
          className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
        >
          Source
        </label>
        <select
          id="source-filter"
          value={filters.source ?? ''}
          onChange={(e) => handleSourceChange(e.target.value)}
          className="block w-32 px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600
                     rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-white
                     focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="">All</option>
          <option value="twitter">Twitter</option>
          <option value="reddit">Reddit</option>
        </select>
      </div>

      {hasFilters && (
        <div className="flex items-end">
          <button
            onClick={handleClear}
            className="px-3 py-1.5 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
          >
            Clear filters
          </button>
        </div>
      )}
    </div>
  );
};
