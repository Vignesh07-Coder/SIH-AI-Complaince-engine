import { useMemo, useState } from 'react'
import './App.css'
import { analyzeConfiguration, generateReport } from './api'

function formatValue(value) {
  if (value === null || value === undefined) {
    return '—'
  }

  if (typeof value === 'object') {
    try {
      return JSON.stringify(value)
    } catch {
      return 'Unserializable value'
    }
  }

  return String(value)
}

function getStatusClass(status) {
  return typeof status === 'string' ? status.toLowerCase() : 'unknown'
}

function getRemediationForFinding(finding, remediations) {
  return remediations.find(
    (remediation) => remediation.control_id === finding.control_id,
  )
}

function getEvidenceForFinding(_finding, evidence) {
  // The backend does not expose a finding-to-evidence identifier, so show the
  // analysis evidence collection without representing it as an exact match.
  return evidence
}

function EvidencePanel({ finding, evidence, expanded, onToggle }) {
  const findingEvidence = getEvidenceForFinding(finding, evidence)

  return (
    <div className="evidence-panel">
      <button
        className="evidence-toggle"
        type="button"
        onClick={() => onToggle(finding.control_id)}
        aria-expanded={expanded}
      >
        {expanded ? 'Hide Evidence' : 'Evidence'}
      </button>
      {expanded && (
        <div className="evidence-list">
          <span>CONFIGURATION EVIDENCE</span>
          {findingEvidence.length === 0 ? (
            <p>No evidence returned for this analysis.</p>
          ) : (
            findingEvidence.map((item, index) => (
              <div
                className="evidence-item"
                key={`${item.source_file ?? 'evidence'}-${item.line_number ?? index}`}
              >
                <small>
                  {formatValue(item.source_file)}
                  {item.line_number !== null && item.line_number !== undefined
                    ? `, line ${item.line_number}`
                    : ''}
                  {item.parser ? ` | ${item.parser}` : ''}
                </small>
                <code>{formatValue(item.raw_text)}</code>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  )
}

function RemediationPanel({ finding, remediations, copiedCommand, onCopy }) {
  const remediation = getRemediationForFinding(finding, remediations)

  if (finding.status === 'PASS') {
    return (
      <div className="remediation-panel quiet">
        <span>RECOMMENDED REMEDIATION</span>
        <p>No remediation required.</p>
      </div>
    )
  }

  if (finding.status === 'UNKNOWN') {
    return (
      <div className="remediation-panel quiet">
        <span>RECOMMENDED REMEDIATION</span>
        <p>No remediation available until the control can be determined.</p>
      </div>
    )
  }

  if (!remediation) {
    return (
      <div className="remediation-panel">
        <span>RECOMMENDED REMEDIATION</span>
        <p>No validated remediation is available for this control.</p>
      </div>
    )
  }

  return (
    <div className="remediation-panel">
      <span>RECOMMENDED REMEDIATION</span>
      <p>{formatValue(remediation.description)}</p>
      <div className="command-row">
        <code>{formatValue(remediation.command)}</code>
        <button
          className="copy-command-button"
          type="button"
          onClick={() => onCopy(remediation.command, finding.control_id)}
        >
          {copiedCommand === finding.control_id ? 'Copied' : 'Copy'}
        </button>
      </div>
      <p>
        {remediation.requires_change_window
          ? 'Change window: Required'
          : 'Change window: Not required'}
      </p>
    </div>
  )
}

function FindingCard({
  finding,
  evidence,
  remediations,
  expandedEvidence,
  onToggleEvidence,
  copiedCommand,
  onCopyCommand,
}) {
  return (
    <article className={`finding-card operational-finding ${getStatusClass(finding.status)}`}>
      <div className="finding-header">
        <div>
          <span className="control-id">{formatValue(finding.control_id)}</span>
          <h3>{formatValue(finding.description)}</h3>
        </div>

        <div className="finding-badges">
          <span className={`severity ${getStatusClass(finding.severity)}`}>
            {formatValue(finding.severity)}
          </span>
          <span className={`status-badge ${getStatusClass(finding.status)}`}>
            {formatValue(finding.status)}
          </span>
        </div>
      </div>

      <div className="finding-details">
        <div>
          <span>EXPECTED</span>
          <p>{formatValue(finding.expected)}</p>
        </div>
        <div>
          <span>OBSERVED</span>
          <p>{formatValue(finding.observed)}</p>
        </div>
      </div>

      <RemediationPanel
        finding={finding}
        remediations={remediations}
        copiedCommand={copiedCommand}
        onCopy={onCopyCommand}
      />
      <EvidencePanel
        finding={finding}
        evidence={evidence}
        expanded={Boolean(expandedEvidence[finding.control_id])}
        onToggle={onToggleEvidence}
      />
    </article>
  )
}

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisComplete, setAnalysisComplete] = useState(false)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [error, setError] = useState('')
  const [activePage, setActivePage] = useState('dashboard')
  const [expandedEvidence, setExpandedEvidence] = useState({})
  const [copiedCommand, setCopiedCommand] = useState('')
  const [isGeneratingReport, setIsGeneratingReport] = useState(false)
  const findings = useMemo(
    () => analysisResult?.findings ?? [],
    [analysisResult],
  )
  const evidence = analysisResult?.evidence ?? []
  const remediations = analysisResult?.remediations ?? []
  const vendor = analysisResult?.vendor?.name ?? '—'
  const vendorConfidence = analysisResult?.vendor?.confidence

  const summary = useMemo(() => {
    const passed = findings.filter(
      (finding) => finding.status === 'PASS',
    ).length
    const failed = findings.filter(
      (finding) => finding.status === 'FAIL',
    ).length

    return {
      total: findings.length,
      passed,
      failed,
      unknown: findings.filter(
        (finding) => finding.status === 'UNKNOWN',
      ).length,
      high: findings.filter(
        (finding) => finding.severity?.toLowerCase() === 'high',
      ).length,
      score: passed + failed > 0
        ? Math.round((passed / (passed + failed)) * 100)
        : null,
    }
  }, [findings])

  const handleFileSelect = (file) => {
    setSelectedFile(file ?? null)
    setAnalysisResult(null)
    setAnalysisComplete(false)
    setError('')
    setExpandedEvidence({})
    setCopiedCommand('')
  }

  const handleAnalyze = async () => {
    if (!selectedFile) {
      return
    }

    setIsAnalyzing(true)
    setError('')
    setAnalysisComplete(false)

    try {
      const result = await analyzeConfiguration(selectedFile)

      setAnalysisResult(result)
      setAnalysisComplete(true)
      setActivePage('findings')
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Unable to analyze configuration.',
      )
    } finally {
      setIsAnalyzing(false)
    }
  }

  const toggleEvidence = (controlId) => {
    setExpandedEvidence((current) => ({
      ...current,
      [controlId]: !current[controlId],
    }))
  }

  const handleCopyCommand = async (command, controlId) => {
    try {
      await navigator.clipboard.writeText(command)
      setCopiedCommand(controlId)
    } catch {
      setError('Unable to copy the remediation command.')
    }
  }

  const triggerDownload = (blob, filename) => {
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    link.remove()
    URL.revokeObjectURL(url)
  }

  const handleDownloadConfiguration = () => {
    if (selectedFile) {
      triggerDownload(selectedFile, selectedFile.name)
    }
  }

  const handleGenerateReport = async () => {
    if (!analysisResult || !selectedFile) {
      return
    }

    setIsGeneratingReport(true)
    setError('')

    try {
      const report = await generateReport(analysisResult, selectedFile.name)
      triggerDownload(report.blob, report.filename)
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Unable to generate the report.',
      )
    } finally {
      setIsGeneratingReport(false)
    }
  }

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
              <strong>{analysisComplete ? 1 : 0}</strong>
              <small>Analyzed</small>
            </div>

            <div className="stat-card">
              <span className="stat-label">Compliance</span>
              <strong>{summary.score === null ? '—' : `${summary.score}%`}</strong>
              <small>Overall score</small>
            </div>

            <div className="stat-card">
              <span className="stat-label">Findings</span>
              <strong>{summary.total}</strong>
              <small>Issues detected</small>
            </div>

            <div className="stat-card">
              <span className="stat-label">Vendor</span>
              <strong>{vendor}</strong>
              <small>
                {typeof vendorConfidence === 'number'
                  ? `${Math.round(vendorConfidence * 100)}% confidence`
                  : 'Detected from analysis'}
              </small>
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
                onChange={(event) => handleFileSelect(event.target.files[0])}
              />
            </label>

            <span className="upload-note">
              Vendor is detected from the uploaded configuration.
            </span>

            {selectedFile && (
              <p className="selected-file">
                Selected: {selectedFile.name}
              </p>
            )}
{selectedFile && !analysisComplete && (
              <button
                className="analyze-button"
                onClick={handleAnalyze}
                disabled={isAnalyzing}
              >
                {isAnalyzing ? 'Analyzing...' : 'Analyze Configuration'}
              </button>
            )}
            {error && <p className="selected-file">{error}</p>}
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
        <strong>{selectedFile?.name ?? '—'}</strong>
      </div>

      <div>
        <span>Vendor</span>
        <strong>
          {vendor}
        </strong>
      </div>

      <div>
        <span>Compliance</span>
        <strong className="pass-text">
          {summary.score === null ? '—' : `${summary.score}%`}
        </strong>
      </div>
    </div>

    <div className="result-actions">
      <button
        className="review-button"
        type="button"
        onClick={handleDownloadConfiguration}
        disabled={!selectedFile}
      >
        Download Configuration
      </button>
      <button
        className="approve-button"
        type="button"
        onClick={handleGenerateReport}
        disabled={!analysisResult || !selectedFile || isGeneratingReport}
      >
        {isGeneratingReport ? 'Generating Report...' : 'Generate Report'}
      </button>
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
        <span className="summary-pass">{summary.passed} Passed</span>
        <span className="summary-fail">{summary.failed} Failed</span>
      </div>
    </div>

    <div className="findings-list">
      {findings.map((finding) => (
        <FindingCard
          key={finding.control_id}
          finding={finding}
          evidence={evidence}
          remediations={remediations}
          expandedEvidence={expandedEvidence}
          onToggleEvidence={toggleEvidence}
          copiedCommand={copiedCommand}
          onCopyCommand={handleCopyCommand}
        />
      ))}
    </div>
    {findings.length === 0 && (
      <p>No findings returned for this analysis.</p>
    )}
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
          onChange={(event) => handleFileSelect(event.target.files[0])}
        />
      </label>

      <span className="upload-note">
        Vendor is detected from the uploaded configuration.
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

      {error && <p className="selected-file">{error}</p>}

      {selectedFile && (
        <button
          className="analyze-main-button"
          onClick={handleAnalyze}
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
        <strong>{summary.total}</strong>
      </div>

      <div className="finding-stat">
        <span>Passed</span>
        <strong>
          {summary.passed}
        </strong>
      </div>

      <div className="finding-stat">
        <span>Failed</span>
        <strong>
          {summary.failed}
        </strong>
      </div>

      <div className="finding-stat">
        <span>High Severity</span>
        <strong>
          {summary.high}
        </strong>
      </div>

    </div>

    <div className="findings-list">

      {findings.map((finding) => (
        <FindingCard
          key={finding.control_id}
          finding={finding}
          evidence={evidence}
          remediations={remediations}
          expandedEvidence={expandedEvidence}
          onToggleEvidence={toggleEvidence}
          copiedCommand={copiedCommand}
          onCopyCommand={handleCopyCommand}
        />

      ))}

    </div>

    {analysisComplete && findings.length === 0 && (
      <p>No findings returned for this analysis.</p>
    )}

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

                <h3>{finding.description}</h3>
              </div>

              <span className="severity-badge">
                {finding.severity}
              </span>

            </div>

            <div className="remediation-info">

              <div>
                <span>DETECTED ISSUE</span>
                <p>{formatValue(finding.observed)}</p>
              </div>

              <div>
                <span>RECOMMENDED ACTION</span>
                <p>
                  {getRemediationForFinding(finding, remediations)
                    ? formatValue(
                      getRemediationForFinding(finding, remediations).description,
                    )
                    : 'No validated remediation is available for this control.'}
                </p>
              </div>

            </div>

            <div className="remediation-command">

              <span>PROPOSED CONFIGURATION CHANGE</span>

              <code>
                {getRemediationForFinding(finding, remediations)
                  ? formatValue(
                    getRemediationForFinding(finding, remediations).command,
                  )
                  : 'No validated remediation is available for this control.'}
              </code>
              <p>
                {getRemediationForFinding(finding, remediations)
                  ? getRemediationForFinding(finding, remediations).requires_change_window
                    ? 'Change window required.'
                    : 'No change window required.'
                  : 'Change-window requirement unavailable.'}
              </p>

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

    {!analysisComplete ? (
      <div className="report-empty">
        <strong>No analysis available</strong>
        <p>Analyze a configuration before generating an audit report.</p>
      </div>
    ) : (
      <>

    <div className="report-overview">

      <div className="report-score">
        <span>COMPLIANCE SCORE</span>

        <strong>{summary.score === null ? '—' : `${summary.score}%`}</strong>

        <small>
          {summary.passed} of {summary.passed + summary.failed} evaluated controls passed
        </small>
      </div>

      <div className="report-stat">
        <span>CONTROLS CHECKED</span>
        <strong>{summary.total}</strong>
      </div>

      <div className="report-stat">
        <span>FAILED</span>
        <strong>
          {summary.failed}
        </strong>
      </div>

      <div className="report-stat">
        <span>HIGH SEVERITY</span>
        <strong>
          {summary.high}
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
          <strong>{vendor}</strong>
        </div>

        <div>
          <span>EVIDENCE</span>
          <strong>{evidence.length} returned</strong>
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
            <strong>{finding.description}</strong>
          </div>

          <span className="report-severity">
            {finding.severity}
          </span>

          <span
            className={`status-badge ${getStatusClass(finding.status)}`}
          >
            {finding.status}
          </span>

        </div>

      ))}

    </div>

    <div className="report-actions">

      <button
        className="review-button"
        type="button"
        onClick={handleDownloadConfiguration}
        disabled={!selectedFile}
      >
        Download Configuration
      </button>

      <button
        className="approve-button"
        type="button"
        onClick={handleGenerateReport}
        disabled={!analysisResult || !selectedFile || isGeneratingReport}
      >
        {isGeneratingReport ? 'Generating Report...' : 'Generate Report'}
      </button>

    </div>

    {error && <p className="selected-file">{error}</p>}

    <div className="report-principle">

      <strong>Evidence-backed reporting</strong>

      <p>
        Every compliance result is linked to the observed
        configuration evidence and the policy that produced
        the decision.
      </p>

    </div>

      </>
    )}

  </section>
)}
        </main>
      </div>
    </div>
  )
}

export default App
