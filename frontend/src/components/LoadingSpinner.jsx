import './LoadingSpinner.css';

const LoadingSpinner = () => {
  return (
    <div className="loading-container">
      <div className="loading-card card">
        <div className="spinner-bar"><div className="spinner-fill"></div></div>
        <p className="loading-title">Analyzing prescription...</p>
        <div className="loading-steps">
          <div className="l-step">Extracting text via OCR</div>
          <div className="l-step">Identifying drug names</div>
          <div className="l-step">Checking interactions</div>
          <div className="l-step">Running AI model</div>
          <div className="l-step">Validating safety</div>
        </div>
        <p className="loading-hint">This may take 15-30 seconds</p>
      </div>
    </div>
  );
};

export default LoadingSpinner;
