import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { FileDropzone } from '../FileDropzone';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Progress } from '../ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Scissors, Download } from 'lucide-react';
import { toast } from 'sonner';

type SplitMode = 'range' | 'pages' | 'every';

export function SplitPDF() {
  const [files, setFiles] = useState<File[]>([]);
  const [splitMode, setSplitMode] = useState<SplitMode>('range');
  const [rangeStart, setRangeStart] = useState('1');
  const [rangeEnd, setRangeEnd] = useState('');
  const [specificPages, setSpecificPages] = useState('');
  const [everyNPages, setEveryNPages] = useState('1');
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [isComplete, setIsComplete] = useState(false);

  const handleSplit = async () => {
    if (files.length === 0) {
      toast.error('Por favor selecciona un archivo PDF');
      return;
    }

    setIsProcessing(true);
    setProgress(0);
    setIsComplete(false);

    // Simular procesamiento
    for (let i = 0; i <= 100; i += 10) {
      await new Promise(resolve => setTimeout(resolve, 150));
      setProgress(i);
    }

    setIsProcessing(false);
    setIsComplete(true);
    toast.success('¡PDF dividido exitosamente!');
  };

  const handleDownload = () => {
    toast.success('Descargando archivos divididos...');
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
              <Scissors className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Dividir PDF
              </h1>
              <p className="text-gray-600">Extrae páginas específicas o divide por rangos</p>
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
              multiple={false}
              maxFiles={1}
              title="Arrastra tu PDF aquí"
              description="o haz clic para seleccionar un archivo"
            />
          </motion.div>

          {/* Split Options */}
          <AnimatePresence>
            {files.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="bg-gray-50 rounded-2xl p-6 border border-gray-200"
              >
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Opciones de división</h3>
                
                <Tabs value={splitMode} onValueChange={(v) => setSplitMode(v as SplitMode)}>
                  <TabsList className="grid w-full grid-cols-3 mb-6">
                    <TabsTrigger value="range">Por rango</TabsTrigger>
                    <TabsTrigger value="pages">Páginas específicas</TabsTrigger>
                    <TabsTrigger value="every">Cada N páginas</TabsTrigger>
                  </TabsList>

                  <TabsContent value="range" className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="rangeStart">Página inicial</Label>
                        <Input
                          id="rangeStart"
                          type="number"
                          min="1"
                          value={rangeStart}
                          onChange={(e) => setRangeStart(e.target.value)}
                          className="mt-2"
                          placeholder="1"
                        />
                      </div>
                      <div>
                        <Label htmlFor="rangeEnd">Página final</Label>
                        <Input
                          id="rangeEnd"
                          type="number"
                          min="1"
                          value={rangeEnd}
                          onChange={(e) => setRangeEnd(e.target.value)}
                          className="mt-2"
                          placeholder="10"
                        />
                      </div>
                    </div>
                    <p className="text-sm text-gray-600">
                      Extrae un rango continuo de páginas del PDF
                    </p>
                  </TabsContent>

                  <TabsContent value="pages" className="space-y-4">
                    <div>
                      <Label htmlFor="specificPages">Páginas (separadas por coma)</Label>
                      <Input
                        id="specificPages"
                        value={specificPages}
                        onChange={(e) => setSpecificPages(e.target.value)}
                        className="mt-2"
                        placeholder="1, 3, 5, 7-10"
                      />
                    </div>
                    <p className="text-sm text-gray-600">
                      Ejemplo: "1, 3, 5-8, 12" extraerá las páginas 1, 3, 5, 6, 7, 8 y 12
                    </p>
                  </TabsContent>

                  <TabsContent value="every" className="space-y-4">
                    <div>
                      <Label htmlFor="everyNPages">Dividir cada N páginas</Label>
                      <Input
                        id="everyNPages"
                        type="number"
                        min="1"
                        value={everyNPages}
                        onChange={(e) => setEveryNPages(e.target.value)}
                        className="mt-2"
                        placeholder="5"
                      />
                    </div>
                    <p className="text-sm text-gray-600">
                      Divide el PDF en múltiples archivos cada N páginas
                    </p>
                  </TabsContent>
                </Tabs>
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
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Dividiendo archivo...</h3>
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
                    <p className="text-sm text-gray-300">Se generaron 3 archivos PDF</p>
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
          >
            <Button
              onClick={handleSplit}
              disabled={files.length === 0 || isProcessing}
              className="w-full bg-black hover:bg-gray-900 text-white h-12 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Scissors className="w-5 h-5 mr-2" />
              {isProcessing ? 'Procesando...' : 'Dividir PDF'}
            </Button>
          </motion.div>
        </div>
      </div>
    </div>
  );
}