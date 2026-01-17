import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { FileDropzone } from '../FileDropzone';
import { Button } from '../ui/button';
import { Progress } from '../ui/progress';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Label } from '../ui/label';
import { ScanText, Download, Languages, FileSearch } from 'lucide-react';
import { toast } from 'sonner';

const languages = [
  { code: 'spa', name: 'Español' },
  { code: 'eng', name: 'Inglés' },
  { code: 'por', name: 'Portugués' },
  { code: 'fra', name: 'Francés' },
  { code: 'deu', name: 'Alemán' },
  { code: 'ita', name: 'Italiano' },
];

export function OCRPdf() {
  const [files, setFiles] = useState<File[]>([]);
  const [language, setLanguage] = useState('spa');
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [isComplete, setIsComplete] = useState(false);
  const [detectedPages, setDetectedPages] = useState(0);
  const [processedPages, setProcessedPages] = useState(0);

  const handleOCR = async () => {
    if (files.length === 0) {
      toast.error('Por favor selecciona un archivo PDF');
      return;
    }

    setIsProcessing(true);
    setProgress(0);
    setIsComplete(false);
    setDetectedPages(15); // Simulado

    // Simular procesamiento OCR
    for (let i = 0; i <= 100; i += 5) {
      await new Promise(resolve => setTimeout(resolve, 120));
      setProgress(i);
      setProcessedPages(Math.floor((i / 100) * 15));
      
      if (i === 10) toast.info('Detectando páginas escaneadas...');
      if (i === 30) toast.info('Aplicando OCR con Tesseract...');
      if (i === 60) toast.info('Extrayendo texto...');
      if (i === 90) toast.info('Generando PDF con capa de texto...');
    }

    setIsProcessing(false);
    setIsComplete(true);
    toast.success('¡OCR completado exitosamente!');
  };

  const handleDownload = () => {
    toast.success('Descargando PDF con texto reconocido...');
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
              <ScanText className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                OCR - Reconocimiento de Texto
              </h1>
              <p className="text-gray-600">Convierte PDFs escaneados en texto buscable</p>
            </div>
          </div>
        </motion.div>

        {/* Main Content */}
        <div className="space-y-6">
          {/* Info Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-gray-50 rounded-2xl p-6 border border-gray-200"
          >
            <div className="flex items-start gap-3">
              <div className="w-10 h-10 bg-black rounded-lg flex items-center justify-center flex-shrink-0">
                <FileSearch className="w-5 h-5 text-white" />
              </div>
              <div>
                <h4 className="font-semibold text-violet-900 mb-2">Detección Automática</h4>
                <p className="text-sm text-violet-700">
                  LocalPDF detecta automáticamente si tu PDF contiene páginas escaneadas y aplica OCR 
                  solo donde es necesario, preservando el texto original cuando ya existe.
                </p>
              </div>
            </div>
          </motion.div>

          {/* File Upload */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <FileDropzone
              onFilesSelected={setFiles}
              accept=".pdf"
              multiple={true}
              maxFiles={10}
              title="Arrastra tus PDFs escaneados aquí"
              description="o haz clic para seleccionar archivos"
            />
          </motion.div>

          {/* Language Selection */}
          <AnimatePresence>
            {files.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="bg-white/60 backdrop-blur-xl rounded-2xl p-6 border border-white/50"
              >
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="language" className="text-base flex items-center gap-2 mb-3">
                      <Languages className="w-5 h-5 text-violet-600" />
                      Idioma del documento
                    </Label>
                    <Select value={language} onValueChange={setLanguage}>
                      <SelectTrigger id="language" className="w-full">
                        <SelectValue placeholder="Selecciona un idioma" />
                      </SelectTrigger>
                      <SelectContent>
                        {languages.map((lang) => (
                          <SelectItem key={lang.code} value={lang.code}>
                            {lang.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="bg-gray-50 rounded-xl p-4">
                    <h4 className="font-medium text-gray-800 mb-2">Powered by Tesseract OCR</h4>
                    <ul className="text-sm text-gray-600 space-y-1">
                      <li className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 bg-violet-500 rounded-full"></div>
                        Reconocimiento de alta precisión
                      </li>
                      <li className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 bg-violet-500 rounded-full"></div>
                        Soporte para múltiples idiomas
                      </li>
                      <li className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 bg-violet-500 rounded-full"></div>
                        100% procesamiento offline
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
                <h3 className="text-lg font-semibold text-gray-800 mb-4">
                  Procesando con OCR...
                </h3>
                <Progress value={progress} className="mb-3" />
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">
                    Procesando: {processedPages} / {detectedPages} páginas
                  </span>
                  <span className="text-gray-600 font-medium">{progress}%</span>
                </div>
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
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-lg font-semibold text-white mb-1">¡OCR completado!</h3>
                      <p className="text-sm text-gray-300">
                        {detectedPages} páginas procesadas con texto reconocido
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

                  <div className="bg-gray-50 rounded-xl p-4">
                    <h4 className="font-medium text-green-800 mb-2">✓ El PDF ahora incluye:</h4>
                    <ul className="text-sm text-green-700 space-y-1">
                      <li className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 bg-green-600 rounded-full"></div>
                        Capa de texto buscable
                      </li>
                      <li className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 bg-green-600 rounded-full"></div>
                        Texto seleccionable y copiable
                      </li>
                      <li className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 bg-green-600 rounded-full"></div>
                        Compatible con lectores de pantalla
                      </li>
                    </ul>
                  </div>
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
              onClick={handleOCR}
              disabled={files.length === 0 || isProcessing}
              className="w-full bg-black hover:bg-gray-900 text-white h-12 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ScanText className="w-5 h-5 mr-2" />
              {isProcessing ? 'Procesando...' : 'Aplicar OCR'}
            </Button>
          </motion.div>
        </div>
      </div>
    </div>
  );
}