import { motion } from 'motion/react';
import { 
  Combine, 
  Scissors, 
  Archive, 
  RefreshCw, 
  Shield, 
  ScanText, 
  FolderClock,
  Wand2,
  ArrowRight,
  Sparkles
} from 'lucide-react';
import type { ViewType } from '../App';

interface DashboardProps {
  onNavigate: (view: ViewType) => void;
}

const quickActions = [
  {
    id: 'merge' as ViewType,
    icon: Combine,
    title: 'Combinar PDFs',
    description: 'Une múltiples archivos en uno solo',
  },
  {
    id: 'split' as ViewType,
    icon: Scissors,
    title: 'Dividir PDF',
    description: 'Separa páginas o rangos',
  },
  {
    id: 'compress' as ViewType,
    icon: Archive,
    title: 'Comprimir',
    description: 'Reduce el tamaño del archivo',
  },
  {
    id: 'convert' as ViewType,
    icon: RefreshCw,
    title: 'Convertir',
    description: 'PDF ↔ Word, Imágenes',
  },
  {
    id: 'security' as ViewType,
    icon: Shield,
    title: 'Seguridad',
    description: 'Encriptar y proteger',
  },
  {
    id: 'ocr' as ViewType,
    icon: ScanText,
    title: 'OCR',
    description: 'Reconocimiento de texto',
  },
];

export function Dashboard({ onNavigate }: DashboardProps) {
  return (
    <div className="h-full overflow-y-auto bg-white dark:bg-black transition-colors duration-300">
      <div className="max-w-7xl mx-auto p-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            Bienvenido a LocalPDF
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Herramienta profesional para manipulación de PDFs — 100% offline
          </p>
        </motion.div>

        {/* Wizard Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          onClick={() => onNavigate('wizard')}
          className="mb-8 bg-gradient-to-br from-gray-900 to-black dark:from-white dark:to-gray-100 rounded-3xl p-8 cursor-pointer group hover:shadow-2xl hover:shadow-indigo-500/20 dark:hover:shadow-white/10 transition-all duration-300"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-white dark:bg-black rounded-2xl flex items-center justify-center shadow-lg">
                <Wand2 className="w-8 h-8 text-black dark:text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white dark:text-black mb-1">Asistente Inteligente</h2>
                <p className="text-gray-300 dark:text-gray-600">
                  Déjanos ayudarte a elegir la mejor operación para tu documento
                </p>
              </div>
            </div>
            <ArrowRight className="w-6 h-6 text-white dark:text-black group-hover:translate-x-2 transition-transform duration-300" />
          </div>
        </motion.div>

        {/* Quick Actions Grid */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Acciones Rápidas</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {quickActions.map((action, index) => {
              const Icon = action.icon;
              return (
                <motion.div
                  key={action.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 + index * 0.05 }}
                  onClick={() => onNavigate(action.id)}
                  className="group cursor-pointer"
                >
                  <div className="bg-gray-50 dark:bg-[#1C1C1E] hover:bg-gray-100 dark:hover:bg-[#2C2C2E] rounded-2xl p-6 transition-all duration-300 border border-gray-200 dark:border-gray-800 h-full">
                    <div className="w-12 h-12 bg-black dark:bg-white rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                      <Icon className="w-6 h-6 text-white dark:text-black" />
                    </div>
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2">{action.title}</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">{action.description}</p>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>

        {/* Advanced Features */}
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Características Avanzadas</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 }}
              onClick={() => onNavigate('batch')}
              className="bg-gray-50 dark:bg-[#1C1C1E] rounded-2xl p-6 border border-gray-200 dark:border-gray-800 hover:bg-gray-100 dark:hover:bg-[#2C2C2E] transition-all duration-300 cursor-pointer group"
            >
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-black dark:bg-white rounded-xl flex items-center justify-center">
                  <FolderClock className="w-6 h-6 text-white dark:text-black" />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-1">Procesamiento por Lotes</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Automatiza operaciones en múltiples archivos</p>
                </div>
                <ArrowRight className="w-5 h-5 text-gray-400 dark:text-gray-600 group-hover:translate-x-2 transition-transform duration-300" />
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.6 }}
              className="bg-gray-50 dark:bg-[#1C1C1E] rounded-2xl p-6 border border-gray-200 dark:border-gray-800"
            >
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-black dark:bg-white rounded-xl flex items-center justify-center">
                  <Sparkles className="w-6 h-6 text-white dark:text-black" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-1">Layout Engine</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Conversión avanzada con análisis de estructura</p>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}