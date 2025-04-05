import React, { useState } from 'react';
import { FileUpload } from '@/components/FileUpload';
import { DataTable } from '@/components/DataTable';
import { analyzeBalance, downloadData } from '@/lib/api';
import dynamic from 'next/dynamic';
import { Card } from '@/components/ui/Card';
import { Chart } from '@/components/Chart';
import Layout from '@/components/Layout';
import { Data } from 'plotly.js';

// Dynamically import Plotly to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <div className="p-6">{children}</div>}
    </div>
  );
}

export default function AnalyzePage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [matchingType, setMatchingType] = useState<'fuzzy' | 'embedding' | 'gpt'>('fuzzy');
  const [loading, setLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [tabValue, setTabValue] = useState(0);

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setLoading(true);
    try {
      const result = await analyzeBalance(selectedFile, matchingType);
      setAnalysisResult(result);
    } catch (error) {
      console.error('Error analyzing file:', error);
      // TODO: Add error handling UI
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (index: number) => {
    setTabValue(index);
  };

  const handleDownload = (data: any[], filename: string) => {
    downloadData(data, filename);
  };

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-semibold text-text-primary">
            Analisi Bilancio
          </h1>
        </div>

        <Card className="p-6 space-y-6">
          <div>
            <FileUpload onFileSelect={handleFileSelect} />
          </div>

          <div>
            <label className="block text-sm font-medium text-text-primary mb-2">
              Tipo di Matching
            </label>
            <select
              value={matchingType}
              onChange={(e) => setMatchingType(e.target.value as 'fuzzy' | 'embedding' | 'gpt')}
              className="w-full p-3 rounded-lg border border-background bg-surface text-text-primary"
            >
              <option value="fuzzy">Fuzzy (Base)</option>
              <option value="embedding">Embedding (Premium)</option>
              <option value="gpt">GPT (Premium)</option>
            </select>
          </div>

          <button
            onClick={handleAnalyze}
            disabled={!selectedFile || loading}
            className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              'Analizza Bilancio'
            )}
          </button>
        </Card>

        {analysisResult && (
          <Card className="p-6">
            <div className="border-b border-background">
              <nav className="flex space-x-8" aria-label="Tabs">
                {['Dati Grezzi', 'Dati Standardizzati', 'Indici Finanziari', 'Grafici'].map((tab, index) => (
                  <button
                    key={tab}
                    onClick={() => handleTabChange(index)}
                    className={`py-4 px-1 border-b-2 font-medium text-sm ${
                      tabValue === index
                        ? 'border-primary text-primary'
                        : 'border-transparent text-text-secondary hover:text-text-primary hover:border-text-secondary'
                    }`}
                  >
                    {tab}
                  </button>
                ))}
              </nav>
            </div>

            <div className="mt-6">
              <TabPanel value={tabValue} index={0}>
                <div className="mb-4">
                  <button
                    onClick={() => handleDownload(analysisResult.raw_data, 'raw_data.csv')}
                    className="px-4 py-2 border border-primary text-primary rounded hover:bg-primary hover:text-white transition-colors"
                  >
                    Scarica CSV
                  </button>
                </div>
                <DataTable
                  data={analysisResult.raw_data}
                  columns={Object.keys(analysisResult.raw_data[0] || {}).map((key) => ({
                    field: key,
                    headerName: key,
                  }))}
                />
              </TabPanel>

              <TabPanel value={tabValue} index={1}>
                <div className="mb-4">
                  <button
                    onClick={() => handleDownload(analysisResult.standardized_data, 'standardized_data.csv')}
                    className="px-4 py-2 border border-primary text-primary rounded hover:bg-primary hover:text-white transition-colors"
                  >
                    Scarica CSV
                  </button>
                </div>
                <DataTable
                  data={analysisResult.standardized_data}
                  columns={Object.keys(analysisResult.standardized_data[0] || {}).map(
                    (key) => ({
                      field: key,
                      headerName: key,
                    })
                  )}
                />
              </TabPanel>

              <TabPanel value={tabValue} index={2}>
                <DataTable
                  data={Object.entries(analysisResult.financial_indices).map(
                    ([year, indices]: [string, any]) => ({
                      year,
                      ...indices,
                    })
                  )}
                  columns={[
                    { field: 'year', headerName: 'Anno' },
                    ...Object.keys(
                      analysisResult.financial_indices[
                        Object.keys(analysisResult.financial_indices)[0]
                      ] || {}
                    ).map((key) => ({
                      field: key,
                      headerName: key,
                    })),
                  ]}
                />
              </TabPanel>

              <TabPanel value={tabValue} index={3}>
                {Object.entries(analysisResult.financial_indices).map(
                  ([year, indices]: [string, any]) => {
                    const chartData: Data[] = [{
                      x: Object.keys(indices),
                      y: Object.values(indices).map(Number),
                      type: 'bar',
                      name: year
                    }];

                    return (
                      <div key={year} className="mb-8">
                        <h2 className="text-xl font-semibold mb-4">
                          Indici Finanziari {year}
                        </h2>
                        <Chart
                          data={chartData}
                          layout={{
                            title: `Indici Finanziari ${year}`,
                            xaxis: { title: 'Indice' },
                            yaxis: { title: 'Valore' }
                          }}
                        />
                      </div>
                    );
                  }
                )}
              </TabPanel>
            </div>
          </Card>
        )}
      </div>
    </Layout>
  );
} 
