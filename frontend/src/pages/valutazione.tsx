import React, { useState, ChangeEvent } from 'react';
import Layout from '@/components/Layout';
import { Card } from '@/components/ui/Card';
import { MdCalculate } from 'react-icons/md';

interface ValuationProps {
  companyName: string;
  sector: string;
  ebitda: number;
  netAssets: number;
}

export default function Valuation({
  companyName,
  sector,
  ebitda,
  netAssets,
}: ValuationProps) {
  const [valuationMethod, setValuationMethod] = useState<'ebitda' | 'assets'>('ebitda');
  const [ebitdaMultiple, setEbitdaMultiple] = useState<number>(5);

  const handleMethodChange = (e: ChangeEvent<HTMLInputElement>) => {
    setValuationMethod(e.target.value as 'ebitda' | 'assets');
  };

  const handleMultipleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setEbitdaMultiple(Number(e.target.value));
  };

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-semibold text-text-primary">
              Valutazione dell&apos;Impresa
            </h1>
            <p className="text-sm text-text-secondary mt-1">
              Calcola il valore stimato dell&apos;azienda utilizzando diversi metodi
            </p>
          </div>
        </div>

        <Card className="p-6">
          <form className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-text-primary mb-2">
                Metodo di Valutazione
              </label>
              <div className="space-y-2">
                <div className="flex items-center">
                  <input
                    type="radio"
                    id="ebitda"
                    name="valuationMethod"
                    value="ebitda"
                    checked={valuationMethod === 'ebitda'}
                    onChange={handleMethodChange}
                    className="w-4 h-4 text-primary border-background focus:ring-primary"
                  />
                  <label htmlFor="ebitda" className="ml-2 text-text-primary">
                    Metodo Reddituale (EBITDA × Multiplo)
                  </label>
                </div>
                <div className="flex items-center">
                  <input
                    type="radio"
                    id="assets"
                    name="valuationMethod"
                    value="assets"
                    checked={valuationMethod === 'assets'}
                    onChange={handleMethodChange}
                    className="w-4 h-4 text-primary border-background focus:ring-primary"
                  />
                  <label htmlFor="assets" className="ml-2 text-text-primary">
                    Metodo Patrimoniale (Patrimonio Netto)
                  </label>
                </div>
              </div>
            </div>

            {valuationMethod === 'ebitda' && (
              <div>
                <label className="block text-sm font-medium text-text-primary mb-2">
                  Multiplo EBITDA
                </label>
                <input
                  type="number"
                  value={ebitdaMultiple}
                  onChange={handleMultipleChange}
                  min="1"
                  max="20"
                  className="w-full p-3 rounded-lg border border-background bg-surface text-text-primary"
                />
              </div>
            )}

            <button
              type="button"
              className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors"
            >
              <MdCalculate className="w-5 h-5" />
              Calcola Valutazione
            </button>
          </form>
        </Card>
      </div>
    </Layout>
  );
}

// Esempio di dati statici per il development
Valuation.defaultProps = {
  companyName: 'Azienda S.p.A.',
  sector: 'Tecnologia',
  ebitda: 1000000,
  netAssets: 1500000,
}; 