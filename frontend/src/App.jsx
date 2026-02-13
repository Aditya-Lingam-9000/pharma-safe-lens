import { useState } from 'react';
import ImageUpload from './components/ImageUpload';
import ResultsDisplay from './components/ResultsDisplay';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import { uploadImage, getApiUrl } from './services/api';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [uploadedImageUrl, setUploadedImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);

  const handleImageSelect = (file) => {
    setSelectedImage(file);
    setUploadedImageUrl(URL.createObjectURL(file));
    setError(null);
    setResults(null);
  };

  const handleUpload = async () => {
    if (!selectedImage) { setError('Please select an image first'); return; }
    setLoading(true); setError(null); setResults(null);
    try {
      console.log('Uploading to:', getApiUrl());
      const data = await uploadImage(selectedImage);
      console.log('Results:', data);
      setResults(data);
    } catch (err) {
      console.error('Upload failed:', err);
      setError(err.message || 'Failed to analyze image.');
    } finally { setLoading(false); }
  };

  const handleReset = () => {
    setSelectedImage(null); setUploadedImageUrl(null);
    setLoading(false); setError(null); setResults(null);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="logo-section">
          <div>
            <h1 className="logo-title">Pharma-Safe Lens</h1>
            <p className="logo-subtitle">AI-Powered Drug Interaction Analysis</p>
          </div>
        </div>
        <div className="header-badge">TxGemma 9B</div>
      </header>

      <main className="main-content">
        <section className="upload-section">
          <ImageUpload
            onImageSelect={handleImageSelect}
            selectedImage={selectedImage}
            uploadedImageUrl={uploadedImageUrl}
            loading={loading}
            onUpload={handleUpload}
            onReset={handleReset}
          />
        </section>

        {loading && <section className="loading-section"><LoadingSpinner /></section>}
        {error && !loading && <section className="error-section"><ErrorMessage message={error} onRetry={handleUpload} /></section>}
        {results && !loading && !error && <section className="results-section"><ResultsDisplay results={results} /></section>}

        {!selectedImage && !loading && !error && !results && (
          <section className="empty-state">
            <h2 className="empty-state-title">Upload a prescription to begin</h2>
            <p className="empty-state-text">Detect potential drug interactions using AI analysis</p>
            <div className="empty-state-features">
              <div className="feature-item">OCR Extraction</div>
              <div className="feature-item">Drug Normalization</div>
              <div className="feature-item">AI Analysis</div>
              <div className="feature-item">Safety Validation</div>
            </div>
          </section>
        )}
      </main>

      <footer className="app-footer">
        <p className="footer-text">For informational purposes only. Always consult healthcare professionals.</p>
        <p className="footer-credits">Powered by TxGemma &middot; React + Vite</p>
      </footer>
    </div>
  );
}

export default App;
