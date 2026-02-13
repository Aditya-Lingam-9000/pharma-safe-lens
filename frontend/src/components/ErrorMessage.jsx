import './ErrorMessage.css';

const ErrorMessage = ({ message, onRetry }) => (
  <div className="error-container">
    <div className="error-card card">
      <p className="error-title">Analysis Failed</p>
      <div className="error-msg-box"><p className="error-msg">{message}</p></div>
      <button onClick={onRetry} className="btn btn-danger">Try Again</button>
      <div className="error-tips">
        <p className="tips-title">Troubleshooting</p>
        <ul className="tips-list">
          <li>Ensure backend is running on Kaggle</li>
          <li>Verify ngrok URL in api.js</li>
          <li>Check image format (JPG/PNG, under 2 MB)</li>
        </ul>
      </div>
    </div>
  </div>
);

export default ErrorMessage;
