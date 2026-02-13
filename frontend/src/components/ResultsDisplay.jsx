import { useState, useEffect, useRef } from 'react';
import './ResultsDisplay.css';

/*  Typewriter hook: reveals text char-by-char  */
const useTypewriter = (text, speed = 12, startDelay = 0) => {
  const [displayed, setDisplayed] = useState('');
  const [done, setDone] = useState(false);
  useEffect(() => {
    if (!text) { setDisplayed(''); setDone(true); return; }
    setDisplayed(''); setDone(false);
    let i = 0;
    const timeout = setTimeout(() => {
      const iv = setInterval(() => {
        i++;
        setDisplayed(text.slice(0, i));
        if (i >= text.length) { clearInterval(iv); setDone(true); }
      }, speed);
      return () => clearInterval(iv);
    }, startDelay);
    return () => clearTimeout(timeout);
  }, [text, speed, startDelay]);
  return { displayed, done };
};

/*  Single animated point  */
const TypewriterPoint = ({ text, delay, onDone }) => {
  const { displayed, done } = useTypewriter(text, 8, delay);
  useEffect(() => { if (done && onDone) onDone(); }, [done]);
  return (
    <div className="ai-point">
      <span className="point-bullet"></span>
      <span className="point-text">
        {displayed}
        {!done && <span className="cursor">|</span>}
      </span>
    </div>
  );
};

/*  Animated section that reveals points sequentially  */
const AnimatedSection = ({ title, points, startDelay = 0 }) => {
  const [visibleCount, setVisibleCount] = useState(1);
  const [open, setOpen] = useState(true);
  if (!points || points.length === 0) return null;

  const handlePointDone = () => {
    setVisibleCount(prev => Math.min(prev + 1, points.length));
  };

  return (
    <div className="ai-section">
      <button className="ai-section-toggle" onClick={() => setOpen(o => !o)}>
        <span className="toggle-arrow">{open ? '\u25BE' : '\u25B8'}</span>
        <span className="toggle-label">{title}</span>
      </button>
      {open && (
        <div className="ai-section-body">
          {points.slice(0, visibleCount).map((pt, i) => (
            <TypewriterPoint
              key={i}
              text={pt}
              delay={i === 0 ? startDelay : 0}
              onDone={i === visibleCount - 1 ? handlePointDone : undefined}
            />
          ))}
        </div>
      )}
    </div>
  );
};

/*  Clean residual markdown  */
const clean = (t) => {
  if (!t) return '';
  return t.replace(/\*\*(.+?)\*\*/g, '').replace(/\*\*/g, '').replace(/#{1,4}\s*/g, '').replace(/\s{2,}/g, ' ').trim();
};

/*  Main Component  */
const ResultsDisplay = ({ results }) => {
  const riskColor = (level) => {
    const l = level?.toLowerCase();
    if (l === 'high') return 'risk-high';
    if (l === 'moderate') return 'risk-mod';
    return 'risk-low';
  };

  return (
    <div className="results-container">
      {/* Summary bar */}
      <div className="results-summary">
        <div className="summary-stat">
          <span className="stat-val">{results.detected_drugs?.length || 0}</span>
          <span className="stat-lbl">Drugs</span>
        </div>
        <div className="summary-stat">
          <span className="stat-val">{results.interaction_count || 0}</span>
          <span className="stat-lbl">Interactions</span>
        </div>
      </div>

      {/* Detected drugs */}
      {results.detected_drugs?.length > 0 && (
        <div className="drugs-row">
          {results.detected_drugs.map((d, i) => (
            <span key={i} className="drug-chip">{d}</span>
          ))}
        </div>
      )}

      {/* Interactions */}
      {results.interactions?.length > 0 ? (
        results.interactions.map((ix, idx) => (
          <div key={idx} className="interaction-card">
            {/* Header */}
            <div className="ix-header">
              <div className="ix-pair">
                <span className="ix-drug">{ix.drug_pair?.[0]}</span>
                <span className="ix-sep">&times;</span>
                <span className="ix-drug">{ix.drug_pair?.[1]}</span>
              </div>
              <span className={ix-risk }>
                {ix.risk_level?.toUpperCase()} RISK
              </span>
            </div>

            {/* Quick info */}
            {ix.basic_info && (
              <div className="ix-quick">
                <div className="quick-row"><span className="quick-label">Mechanism</span><span className="quick-val">{ix.basic_info.mechanism}</span></div>
                <div className="quick-row"><span className="quick-label">Effect</span><span className="quick-val">{ix.basic_info.clinical_effect}</span></div>
                <div className="quick-row"><span className="quick-label">Action</span><span className="quick-val">{ix.basic_info.recommendation}</span></div>
              </div>
            )}

            {/* AI Analysis with typewriter */}
            {ix.ai_explanation && (
              <div className="ai-analysis">
                <div className="ai-header">AI Analysis</div>
                <AnimatedSection title="Mechanism of Interaction"
                  points={ix.ai_explanation.mechanism_of_interaction?.map(clean)} startDelay={200} />
                <AnimatedSection title="Clinical Manifestations"
                  points={ix.ai_explanation.clinical_manifestations?.map(clean)} startDelay={0} />
                <AnimatedSection title="Risk Factors"
                  points={ix.ai_explanation.risk_factors?.map(clean)} startDelay={0} />
                <AnimatedSection title="Monitoring Recommendations"
                  points={ix.ai_explanation.monitoring_recommendations?.map(clean)} startDelay={0} />
                <AnimatedSection title="Alternative Suggestions"
                  points={ix.ai_explanation.alternative_suggestions?.map(clean)} startDelay={0} />
              </div>
            )}
          </div>
        ))
      ) : (
        <div className="no-ix">No interactions detected.</div>
      )}

      {/* Disclaimer */}
      <div className="disclaimer">
        For informational purposes only. Always consult qualified healthcare professionals before making medication decisions.
      </div>

      {/* Actions */}
      <div className="results-actions">
        <button onClick={() => window.location.reload()} className="btn btn-secondary">New Analysis</button>
      </div>
    </div>
  );
};

export default ResultsDisplay;
