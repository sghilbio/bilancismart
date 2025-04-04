import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface AnalysisResponse {
  raw_data: any[];
  standardized_data: any[];
  financial_indices: {
    [year: string]: {
      [index: string]: number;
    };
  };
}

export const analyzeBalance = async (
  file: File,
  matchingType: 'fuzzy' | 'embedding' | 'gpt'
): Promise<AnalysisResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('matching_type', matchingType);

  const response = await api.post<AnalysisResponse>('/api/v1/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const downloadData = async (
  data: any[],
  filename: string
): Promise<void> => {
  const blob = new Blob([JSON.stringify(data, null, 2)], {
    type: 'application/json',
  });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
}; 