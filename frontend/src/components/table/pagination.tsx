import type { FC } from 'react';

interface PaginationProps {
  /** Current page number */
  page: number;
  /** Total number of pages */
  totalPages: number;
  /** Total number of items */
  total: number;
  /** Page change callback */
  onPageChange: (page: number) => void;
}

/**
 * Pagination controls for the sentiments table.
 */
export const Pagination: FC<PaginationProps> = ({
  page,
  totalPages,
  total,
  onPageChange,
}) => {
  const canGoPrev = page > 1;
  const canGoNext = page < totalPages;

  return (
    <div className="flex items-center justify-between">
      <p className="text-sm text-gray-600 dark:text-gray-400">
        Page {page} of {totalPages} ({total.toLocaleString()} total)
      </p>
      <div className="flex gap-2">
        <button
          onClick={() => onPageChange(page - 1)}
          disabled={!canGoPrev}
          className="px-3 py-1 text-sm rounded border border-gray-300 dark:border-gray-600
                     disabled:opacity-50 disabled:cursor-not-allowed
                     hover:bg-gray-50 dark:hover:bg-gray-700
                     bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200"
        >
          Previous
        </button>
        <button
          onClick={() => onPageChange(page + 1)}
          disabled={!canGoNext}
          className="px-3 py-1 text-sm rounded border border-gray-300 dark:border-gray-600
                     disabled:opacity-50 disabled:cursor-not-allowed
                     hover:bg-gray-50 dark:hover:bg-gray-700
                     bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200"
        >
          Next
        </button>
      </div>
    </div>
  );
};
