import React from 'react';
import Layout from '@/components/Layout';
import { Card } from '@/components/ui/Card';
import { MdFileDownload } from 'react-icons/md';

interface InvestorSheetProps {
  companyName: string;
  sector: string;
  atecoCode: string;
  year: string;
  fundDestination: string;
}

export default function InvestorSheet({
  companyName,
  sector,
  atecoCode,
  year,
  fundDestination,
}: InvestorSheetProps) {
  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-semibold text-text-primary">
              Scheda Investitore
            </h1>
            <p className="text-sm text-text-secondary mt-1">
              Genera una scheda professionale in formato PDF da presentare a istituti di credito o investitori
            </p>
          </div>
        </div>

        <Card className="p-6">
          <form className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-text-primary mb-2">
                  Nome Azienda
                </label>
                <input
                  type="text"
                  value={companyName}
                  readOnly
                  className="w-full p-3 rounded-lg border border-background bg-surface text-text-primary"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-text-primary mb-2">
                  Anno di Riferimento
                </label>
                <input
                  type="text"
                  value={year}
                  readOnly
                  className="w-full p-3 rounded-lg border border-background bg-surface text-text-primary"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-text-primary mb-2">
                  Settore
                </label>
                <input
                  type="text"
                  value={sector}
                  readOnly
                  className="w-full p-3 rounded-lg border border-background bg-surface text-text-primary"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-text-primary mb-2">
                  Codice ATECO
                </label>
                <input
                  type="text"
                  value={atecoCode}
                  readOnly
                  className="w-full p-3 rounded-lg border border-background bg-surface text-text-primary"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-text-primary mb-2">
                Destinazione dei Fondi
              </label>
              <textarea
                value={fundDestination}
                readOnly
                rows={4}
                className="w-full p-3 rounded-lg border border-background bg-surface text-text-primary resize-none"
              />
            </div>

            <button
              type="button"
              className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors"
            >
              <MdFileDownload className="w-5 h-5" />
              Genera e Scarica Scheda Investitore
            </button>
          </form>
        </Card>
      </div>
    </Layout>
  );
}

// Esempio di dati statici per il development
InvestorSheet.defaultProps = {
  companyName: 'Azienda S.p.A.',
  sector: 'Tecnologia',
  atecoCode: '62.01.00',
  year: '2025',
  fundDestination: 'Investimenti in ricerca e sviluppo per nuove tecnologie e espansione internazionale.',
}; 