import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { IconType } from 'react-icons';
import { 
  MdDashboard, 
  MdBusiness, 
  MdDescription, 
  MdAssessment,
  MdAnalytics,
  MdSwapHoriz,
  MdPerson
} from 'react-icons/md';

interface SidebarItemProps {
  href: string;
  icon: IconType;
  text: string;
  isActive?: boolean;
}

const SidebarItem: React.FC<SidebarItemProps> = ({ href, icon: Icon, text, isActive }) => (
  <Link 
    href={href}
    className={`flex items-center px-4 py-3 text-sm transition-colors ${
      isActive 
        ? 'bg-secondary/10 text-secondary border-l-4 border-secondary' 
        : 'text-text-primary hover:bg-background'
    }`}
  >
    <Icon className="w-5 h-5 mr-3" />
    <span>{text}</span>
  </Link>
);

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const router = useRouter();
  const currentPath = router.pathname;

  return (
    <div className="flex min-h-screen bg-background">
      {/* Sidebar */}
      <aside className="w-64 bg-surface border-r border-background">
        {/* Logo */}
        <div className="p-4 border-b border-background">
          <Link href="/" className="flex items-center space-x-2">
            <MdAnalytics className="w-6 h-6 text-primary" />
            <div>
              <h1 className="text-lg font-semibold text-primary">Fiscal Forecast Flow</h1>
              <p className="text-xs text-text-secondary">Analisi Finanziaria</p>
            </div>
          </Link>
        </div>

        {/* Navigation */}
        <nav className="py-4">
          <SidebarItem 
            href="/dashboard" 
            icon={MdDashboard} 
            text="Dashboard"
            isActive={currentPath === '/dashboard'}
          />
          <SidebarItem 
            href="/aziende" 
            icon={MdBusiness} 
            text="Aziende"
            isActive={currentPath === '/aziende'}
          />
          <div className="px-4 py-2 text-xs font-semibold text-text-secondary uppercase mt-4">
            Analisi
          </div>
          <SidebarItem 
            href="/business-plan" 
            icon={MdDescription} 
            text="Business Plan"
            isActive={currentPath === '/business-plan'}
          />
          <SidebarItem 
            href="/valutazione" 
            icon={MdAssessment} 
            text="Valutazione"
            isActive={currentPath === '/valutazione'}
          />
          <SidebarItem 
            href="/check-revisore" 
            icon={MdAnalytics} 
            text="Check Revisore"
            isActive={currentPath === '/check-revisore'}
          />
          <SidebarItem 
            href="/analisi-swot" 
            icon={MdSwapHoriz} 
            text="Analisi SWOT"
            isActive={currentPath === '/analisi-swot'}
          />
          <SidebarItem 
            href="/scheda-investitore" 
            icon={MdPerson} 
            text="Scheda Investitore"
            isActive={currentPath === '/scheda-investitore'}
          />
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1">
        {/* Header */}
        <header className="h-16 bg-surface border-b border-background flex items-center justify-between px-6">
          <h2 className="text-xl font-semibold text-text-primary">
            Fiscal Forecast Flow
          </h2>
          <div className="flex items-center space-x-2">
            <div className="px-4 py-2 bg-primary text-white rounded-lg">
              Azienda S.p.A.
            </div>
            <div className="px-3 py-1 bg-secondary/10 text-text-primary rounded-lg text-sm">
              Tecnologia
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="p-6">
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout; 