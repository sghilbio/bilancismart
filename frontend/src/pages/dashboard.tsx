import React from 'react';
import Layout from '@/components/Layout';
import { Card } from '@/components/ui/Card';

interface CompanyInfo {
  name: string;
  sector: string;
  ateco: string;
  availableYears: string[];
}

interface DashboardProps {
  companyInfo: CompanyInfo;
  lastUpdate: string;
  analysisCount: number;
}

export default function Dashboard({ companyInfo, lastUpdate, analysisCount }: DashboardProps) {
  return (
    <Layout>
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold text-text-primary">
          Dashboard: {companyInfo.name}
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Company Information */}
          <Card>
            <div className="p-6">
              <h2 className="text-xl font-semibold mb-4">Informazioni Azienda</h2>
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-text-secondary">Settore</p>
                  <p className="text-text-primary">{companyInfo.sector}</p>
                </div>
                <div>
                  <p className="text-sm text-text-secondary">Codice ATECO</p>
                  <p className="text-text-primary">{companyInfo.ateco}</p>
                </div>
                <div>
                  <p className="text-sm text-text-secondary">Anni disponibili</p>
                  <p className="text-text-primary">{companyInfo.availableYears.join(', ')}</p>
                </div>
              </div>
            </div>
          </Card>

          {/* Analysis Status */}
          <Card>
            <div className="p-6">
              <h2 className="text-xl font-semibold mb-4">Analisi Effettuate</h2>
              <div className="text-center">
                <p className="text-5xl font-bold text-primary mb-2">{analysisCount}</p>
                <p className="text-sm text-text-secondary">
                  Ultimo aggiornamento: {lastUpdate}
                </p>
              </div>
            </div>
          </Card>
        </div>

        {/* Create Analysis Button */}
        {analysisCount === 0 && (
          <Card className="p-6 text-center">
            <p className="text-lg text-text-primary mb-4">
              Nessuna analisi disponibile per questa azienda.
            </p>
            <button className="px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors">
              Crea la tua prima analisi
            </button>
          </Card>
        )}
      </div>
    </Layout>
  );
}

// Esempio di dati statici per il development
Dashboard.defaultProps = {
  companyInfo: {
    name: 'Azienda S.p.A.',
    sector: 'Tecnologia',
    ateco: '62.01.00',
    availableYears: ['2025'],
  },
  lastUpdate: '05/04/2025',
  analysisCount: 0,
}; 