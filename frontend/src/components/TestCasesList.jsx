import { motion } from 'framer-motion';
import { Play, Trash2, X, FileImage } from 'lucide-react';
import './TestCasesList.css';

function TestCasesList({ testCases, onDelete, onClearAll, onRunTests, isLoading }) {
  return (
    <motion.div
      className="test-cases-card card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
    >
      <div className="card-header">
        <h2 className="section-title">
          <FileImage className="title-icon" />
          Test Cases
          <span className="count-badge">{testCases.length}</span>
        </h2>

        <div className="action-buttons">
          <button
            className="btn btn-success"
            onClick={onRunTests}
            disabled={isLoading || testCases.length === 0}
          >
            {isLoading ? (
              <>
                <div className="spinner-small"></div>
                Running...
              </>
            ) : (
              <>
                <Play size={20} />
                Run All Tests
              </>
            )}
          </button>
          <button
            className="btn btn-danger"
            onClick={onClearAll}
            disabled={testCases.length === 0}
          >
            <Trash2 size={20} />
            Clear All
          </button>
        </div>
      </div>

      <div className="test-cases-list">
        {testCases.length === 0 ? (
          <motion.div
            className="empty-state"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <FileImage size={80} className="empty-icon" />
            <p>No test cases yet. Add your first test case above!</p>
          </motion.div>
        ) : (
          testCases.map((testCase, index) => (
            <motion.div
              key={testCase.id}
              className="test-case-item"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
              whileHover={{ scale: 1.02 }}
            >
              <div className="test-case-image-container">
                <img
                  src={`http://localhost:5000/uploads/${testCase.image_path}`}
                  alt={`Test ${testCase.id}`}
                  className="test-case-image"
                />
                <div className="test-case-id">#{testCase.id}</div>
              </div>

              <div className="test-case-info">
                <h4>Test Case #{testCase.id}</h4>
                <p>{testCase.expected_description}</p>
              </div>

              <button
                className="btn-icon btn-danger-icon"
                onClick={() => onDelete(testCase.id)}
                title="Delete test case"
              >
                <X size={20} />
              </button>
            </motion.div>
          ))
        )}
      </div>
    </motion.div>
  );
}

export default TestCasesList;
