import React from 'react';
import dynamic from 'next/dynamic';
import { Data, Layout } from 'plotly.js';

// Import Plotly dynamically to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

interface ChartProps {
  data: Data[];
  layout?: Partial<Layout>;
  style?: { width: string; height: string };
}

export const Chart: React.FC<ChartProps> = ({ data, layout = {}, style = { width: '100%', height: '400px' } }) => {
  return (
    <Plot
      data={data}
      layout={{
        margin: { t: 20, r: 20, b: 40, l: 40 },
        showlegend: true,
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        ...layout,
      }}
      style={style}
      config={{ responsive: true }}
    />
  );
}; 