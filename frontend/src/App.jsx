import { useState } from 'react'
import './App.css'

const findings = [
  {
    control_id: 'NET-SSH-001',
    framework: 'CIS',
    title: 'SSH Version',
    status: 'PASS',
    severity: 'Low',
    expected: 'SSH version 2',
    observed: 'SSH version 2',
    evidence: 'ip ssh version 2',
    remediation: 'No action required'
  },
  {
    control_id: 'NET-REMOTE-002',
    framework: 'CIS',
    title: 'Telnet Access',
    status: 'FAIL',
    severity: 'High',
    expected: 'Telnet must be disabled',
    observed: 'Telnet service enabled',
    evidence: 'line vty 0 4 → transport input telnet',
    remediation: 'Disable Telnet and allow SSH only'
  },
  {
    control_id: 'NET-LOG-003',
    framework: 'NIST',
    title: 'System Logging',
    status: 'FAIL',
    severity: 'Medium',
    expected: 'Centralized logging enabled',
    observed: 'No logging server configured',
    evidence: 'No logging host configuration found',
    remediation: 'Configure the approved centralized logging server'
  }
]

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisComplete, setAnalysisComplete] = useState(false)
  const [activePage, setActivePage] = useState('dashboard')
  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">S</div>

          <div>
            <h1>SIH Compliance Auditor</h1>
            <p>Multi-Vendor Network Security</p>
          </div>
        </div>

        <div className="topbar-status">
          <span className="status-dot"></span>
          System Ready
        </div>
      </header>

      <div className="layout">
        <aside className="sidebar">
          <nav>
            <button
  className={`nav-item ${activePage === 'dashboard' ? 'active' : ''}`}
  onClick={() => setActivePage('dashboard')}
>
  <span>▦</span>
  Dashboard
</button>

            <button
  className={`nav-item ${activePage === 'analyze' ? 'active' : ''}`}
  onClick={() => setActivePage('analyze')}
>
  <span>↑</span>
  Analyze Config
</button>

            <button
  className={`nav-item ${activePage === 'findings' ? 'active' : ''}`}
  onClick={() => setActivePage('findings')}
>
  <span>✓</span>
  Findings
</button>

            <button
  className={`nav-item ${activePage === 'remediation' ? 'active' : ''}`}
  onClick={() => setActivePage('remediation')}
>
  <span>↻</span>
  Remediation
</button>

            <button
  className={`nav-item ${activePage === 'ai' ? 'active' : ''}`}
  onClick={() => setActivePage('ai')}
>
  <span>✦</span>
  AI Training
</button>

            <button
  className={`nav-item ${activePage === 'reports' ? 'active' : ''}`}
  onClick={() => setActivePage('reports')}
>
  <span>▤</span>
  Reports
</button>
          </nav>

          <div className="sidebar-bottom">
            <p>SIH 2026</p>
            <span>Security Compliance Platform</span>
          </div>
        </aside>

        <main className="main-content">

          {activePage === 'dashboard' && (
            <>
              <section className="welcome">
            <div>
              <p className="eyebrow">NETWORK SECURITY</p>

              <h2>
                Security Compliance
                <br />
                <span>Auditor</span>
              </h2>

              <p className="description">
                Analyze configurations across multiple network vendors,
                detect compliance issues, preserve evidence, and generate
                validated remediation.
              </p>
            </div>

            <div className="hero-badge">
              <div className="shield">◆</div>
              <p>AI-Assisted</p>
              <span>Policy-Driven Analysis</span>
            </div>
          </section>

          <section className="stats">
            <div className="stat-card">
              <span className="stat-label">Configurations</span>
              <strong>0</strong>
              <small>Analyzed</small>
            </div>

            <div className="stat-card">
              <span className="stat-label">Compliance</span>
              <strong>—</strong>
              <small>Overall score</small>
            </div>

            <div className="stat-card">
              <span className="stat-label">Findings</span>
              <strong>0</strong>
              <small>Issues detected</small>
            </div>

            <div className="stat-card">
              <span className="stat-label">Vendors</span>
              <strong>3</strong>
              <small>Cisco · Juniper · Palo Alto</small>
            </div>
          </section>

          <section className="upload-card">
            <div className="upload-icon">↑</div>

            <h3>Analyze a Network Configuration</h3>

            <p>
              Upload a configuration file to detect the vendor, normalize
              the configuration, and evaluate security compliance.
            </p>

            <label className="primary-button">
              Upload Configuration

              <input
                type="file"
                accept=".txt,.cfg,.conf"
                hidden
                onChange={(event) => setSelectedFile(event.target.files[0])}
              />
            </label>

            <span className="upload-note">
              Supported vendors: Cisco · Juniper · Palo Alto
            </span>

            {selectedFile && (
              <p className="selected-file">
                Selected: {selectedFile.name}
              </p>
            )}
            {selectedFile && !analysisComplete && (
  <button
    className="analyze-button"
    onClick={() => {
      setIsAnalyzing(true)

      setTimeout(() => {
        setIsAnalyzing(false)
        setAnalysisComplete(true)
      }, 1500)
    }}
    disabled={isAnalyzing}
  >
    {isAnalyzing ? 'Analyzing...' : 'Analyze Configuration'}
  </button>
)}
          </section>

          {analysisComplete && (
  <section className="results-preview">
    <div className="results-header">
      <div>
        <p className="eyebrow">ANALYSIS COMPLETE</p>
        <h3>Configuration Results</h3>
      </div>

      <span className="passed-badge">Analysis Successful</span>
    </div>

    <div className="result-info">
      <div>
        <span>Configuration</span>
        <strong>{selectedFile.name}</strong>
      </div>

      <div>
        <span>Vendor</span>
        <strong>Cisco</strong>
      </div>

      <div>
        <span>Status</span>
        <strong className="pass-text">Analyzed</strong>
      </div>
    </div>

    <div className="result-message">
      <strong>Next step</strong>
      <p>
        The configuration has been processed and is ready for
        compliance evaluation.
      </p>
    </div>
  </section>
)}
{analysisComplete && (
  <section className="findings-section">
    <div className="section-heading">
      <div>
        <p className="eyebrow">COMPLIANCE EVALUATION</p>
        <h3>Security Findings</h3>
      </div>

      <div className="finding-summary">
        <span className="summary-pass">1 Passed</span>
        <span className="summary-fail">2 Failed</span>
      </div>
    </div>

    <div className="findings-list">
      {findings.map((finding) => (
        <div className="finding-card" key={finding.control_id}>

          <div className="finding-top">
            <div>
              <span className="control-id">
                {finding.control_id}
              </span>

              <h4>{finding.title}</h4>
            </div>

            <div className="finding-badges">
              <span className={`severity ${finding.severity.toLowerCase()}`}>
                {finding.severity}
              </span>

              <span className={`status ${finding.status.toLowerCase()}`}>
                {finding.status}
              </span>
            </div>
          </div>

          <div className="finding-details">

            <div>
              <span>Framework</span>
              <strong>{finding.framework}</strong>
            </div>

            <div>
              <span>Expected</span>
              <strong>{finding.expected}</strong>
            </div>

            <div>
              <span>Observed</span>
              <strong>{finding.observed}</strong>
            </div>

          </div>

          <div className="evidence">
            <span>Evidence</span>
            <code>{finding.evidence}</code>
          </div>

          <div className="remediation">
            <span>Remediation</span>
            <p>{finding.remediation}</p>
          </div>

        </div>
      ))}
    </div>
  </section>
)}

          <section className="principles">
            <div>
              <strong>AI understands.</strong>
              <span>Unknown syntax is interpreted with confidence.</span>
            </div>

            <div>
              <strong>Policy decides.</strong>
              <span>Deterministic compliance rules evaluate controls.</span>
            </div>

            <div>
              <strong>Evidence proves.</strong>
              <span>Every finding retains configuration evidence.</span>
            </div>
          </section>
              </>
  )}
  {activePage === 'analyze' && (
  <section className="analyze-page">

    <div className="page-title">
      <p className="eyebrow">CONFIGURATION ANALYSIS</p>

      <h2>Analyze Network Configuration</h2>

      <p>
        Upload a network device configuration to detect the vendor,
        normalize its syntax, and evaluate security compliance.
      </p>
    </div>

    <div className="config-upload-area">

      <div className="large-upload-icon">
        ↑
      </div>

      <h3>Upload Configuration</h3>

      <p>
        Drag and drop your configuration file here,
        or select a file from your computer.
      </p>

      <label className="primary-button upload-label">
        Choose Configuration

        <input
          type="file"
          accept=".txt,.cfg,.conf"
          hidden
          onChange={(event) => {
            const file = event.target.files[0]

            if (file) {
              setSelectedFile(file)
              setAnalysisComplete(false)
            }
          }}
        />
      </label>

      <span className="upload-note">
        Supported: Cisco · Juniper · Palo Alto
      </span>

      {selectedFile && (
        <div className="selected-config">
          <div>
            <span className="file-label">SELECTED FILE</span>
            <strong>{selectedFile.name}</strong>
          </div>

          <span className="file-ready">
            Ready
          </span>
        </div>
      )}

      {selectedFile && (
        <button
          className="analyze-main-button"
          onClick={() => {
            setIsAnalyzing(true)

            setTimeout(() => {
              setIsAnalyzing(false)
              setAnalysisComplete(true)
              setActivePage('findings')
            }, 1500)
          }}
          disabled={isAnalyzing}
        >
          {isAnalyzing
            ? 'Analyzing Configuration...'
            : 'Analyze Configuration'}
        </button>
      )}

    </div>

    <div className="pipeline">

      <div className="pipeline-step">
        <span>01</span>
        <strong>Upload</strong>
        <small>Configuration</small>
      </div>

      <div className="pipeline-line"></div>

      <div className="pipeline-step">
        <span>02</span>
        <strong>Detect</strong>
        <small>Vendor</small>
      </div>

      <div className="pipeline-line"></div>

      <div className="pipeline-step">
        <span>03</span>
        <strong>Normalize</strong>
        <small>SBM Model</small>
      </div>

      <div className="pipeline-line"></div>

      <div className="pipeline-step">
        <span>04</span>
        <strong>Evaluate</strong>
        <small>Policies</small>
      </div>

    </div>

    <div className="analysis-note">
      <strong>How it works</strong>

      <p>
        The system first identifies the configuration vendor,
        converts vendor-specific syntax into the Security Baseline
        Model, and then evaluates deterministic compliance policies.
      </p>
    </div>

  </section>
)}

{activePage === 'findings' && (
  <section className="findings-page">

    <div className="page-title">
      <p className="eyebrow">COMPLIANCE FINDINGS</p>

      <h2>Security Findings</h2>

      <p>
        Review detected compliance issues, supporting evidence,
        severity, and recommended remediation.
      </p>
    </div>

    <div className="finding-summary">

      <div className="finding-stat">
        <span>Total Findings</span>
        <strong>{findings.length}</strong>
      </div>

      <div className="finding-stat">
        <span>Passed</span>
        <strong>
          {findings.filter((finding) => finding.status === 'PASS').length}
        </strong>
      </div>

      <div className="finding-stat">
        <span>Failed</span>
        <strong>
          {findings.filter((finding) => finding.status === 'FAIL').length}
        </strong>
      </div>

      <div className="finding-stat">
        <span>High Severity</span>
        <strong>
          {
            findings.filter(
              (finding) => finding.severity === 'High'
            ).length
          }
        </strong>
      </div>

    </div>

    <div className="findings-list">

      {findings.map((finding) => (

        <article
          className={`finding-card ${finding.status.toLowerCase()}`}
          key={finding.control_id}
        >

          <div className="finding-header">

            <div>
              <span className="control-id">
                {finding.control_id}
              </span>

              <h3>{finding.title}</h3>
            </div>

            <span
              className={`status-badge ${finding.status.toLowerCase()}`}
            >
              {finding.status}
            </span>

          </div>

          <div className="finding-meta">
            <span>Framework: {finding.framework}</span>
            <span>Severity: {finding.severity}</span>
          </div>

          <div className="finding-details">

            <div>
              <span>EXPECTED</span>
              <p>{finding.expected}</p>
            </div>

            <div>
              <span>OBSERVED</span>
              <p>{finding.observed}</p>
            </div>

          </div>

          <div className="evidence-box">

            <span>EVIDENCE</span>

            <code>
              {finding.evidence}
            </code>

          </div>

          <div className="remediation-box">

            <span>RECOMMENDED REMEDIATION</span>

            <p>
              {finding.remediation}
            </p>

          </div>

        </article>

      ))}

    </div>

  </section>
)}

{activePage === 'remediation' && (
  <section className="remediation-page">

    <div className="page-title">
      <p className="eyebrow">CONTROLLED REMEDIATION</p>

      <h2>Remediation Center</h2>

      <p>
        Review recommended fixes for failed compliance controls
        before applying any configuration changes.
      </p>
    </div>

    <div className="remediation-warning">
      <span>⚠</span>

      <div>
        <strong>Human approval required</strong>
        <p>
          Remediation suggestions are generated from the detected
          finding and matched to the target vendor and platform.
          Changes are never applied automatically.
        </p>
      </div>
    </div>

    <div className="remediation-list">

      {findings
        .filter((finding) => finding.status === 'FAIL')
        .map((finding) => (

          <article
            className="remediation-card"
            key={finding.control_id}
          >

            <div className="remediation-header">

              <div>
                <span className="control-id">
                  {finding.control_id}
                </span>

                <h3>{finding.title}</h3>
              </div>

              <span className="severity-badge">
                {finding.severity}
              </span>

            </div>

            <div className="remediation-info">

              <div>
                <span>DETECTED ISSUE</span>
                <p>{finding.observed}</p>
              </div>

              <div>
                <span>RECOMMENDED ACTION</span>
                <p>{finding.remediation}</p>
              </div>

            </div>

            <div className="remediation-command">

              <span>PROPOSED CONFIGURATION CHANGE</span>

              <code>
                {finding.control_id === 'NET-REMOTE-002'
                  ? 'line vty 0 4 → transport input ssh'
                  : 'logging host &lt;approved-log-server&gt;'}
              </code>

            </div>

            <div className="remediation-actions">

              <button className="review-button">
                Review Change
              </button>

              <button className="approve-button">
                Approve Remediation
              </button>

            </div>

          </article>

        ))}

    </div>

  </section>
)}

{activePage === 'ai' && (
  <section className="ai-page">

    <div className="page-title">
      <p className="eyebrow">ADAPTIVE SYNTAX INTELLIGENCE</p>

      <h2>AI Training Center</h2>

      <p>
        Review unknown configuration syntax, validate AI-generated
        interpretations, and create reusable vendor mappings.
      </p>
    </div>

    <div className="ai-flow">

      <div className="ai-flow-step">
        <span>01</span>
        <strong>Unknown Syntax</strong>
        <small>Detected by parser</small>
      </div>

      <div className="ai-flow-arrow">→</div>

      <div className="ai-flow-step">
        <span>02</span>
        <strong>AI Interpretation</strong>
        <small>Candidate meaning</small>
      </div>

      <div className="ai-flow-arrow">→</div>

      <div className="ai-flow-step">
        <span>03</span>
        <strong>Human Approval</strong>
        <small>Review & validate</small>
      </div>

      <div className="ai-flow-arrow">→</div>

      <div className="ai-flow-step">
        <span>04</span>
        <strong>Learned Mapping</strong>
        <small>Reusable knowledge</small>
      </div>

    </div>

    <div className="unknown-syntax-card">

      <div className="ai-card-header">

        <div>
          <span className="control-id">
            UNKNOWN SYNTAX DETECTED
          </span>

          <h3>Unrecognized Configuration Command</h3>
        </div>

        <span className="unknown-badge">
          NEEDS REVIEW
        </span>

      </div>

      <div className="syntax-block">

        <span>RAW CONFIGURATION</span>

        <code>
          set security unknown-feature enable
        </code>

      </div>

      <div className="ai-suggestion">

        <div className="suggestion-header">
          <span>AI CANDIDATE INTERPRETATION</span>

          <strong>87% confidence</strong>
        </div>

        <p>
          Possible interpretation: this command enables a
          security-related device feature.
        </p>

      </div>

      <div className="mapping-preview">

        <div>
          <span>NORMALIZED FIELD</span>
          <strong>security.feature.enabled</strong>
        </div>

        <div>
          <span>VENDOR</span>
          <strong>Unknown Vendor</strong>
        </div>

        <div>
          <span>STATUS</span>
          <strong>Pending Approval</strong>
        </div>

      </div>

      <div className="ai-actions">

        <button className="reject-button">
          Reject
        </button>

        <button className="edit-button">
          Edit Interpretation
        </button>

        <button className="approve-button">
          Approve & Learn
        </button>

      </div>

    </div>

    <div className="ai-principle">

      <div className="ai-principle-icon">
        AI
      </div>

      <div>
        <strong>AI assists — it does not decide compliance.</strong>

        <p>
          The AI proposes an interpretation for unknown syntax.
          A human validates the mapping, after which the deterministic
          policy engine can use the approved normalized value.
        </p>
      </div>

    </div>

  </section>
)}

{activePage === 'reports' && (
  <section className="reports-page">

    <div className="page-title">
      <p className="eyebrow">AUDIT REPORTING</p>

      <h2>Compliance Reports</h2>

      <p>
        Generate and review security compliance reports with
        findings, evidence, severity, and remediation details.
      </p>
    </div>

    <div className="report-overview">

      <div className="report-score">
        <span>COMPLIANCE SCORE</span>

        <strong>33%</strong>

        <small>
          1 of 3 controls passed
        </small>
      </div>

      <div className="report-stat">
        <span>CONTROLS CHECKED</span>
        <strong>{findings.length}</strong>
      </div>

      <div className="report-stat">
        <span>FAILED</span>
        <strong>
          {findings.filter(
            (finding) => finding.status === 'FAIL'
          ).length}
        </strong>
      </div>

      <div className="report-stat">
        <span>HIGH SEVERITY</span>
        <strong>
          {
            findings.filter(
              (finding) => finding.severity === 'High'
            ).length
          }
        </strong>
      </div>

    </div>

    <div className="report-card">

      <div className="report-card-header">

        <div>
          <span className="control-id">
            AUDIT SUMMARY
          </span>

          <h3>Network Security Compliance Audit</h3>
        </div>

        <span className="report-status">
          COMPLETED
        </span>

      </div>

      <div className="report-details">

        <div>
          <span>VENDOR</span>
          <strong>Cisco</strong>
        </div>

        <div>
          <span>FRAMEWORK</span>
          <strong>CIS</strong>
        </div>

        <div>
          <span>CONFIGURATION</span>
          <strong>
            {selectedFile
              ? selectedFile.name
              : 'No configuration selected'}
          </strong>
        </div>

        <div>
          <span>STATUS</span>
          <strong>Audit Completed</strong>
        </div>

      </div>

    </div>

    <div className="report-findings">

      <div className="section-heading">
        <div>
          <span className="eyebrow">FINDINGS SUMMARY</span>
          <h3>Control Results</h3>
        </div>
      </div>

      {findings.map((finding) => (

        <div
          className="report-finding-row"
          key={finding.control_id}
        >

          <div>
            <span>{finding.control_id}</span>
            <strong>{finding.title}</strong>
          </div>

          <span className="report-framework">
            {finding.framework}
          </span>

          <span className="report-severity">
            {finding.severity}
          </span>

          <span
            className={`status-badge ${finding.status.toLowerCase()}`}
          >
            {finding.status}
          </span>

        </div>

      ))}

    </div>

    <div className="report-actions">

      <button className="review-button">
        Preview Report
      </button>

      <button className="approve-button">
        Generate Report
      </button>

    </div>

    <div className="report-principle">

      <strong>Evidence-backed reporting</strong>

      <p>
        Every compliance result is linked to the observed
        configuration evidence and the policy that produced
        the decision.
      </p>

    </div>

  </section>
)}
        </main>
      </div>
    </div>
  )
}

export default App