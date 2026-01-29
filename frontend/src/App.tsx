import type { FC } from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

interface HealthResponse {
  status: string;
  version: string;
}

const App: FC = () => {
  const { data, isLoading, error } = useQuery<HealthResponse>({
    queryKey: ['health'],
    queryFn: async () => {
      const response = await axios.get<HealthResponse>(`${API_URL}/health`);
      return response.data;
    },
  });

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          Sentiment Analysis Dashboard
        </h1>
        <p className="text-gray-600 mb-8">Real-time sentiment analysis using NLP/ML</p>

        <div className="bg-white rounded-lg shadow-md p-6 max-w-md mx-auto">
          <h2 className="text-lg font-semibold mb-2">API Status</h2>
          {isLoading && <p className="text-gray-500">Checking connection...</p>}
          {error && (
            <p className="text-red-500">
              Not connected - Start the backend server
            </p>
          )}
          {data && (
            <p className="text-green-500">
              Connected ({data.status} - {data.version})
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
