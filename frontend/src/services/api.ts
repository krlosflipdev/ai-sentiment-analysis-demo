import axios from 'axios';
import type {
  PaginatedResponse,
  SingleResponse,
  SentimentRecord,
  SentimentStats,
  TimelinePoint,
  SentimentFilters,
  TimelineGranularity,
} from '../types/sentiment';

const API_URL = import.meta.env.VITE_API_URL || '/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Sentiment API service.
 * Provides typed methods for all sentiment-related API endpoints.
 */
export const sentimentApi = {
  /**
   * Get paginated sentiments with optional filters.
   * @param page - Page number (1-indexed)
   * @param limit - Items per page
   * @param filters - Optional filter parameters
   */
  getSentiments: async (
    page: number = 1,
    limit: number = 20,
    filters?: SentimentFilters
  ): Promise<PaginatedResponse<SentimentRecord>> => {
    const params = new URLSearchParams({
      page: String(page),
      limit: String(limit),
    });

    if (filters?.sentiment) params.set('sentiment', filters.sentiment);
    if (filters?.source) params.set('source', filters.source);
    if (filters?.date_from) params.set('date_from', filters.date_from);
    if (filters?.date_to) params.set('date_to', filters.date_to);

    const response = await api.get<PaginatedResponse<SentimentRecord>>(
      `/sentiments?${params}`
    );
    return response.data;
  },

  /**
   * Get a single sentiment by ID.
   * @param id - Sentiment record ID
   */
  getSentiment: async (id: string): Promise<SingleResponse<SentimentRecord>> => {
    const response = await api.get<SingleResponse<SentimentRecord>>(
      `/sentiments/${id}`
    );
    return response.data;
  },

  /**
   * Get aggregated sentiment statistics.
   */
  getStats: async (): Promise<SingleResponse<SentimentStats>> => {
    const response = await api.get<SingleResponse<SentimentStats>>('/stats/summary');
    return response.data;
  },

  /**
   * Get timeline data for charts.
   * @param granularity - Time bucket size (hour, day, week, month)
   * @param dateFrom - Optional start date (ISO string)
   * @param dateTo - Optional end date (ISO string)
   */
  getTimeline: async (
    granularity: TimelineGranularity = 'day',
    dateFrom?: string,
    dateTo?: string
  ): Promise<SingleResponse<TimelinePoint[]>> => {
    const params = new URLSearchParams({ granularity });
    if (dateFrom) params.set('date_from', dateFrom);
    if (dateTo) params.set('date_to', dateTo);

    const response = await api.get<SingleResponse<TimelinePoint[]>>(
      `/stats/timeline?${params}`
    );
    return response.data;
  },

  /**
   * Check API health status.
   */
  healthCheck: async (): Promise<{ status: string }> => {
    const response = await api.get<{ status: string }>('/health');
    return response.data;
  },
};

export default api;
