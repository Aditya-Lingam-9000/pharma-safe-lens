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
  return t.replace(/\*\*(.+?)\*\*/g, '$1').replace(/\*\*/g, '').replace(/#{1,4}\s*/g, '').replace(/\s{2,}/g, ' ').trim();
};

/*  Mini loading bar for a pending interaction  */
const InteractionPending = ({ index, total, drugPair }) => (
  <div className="interaction-card interaction-pending">
    <div className="ix-header">
      <div className="ix-pair">
        <span className="ix-drug">{drugPair?.[0]}</span>
        <span className="ix-sep">&times;</span>
        <span className="ix-drug">{drugPair?.[1]}</span>
      </div>
      <span className="ix-pending-badge">Waiting...</span>
    </div>
    <div className="ix-pending-body">
      <div className="pending-bar"><div className="pending-fill"></div></div>
      <p className="pending-text">AI analysis queued ({index + 1} of {total})</p>
    </div>
  </div>
);

/*  Loading bar for the interaction currently being generated  */
const InteractionLoading = ({ index, total, drugPair, basicInfo }) => (
  <div className="interaction-card interaction-loading">
    <div className="ix-header">
      <div className="ix-pair">
        <span className="ix-drug">{drugPair?.[0]}</span>
        <span className="ix-sep">&times;</span>
        <span className="ix-drug">{drugPair?.[1]}</span>
      </div>
      <span className="ix-loading-badge">Generating...</span>
    </div>
    {basicInfo && (
      <div className="ix-quick">
        <div className="quick-row"><span className="quick-label">Mechanism</span><span className="quick-val">{basicInfo.mechanism}</span></div>
        <div className="quick-row"><span className="quick-label">Effect</span><span className="quick-val">{basicInfo.clinical_effect}</span></div>
      </div>
    )}
    <div className="ix-generating">
      <div className="generating-bar"><div className="generating-fill"></div></div>
      <p className="generating-text">Generating AI explanation... ({index + 1} of {total})</p>
    </div>
  </div>
);


/*  ============  Main Component  ============  */
const ResultsDisplay = ({ results, streaming = false, completedCount = 0, totalCount = 0 }) => {
  const riskColor = (level) => {
    const l = level?.toLowerCase();
    if (l === 'high') return 'risk-high';
    if (l === 'moderate') return 'risk-mod';
    return 'risk-low';
  };

  const remaining = totalCount - completedCount;

  return (
    <div className="results-container">
      {/* Summary bar */}
      <div className="results-summary">
        <div className="summary-stat">
          <span className="stat-val">{results.detected_drugs?.length || 0}</span>
          <span className="stat-lbl">Drugs</span>
        </div>
        <div className="summary-stat">
          <span className="stat-val">{totalCount || results.interaction_count || 0}</span>
          <span className="stat-lbl">Interactions</span>
        </div>
        {streaming && (
          <div className="summary-stat summary-progress">
            <span className="stat-val progress-val">{completedCount}/{totalCount}</span>
            <span className="stat-lbl">Analyzed</span>
          </div>
        )}
      </div>

      {/* Streaming progress bar */}
      {streaming && totalCount > 0 && (
        <div className="stream-progress">
          <div className="stream-progress-bar">
            <div
              className="stream-progress-fill"
              style={{ width: `${(completedCount / totalCount) * 100}%` }}
            ></div>
          </div>
          <p className="stream-progress-text">
            {remaining > 0
              ? `Generating AI analysis... ${remaining} interaction${remaining > 1 ? 's' : ''} remaining`
              : 'Finishing up...'
            }
          </p>
        </div>
      )}

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
        results.interactions.map((ix, idx) => {
          const hasAI = ix.ai_explanation !== null && ix.ai_explanation !== undefined;
          const isNextToGenerate = streaming && !hasAI && idx === completedCount;
          const isPending = streaming && !hasAI && idx > completedCount;

          // Case 1: AI is fully loaded — show complete card
          if (hasAI) {
            return (
              <div key={idx} className="interaction-card interaction-ready">
                <div className="ix-header">
                  <div className="ix-pair">
                    <span className="ix-drug">{ix.drug_pair?.[0]}</span>
                    <span className="ix-sep">&times;</span>
                    <span className="ix-drug">{ix.drug_pair?.[1]}</span>
                  </div>
                  <span className={`ix-risk ${riskColor(ix.risk_level)}`}>
                    {ix.risk_level?.toUpperCase()} RISK
                  </span>
                </div>
                {ix.basic_info && (
                  <div className="ix-quick">
                    <div className="quick-row"><span className="quick-label">Mechanism</span><span className="quick-val">{ix.basic_info.mechanism}</span></div>
                    <div className="quick-row"><span className="quick-label">Effect</span><span className="quick-val">{ix.basic_info.clinical_effect}</span></div>
                    <div className="quick-row"><span className="quick-label">Action</span><span className="quick-val">{ix.basic_info.recommendation}</span></div>
                  </div>
                )}
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
              </div>
            );
          }

          // Case 2: Currently being generated by AI
          if (isNextToGenerate) {
            return (
              <InteractionLoading
                key={idx}
                index={idx}
                total={totalCount}
                drugPair={ix.drug_pair}
                basicInfo={ix.basic_info}
              />
            );
          }

          // Case 3: Still waiting in queue
          if (isPending) {
            return (
              <InteractionPending
                key={idx}
                index={idx}
                total={totalCount}
                drugPair={ix.drug_pair}
              />
            );
          }

          // Case 4: Not streaming, no AI (fallback) — show basic info only
          return (
            <div key={idx} className="interaction-card">
              <div className="ix-header">
                <div className="ix-pair">
                  <span className="ix-drug">{ix.drug_pair?.[0]}</span>
                  <span className="ix-sep">&times;</span>
                  <span className="ix-drug">{ix.drug_pair?.[1]}</span>
                </div>
                <span className={`ix-risk ${riskColor(ix.risk_level)}`}>
                  {ix.risk_level?.toUpperCase()} RISK
                </span>
              </div>
              {ix.basic_info && (
                <div className="ix-quick">
                  <div className="quick-row"><span className="quick-label">Mechanism</span><span className="quick-val">{ix.basic_info.mechanism}</span></div>
                  <div className="quick-row"><span className="quick-label">Effect</span><span className="quick-val">{ix.basic_info.clinical_effect}</span></div>
                  <div className="quick-row"><span className="quick-label">Action</span><span className="quick-val">{ix.basic_info.recommendation}</span></div>
                </div>
              )}
            </div>
          );
        })
      ) : (
        !streaming && <div className="no-ix">No interactions detected.</div>
      )}

      {/* Disclaimer */}
      {!streaming && (
        <div className="disclaimer">
          For informational purposes only. Always consult qualified healthcare professionals before making medication decisions.
        </div>
      )}

      {/* Actions */}
      {!streaming && (
        <div className="results-actions">
          <button onClick={() => window.location.reload()} className="btn btn-secondary">New Analysis</button>
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay;
