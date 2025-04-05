import React, { useState } from 'react';
import {
  Container,
  Box,
  Typography,
  Tabs,
  Tab,
  Button,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Paper,
} from '@mui/material';
import { FileUpload } from '@/components/FileUpload';
import { DataTable } from '@/components/DataTable';
import { analyzeBalance, downloadData } from '@/lib/api';
import dynamic from 'next/dynamic';
import { PlotData } from 'plotly.js';

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
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
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

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleDownload = (data: any[], filename: string) => {
    downloadData(data, filename);
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Analisi Bilancio
      </Typography>

      <Paper sx={{ p: 3, mb: 4 }}>
        <Box sx={{ mb: 3 }}>
          <FileUpload onFileSelect={handleFileSelect} />
        </Box>

        <Box sx={{ mb: 3 }}>
          <FormControl fullWidth>
            <InputLabel>Tipo di Matching</InputLabel>
            <Select
              value={matchingType}
              label="Tipo di Matching"
              onChange={(e) => setMatchingType(e.target.value as any)}
            >
              <MenuItem value="fuzzy">Fuzzy (Base)</MenuItem>
              <MenuItem value="embedding">Embedding (Premium)</MenuItem>
              <MenuItem value="gpt">GPT (Premium)</MenuItem>
            </Select>
          </FormControl>
        </Box>

        <Button
          variant="contained"
          onClick={handleAnalyze}
          disabled={!selectedFile || loading}
          fullWidth
        >
          {loading ? <CircularProgress size={24} /> : 'Analizza Bilancio'}
        </Button>
      </Paper>

      {analysisResult && (
        <Box sx={{ width: '100%' }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={tabValue} onChange={handleTabChange}>
              <Tab label="Dati Grezzi" />
              <Tab label="Dati Standardizzati" />
              <Tab label="Indici Finanziari" />
              <Tab label="Grafici" />
            </Tabs>
          </Box>

          <TabPanel value={tabValue} index={0}>
            <Box sx={{ mb: 2 }}>
              <Button
                variant="outlined"
                onClick={() => handleDownload(analysisResult.raw_data, 'raw_data.csv')}
              >
                Scarica CSV
              </Button>
            </Box>
            <DataTable
              data={analysisResult.raw_data}
              columns={Object.keys(analysisResult.raw_data[0] || {}).map((key) => ({
                field: key,
                headerName: key,
              }))}
            />
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <Box sx={{ mb: 2 }}>
              <Button
                variant="outlined"
                onClick={() =>
                  handleDownload(analysisResult.standardized_data, 'standardized_data.csv')
                }
              >
                Scarica CSV
              </Button>
            </Box>
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
                const chartData: Partial<PlotData>[] = [{
                  type: 'bar',
                  x: Array.from(Object.keys(indices)) as string[],
                  y: Array.from(Object.values(indices)).map(Number) as number[],
                }];

                return (
                  <Box key={year} sx={{ mb: 4 }}>
                    <Typography variant="h6" gutterBottom>
                      {year}
                    </Typography>
                    <Plot
                      data={chartData}
                      layout={{
                        title: `Indici Finanziari ${year}`,
                        xaxis: { title: 'Indice' },
                        yaxis: { title: 'Valore' }
                      }}
                      style={{ width: '100%', height: '400px' }}
                    />
                  </Box>
                );
              }
            )}
          </TabPanel>
        </Box>
      )}
    </Container>
  );
} 