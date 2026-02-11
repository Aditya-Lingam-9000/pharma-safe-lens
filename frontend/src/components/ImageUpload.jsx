import { useState, useRef } from 'react';
import './ImageUpload.css';

const ImageUpload = ({ onImageSelect, selectedImage, uploadedImageUrl, loading, onUpload, onReset }) => {
  const [dragActive, setDragActive] = useState(false);
  const [validationError, setValidationError] = useState(null);
  const fileInputRef = useRef(null);

  const MAX_FILE_SIZE = 2 * 1024 * 1024; // 2MB
  const ALLOWED_TYPES = ['image/jpeg', 'image/jpg', 'image/png'];

  const validateFile = (file) => {
    if (!file) {
      setValidationError('No file selected');
      return false;
    }

    if (!ALLOWED_TYPES.includes(file.type)) {
      setValidationError('Only JPG, JPEG, and PNG files are allowed');
      return false;
    }

    if (file.size > MAX_FILE_SIZE) {
      setValidationError('File size must be less than 2MB');
      return false;
    }

    setValidationError(null);
    return true;
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (validateFile(file)) {
        onImageSelect(file);
      }
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (validateFile(file)) {
        onImageSelect(file);
      }
    }
  };

  const handleClick = () => {
    if (!loading) {
      fileInputRef.current?.click();
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <div className="image-upload-container">
      <div className="upload-card card">
        <h2 className="upload-title">📸 Upload Prescription Image</h2>
        <p className="upload-subtitle">Drag & drop or click to browse</p>

        {!selectedImage ? (
          // Upload Zone
          <div
            className={`upload-dropzone ${dragActive ? 'drag-active' : ''}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={handleClick}
          >
            <div className="dropzone-content">
              <div className="dropzone-icon">
                {dragActive ? '📥' : '🖼️'}
              </div>
              <p className="dropzone-text">
                {dragActive ? 'Drop image here' : 'Click or drag image here'}
              </p>
              <p className="dropzone-hint">
                Supported: JPG, JPEG, PNG • Max size: 2MB
              </p>
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/jpeg,image/jpg,image/png"
              onChange={handleChange}
              style={{ display: 'none' }}
              disabled={loading}
            />
          </div>
        ) : (
          // Preview Zone
          <div className="upload-preview">
            <div className="preview-image-container">
              <img
                src={uploadedImageUrl}
                alt="Selected prescription"
                className="preview-image"
              />
              <div className="preview-overlay">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onReset();
                    setValidationError(null);
                  }}
                  className="preview-remove-btn"
                  disabled={loading}
                >
                  ❌ Remove
                </button>
              </div>
            </div>
            <div className="preview-info">
              <div className="preview-filename">
                <span className="filename-icon">📄</span>
                <span className="filename-text">{selectedImage.name}</span>
              </div>
              <div className="preview-filesize">
                <span className="filesize-icon">💾</span>
                <span className="filesize-text">{formatFileSize(selectedImage.size)}</span>
              </div>
            </div>
          </div>
        )}

        {/* Validation Error */}
        {validationError && (
          <div className="validation-error">
            <span className="error-icon">⚠️</span>
            <span>{validationError}</span>
          </div>
        )}

        {/* Action Buttons */}
        <div className="upload-actions">
          {selectedImage && (
            <>
              <button
                onClick={onUpload}
                disabled={loading || !!validationError}
                className="btn btn-primary upload-btn"
              >
                {loading ? (
                  <>
                    <span className="btn-spinner"></span>
                    Analyzing...
                  </>
                ) : (
                  <>
                    🚀 Analyze Prescription
                  </>
                )}
              </button>
              {!loading && (
                <button
                  onClick={onReset}
                  className="btn btn-secondary"
                >
                  🔄 Choose Different Image
                </button>
              )}
            </>
          )}
        </div>

        {/* Instructions */}
        <div className="upload-instructions">
          <div className="instruction-item">
            <span className="instruction-number">1</span>
            <span className="instruction-text">Upload clear prescription image</span>
          </div>
          <div className="instruction-item">
            <span className="instruction-number">2</span>
            <span className="instruction-text">AI extracts drug names using OCR</span>
          </div>
          <div className="instruction-item">
            <span className="instruction-number">3</span>
            <span className="instruction-text">MedGemma analyzes interactions</span>
          </div>
          <div className="instruction-item">
            <span className="instruction-number">4</span>
            <span className="instruction-text">Get detailed safety report</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImageUpload;
