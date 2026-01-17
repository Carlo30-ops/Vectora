import { motion } from 'motion/react';
import { LucideIcon } from 'lucide-react';

interface OperationHeaderProps {
  icon: LucideIcon;
  title: string;
  description: string;
}

export function OperationHeader({ icon: Icon, title, description }: OperationHeaderProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-8"
    >
      <div className="flex items-center gap-4 mb-4">
        <div className="w-14 h-14 bg-black rounded-2xl flex items-center justify-center">
          <Icon className="w-7 h-7 text-white" />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">{title}</h1>
          <p className="text-gray-600">{description}</p>
        </div>
      </div>
    </motion.div>
  );
}
