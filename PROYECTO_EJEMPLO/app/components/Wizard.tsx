import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Button } from './ui/button';
import { 
  Wand2, 
  FileText, 
  HelpCircle, 
  Sparkles, 
  ChevronRight,
  Combine,
  Scissors,
  Archive,
  RefreshCw,
  Shield,
  ScanText,
  CheckCircle2
} from 'lucide-react';
import type { ViewType } from '../App';

interface WizardProps {
  onNavigate: (view: ViewType) => void;
}

interface Question {
  id: string;
  question: string;
  options: {
    text: string;
    icon: typeof FileText;
    result?: ViewType;
    nextQuestion?: string;
  }[];
}

const wizardQuestions: Record<string, Question> = {
  start: {
    id: 'start',
    question: '¿Qué quieres hacer con tus PDFs?',
    options: [
      {
        text: 'Combinar varios archivos en uno',
        icon: Combine,
        result: 'merge',
      },
      {
        text: 'Separar o extraer páginas',
        icon: Scissors,
        result: 'split',
      },
      {
        text: 'Reducir el tamaño del archivo',
        icon: Archive,
        result: 'compress',
      },
      {
        text: 'Convertir a otro formato',
        icon: RefreshCw,
        nextQuestion: 'convert',
      },
      {
        text: 'Proteger con contraseña',
        icon: Shield,
        result: 'security',
      },
      {
        text: 'Hacer el texto buscable (OCR)',
        icon: ScanText,
        result: 'ocr',
      },
    ],
  },
  convert: {
    id: 'convert',
    question: '¿A qué formato quieres convertir?',
    options: [
      {
        text: 'PDF a Word (DOCX)',
        icon: FileText,
        result: 'convert',
      },
      {
        text: 'Word a PDF',
        icon: FileText,
        result: 'convert',
      },
      {
        text: 'PDF a Imágenes',
        icon: RefreshCw,
        result: 'convert',
      },
      {
        text: 'Imágenes a PDF',
        icon: RefreshCw,
        result: 'convert',
      },
    ],
  },
};

export function Wizard({ onNavigate }: WizardProps) {
  const [currentQuestion, setCurrentQuestion] = useState('start');
  const [selectedPath, setSelectedPath] = useState<string[]>([]);
  const [isComplete, setIsComplete] = useState(false);
  const [recommendedAction, setRecommendedAction] = useState<ViewType | null>(null);

  const question = wizardQuestions[currentQuestion];

  const handleOptionSelect = (option: typeof question.options[0]) => {
    const newPath = [...selectedPath, option.text];
    setSelectedPath(newPath);

    if (option.result) {
      setRecommendedAction(option.result);
      setIsComplete(true);
    } else if (option.nextQuestion) {
      setCurrentQuestion(option.nextQuestion);
    }
  };

  const handleReset = () => {
    setCurrentQuestion('start');
    setSelectedPath([]);
    setIsComplete(false);
    setRecommendedAction(null);
  };

  const handleGoToAction = () => {
    if (recommendedAction) {
      onNavigate(recommendedAction);
    }
  };

  return (
    <div className="h-full overflow-y-auto bg-white dark:bg-black transition-colors duration-300">
      <div className="max-w-4xl mx-auto p-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center gap-4 mb-4">
            <div className="w-14 h-14 bg-black dark:bg-white rounded-2xl flex items-center justify-center transition-colors duration-300">
              <Wand2 className="w-7 h-7 text-white dark:text-black" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                Asistente Inteligente
              </h1>
              <p className="text-gray-600 dark:text-gray-400">Responde unas preguntas y te ayudaré a encontrar la función perfecta</p>
            </div>
          </div>
        </motion.div>

        {/* Breadcrumb */}
        <AnimatePresence>
          {selectedPath.length > 0 && !isComplete && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="mb-6 flex items-center gap-2 flex-wrap"
            >
              {selectedPath.map((step, index) => (
                <div key={index} className="flex items-center gap-2">
                  <span className="text-sm text-gray-600 dark:text-gray-400 bg-white/60 dark:bg-white/10 backdrop-blur-xl px-3 py-1 rounded-full">
                    {step}
                  </span>
                  {index < selectedPath.length - 1 && (
                    <ChevronRight className="w-4 h-4 text-gray-400 dark:text-gray-600" />
                  )}
                </div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Main Content */}
        <AnimatePresence mode="wait">
          {!isComplete ? (
            <motion.div
              key={currentQuestion}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              {/* Question Card */}
              <div className="bg-gray-50 dark:bg-[#1C1C1E] rounded-2xl p-8 border border-gray-200 dark:border-gray-800 mb-6 transition-colors duration-300">
                <div className="flex items-start gap-3 mb-6">
                  <HelpCircle className="w-6 h-6 text-indigo-500 dark:text-indigo-400 flex-shrink-0 mt-1" />
                  <h2 className="text-2xl font-semibold text-gray-800 dark:text-white">
                    {question.question}
                  </h2>
                </div>

                {/* Options */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {question.options.map((option, index) => {
                    const Icon = option.icon;
                    return (
                      <motion.button
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                        onClick={() => handleOptionSelect(option)}
                        className="group relative p-6 bg-white dark:bg-[#2C2C2E] hover:bg-gray-50 dark:hover:bg-[#3A3A3C] rounded-2xl border border-gray-200 dark:border-gray-700 hover:border-gray-900 dark:hover:border-gray-500 transition-all text-left hover:shadow-md"
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                      >
                        <div className="flex items-start gap-4">
                          <div className="w-12 h-12 bg-black dark:bg-white rounded-xl flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                            <Icon className="w-6 h-6 text-white dark:text-black" />
                          </div>
                          <div className="flex-1">
                            <p className="font-medium text-gray-800 dark:text-white group-hover:text-indigo-900 dark:group-hover:text-indigo-400">
                              {option.text}
                            </p>
                          </div>
                          <ChevronRight className="w-5 h-5 text-gray-400 dark:text-gray-600 group-hover:text-indigo-500 dark:group-hover:text-indigo-400 group-hover:translate-x-1 transition-all" />
                        </div>
                      </motion.button>
                    );
                  })}
                </div>
              </div>

              {/* Back Button */}
              {selectedPath.length > 0 && (
                <Button
                  onClick={handleReset}
                  variant="outline"
                  className="w-full dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-800"
                >
                  Volver al inicio
                </Button>
              )}
            </motion.div>
          ) : (
            /* Result */
            <motion.div
              key="result"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.4 }}
            >
              <div className="bg-gradient-to-br from-gray-900 to-black dark:from-white dark:to-gray-100 rounded-2xl p-8 transition-colors duration-300">
                <div className="text-center mb-6">
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
                    className="w-20 h-20 bg-white dark:bg-black rounded-full flex items-center justify-center mx-auto mb-4 shadow-xl"
                  >
                    <CheckCircle2 className="w-10 h-10 text-black dark:text-white" />
                  </motion.div>
                  <h2 className="text-2xl font-bold text-white dark:text-black mb-2">
                    ¡Perfecto! Te recomiendo:
                  </h2>
                  <p className="text-gray-300 dark:text-gray-600">
                    Basándome en tus respuestas, esta es la mejor opción para ti
                  </p>
                </div>

                {/* Recommendation Path */}
                <div className="bg-white/10 dark:bg-black/10 backdrop-blur-xl rounded-xl p-6 mb-6">
                  <h3 className="font-semibold text-white dark:text-black mb-3">Tu selección:</h3>
                  <div className="space-y-2">
                    {selectedPath.map((step, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.3 + index * 0.1 }}
                        className="flex items-center gap-3"
                      >
                        <div className="w-6 h-6 bg-white dark:bg-black rounded-full flex items-center justify-center flex-shrink-0">
                          <span className="text-black dark:text-white text-xs font-bold">{index + 1}</span>
                        </div>
                        <p className="text-gray-300 dark:text-gray-600">{step}</p>
                      </motion.div>
                    ))}
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-3">
                  <Button
                    onClick={handleGoToAction}
                    className="flex-1 bg-white dark:bg-black hover:bg-gray-100 dark:hover:bg-gray-900 text-black dark:text-white h-12 text-lg"
                  >
                    <Wand2 className="w-5 h-5 mr-2" />
                    Ir a la función
                  </Button>
                  <Button
                    onClick={handleReset}
                    variant="outline"
                    className="px-6 border-white dark:border-black text-white dark:text-black hover:bg-white/10 dark:hover:bg-black/10"
                  >
                    Empezar de nuevo
                  </Button>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Help Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mt-8 bg-gray-50 dark:bg-[#1C1C1E] rounded-2xl p-6 border border-gray-200 dark:border-gray-800 transition-colors duration-300"
        >
          <div className="flex items-start gap-3">
            <Sparkles className="w-6 h-6 text-gray-600 dark:text-gray-400 flex-shrink-0" />
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Sugerencia</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Si no estás seguro de qué operación necesitas, este asistente te ayudará a 
                descubrir la mejor función para tu caso específico. Simplemente responde 
                las preguntas y te guiaremos al lugar correcto.
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}