import React from 'react';
import Layout from '@/components/Layout';
import { Card } from '@/components/ui/Card';
import { MdCheckCircle } from 'react-icons/md';

interface FinancialIndicator {
  name: string;
  value: string | number;
  threshold: string | number;
  status: 'OK' | 'WARNING' | 'ERROR';
  comment: string;
}

interface CheckRevisoreProps {
  year: string;
  score: number;
  grade: string;
  indicators: FinancialIndicator[];
}

const StatusBadge: React.FC<{ status: FinancialIndicator['status'] }> = ({ status }) => {
  const colors = {
    OK: 'bg-success text-white',
    WARNING: 'bg-warning text-white',
    ERROR: 'bg-error text-white',
  };

  return (
    <div className={`px-3 py-1 rounded-full text-sm ${colors[status]}`}>
      {status === 'OK' && 'OK'}
      {status === 'WARNING' && 'Attenzione'}
      {status === 'ERROR' && 'Errore'}
    </div>
  );
};

export default function CheckRevisore({ year, score, grade, indicators }: CheckRevisoreProps) {
  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-semibold text-text-primary">
              Check Revisore
            </h1>
            <p className="text-sm text-text-secondary mt-1">
              Analisi automatica del bilancio e identificazione di potenziali criticità
            </p>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm text-text-secondary">Stato di Salute Finanziaria</p>
              <p className="text-lg font-semibold">Anno di riferimento: {year}</p>
            </div>
            <div className="flex items-center justify-center w-20 h-20 rounded-full bg-success text-white text-2xl font-bold">
              {grade}
            </div>
          </div>
        </div>

        <Card>
          <div className="p-6">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-background">
                    <th className="text-left py-3 px-4 text-text-secondary font-medium">Indicatore</th>
                    <th className="text-left py-3 px-4 text-text-secondary font-medium">Valore</th>
                    <th className="text-left py-3 px-4 text-text-secondary font-medium">Soglia</th>
                    <th className="text-left py-3 px-4 text-text-secondary font-medium">Esito</th>
                    <th className="text-left py-3 px-4 text-text-secondary font-medium">Commento</th>
                  </tr>
                </thead>
                <tbody>
                  {indicators.map((indicator, index) => (
                    <tr key={index} className="border-b border-background">
                      <td className="py-4 px-4">{indicator.name}</td>
                      <td className="py-4 px-4">{indicator.value}</td>
                      <td className="py-4 px-4">{indicator.threshold}</td>
                      <td className="py-4 px-4">
                        <StatusBadge status={indicator.status} />
                      </td>
                      <td className="py-4 px-4 flex items-center gap-2">
                        <MdCheckCircle className="text-success" />
                        {indicator.comment}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </Card>

        <p className="text-sm text-text-secondary">
          I dati si riferiscono all&apos;anno {year}
        </p>
      </div>
    </Layout>
  );
}

// Esempio di dati statici per il development
CheckRevisore.defaultProps = {
  year: '2024',
  score: 100,
  grade: 'A',
  indicators: [
    {
      name: 'Patrimonio Netto',
      value: '1.500.000 €',
      threshold: '> 0',
      status: 'OK',
      comment: 'Il capitale proprio è positivo.',
    },
    {
      name: 'ROE',
      value: '46,7%',
      threshold: '> 3%',
      status: 'OK',
      comment: 'Buona redditività del capitale proprio.',
    },
    {
      name: 'Margine EBITDA',
      value: '20,0%',
      threshold: '> 10%',
      status: 'OK',
      comment: 'Buon margine operativo.',
    },
    {
      name: 'Utile Netto',
      value: '700.000 €',
      threshold: '> 0',
      status: 'OK',
      comment: 'L\'azienda è in utile.',
    },
    {
      name: 'ROI',
      value: '23,3%',
      threshold: '> 5%',
      status: 'OK',
      comment: 'Buon ritorno sugli investimenti.',
    },
  ],
}; 