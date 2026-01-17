import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { FileDropzone } from '../FileDropzone';
import { Button } from '../ui/button';
import { Progress } from '../ui/progress';
import { RefreshCw, Download, FileText, Image, FileSpreadsheet } from 'lucide-react';
import { toast } from 'sonner';

type ConversionType = 'pdf-to-word' | 'pdf-to-images' | 'word-to-pdf' | 'images-to-pdf';

const conversionTypes = [
  {
    id: 'pdf-to-word' as ConversionType,
    title: 'PDF → Word',
    description: 'Convierte PDF a formato DOCX editable',
    icon: FileText,
    gradient: 'from-blue-500 to-indigo-500',
    bgGradient: 'from-blue-50 to-indigo-50',
    accept: '.pdf',
  },
  {
    id: 'word-to-pdf' as ConversionType,
    title: 'Word → PDF',
    description: 'Convierte documentos Word a PDF',
    icon: FileSpreadsheet,
    gradient: 'from-purple-500 to-pink-500',
    bgGradient: 'from-purple-50 to-pink-50',
    accept: '.doc,.docx',
  },
  {
    id: 'pdf-to-images' as ConversionType,
    title: 'PDF → Imágenes',
    description: 'Extrae cada página como imagen PNG/JPG',
    icon: Image,
    gradient: 'from-emerald-500 to-teal-500',
    bgGradient: 'from-emerald-50 to-teal-50',
    accept: '.pdf',
  },
  {
    id: 'images-to-pdf' as ConversionType,
    title: 'Imágenes → PDF',
    description: 'Combina imágenes en un PDF',
    icon: Image,
    gradient: 'from-orange-500 to-red-500',
    bgGradient: 'from-orange-50 to-red-50',
    accept: '.jpg,.jpeg,.png',
  },
];

export function ConvertPDF() {
  const [selectedType, setSelectedType] = useState<ConversionType>('pdf-to-word');
  const [files, setFiles] = useState<File[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [isComplete, setIsComplete] = useState(false);

  const currentConversion = conversionTypes.find(t => t.id === selectedType)!;

  const handleConvert = async () => {
    if (files.length === 0) {
      toast.error('Por favor selecciona archivos para convertir');
      return;
    }

    setIsProcessing(true);
    setProgress(0);
    setIsComplete(false);

    // Simular procesamiento con Layout Engine
    for (let i = 0; i <= 100; i += 5) {
      await new Promise(resolve => setTimeout(resolve, 100));
      setProgress(i);
      
      if (i === 25) toast.info('Analizando estructura del documento...');
      if (i === 50) toast.info('Aplicando Layout Engine...');
      if (i === 75) toast.info('Generando archivo final...');
    }

    setIsProcessing(false);
    setIsComplete(true);
    toast.success('¡Conversión completada exitosamente!');
  };

  const handleDownload = () => {
    toast.success('Descargando archivo convertido...');
  };

  return (
    <div className="h-full overflow-y-auto bg-white">
      <div className="max-w-4xl mx-auto p-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center gap-4 mb-4">
            <div className="w-14 h-14 bg-black rounded-2xl flex items-center justify-center">
              <RefreshCw className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Convertir Archivos
              </h1>
              <p className="text-gray-600">Transforma tus documentos entre diferentes formatos</p>
            </div>
          </div>
        </motion.div>

        {/* Main Content */}
        <div className="space-y-6">
          {/* Conversion Type Selection */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Tipo de conversión</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {conversionTypes.map((type) => {
                const Icon = type.icon;
                const isSelected = selectedType === type.id;
                
                return (
                  <motion.button
                    key={type.id}
                    onClick={() => {
                      setSelectedType(type.id);
                      setFiles([]);
                      setIsComplete(false);
                    }}
                    className={`
                      relative p-6 rounded-2xl text-left transition-all
                      ${isSelected 
                        ? 'bg-gray-900 text-white border-2 border-gray-900 shadow-md' 
                        : 'bg-gray-50 border border-gray-200 hover:bg-gray-100'
                      }
                    `}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    {isSelected && (
                      <motion.div
                        layoutId="selectedConversion"
                        className={`absolute inset-0 bg-gradient-to-br ${type.bgGradient} rounded-2xl`}
                        transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
                      />
                    )}
                    <div className="relative flex items-start gap-4">
                      <div className={`w-12 h-12 ${isSelected ? 'bg-white' : 'bg-black'} rounded-xl flex items-center justify-center flex-shrink-0 shadow-md`}>
                        <Icon className={`w-6 h-6 ${isSelected ? 'text-black' : 'text-white'}`} />
                      </div>
                      <div>
                        <h4 className={`font-semibold ${isSelected ? 'text-white' : 'text-gray-900'} mb-1`}>{type.title}</h4>
                        <p className={`text-sm ${isSelected ? 'text-gray-300' : 'text-gray-600'}`}>{type.description}</p>
                      </div>
                    </div>
                  </motion.button>
                );
              })}
            </div>
          </motion.div>

          {/* File Upload */}
          <motion.div
            key={selectedType}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <FileDropzone
              onFilesSelected={setFiles}
              accept={currentConversion.accept}
              multiple={selectedType === 'images-to-pdf'}
              maxFiles={selectedType === 'images-to-pdf' ? 50 : 10}
              title={`Arrastra tus archivos ${currentConversion.title.split(' ')[0]} aquí`}
              description="o haz clic para seleccionar"
            />
          </motion.div>

          {/* Layout Engine Info */}
          <AnimatePresence>
            {files.length > 0 && selectedType === 'pdf-to-word' && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="bg-gray-50 rounded-2xl p-6 border border-gray-200"
              >
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 bg-black rounded-lg flex items-center justify-center flex-shrink-0">
                    <RefreshCw className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-indigo-900 mb-2">Layout Engine Avanzado</h4>
                    <p className="text-sm text-indigo-700 mb-2">
                      Este proceso utiliza nuestro motor avanzado de análisis de layout para:
                    </p>
                    <ul className="text-sm text-indigo-700 space-y-1">
                      <li className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full"></div>
                        Detectar y preservar la estructura del documento
                      </li>
                      <li className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full"></div>
                        Mantener el formato de tablas, columnas y listas
                      </li>
                      <li className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full"></div>
                        Reconocer imágenes y gráficos automáticamente
                      </li>
                    </ul>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Processing */}
          <AnimatePresence>
            {isProcessing && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="bg-white/60 backdrop-blur-xl rounded-2xl p-6 border border-white/50"
              >
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Convirtiendo archivos...</h3>
                <Progress value={progress} className="mb-2" />
                <p className="text-sm text-gray-600 text-center">{progress}%</p>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Success */}
          <AnimatePresence>
            {isComplete && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-gray-900 rounded-2xl p-6"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-semibold text-white mb-1">¡Conversión completada!</h3>
                    <p className="text-sm text-gray-300">
                      {files.length} archivo{files.length > 1 ? 's' : ''} convertido{files.length > 1 ? 's' : ''} exitosamente
                    </p>
                  </div>
                  <Button
                    onClick={handleDownload}
                    className="bg-white hover:bg-gray-100 text-black"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Descargar
                  </Button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Action Buttons */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            <Button
              onClick={handleConvert}
              disabled={files.length === 0 || isProcessing}
              className="w-full bg-black hover:bg-gray-900 text-white h-12 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <RefreshCw className="w-5 h-5 mr-2" />
              {isProcessing ? 'Procesando...' : 'Convertir Archivos'}
            </Button>
          </motion.div>
        </div>
      </div>
    </div>
  );
}