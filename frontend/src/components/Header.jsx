import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';
import './Header.css';

function Header() {
  return (
    <motion.header
      className="header glass-dark"
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, type: "spring" }}
    >
      <div className="header-content">
        <motion.div
          className="header-icon"
          animate={{
            rotate: [0, 10, -10, 0],
            scale: [1, 1.1, 1],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        >
          <Sparkles size={40} />
        </motion.div>
        <div>
          <h1 className="header-title">Image Testing System</h1>
          <p className="header-subtitle">Automated vision AI testing with semantic comparison</p>
        </div>
      </div>
    </motion.header>
  );
}

export default Header;
