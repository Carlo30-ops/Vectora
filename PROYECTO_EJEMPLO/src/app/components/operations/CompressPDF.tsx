import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { FileDropzone } from '../FileDropzone';
import { Button } from '../ui/button';
import { Progress } from '../ui/progress';
import { Slider } from '../ui/slider';
import { Label } from '../ui/label';
import { Archive, Download, FileText, Sparkles } from 'lucide-react';
import { toast } from 'sonner';

type CompressionLevel = 'low' | 'medium' | 'high' | 'extreme';

const compressionLevels = {
  low: { value: 25, label: 'Baja', reduction: '~20%', quality: 'Alta calidad' },
  medium: { value: 50, label: 'Media', reduction: '~40%', quality: 'Calidad equilibrada' },
  high: { value: 75, label: 'Alta', reduction: '~60%', quality: 'Compresión fuerte' },
  extreme: { value: 100, label: 'Extrema', reduction: '~80%', quality: 'Máxima compresión' },
};

export function CompressPDF() {
  const [files, setFiles] = useState<File[]>([]);
  const [compressionValue, setCompressionValue] = useState([50]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [isComplete, setIsComplete] = useState(false);
  const [originalSize, setOriginalSize] = useState(0);
  const [compressedSize, setCompressedSize] = useState(0);

  const getCompressionLevel = (value: number): CompressionLevel => {
    if (value <= 25) return 'low';
    if (value <= 50) return 'medium';
    if (value <= 75) return 'high';
    return 'extreme';
  };

  const handleCompress = async () => {
    if (files.length === 0) {
      toast.error('Por favor selecciona un archivo PDF');
      return;
    }

    const totalSize = files.reduce((acc, file) => acc + file.size, 0);
    setOriginalSize(totalSize);

    setIsProcessing(true);
    setProgress(0);
    setIsComplete(false);

    // Simular procesamiento
    for (let i = 0; i <= 100; i += 10) {
      await new Promise(resolve => setTimeout(resolve, 180));
      setProgress(i);
    }

    // Calcular tamaño comprimido simulado
    const reduction = compressionValue[0] / 100;
    const compressed = totalSize * (1 - reduction * 0.7);
    setCompressedSize(compressed);

    setIsProcessing(false);
    setIsComplete(true);
    toast.success('¡PDF comprimido exitosamente!');
  };

  const handleDownload = () => {
    toast.success('Descargando archivo comprimido...');
  };

  const currentLevel = getCompressionLevel(compressionValue[0]);
  const levelInfo = compressionLevels[currentLevel];

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
              <Archive className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Comprimir PDF
              </h1>
              <p className="text-gray-600">Reduce el tamaño de tus archivos PDF</p>
            </div>
          </div>
        </motion.div>

        {/* Main Content */}
        <div className="space-y-6">
          {/* File Upload */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <FileDropzone
              onFilesSelected={setFiles}
              accept=".pdf"
              multiple={true}
              maxFiles={10}
              title="Arrastra tus PDFs aquí"
              description="o haz clic para seleccionar archivos"
            />
          </motion.div>

          {/* Compression Settings */}
          <AnimatePresence>
            {files.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="bg-gray-50 rounded-2xl p-6 border border-gray-200"
              >
                <h3 className="text-lg font-semibold text-gray-800 mb-6">Nivel de compresión</h3>
                
                <div className="space-y-6">
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <Label className="text-base">{levelInfo.label}</Label>
                      <div className="flex items-center gap-2">
                        <Sparkles className="w-4 h-4 text-emerald-500" />
                        <span className="text-sm font-medium text-emerald-600">{levelInfo.reduction}</span>
                      </div>
                    </div>
                    <Slider
                      value={compressionValue}
                      onValueChange={setCompressionValue}
                      max={100}
                      step={1}
                      className="mb-3"
                    />
                    <p className="text-sm text-gray-600">{levelInfo.quality}</p>
                  </div>

                  {/* Compression Level Indicators */}
                  <div className="grid grid-cols-4 gap-2">
                    {Object.entries(compressionLevels).map(([key, info]) => (
                      <button
                        key={key}
                        onClick={() => setCompressionValue([info.value])}
                        className={`
                          p-3 rounded-xl text-center transition-all
                          ${currentLevel === key 
                            ? 'bg-black text-white shadow-md' 
                            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                          }
                        `}
                      >
                        <p className="text-xs font-medium">{info.label}</p>
                        <p className="text-xs opacity-80 mt-1">{info.reduction}</p>
                      </button>
                    ))}
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
                className="bg-gray-50 rounded-2xl p-6 border border-gray-200"
              >
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Comprimiendo archivos...</h3>
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
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-lg font-semibold text-white mb-1">¡Proceso completado!</h3>
                      <p className="text-sm text-gray-300">Tu PDF ha sido comprimido</p>
                    </div>
                    <Button
                      onClick={handleDownload}
                      className="bg-white hover:bg-gray-100 text-black"
                    >
                      <Download className="w-4 h-4 mr-2" />
                      Descargar
                    </Button>
                  </div>

                  {/* Size Comparison */}
                  <div className="grid grid-cols-3 gap-4 pt-4 border-t border-green-200">
                    <div className="text-center">
                      <FileText className="w-8 h-8 text-green-600 mx-auto mb-2" />
                      <p className="text-xs text-green-700 mb-1">Tamaño original</p>
                      <p className="text-lg font-bold text-green-800">
                        {(originalSize / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                    <div className="text-center">
                      <Archive className="w-8 h-8 text-emerald-600 mx-auto mb-2" />
                      <p className="text-xs text-green-700 mb-1">Nuevo tamaño</p>
                      <p className="text-lg font-bold text-emerald-800">
                        {(compressedSize / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                    <div className="text-center">
                      <Sparkles className="w-8 h-8 text-teal-600 mx-auto mb-2" />
                      <p className="text-xs text-green-700 mb-1">Ahorro</p>
                      <p className="text-lg font-bold text-teal-800">
                        {(((originalSize - compressedSize) / originalSize) * 100).toFixed(0)}%
                      </p>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Action Buttons */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
          >
            <Button
              onClick={handleCompress}
              disabled={files.length === 0 || isProcessing}
              className="w-full bg-black hover:bg-gray-900 text-white h-12 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Archive className="w-5 h-5 mr-2" />
              {isProcessing ? 'Procesando...' : 'Comprimir PDF'}
            </Button>
          </motion.div>
        </div>
      </div>
    </div>
  );
}