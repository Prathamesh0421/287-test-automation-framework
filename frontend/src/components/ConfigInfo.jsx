import { motion } from 'framer-motion';
import { Settings, Zap } from 'lucide-react';
import './ConfigInfo.css';

function ConfigInfo({ config }) {
  if (!config) return null;

  return (
    <motion.div
      className="config-info glass"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
    >
      <div className="config-item">
        <Settings size={20} className="config-icon" />
        <span className="config-label">API Provider:</span>
        <span className="config-value">{config.api_provider.toUpperCase()}</span>
      </div>
      <div className="config-divider"></div>
      <div className="config-item">
        <Zap size={20} className="config-icon" />
        <span className="config-label">Similarity Threshold:</span>
        <span className="config-value">{config.similarity_threshold}</span>
      </div>
    </motion.div>
  );
}

export default ConfigInfo;
