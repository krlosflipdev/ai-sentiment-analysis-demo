import { useState, type FC } from 'react';
import { useSentiments } from '../../hooks/use-sentiments';
import { SentimentBadge } from './sentiment-badge';
import { Pagination } from './pagination';
import { Filters } from './filters';
import { EmptyState } from '../common';
import type { SentimentFilters } from '../../types/sentiment';

/**
 * Paginated table of sentiment records with filters.
 */
export const SentimentsTable: FC = () => {
  const [page, setPage] = useState(1);
  const [filters, setFilters] = useState<SentimentFilters>({});
  const limit = 10;

  const { data, isLoading, error } = useSentiments(page, limit, filters);
  const records = data?.data ?? [];
  const meta = data?.meta;

  // Reset to page 1 when filters change
  const handleFilterChange = (newFilters: SentimentFilters) => {
    setFilters(newFilters);
    setPage(1);
  };

  if (error) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div className="text-red-500 dark:text-red-400">
          Failed to load sentiments
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <Filters filters={filters} onChange={handleFilterChange} />
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 dark:bg-gray-700/50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Text
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Sentiment
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Score
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Source
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Date
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
            {isLoading ? (
              [...Array(limit)].map((_, i) => (
                <tr key={i}>
                  <td colSpan={5} className="px-4 py-3">
                    <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
                  </td>
                </tr>
              ))
            ) : records.length === 0 ? (
              <tr>
                <td colSpan={5}>
                  <EmptyState
                    title="No sentiments found"
                    description="Try adjusting your filters or wait for the worker to fetch new data."
                  />
                </td>
              </tr>
            ) : (
              records.map((record) => (
                <tr
                  key={record.id}
                  className="hover:bg-gray-50 dark:hover:bg-gray-700/50"
                >
                  <td className="px-4 py-3 text-sm text-gray-900 dark:text-white max-w-md">
                    <p className="truncate" title={record.text}>
                      {record.text}
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <SentimentBadge sentiment={record.sentiment} />
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                    {(record.score * 100).toFixed(1)}%
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400 capitalize">
                    {record.source}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                    {new Date(record.created_at).toLocaleDateString()}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {meta && meta.total > 0 && (
        <div className="p-4 border-t border-gray-200 dark:border-gray-700">
          <Pagination
            page={meta.page}
            totalPages={meta.total_pages}
            total={meta.total}
            onPageChange={setPage}
          />
        </div>
      )}
    </div>
  );
};
