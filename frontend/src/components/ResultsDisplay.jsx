import { useState } from 'react';
import './ResultsDisplay.css';

const ResultsDisplay = ({ results, imageUrl }) => {
  const [expandedSections, setExpandedSections] = useState({
    mechanism: true,
    clinical: true,
    risks: true,
    monitoring: true,
    alternatives: true
  });

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const getRiskBadgeClass = (riskLevel) => {
    const level = riskLevel?.toLowerCase();
    if (level === 'high') return 'risk-badge-high';
    if (level === 'moderate') return 'risk-badge-moderate';
    if (level === 'low') return 'risk-badge-low';
    if (level === 'none') return 'risk-badge-none';
    return 'risk-badge-unknown';
  };

  const getRiskIcon = (riskLevel) => {
    const level = riskLevel?.toLowerCase();
    if (level === 'high') return '🔴';
    if (level === 'moderate') return '🟡';
    if (level === 'low') return '🟢';
    if (level === 'none') return '⚪';
    return '⚫';
  };

  return (
    <div className="results-container">
      {/* Summary Card */}
      <div className="results-summary card">
        <h2 className="results-title">📊 Analysis Complete</h2>
        <div className="summary-grid">
          <div className="summary-item">
            <div className="summary-icon">💊</div>
            <div className="summary-content">
              <div className="summary-label">Drugs Detected</div>
              <div className="summary-value">{results.detected_drugs?.length || 0}</div>
            </div>
          </div>
          <div className="summary-item">
            <div className="summary-icon">🔗</div>
            <div className="summary-content">
              <div className="summary-label">Interactions Found</div>
              <div className="summary-value">{results.interaction_count || 0}</div>
            </div>
          </div>
          <div className="summary-item">
            <div className="summary-icon">⏱️</div>
            <div className="summary-content">
              <div className="summary-label">Analysis Time</div>
              <div className="summary-value">
                {results.analysis_time ? `${results.analysis_time.toFixed(1)}s` : 'N/A'}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Detected Drugs */}
      {results.detected_drugs && results.detected_drugs.length > 0 && (
        <div className="detected-drugs-section card">
          <h3 className="section-title">💊 Detected Drugs</h3>
          <div className="drugs-grid">
            {results.detected_drugs.map((drug, index) => (
              <div key={index} className="drug-card">
                <div className="drug-icon">💊</div>
                <div className="drug-name">{drug}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Interactions Section */}
      {results.interactions && results.interactions.length > 0 ? (
        results.interactions.map((interaction, index) => (
          <div key={index} className="interaction-section card">
            {/* Interaction Header */}
            <div className="interaction-header">
              <div className="interaction-title-row">
                <h3 className="interaction-title">
                  ⚠️ Drug Interaction Detected
                </h3>
                <div className={`risk-badge ${getRiskBadgeClass(interaction.risk_level)}`}>
                  <span className="risk-icon">{getRiskIcon(interaction.risk_level)}</span>
                  <span className="risk-text">{interaction.risk_level?.toUpperCase() || 'UNKNOWN'} RISK</span>
                </div>
              </div>
              <div className="drug-pair">
                <span className="drug-pair-item">{interaction.drug_pair?.[0]}</span>
                <span className="drug-pair-separator">+</span>
                <span className="drug-pair-item">{interaction.drug_pair?.[1]}</span>
              </div>
            </div>

            {/* Quick Summary */}
            {interaction.basic_info && (
              <div className="quick-summary">
                <div className="summary-row">
                  <strong>Mechanism:</strong> {interaction.basic_info.mechanism}
                </div>
                <div className="summary-row">
                  <strong>Clinical Effect:</strong> {interaction.basic_info.clinical_effect}
                </div>
                <div className="summary-row">
                  <strong>Recommendation:</strong> {interaction.basic_info.recommendation}
                </div>
              </div>
            )}

            {/* Detailed Explanation */}
            {interaction.ai_explanation && (
              <div className="ai-explanation">
                <h4 className="explanation-header">🧠 Detailed AI Analysis</h4>
                
                {/* Mechanism of Interaction */}
                {interaction.ai_explanation.mechanism_of_interaction && (
                  <div className="explanation-section">
                    <button
                      className="section-toggle"
                      onClick={() => toggleSection('mechanism')}
                    >
                      <span className="toggle-icon">
                        {expandedSections.mechanism ? '▼' : '▶'}
                      </span>
                      <span className="toggle-text">
                        🔬 Mechanism of Interaction
                      </span>
                    </button>
                    {expandedSections.mechanism && (
                      <ul className="explanation-list">
                        {interaction.ai_explanation.mechanism_of_interaction.map((point, i) => (
                          <li key={i}>{point}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}

                {/* Clinical Manifestations */}
                {interaction.ai_explanation.clinical_manifestations && (
                  <div className="explanation-section">
                    <button
                      className="section-toggle"
                      onClick={() => toggleSection('clinical')}
                    >
                      <span className="toggle-icon">
                        {expandedSections.clinical ? '▼' : '▶'}
                      </span>
                      <span className="toggle-text">
                        🏥 Clinical Manifestations
                      </span>
                    </button>
                    {expandedSections.clinical && (
                      <ul className="explanation-list">
                        {interaction.ai_explanation.clinical_manifestations.map((point, i) => (
                          <li key={i}>{point}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}

                {/* Risk Factors */}
                {interaction.ai_explanation.risk_factors && (
                  <div className="explanation-section">
                    <button
                      className="section-toggle"
                      onClick={() => toggleSection('risks')}
                    >
                      <span className="toggle-icon">
                        {expandedSections.risks ? '▼' : '▶'}
                      </span>
                      <span className="toggle-text">
                        ⚠️ Risk Factors
                      </span>
                    </button>
                    {expandedSections.risks && (
                      <ul className="explanation-list">
                        {interaction.ai_explanation.risk_factors.map((point, i) => (
                          <li key={i}>{point}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}

                {/* Monitoring Recommendations */}
                {interaction.ai_explanation.monitoring_recommendations && (
                  <div className="explanation-section">
                    <button
                      className="section-toggle"
                      onClick={() => toggleSection('monitoring')}
                    >
                      <span className="toggle-icon">
                        {expandedSections.monitoring ? '▼' : '▶'}
                      </span>
                      <span className="toggle-text">
                        📋 Monitoring Recommendations
                      </span>
                    </button>
                    {expandedSections.monitoring && (
                      <ul className="explanation-list">
                        {interaction.ai_explanation.monitoring_recommendations.map((point, i) => (
                          <li key={i}>{point}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}

                {/* Alternative Suggestions */}
                {interaction.ai_explanation.alternative_suggestions && (
                  <div className="explanation-section">
                    <button
                      className="section-toggle"
                      onClick={() => toggleSection('alternatives')}
                    >
                      <span className="toggle-icon">
                        {expandedSections.alternatives ? '▼' : '▶'}
                      </span>
                      <span className="toggle-text">
                        💡 Alternative Suggestions
                      </span>
                    </button>
                    {expandedSections.alternatives && (
                      <ul className="explanation-list">
                        {interaction.ai_explanation.alternative_suggestions.map((point, i) => (
                          <li key={i}>{point}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        ))
      ) : (
        <div className="no-interactions card">
          <div className="no-interactions-icon">✅</div>
          <h3 className="no-interactions-title">No Interactions Detected</h3>
          <p className="no-interactions-text">
            The detected drugs do not have known interactions in our database.
            However, always consult with a healthcare professional.
          </p>
        </div>
      )}

      {/* Disclaimer */}
      <div className="disclaimer-section card">
        <div className="disclaimer-icon">ℹ️</div>
        <div className="disclaimer-content">
          <h4 className="disclaimer-title">Important Disclaimer</h4>
          <p className="disclaimer-text">
            This analysis is for <strong>informational purposes only</strong> and should not replace professional medical advice.
            Drug interactions can vary based on individual health conditions, dosages, and other factors.
            <strong> Always consult qualified healthcare professionals</strong> before making any medication decisions.
          </p>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="results-actions">
        <button
          onClick={() => window.print()}
          className="btn btn-secondary"
        >
          🖨️ Print Report
        </button>
        <button
          onClick={() => window.location.reload()}
          className="btn btn-primary"
        >
          🔄 Analyze Another Prescription
        </button>
      </div>
    </div>
  );
};

export default ResultsDisplay;
