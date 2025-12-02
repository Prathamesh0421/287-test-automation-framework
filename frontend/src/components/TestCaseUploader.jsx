import { useState } from 'react';
import { motion } from 'framer-motion';
import { useDropzone } from 'react-dropzone';
import { Upload, Image as ImageIcon, FileText, Plus } from 'lucide-react';
import './TestCaseUploader.css';

function TestCaseUploader({ onTestCaseAdded }) {
  const [description, setDescription] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.webp']
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        const file = acceptedFiles[0];
        setSelectedFile(file);
        setPreviewUrl(URL.createObjectURL(file));
      }
    }
  });

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedFile) {
      alert('Please select an image');
      return;
    }

    if (!description) {
      alert('Please enter an expected description');
      return;
    }

    setIsUploading(true);

    const formData = new FormData();
    formData.append('image', selectedFile);
    formData.append('description', description);

    try {
      const response = await fetch('http://localhost:5000/api/test-cases', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        setDescription('');
        setSelectedFile(null);
        setPreviewUrl(null);
        onTestCaseAdded();
      } else {
        const error = await response.json();
        alert('Error: ' + error.error);
      }
    } catch (error) {
      alert('Error adding test case: ' + error.message);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <motion.div
      className="uploader-card card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.1 }}
    >
      <h2 className="section-title">
        <Plus className="title-icon" />
        Add Test Case
      </h2>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>
            <ImageIcon size={18} />
            Image
          </label>
          <div
            {...getRootProps()}
            className={`dropzone ${isDragActive ? 'active' : ''} ${previewUrl ? 'has-image' : ''}`}
          >
            <input {...getInputProps()} />
            {previewUrl ? (
              <div className="preview-container">
                <img src={previewUrl} alt="Preview" className="preview-image" />
                <div className="preview-overlay">
                  <Upload size={30} />
                  <p>Click or drag to change</p>
                </div>
              </div>
            ) : (
              <div className="dropzone-content">
                <Upload size={48} className="dropzone-icon" />
                <p className="dropzone-text">
                  {isDragActive ? 'Drop your image here' : 'Click to upload or drag and drop'}
                </p>
                <p className="dropzone-hint">PNG, JPG, GIF, WEBP (Max 16MB)</p>
              </div>
            )}
          </div>
        </div>

        <div className="form-group">
          <label>
            <FileText size={18} />
            Expected Description
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Enter the expected description of the image..."
            rows="4"
          />
        </div>

        <button type="submit" className="btn btn-primary" disabled={isUploading}>
          {isUploading ? (
            <>
              <div className="spinner-small"></div>
              Adding...
            </>
          ) : (
            <>
              <Plus size={20} />
              Add Test Case
            </>
          )}
        </button>
      </form>
    </motion.div>
  );
}

export default TestCaseUploader;
