import React from 'react';
import Layout from '@/components/Layout';
import { Card } from '@/components/ui/Card';
import { MdTrendingUp, MdTrendingDown, MdLightbulb, MdWarning } from 'react-icons/md';

interface SwotItem {
  title: string;
  items: string[];
}

interface SwotAnalysisProps {
  strengths: SwotItem;
  weaknesses: SwotItem;
  opportunities: SwotItem;
  threats: SwotItem;
  year: string;
}

const SwotSection: React.FC<{
  title: string;
  items: string[];
  icon: React.ElementType;
  bgColor: string;
  iconColor: string;
}> = ({ title, items, icon: Icon, bgColor, iconColor }) => (
  <Card className={`${bgColor} h-full`}>
    <div className="p-6">
      <div className="flex items-center gap-3 mb-4">
        <Icon className={`w-6 h-6 ${iconColor}`} />
        <h3 className="text-lg font-semibold text-text-primary">{title}</h3>
      </div>
      <div className="space-y-2">
        {items.map((item, index) => (
          <p key={index} className="text-text-primary">
            {item}
          </p>
        ))}
      </div>
    </div>
  </Card>
);

export default function SwotAnalysis({ strengths, weaknesses, opportunities, threats, year }: SwotAnalysisProps) {
  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-semibold text-text-primary">
            Analisi SWOT
          </h1>
          <p className="text-sm text-text-secondary">
            Analisi automatica di punti di forza, debolezze, opportunità e minacce in base ai dati finanziari
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <SwotSection
            title="Punti di Forza"
            items={strengths.items}
            icon={MdTrendingUp}
            bgColor="bg-green-50"
            iconColor="text-secondary"
          />
          <SwotSection
            title="Debolezze"
            items={weaknesses.items}
            icon={MdTrendingDown}
            bgColor="bg-red-50"
            iconColor="text-error"
          />
          <SwotSection
            title="Opportunità"
            items={opportunities.items}
            icon={MdLightbulb}
            bgColor="bg-blue-50"
            iconColor="text-primary"
          />
          <SwotSection
            title="Minacce"
            items={threats.items}
            icon={MdWarning}
            bgColor="bg-yellow-50"
            iconColor="text-warning"
          />
        </div>

        <div className="mt-8 text-sm text-text-secondary">
          Analisi basata sui dati dell&apos;anno {year}. Questo report è generato automaticamente in base a regole predefinite, senza l&apos;uso di intelligenza artificiale.
        </div>
      </div>
    </Layout>
  );
}

// Esempio di dati statici per il development
SwotAnalysis.defaultProps = {
  strengths: {
    title: 'Punti di Forza',
    items: [
      'Alta redditività del capitale proprio (ROE: 46,7%)',
      'Buona redditività delle vendite (Utile/Ricavi: 14.0%)',
      'Elevato ritorno sugli investimenti (ROI: 23.3%)',
    ],
  },
  weaknesses: {
    title: 'Debolezze',
    items: ['Nessuna debolezza significativa rilevata dall\'analisi automatica.'],
  },
  opportunities: {
    title: 'Opportunità',
    items: ['Dati storici non disponibili per l\'analisi delle opportunità'],
  },
  threats: {
    title: 'Minacce',
    items: ['Dati storici non disponibili per l\'analisi delle minacce'],
  },
  year: '2024',
}; 