export default function ResultPanel({ summary, content }) {
  if (!content) {
    return <div className="result-empty">No result yet. Upload a PDF and click Generate.</div>;
  }

  return (
    <div className="result-panel">
      <h2>AI Generated Study Output</h2>
      {summary && (
        <div className="kyccard">
          <h3>Preview</h3>
          <pre>{summary}</pre>
        </div>
      )}
      <div className="result-content">
        <pre>{content}</pre>
      </div>
    </div>
  );
}
