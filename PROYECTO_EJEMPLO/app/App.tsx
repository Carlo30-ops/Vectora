import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Dashboard } from './components/Dashboard';
import { MergePDF } from './components/operations/MergePDF';
import { SplitPDF } from './components/operations/SplitPDF';
import { CompressPDF } from './components/operations/CompressPDF';
import { ConvertPDF } from './components/operations/ConvertPDF';
import { SecurityPDF } from './components/operations/SecurityPDF';
import { OCRPdf } from './components/operations/OCRPdf';
import { BatchProcessing } from './components/operations/BatchProcessing';
import { Wizard } from './components/Wizard';
import { Toaster } from './components/ui/sonner';
import { ThemeProvider } from './context/ThemeContext';

export type ViewType = 
  | 'dashboard' 
  | 'merge' 
  | 'split' 
  | 'compress' 
  | 'convert' 
  | 'security' 
  | 'ocr' 
  | 'batch'
  | 'wizard';

export default function App() {
  const [currentView, setCurrentView] = useState<ViewType>('dashboard');

  const renderView = () => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard onNavigate={setCurrentView} />;
      case 'merge':
        return <MergePDF />;
      case 'split':
        return <SplitPDF />;
      case 'compress':
        return <CompressPDF />;
      case 'convert':
        return <ConvertPDF />;
      case 'security':
        return <SecurityPDF />;
      case 'ocr':
        return <OCRPdf />;
      case 'batch':
        return <BatchProcessing />;
      case 'wizard':
        return <Wizard onNavigate={setCurrentView} />;
      default:
        return <Dashboard onNavigate={setCurrentView} />;
    }
  };

  return (
    <ThemeProvider>
      <div className="flex h-screen bg-gray-50 dark:bg-black overflow-hidden transition-colors duration-300">
        <Sidebar currentView={currentView} onNavigate={setCurrentView} />
        <main className="flex-1 overflow-hidden">
          {renderView()}
        </main>
        <Toaster position="top-right" />
      </div>
    </ThemeProvider>
  );
}