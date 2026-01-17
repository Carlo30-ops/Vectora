import { motion } from 'motion/react';
import { Moon, Sun } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();
  const isDark = theme === 'dark';

  return (
    <button
      onClick={toggleTheme}
      className="relative w-16 h-8 rounded-full bg-gray-200 dark:bg-gray-700 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-900"
      aria-label="Toggle theme"
    >
      {/* Track */}
      <motion.div
        className="absolute inset-0 rounded-full"
        animate={{
          backgroundColor: isDark ? '#374151' : '#E5E7EB',
        }}
        transition={{ duration: 0.3 }}
      />
      
      {/* Knob */}
      <motion.div
        className="absolute top-1 left-1 w-6 h-6 bg-white dark:bg-gray-900 rounded-full shadow-lg flex items-center justify-center"
        animate={{
          x: isDark ? 32 : 0,
        }}
        transition={{
          type: 'spring',
          stiffness: 500,
          damping: 30,
        }}
      >
        {/* Icon inside knob */}
        <motion.div
          initial={false}
          animate={{
            scale: isDark ? 1 : 0,
            opacity: isDark ? 1 : 0,
          }}
          className="absolute"
        >
          <Moon className="w-3.5 h-3.5 text-indigo-400" />
        </motion.div>
        
        <motion.div
          initial={false}
          animate={{
            scale: isDark ? 0 : 1,
            opacity: isDark ? 0 : 1,
          }}
          className="absolute"
        >
          <Sun className="w-3.5 h-3.5 text-amber-500" />
        </motion.div>
      </motion.div>
      
      {/* Background icons */}
      <div className="absolute inset-0 flex items-center justify-between px-2 pointer-events-none">
        <motion.div
          animate={{
            opacity: isDark ? 0.3 : 0,
            scale: isDark ? 1 : 0.8,
          }}
        >
          <Moon className="w-3 h-3 text-gray-400" />
        </motion.div>
        <motion.div
          animate={{
            opacity: isDark ? 0 : 0.3,
            scale: isDark ? 0.8 : 1,
          }}
        >
          <Sun className="w-3 h-3 text-gray-500" />
        </motion.div>
      </div>
    </button>
  );
}
