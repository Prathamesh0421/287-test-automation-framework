import { motion } from 'framer-motion';
import { TrendingUp, CheckCircle, XCircle, Target } from 'lucide-react';
import { Doughnut, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import './TestResults.css';

ChartJS.register(
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function TestResults({ results }) {
  const doughnutData = {
    labels: ['Passed', 'Failed'],
    datasets: [
      {
        data: [results.passed, results.failed],
        backgroundColor: [
          'rgba(56, 239, 125, 0.8)',
          'rgba(235, 51, 73, 0.8)',
        ],
        borderWidth: 0,
      },
    ],
  };

  const barData = {
    labels: results.test_cases.map((tc) => `Test ${tc.id}`),
    datasets: [
      {
        label: 'Similarity Score (%)',
        data: results.test_cases.map((tc) => (tc.similarity_score * 100).toFixed(1)),
        backgroundColor: results.test_cases.map((tc) =>
          tc.passed ? 'rgba(56, 239, 125, 0.8)' : 'rgba(235, 51, 73, 0.8)'
        ),
        borderRadius: 8,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          padding: 20,
          font: {
            size: 14,
            weight: 600,
          },
        },
      },
    },
  };

  const barOptions = {
    ...chartOptions,
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: (value) => value + '%',
        },
      },
    },
    plugins: {
      ...chartOptions.plugins,
      legend: {
        display: false,
      },
    },
  };

  return (
    <motion.div
      className="results-card card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.5 }}
    >
      <h2 className="section-title">
        <TrendingUp className="title-icon" />
        Test Results
      </h2>

      <div className="stats-grid">
        <motion.div
          className="stat-card"
          whileHover={{ scale: 1.05 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <Target className="stat-icon" />
          <h3 className="stat-value">{results.total_tests}</h3>
          <p className="stat-label">Total Tests</p>
        </motion.div>

        <motion.div
          className="stat-card success"
          whileHover={{ scale: 1.05 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <CheckCircle className="stat-icon" />
          <h3 className="stat-value">{results.passed}</h3>
          <p className="stat-label">Passed</p>
        </motion.div>

        <motion.div
          className="stat-card danger"
          whileHover={{ scale: 1.05 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <XCircle className="stat-icon" />
          <h3 className="stat-value">{results.failed}</h3>
          <p className="stat-label">Failed</p>
        </motion.div>

        <motion.div
          className="stat-card primary"
          whileHover={{ scale: 1.05 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <TrendingUp className="stat-icon" />
          <h3 className="stat-value">{results.success_rate.toFixed(1)}%</h3>
          <p className="stat-label">Success Rate</p>
        </motion.div>
      </div>

      <div className="charts-grid">
        <div className="chart-container">
          <h3 className="chart-title">Test Results Overview</h3>
          <div className="chart-wrapper">
            <Doughnut data={doughnutData} options={chartOptions} />
          </div>
        </div>

        <div className="chart-container">
          <h3 className="chart-title">Similarity Scores by Test Case</h3>
          <div className="chart-wrapper">
            <Bar data={barData} options={barOptions} />
          </div>
        </div>
      </div>

      <div className="results-table-container">
        <h3 className="table-title">Detailed Results</h3>
        <div className="table-wrapper">
          <table className="results-table">
            <thead>
              <tr>
                <th>Test ID</th>
                <th>Status</th>
                <th>Similarity</th>
                <th>Expected</th>
                <th>Actual</th>
              </tr>
            </thead>
            <tbody>
              {results.test_cases.map((tc, index) => (
                <motion.tr
                  key={tc.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.05 }}
                >
                  <td>
                    <span className="test-id">#{tc.id}</span>
                  </td>
                  <td>
                    <span className={`badge ${tc.passed ? 'badge-success' : 'badge-danger'}`}>
                      {tc.passed ? (
                        <>
                          <CheckCircle size={16} />
                          PASS
                        </>
                      ) : (
                        <>
                          <XCircle size={16} />
                          FAIL
                        </>
                      )}
                    </span>
                  </td>
                  <td>
                    <span className="similarity-score">
                      {(tc.similarity_score * 100).toFixed(1)}%
                    </span>
                  </td>
                  <td className="description-cell">{tc.expected_description}</td>
                  <td className="description-cell">{tc.actual_description}</td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </motion.div>
  );
}

export default TestResults;
