import { motion } from 'motion/react';
import { 
  FileText, 
  Home, 
  Combine, 
  Scissors, 
  Archive, 
  RefreshCw, 
  Shield, 
  ScanText, 
  FolderClock,
  Wand2
} from 'lucide-react';
import type { ViewType } from '../App';
import { ThemeToggle } from './ThemeToggle';

interface SidebarProps {
  currentView: ViewType;
  onNavigate: (view: ViewType) => void;
}

const menuItems = [
  { id: 'dashboard' as ViewType, icon: Home, label: 'Dashboard', badge: null },
  { id: 'wizard' as ViewType, icon: Wand2, label: 'Asistente', badge: 'Nuevo' },
  { id: 'merge' as ViewType, icon: Combine, label: 'Combinar', badge: null },
  { id: 'split' as ViewType, icon: Scissors, label: 'Dividir', badge: null },
  { id: 'compress' as ViewType, icon: Archive, label: 'Comprimir', badge: null },
  { id: 'convert' as ViewType, icon: RefreshCw, label: 'Convertir', badge: null },
  { id: 'security' as ViewType, icon: Shield, label: 'Seguridad', badge: null },
  { id: 'ocr' as ViewType, icon: ScanText, label: 'OCR', badge: null },
  { id: 'batch' as ViewType, icon: FolderClock, label: 'Lotes', badge: null },
];

export function Sidebar({ currentView, onNavigate }: SidebarProps) {
  return (
    <aside className="w-64 bg-white dark:bg-[#1C1C1E] border-r border-gray-200 dark:border-gray-800 flex flex-col transition-colors duration-300">
      {/* Header */}
      <div className="p-6 border-b border-gray-200 dark:border-gray-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-black dark:bg-white rounded-2xl flex items-center justify-center transition-colors duration-300">
            <FileText className="w-6 h-6 text-white dark:text-black" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-gray-900 dark:text-white">
              LocalPDF
            </h1>
            <p className="text-xs text-gray-500 dark:text-gray-400">v5.0</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 overflow-y-auto">
        <div className="space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentView === item.id;

            return (
              <motion.button
                key={item.id}
                onClick={() => onNavigate(item.id)}
                className={`
                  w-full flex items-center gap-3 px-4 py-3 rounded-xl
                  transition-all duration-200 relative
                  ${isActive 
                    ? 'bg-gray-900 dark:bg-white text-white dark:text-black' 
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                  }
                `}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <Icon className={`w-5 h-5 ${isActive ? 'text-white dark:text-black' : 'text-gray-600 dark:text-gray-400'}`} />
                <span className={`font-medium ${isActive ? 'text-white dark:text-black' : 'text-gray-700 dark:text-gray-300'}`}>
                  {item.label}
                </span>
                {item.badge && (
                  <span className="ml-auto px-2 py-0.5 text-xs font-semibold bg-black dark:bg-white text-white dark:text-black rounded-full">
                    {item.badge}
                  </span>
                )}
              </motion.button>
            );
          })}
        </div>
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-800 space-y-3">
        {/* Theme Toggle */}
        <div className="flex items-center justify-between px-2">
          <span className="text-xs font-medium text-gray-600 dark:text-gray-400">Tema</span>
          <ThemeToggle />
        </div>
        
        {/* Offline Badge */}
        <div className="bg-gray-100 dark:bg-gray-800 rounded-xl p-4 transition-colors duration-300">
          <p className="text-xs text-gray-900 dark:text-white font-medium mb-1">100% Offline</p>
          <p className="text-xs text-gray-600 dark:text-gray-400">Sin conexión requerida</p>
        </div>
      </div>
    </aside>
  );
}