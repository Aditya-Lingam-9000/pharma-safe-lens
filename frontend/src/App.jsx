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
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      console.log('📤 Uploading image to backend...');
      const data = await uploadImage(selectedImage);
      console.log('✅ Received results:', data);
      setResults(data);
    } catch (err) {
      console.error('❌ Upload failed:', err);
      setError(err.message || 'Failed to analyze image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setUploadedImageUrl(null);
    setLoading(false);
    setError(null);
    setResults(null);
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <div className="logo-section">
          <div className="logo-icon">💊</div>
          <div className="logo-text">
            <h1 className="logo-title">PHARMA-SAFE LENS</h1>
            <p className="logo-subtitle">AI-Powered Drug Interaction Analyzer</p>
          </div>
        </div>
        <div className="api-status">
          <span className="status-dot"></span>
          <span className="status-text">Backend: {getApiUrl()}</span>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {/* Upload Section */}
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

        {/* Loading State */}
        {loading && (
          <section className="loading-section">
            <LoadingSpinner />
          </section>
        )}

        {/* Error State */}
        {error && !loading && (
          <section className="error-section">
            <ErrorMessage message={error} onRetry={handleUpload} />
          </section>
        )}

        {/* Results Section */}
        {results && !loading && !error && (
          <section className="results-section">
            <ResultsDisplay results={results} imageUrl={uploadedImageUrl} />
          </section>
        )}

        {/* Empty State */}
        {!selectedImage && !loading && !error && !results && (
          <section className="empty-state">
            <div className="empty-state-icon">📋</div>
            <h2 className="empty-state-title">Ready to Analyze</h2>
            <p className="empty-state-text">
              Upload a prescription image to detect potential drug interactions
            </p>
            <div className="empty-state-features">
              <div className="feature-item">
                <span className="feature-icon">🔍</span>
                <span>OCR Text Extraction</span>
              </div>
              <div className="feature-item">
                <span className="feature-icon">🧠</span>
                <span>AI-Powered Analysis</span>
              </div>
              <div className="feature-item">
                <span className="feature-icon">⚕️</span>
                <span>FDA-Verified Database</span>
              </div>
              <div className="feature-item">
                <span className="feature-icon">🛡️</span>
                <span>Safety Guardrails</span>
              </div>
            </div>
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p className="footer-text">
          ⚠️ This tool is for informational purposes only. Always consult qualified healthcare professionals before making medication decisions.
        </p>
        <p className="footer-credits">
          Powered by MedGemma | Built with React + Vite
        </p>
      </footer>
    </div>
  );
}

export default App;
