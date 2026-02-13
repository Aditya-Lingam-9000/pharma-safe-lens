import { useState, useRef } from 'react';
import './ImageUpload.css';

const ImageUpload = ({ onImageSelect, selectedImage, uploadedImageUrl, loading, onUpload, onReset }) => {
  const [dragActive, setDragActive] = useState(false);
  const [validationError, setValidationError] = useState(null);
  const fileInputRef = useRef(null);
  const MAX_FILE_SIZE = 2 * 1024 * 1024;
  const ALLOWED_TYPES = ['image/jpeg', 'image/jpg', 'image/png'];

  const validateFile = (file) => {
    if (!file) { setValidationError('No file selected'); return false; }
    if (!ALLOWED_TYPES.includes(file.type)) { setValidationError('Only JPG/PNG allowed'); return false; }
    if (file.size > MAX_FILE_SIZE) { setValidationError('Max 2 MB'); return false; }
    setValidationError(null); return true;
  };

  const handleDrag = (e) => { e.preventDefault(); e.stopPropagation(); setDragActive(e.type === 'dragenter' || e.type === 'dragover'); };
  const handleDrop = (e) => { e.preventDefault(); e.stopPropagation(); setDragActive(false); if (e.dataTransfer.files?.[0] && validateFile(e.dataTransfer.files[0])) onImageSelect(e.dataTransfer.files[0]); };
  const handleChange = (e) => { e.preventDefault(); if (e.target.files?.[0] && validateFile(e.target.files[0])) onImageSelect(e.target.files[0]); };
  const handleClick = () => { if (!loading) fileInputRef.current?.click(); };
  const fmt = (b) => b < 1024 ? b + ' B' : b < 1048576 ? (b/1024).toFixed(1) + ' KB' : (b/1048576).toFixed(1) + ' MB';

  return (
    <div className="image-upload-container">
      <div className="upload-card card">
        <h2 className="upload-title">Upload Prescription</h2>
        <p className="upload-subtitle">Drag & drop or click to select an image</p>

        {!selectedImage ? (
          <div className={upload-dropzone }
            onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag}
            onDrop={handleDrop} onClick={handleClick}>
            <div className="dropzone-content">
              <div className="dropzone-icon">{dragActive ? '\u2193' : '\u2912'}</div>
              <p className="dropzone-text">{dragActive ? 'Drop here' : 'Click or drag image here'}</p>
              <p className="dropzone-hint">JPG, PNG \u00b7 Max 2 MB</p>
            </div>
            <input ref={fileInputRef} type="file" accept="image/jpeg,image/jpg,image/png"
              onChange={handleChange} style={{ display: 'none' }} disabled={loading} />
          </div>
        ) : (
          <div className="upload-preview">
            <div className="preview-image-container">
              <img src={uploadedImageUrl} alt="Prescription" className="preview-image" />
              <div className="preview-overlay">
                <button onClick={(e) => { e.stopPropagation(); onReset(); setValidationError(null); }}
                  className="preview-remove-btn" disabled={loading}>Remove</button>
              </div>
            </div>
            <div className="preview-info">
              <span className="filename-text">{selectedImage.name}</span>
              <span className="filesize-text">{fmt(selectedImage.size)}</span>
            </div>
          </div>
        )}

        {validationError && <div className="validation-error">{validationError}</div>}

        <div className="upload-actions">
          {selectedImage && (
            <>
              <button onClick={onUpload} disabled={loading || !!validationError} className="btn btn-primary upload-btn">
                {loading ? <><span className="btn-spinner"></span>Analyzing...</> : 'Analyze'}
              </button>
              {!loading && <button onClick={onReset} className="btn btn-secondary">Change Image</button>}
            </>
          )}
        </div>

        <div className="upload-instructions">
          <div className="instruction-item"><span className="instruction-number">1</span><span>Upload image</span></div>
          <div className="instruction-item"><span className="instruction-number">2</span><span>OCR extraction</span></div>
          <div className="instruction-item"><span className="instruction-number">3</span><span>AI analysis</span></div>
          <div className="instruction-item"><span className="instruction-number">4</span><span>Safety report</span></div>
        </div>
      </div>
    </div>
  );
};

export default ImageUpload;
