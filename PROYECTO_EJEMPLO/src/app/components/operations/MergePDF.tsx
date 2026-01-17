import { useState } from 'react';
import { motion, AnimatePresence, Reorder } from 'motion/react';
import { FileDropzone } from '../FileDropzone';
import { Button } from '../ui/button';
import { Progress } from '../ui/progress';
import { Combine, GripVertical, Download, ArrowRight } from 'lucide-react';
import { toast } from 'sonner';

export function MergePDF() {
  const [files, setFiles] = useState<File[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [isComplete, setIsComplete] = useState(false);

  const handleMerge = async () => {
    if (files.length < 2) {
      toast.error('Necesitas al menos 2 archivos para combinar');
      return;
    }

    setIsProcessing(true);
    setProgress(0);
    setIsComplete(false);

    // Simular procesamiento
    for (let i = 0; i <= 100; i += 10) {
      await new Promise(resolve => setTimeout(resolve, 200));
      setProgress(i);
    }

    setIsProcessing(false);
    setIsComplete(true);
    toast.success('¡PDFs combinados exitosamente!');
  };

  const handleDownload = () => {
    toast.success('Descargando archivo combinado...');
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
              <Combine className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Combinar PDFs
              </h1>
              <p className="text-gray-600">Une múltiples archivos PDF en uno solo</p>
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
              maxFiles={20}
              title="Arrastra tus PDFs aquí"
              description="o haz clic para seleccionar archivos"
            />
          </motion.div>

          {/* Reorderable File List */}
          <AnimatePresence>
            {files.length > 0 && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="bg-gray-50 rounded-2xl p-6 border border-gray-200"
              >
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                  <GripVertical className="w-5 h-5 text-gray-400" />
                  Orden de combinación (arrastra para reordenar)
                </h3>
                <Reorder.Group axis="y" values={files} onReorder={setFiles} className="space-y-2">
                  {files.map((file, index) => (
                    <Reorder.Item
                      key={file.name}
                      value={file}
                      className="flex items-center gap-3 p-4 bg-white rounded-xl hover:shadow-sm transition-shadow cursor-move border border-gray-200"
                    >
                      <GripVertical className="w-5 h-5 text-gray-400" />
                      <div className="flex items-center justify-center w-8 h-8 bg-gray-900 text-white rounded-lg font-semibold text-sm">
                        {index + 1}
                      </div>
                      <div className="flex-1">
                        <p className="font-medium text-gray-900">{file.name}</p>
                        <p className="text-xs text-gray-500">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                      </div>
                      {index < files.length - 1 && (
                        <ArrowRight className="w-4 h-4 text-gray-400" />
                      )}
                    </Reorder.Item>
                  ))}
                </Reorder.Group>
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
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Combinando archivos...</h3>
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
                    <h3 className="text-lg font-semibold text-white mb-1">¡Proceso completado!</h3>
                    <p className="text-sm text-gray-300">Tu PDF combinado está listo</p>
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
            transition={{ delay: 0.2 }}
            className="flex gap-3"
          >
            <Button
              onClick={handleMerge}
              disabled={files.length < 2 || isProcessing}
              className="flex-1 bg-black hover:bg-gray-900 text-white h-12 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Combine className="w-5 h-5 mr-2" />
              {isProcessing ? 'Procesando...' : 'Combinar PDFs'}
            </Button>
          </motion.div>
        </div>
      </div>
    </div>
  );
}