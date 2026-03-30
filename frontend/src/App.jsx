import { useMemo, useState } from 'react';
import FileUploader from './components/FileUploader';
import ResultPanel from './components/ResultPanel';

const API_BASE = import.meta.env.VITE_API_BASE || '';

function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('idle');
  const [error, setError] = useState('');
  const [result, setResult] = useState('');

  const canSubmit = Boolean(file) && status !== 'loading';

  const summary = useMemo(() => {
    if (!result) return null;
    const lines = result.split('\n').slice(0, 8).join('\n');
    return lines;
  }, [result]);

  const uploadFile = async () => {
    if (!file) return;

    setStatus('loading');
    setError('');
    setResult('');

    try {
      const body = new FormData();
      body.append('file', file);

      const response = await fetch(`${API_BASE}/summarize`, {
        method: 'POST',
        body,
      });

      if (!response.ok) {
        const payload = await response.json().catch(() => null);
        throw new Error(payload?.error || `HTTP ${response.status}`);
      }

      const payload = await response.json();
      if (!payload.result || !payload.result.trim()) {
        throw new Error(payload.error || 'No content returned from AI. Check backend logs and API key.');
      }
      setResult(payload.result);
      setStatus('success');
    } catch (err) {
      setStatus('error');
      setError(err.message || 'There was a problem processing the file.');
    }
  };

  return (
    <main className="app-shell">
      <section className="hero">
        <div className="hero-content">
          <h1>AI Study Buddy</h1>
          <p>Upload PDF notes and generate study summaries, flashcards, and quizzes.</p>

          <FileUploader onFileSelect={setFile} selectedFile={file} />

          <button className="primary-btn" disabled={!canSubmit} onClick={uploadFile}>
            {status === 'loading' ? 'Processing...' : 'Generate Results'}
          </button>

          <p className="hint">We recommend 1–10 pages per upload for consistent output quality.</p>

          {status === 'error' && <div className="alert error">{error}</div>}
          {status === 'success' && !error && <div className="alert success">Results generated successfully.</div>}
        </div>
      </section>

      <section className="result-section">
        <ResultPanel summary={summary} content={result} />
      </section>
    </main>
  );
}

export default App;
