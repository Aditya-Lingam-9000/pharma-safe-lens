import { useState } from 'react';
import ImageUpload from './components/ImageUpload';
import ResultsDisplay from './components/ResultsDisplay';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import { uploadImageStream, getApiUrl } from './services/api';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [uploadedImageUrl, setUploadedImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Progressive results state
  const [results, setResults] = useState(null);
  // Track which phase we're in: null | 'ocr' | 'generating' | 'done'
  const [streamPhase, setStreamPhase] = useState(null);
  // How many interactions have been fully analyzed
  const [completedCount, setCompletedCount] = useState(0);

  const handleImageSelect = (file) => {
    setSelectedImage(file);
    setUploadedImageUrl(URL.createObjectURL(file));
    setError(null);
    setResults(null);
    setStreamPhase(null);
    setCompletedCount(0);
  };

  const handleUpload = async () => {
    if (!selectedImage) { setError('Please select an image first'); return; }
    setLoading(true); setError(null); setResults(null);
    setStreamPhase('ocr'); setCompletedCount(0);

    try {
      console.log('Streaming upload to:', getApiUrl());

      await uploadImageStream(selectedImage, {
        // Called once: drugs detected, interaction count known
        onInit: (data) => {
          console.log('SSE init:', data);
          setStreamPhase('generating');
          setResults({
            status: 'success',
            detected_drugs: data.detected_drugs,
            interaction_count: data.interaction_count,
            interactions: data.interactions_basic || []
          });
        },

        // Called per interaction as AI finishes each one
        onInteraction: (data) => {
          console.log('SSE interaction:', data.index);
          setResults(prev => {
            if (!prev) return prev;
            const updated = [...prev.interactions];
            updated[data.index] = data.interaction;
            return { ...prev, interactions: updated };
          });
          setCompletedCount(c => c + 1);
        },

        // All interactions done
        onDone: () => {
          console.log('SSE done');
          setStreamPhase('done');
          setLoading(false);
        },

        // Server error mid-stream
        onError: (detail) => {
          console.error('SSE error:', detail);
          setError(detail);
          setLoading(false);
          setStreamPhase(null);
        }
      });

      // If stream ends without explicit done event
      setLoading(false);
      if (streamPhase !== 'done') setStreamPhase('done');

    } catch (err) {
      console.error('Upload failed:', err);
      setError(err.message || 'Failed to analyze image.');
      setLoading(false);
      setStreamPhase(null);
    }
  };

  const handleReset = () => {
    setSelectedImage(null); setUploadedImageUrl(null);
    setLoading(false); setError(null); setResults(null);
    setStreamPhase(null); setCompletedCount(0);
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

        {/* Show spinner only during OCR phase (before any results arrive) */}
        {loading && !results && <section className="loading-section"><LoadingSpinner /></section>}

        {error && !loading && <section className="error-section"><ErrorMessage message={error} onRetry={handleUpload} /></section>}

        {/* Show results as soon as init event arrives, even while still streaming */}
        {results && (
          <section className="results-section">
            <ResultsDisplay
              results={results}
              streaming={loading && streamPhase === 'generating'}
              completedCount={completedCount}
              totalCount={results.interaction_count || 0}
            />
          </section>
        )}

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
