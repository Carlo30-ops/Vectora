import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { FileDropzone } from '../FileDropzone';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Switch } from '../ui/switch';
import { Progress } from '../ui/progress';
import { Shield, Download, Lock, Unlock, Eye, EyeOff } from 'lucide-react';
import { toast } from 'sonner';

type SecurityMode = 'encrypt' | 'decrypt' | 'permissions';

const securityModes = [
  {
    id: 'encrypt' as SecurityMode,
    title: 'Encriptar',
    description: 'Protege tu PDF con contraseña',
    icon: Lock,
    gradient: 'from-blue-500 to-indigo-500',
  },
  {
    id: 'decrypt' as SecurityMode,
    title: 'Desencriptar',
    description: 'Remueve la protección del PDF',
    icon: Unlock,
    gradient: 'from-purple-500 to-pink-500',
  },
  {
    id: 'permissions' as SecurityMode,
    title: 'Permisos',
    description: 'Configura restricciones específicas',
    icon: Shield,
    gradient: 'from-emerald-500 to-teal-500',
  },
];

export function SecurityPDF() {
  const [mode, setMode] = useState<SecurityMode>('encrypt');
  const [files, setFiles] = useState<File[]>([]);
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [isComplete, setIsComplete] = useState(false);

  // Permissions
  const [allowPrint, setAllowPrint] = useState(true);
  const [allowCopy, setAllowCopy] = useState(true);
  const [allowModify, setAllowModify] = useState(false);
  const [allowAnnotations, setAllowAnnotations] = useState(true);

  const handleProcess = async () => {
    if (files.length === 0) {
      toast.error('Por favor selecciona un archivo PDF');
      return;
    }

    if (mode === 'encrypt' || mode === 'decrypt') {
      if (!password) {
        toast.error('Por favor ingresa una contraseña');
        return;
      }

      if (mode === 'encrypt' && password !== confirmPassword) {
        toast.error('Las contraseñas no coinciden');
        return;
      }
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
    
    if (mode === 'encrypt') {
      toast.success('¡PDF encriptado exitosamente!');
    } else if (mode === 'decrypt') {
      toast.success('¡PDF desencriptado exitosamente!');
    } else {
      toast.success('¡Permisos configurados exitosamente!');
    }
  };

  const handleDownload = () => {
    toast.success('Descargando archivo procesado...');
  };

  const currentMode = securityModes.find(m => m.id === mode)!;

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
              <Shield className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Seguridad PDF
              </h1>
              <p className="text-gray-600">Protege y gestiona la seguridad de tus documentos</p>
            </div>
          </div>
        </motion.div>

        {/* Main Content */}
        <div className="space-y-6">
          {/* Mode Selection */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Tipo de operación</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {securityModes.map((item) => {
                const Icon = item.icon;
                const isSelected = mode === item.id;
                
                return (
                  <motion.button
                    key={item.id}
                    onClick={() => {
                      setMode(item.id);
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
                    <div className={`w-12 h-12 bg-black rounded-xl flex items-center justify-center mb-3`}>
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    <h4 className={`font-semibold ${isSelected ? 'text-white' : 'text-gray-900'} mb-1`}>{item.title}</h4>
                    <p className={`text-sm ${isSelected ? 'text-gray-300' : 'text-gray-600'}`}>{item.description}</p>
                  </motion.button>
                );
              })}
            </div>
          </motion.div>

          {/* File Upload */}
          <motion.div
            key={mode}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
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

          {/* Security Settings */}
          <AnimatePresence>
            {files.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="bg-gray-50 rounded-2xl p-6 border border-gray-200"
              >
                <h3 className="text-lg font-semibold text-gray-800 mb-4">
                  {mode === 'encrypt' && 'Configuración de encriptación'}
                  {mode === 'decrypt' && 'Desencriptar documento'}
                  {mode === 'permissions' && 'Configurar permisos'}
                </h3>

                {/* Password Fields */}
                {(mode === 'encrypt' || mode === 'decrypt') && (
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="password">Contraseña</Label>
                      <div className="relative mt-2">
                        <Input
                          id="password"
                          type={showPassword ? 'text' : 'password'}
                          value={password}
                          onChange={(e) => setPassword(e.target.value)}
                          placeholder="Ingresa una contraseña segura"
                          className="pr-10"
                        />
                        <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                        >
                          {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                        </button>
                      </div>
                    </div>

                    {mode === 'encrypt' && (
                      <div>
                        <Label htmlFor="confirmPassword">Confirmar contraseña</Label>
                        <Input
                          id="confirmPassword"
                          type={showPassword ? 'text' : 'password'}
                          value={confirmPassword}
                          onChange={(e) => setConfirmPassword(e.target.value)}
                          placeholder="Confirma tu contraseña"
                          className="mt-2"
                        />
                      </div>
                    )}

                    <div className="bg-blue-50 rounded-xl p-4">
                      <p className="text-sm text-blue-800">
                        💡 <strong>Consejo:</strong> Usa una contraseña de al menos 8 caracteres con letras, números y símbolos
                      </p>
                    </div>
                  </div>
                )}

                {/* Permissions */}
                {mode === 'permissions' && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                      <div>
                        <Label htmlFor="allowPrint" className="text-base">Permitir impresión</Label>
                        <p className="text-sm text-gray-600 mt-1">Los usuarios pueden imprimir el documento</p>
                      </div>
                      <Switch
                        id="allowPrint"
                        checked={allowPrint}
                        onCheckedChange={setAllowPrint}
                      />
                    </div>

                    <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                      <div>
                        <Label htmlFor="allowCopy" className="text-base">Permitir copiar texto</Label>
                        <p className="text-sm text-gray-600 mt-1">Los usuarios pueden copiar contenido</p>
                      </div>
                      <Switch
                        id="allowCopy"
                        checked={allowCopy}
                        onCheckedChange={setAllowCopy}
                      />
                    </div>

                    <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                      <div>
                        <Label htmlFor="allowModify" className="text-base">Permitir modificar</Label>
                        <p className="text-sm text-gray-600 mt-1">Los usuarios pueden editar el documento</p>
                      </div>
                      <Switch
                        id="allowModify"
                        checked={allowModify}
                        onCheckedChange={setAllowModify}
                      />
                    </div>

                    <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                      <div>
                        <Label htmlFor="allowAnnotations" className="text-base">Permitir anotaciones</Label>
                        <p className="text-sm text-gray-600 mt-1">Los usuarios pueden agregar comentarios</p>
                      </div>
                      <Switch
                        id="allowAnnotations"
                        checked={allowAnnotations}
                        onCheckedChange={setAllowAnnotations}
                      />
                    </div>
                  </div>
                )}
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
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Procesando...</h3>
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
                    <p className="text-sm text-gray-300">Tu PDF ha sido procesado exitosamente</p>
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
              onClick={handleProcess}
              disabled={files.length === 0 || isProcessing}
              className="w-full bg-black hover:bg-gray-900 text-white h-12 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Shield className="w-5 h-5 mr-2" />
              {isProcessing ? 'Procesando...' : currentMode.title}
            </Button>
          </motion.div>
        </div>
      </div>
    </div>
  );
}