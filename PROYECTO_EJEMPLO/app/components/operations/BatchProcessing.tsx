import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { FileDropzone } from '../FileDropzone';
import { Button } from '../ui/button';
import { Progress } from '../ui/progress';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Label } from '../ui/label';
import { Switch } from '../ui/switch';
import { FolderClock, Download, Play, Folder, CheckCircle2, Clock } from 'lucide-react';
import { toast } from 'sonner';

type BatchOperation = 'merge' | 'compress' | 'convert' | 'ocr' | 'encrypt';

const batchOperations = [
  { id: 'merge' as BatchOperation, name: 'Combinar todos', description: 'Une todos los archivos en uno' },
  { id: 'compress' as BatchOperation, name: 'Comprimir cada uno', description: 'Reduce el tamaño de cada PDF' },
  { id: 'convert' as BatchOperation, name: 'Convertir a Word', description: 'Convierte cada PDF a DOCX' },
  { id: 'ocr' as BatchOperation, name: 'Aplicar OCR', description: 'Reconocimiento de texto en todos' },
  { id: 'encrypt' as BatchOperation, name: 'Encriptar todos', description: 'Protege con contraseña' },
];

interface FileStatus {
  name: string;
  status: 'pending' | 'processing' | 'completed' | 'error';
  progress: number;
}

export function BatchProcessing() {
  const [files, setFiles] = useState<File[]>([]);
  const [operation, setOperation] = useState<BatchOperation>('compress');
  const [watchFolder, setWatchFolder] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [overallProgress, setOverallProgress] = useState(0);
  const [fileStatuses, setFileStatuses] = useState<FileStatus[]>([]);
  const [isComplete, setIsComplete] = useState(false);

  const handleProcess = async () => {
    if (files.length === 0) {
      toast.error('Por favor selecciona archivos para procesar');
      return;
    }

    setIsProcessing(true);
    setOverallProgress(0);
    setIsComplete(false);

    // Inicializar estados de archivos
    const statuses: FileStatus[] = files.map(file => ({
      name: file.name,
      status: 'pending',
      progress: 0,
    }));
    setFileStatuses(statuses);

    // Simular procesamiento por lotes
    for (let i = 0; i < files.length; i++) {
      // Actualizar estado a procesando
      setFileStatuses(prev => prev.map((s, idx) => 
        idx === i ? { ...s, status: 'processing' } : s
      ));

      // Simular progreso del archivo individual
      for (let p = 0; p <= 100; p += 20) {
        await new Promise(resolve => setTimeout(resolve, 100));
        setFileStatuses(prev => prev.map((s, idx) => 
          idx === i ? { ...s, progress: p } : s
        ));
      }

      // Marcar como completado
      setFileStatuses(prev => prev.map((s, idx) => 
        idx === i ? { ...s, status: 'completed', progress: 100 } : s
      ));

      // Actualizar progreso general
      const overall = ((i + 1) / files.length) * 100;
      setOverallProgress(overall);
    }

    setIsProcessing(false);
    setIsComplete(true);
    toast.success(`¡${files.length} archivos procesados exitosamente!`);
  };

  const handleDownload = () => {
    toast.success('Descargando archivos procesados...');
  };

  return (
    <div className="h-full overflow-y-auto bg-white">
      <div className="max-w-5xl mx-auto p-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center gap-4 mb-4">
            <div className="w-14 h-14 bg-black rounded-2xl flex items-center justify-center">
              <FolderClock className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Procesamiento por Lotes
              </h1>
              <p className="text-gray-600">Automatiza operaciones en múltiples archivos</p>
            </div>
          </div>
        </motion.div>

        {/* Main Content */}
        <div className="space-y-6">
          {/* Operation Selection */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-gray-50 rounded-2xl p-6 border border-gray-200"
          >
            <div className="space-y-4">
              <div>
                <Label htmlFor="operation" className="text-base mb-3 block">
                  Operación a realizar
                </Label>
                <Select value={operation} onValueChange={(v) => setOperation(v as BatchOperation)}>
                  <SelectTrigger id="operation" className="w-full">
                    <SelectValue placeholder="Selecciona una operación" />
                  </SelectTrigger>
                  <SelectContent>
                    {batchOperations.map((op) => (
                      <SelectItem key={op.id} value={op.id}>
                        <div className="flex flex-col items-start">
                          <span className="font-medium">{op.name}</span>
                          <span className="text-xs text-gray-500">{op.description}</span>
                        </div>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="flex items-center justify-between p-4 bg-amber-50 rounded-xl">
                <div className="flex items-center gap-3">
                  <Folder className="w-5 h-5 text-amber-600" />
                  <div>
                    <Label htmlFor="watchFolder" className="text-base">Carpeta vigilada</Label>
                    <p className="text-sm text-gray-600 mt-1">
                      Procesa automáticamente archivos nuevos
                    </p>
                  </div>
                </div>
                <Switch
                  id="watchFolder"
                  checked={watchFolder}
                  onCheckedChange={setWatchFolder}
                />
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
              maxFiles={50}
              title="Arrastra múltiples archivos aquí"
              description="o haz clic para seleccionar (máximo 50 archivos)"
            />
          </motion.div>

          {/* File Status List */}
          <AnimatePresence>
            {fileStatuses.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="bg-gray-50 rounded-2xl p-6 border border-gray-200"
              >
                <h3 className="text-lg font-semibold text-gray-800 mb-4">
                  Estado del procesamiento
                </h3>

                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {fileStatuses.map((file, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.05 }}
                      className="flex items-center gap-3 p-3 bg-white rounded-xl"
                    >
                      {/* Status Icon */}
                      <div className="flex-shrink-0">
                        {file.status === 'pending' && (
                          <Clock className="w-5 h-5 text-gray-400" />
                        )}
                        {file.status === 'processing' && (
                          <motion.div
                            animate={{ rotate: 360 }}
                            transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                          >
                            <Play className="w-5 h-5 text-blue-500" />
                          </motion.div>
                        )}
                        {file.status === 'completed' && (
                          <CheckCircle2 className="w-5 h-5 text-green-500" />
                        )}
                      </div>

                      {/* File Info */}
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-800 truncate">
                          {file.name}
                        </p>
                        {file.status === 'processing' && (
                          <Progress value={file.progress} className="mt-2 h-1" />
                        )}
                      </div>

                      {/* Status Badge */}
                      <div className="flex-shrink-0">
                        {file.status === 'pending' && (
                          <span className="text-xs px-2 py-1 bg-gray-100 text-gray-600 rounded-full">
                            Pendiente
                          </span>
                        )}
                        {file.status === 'processing' && (
                          <span className="text-xs px-2 py-1 bg-blue-100 text-blue-600 rounded-full">
                            {file.progress}%
                          </span>
                        )}
                        {file.status === 'completed' && (
                          <span className="text-xs px-2 py-1 bg-green-100 text-green-600 rounded-full">
                            ✓ Listo
                          </span>
                        )}
                      </div>
                    </motion.div>
                  ))}
                </div>

                {/* Overall Progress */}
                {isProcessing && (
                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-gray-700">Progreso general</span>
                      <span className="text-sm font-semibold text-amber-600">
                        {Math.round(overallProgress)}%
                      </span>
                    </div>
                    <Progress value={overallProgress} className="h-2" />
                  </div>
                )}
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
                    <h3 className="text-lg font-semibold text-white mb-1">
                      ¡Lote completado!
                    </h3>
                    <p className="text-sm text-gray-300">
                      {files.length} archivos procesados exitosamente
                    </p>
                  </div>
                  <Button
                    onClick={handleDownload}
                    className="bg-white hover:bg-gray-100 text-black"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Descargar Todo
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
              onClick={handleProcess}
              disabled={files.length === 0 || isProcessing}
              className="w-full bg-black hover:bg-gray-900 text-white h-12 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Play className="w-5 h-5 mr-2" />
              {isProcessing ? 'Procesando...' : 'Iniciar Procesamiento'}
            </Button>
          </motion.div>
        </div>
      </div>
    </div>
  );
}