import { useQuery, keepPreviousData } from '@tanstack/react-query';
import { sentimentApi } from '../services/api';
import type { SentimentFilters, TimelineGranularity } from '../types/sentiment';

/**
 * Hook for fetching paginated sentiments list.
 * @param page - Page number (1-indexed)
 * @param limit - Items per page
 * @param filters - Optional filter parameters
 */
export function useSentiments(
  page: number = 1,
  limit: number = 20,
  filters?: SentimentFilters
) {
  return useQuery({
    queryKey: ['sentiments', page, limit, filters],
    queryFn: () => sentimentApi.getSentiments(page, limit, filters),
    placeholderData: keepPreviousData,
    staleTime: 30_000, // 30 seconds
  });
}

/**
 * Hook for fetching aggregated sentiment statistics.
 * Auto-refreshes every minute.
 */
export function useStats() {
  return useQuery({
    queryKey: ['stats'],
    queryFn: () => sentimentApi.getStats(),
    staleTime: 60_000, // 1 minute
    refetchInterval: 60_000, // Auto-refresh every minute
  });
}

/**
 * Hook for fetching timeline chart data.
 * @param granularity - Time bucket size
 * @param dateFrom - Optional start date
 * @param dateTo - Optional end date
 */
export function useTimeline(
  granularity: TimelineGranularity = 'day',
  dateFrom?: string,
  dateTo?: string
) {
  return useQuery({
    queryKey: ['timeline', granularity, dateFrom, dateTo],
    queryFn: () => sentimentApi.getTimeline(granularity, dateFrom, dateTo),
    staleTime: 60_000, // 1 minute
  });
}

/**
 * Hook for fetching a single sentiment record.
 * @param id - Sentiment record ID
 */
export function useSentiment(id: string) {
  return useQuery({
    queryKey: ['sentiment', id],
    queryFn: () => sentimentApi.getSentiment(id),
    enabled: !!id,
  });
}

/**
 * Hook for checking API health status.
 */
export function useHealthCheck() {
  return useQuery({
    queryKey: ['health'],
    queryFn: () => sentimentApi.healthCheck(),
    staleTime: 30_000,
    retry: 1,
  });
}
