import './ErrorMessage.css';

const ErrorMessage = ({ message, onRetry }) => {
  return (
    <div className="error-container">
      <div className="error-card card">
        <div className="error-icon-wrapper">
          <div className="error-icon">❌</div>
          <div className="error-pulse"></div>
        </div>
        
        <h3 className="error-title">Analysis Failed</h3>
        
        <div className="error-message-box">
          <p className="error-message">{message}</p>
        </div>
        
        <div className="error-actions">
          <button onClick={onRetry} className="btn btn-danger">
            🔄 Try Again
          </button>
        </div>
        
        <div className="error-tips">
          <p className="tips-title">💡 Troubleshooting Tips:</p>
          <ul className="tips-list">
            <li>Ensure backend is running on Kaggle</li>
            <li>Check if ngrok URL is correctly configured</li>
            <li>Verify image file is valid (JPG/PNG, &lt;2MB)</li>
            <li>Check internet connection</li>
            <li>Wait a moment and try again</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ErrorMessage;
