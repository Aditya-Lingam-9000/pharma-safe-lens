import './LoadingSpinner.css';

const LoadingSpinner = () => {
  return (
    <div className="loading-container">
      <div className="loading-card card">
        <div className="spinner-wrapper">
          <div className="spinner-outer">
            <div className="spinner-inner"></div>
          </div>
          <div className="spinner-pulse"></div>
        </div>
        
        <h3 className="loading-title">Analyzing Prescription...</h3>
        
        <div className="loading-steps">
          <div className="loading-step active">
            <div className="step-icon">🔍</div>
            <div className="step-text">Extracting text from image</div>
          </div>
          <div className="loading-step active">
            <div className="step-icon">💊</div>
            <div className="step-text">Identifying drug names</div>
          </div>
          <div className="loading-step active">
            <div className="step-icon">🔗</div>
            <div className="step-text">Checking interactions</div>
          </div>
          <div className="loading-step active">
            <div className="step-icon">🧠</div>
            <div className="step-text">Generating AI analysis</div>
          </div>
          <div className="loading-step active">
            <div className="step-icon">🛡️</div>
            <div className="step-text">Validating safety</div>
          </div>
        </div>
        
        <p className="loading-hint">
          This may take 15-30 seconds...
        </p>
      </div>
    </div>
  );
};

export default LoadingSpinner;
