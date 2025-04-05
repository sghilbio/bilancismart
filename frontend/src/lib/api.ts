const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface AnalysisResponse {
  raw_data: any[];
  standardized_data: any[];
  financial_indices: {
    [year: string]: {
      [index: string]: number;
    };
  };
}

export async function analyzeBalance(file: File, matchingType: 'fuzzy' | 'embedding' | 'gpt'): Promise<AnalysisResponse> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('matching_type', matchingType);

  const response = await fetch(`${API_BASE_URL}/api/v1/analyze`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Failed to analyze balance sheet');
  }

  return response.json();
}

export function downloadData(data: any[], filename: string): void {
  const csvContent = convertToCSV(data);
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  if (link.download !== undefined) {
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}

function convertToCSV(data: any[]): string {
  if (data.length === 0) return '';

  const headers = Object.keys(data[0]);
  const rows = data.map(obj => headers.map(header => obj[header]));

  const csvArray = [
    headers.join(','),
    ...rows.map(row => row.map(formatCSVValue).join(','))
  ];

  return csvArray.join('\n');
}

function formatCSVValue(value: any): string {
  if (value === null || value === undefined) return '';
  const stringValue = String(value);
  if (stringValue.includes(',') || stringValue.includes('"') || stringValue.includes('\n')) {
    return `"${stringValue.replace(/"/g, '""')}"`;
  }
  return stringValue;
} 