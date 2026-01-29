/** Sentiment classification labels */
export type SentimentLabel = 'positive' | 'negative' | 'neutral';

/** A single sentiment analysis record */
export interface SentimentRecord {
  id: string;
  text: string;
  sentiment: SentimentLabel;
  score: number;
  source: string;
  created_at: string;
}

/** Pagination metadata */
export interface PaginationMeta {
  page: number;
  limit: number;
  total: number;
  total_pages: number;
}

/** Paginated API response */
export interface PaginatedResponse<T> {
  data: T[];
  meta: PaginationMeta;
}

/** Single item API response */
export interface SingleResponse<T> {
  data: T;
}

/** Aggregated sentiment statistics */
export interface SentimentStats {
  total_count: number;
  positive_count: number;
  negative_count: number;
  neutral_count: number;
  positive_percentage: number;
  negative_percentage: number;
  neutral_percentage: number;
  average_score: number;
}

/** Timeline data point for charts */
export interface TimelinePoint {
  date: string;
  positive: number;
  negative: number;
  neutral: number;
  total: number;
}

/** Filter parameters for sentiments list */
export interface SentimentFilters {
  sentiment?: SentimentLabel;
  source?: string;
  date_from?: string;
  date_to?: string;
}

/** Timeline granularity options */
export type TimelineGranularity = 'hour' | 'day' | 'week' | 'month';
