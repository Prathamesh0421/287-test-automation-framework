import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Image, Upload, Play, Trash2, TrendingUp, CheckCircle, XCircle } from 'lucide-react';
import TestCaseUploader from './components/TestCaseUploader';
import TestCasesList from './components/TestCasesList';
import TestResults from './components/TestResults';
import Header from './components/Header';
import ConfigInfo from './components/ConfigInfo';
import './App.css';

function App() {
  const [testCases, setTestCases] = useState([]);
  const [config, setConfig] = useState(null);
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadConfig();
    loadTestCases();
  }, []);

  const loadConfig = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/config');
      const data = await response.json();
      setConfig(data);
    } catch (error) {
      console.error('Error loading config:', error);
    }
  };

  const loadTestCases = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/test-cases');
      const data = await response.json();
      setTestCases(data.test_cases);
    } catch (error) {
      console.error('Error loading test cases:', error);
    }
  };

  const handleTestCaseAdded = () => {
    loadTestCases();
  };

  const handleDeleteTestCase = async (id) => {
    try {
      await fetch(`http://localhost:5000/api/test-cases/${id}`, {
        method: 'DELETE',
      });
      loadTestCases();
    } catch (error) {
      console.error('Error deleting test case:', error);
    }
  };

  const handleClearAll = async () => {
    if (!window.confirm('Are you sure you want to clear all test cases?')) return;

    try {
      await fetch('http://localhost:5000/api/test-cases/clear', {
        method: 'POST',
      });
      loadTestCases();
      setResults(null);
    } catch (error) {
      console.error('Error clearing test cases:', error);
    }
  };

  const handleRunTests = async () => {
    if (testCases.length === 0) {
      alert('Please add test cases first');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/run-tests', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}), // Send empty JSON object
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to run tests');
      }

      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error running tests:', error);
      alert(`Error running tests: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="background-gradient"></div>
      <div className="background-pattern"></div>

      <Header />

      <motion.div
        className="container"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <ConfigInfo config={config} />

        <TestCaseUploader onTestCaseAdded={handleTestCaseAdded} />

        <TestCasesList
          testCases={testCases}
          onDelete={handleDeleteTestCase}
          onClearAll={handleClearAll}
          onRunTests={handleRunTests}
          isLoading={isLoading}
        />

        <AnimatePresence>
          {results && (
            <TestResults results={results} />
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
}

export default App;
