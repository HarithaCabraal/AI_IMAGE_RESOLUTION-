import React, { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [mode, setMode] = useState('auto');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  // Handle local image picking and create a local preview URL
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreviewUrl(URL.createObjectURL(selectedFile));
      setResult(null);
      setError('');
    }
  };

  // Ship the payload to our running FastAPI backend endpoint
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select an image file first.');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('mode', mode);

    try {
      const response = await fetch('http://localhost:8000/enhance', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setResult(data);
      } else {
        setError(data.error || 'The backend agent failed to process the image pipeline.');
      }
    } catch (err) {
      setError('Could not connect to the backend server. Make sure your Uvicorn server is running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-6 md:p-12 max-w-6xl mx-auto flex flex-col justify-between">
      {/* Top Navigation Row */}
      <header className="border-b border-slate-800 pb-6 mb-8">
        <h1 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
          AI Image Enhancer Agent
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Hackathon Edition · Multi-Service API Orchestration
        </p>
      </header>

      {/* Main Grid Working Space */}
      <main className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start mb-auto">
        
        {/* Left Hand Processing Controls Form (5 Columns wide) */}
        <form onSubmit={handleSubmit} className="lg:col-span-5 bg-slate-800/50 border border-slate-800 rounded-2xl p-6 space-y-6">
          <h2 className="text-xl font-bold tracking-wide">1. Configuration</h2>
          
          {/* File Picker Wrapper Box */}
          <div className="space-y-2">
            <label className="block text-sm font-semibold text-slate-300">Target Image</label>
            <div className="relative border-2 border-dashed border-slate-700 hover:border-cyan-500/50 rounded-xl p-4 transition-all bg-slate-900/40 text-center cursor-pointer">
              <input 
                type="file" 
                accept="image/*" 
                onChange={handleFileChange} 
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
              />
              <p className="text-slate-400 text-sm">
                Click or drag image file here to parse
              </p>
              <span className="text-xs text-slate-500 block mt-1">Supports PNG, JPG, JPEG</span>
            </div>
          </div>

          {/* AI Mode Selector Dropdown */}
          <div className="space-y-2">
            <label className="block text-sm font-semibold text-slate-300">Agent Processing Mode</label>
            <select 
              value={mode} 
              onChange={(e) => setMode(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-cyan-500 text-white font-medium"
            >
              <option value="auto">Auto-Detect & Enhance All (Recommended)</option>
              <option value="colorize">Colorize Only (DeepAI)</option>
              <option value="upscale">Super-Resolution Upscale Only (Cloudinary)</option>
            </select>
          </div>

          {/* Operational Submit Action Button */}
          <button
            type="submit"
            disabled={loading}
            className={`w-full py-3.5 rounded-xl font-bold tracking-wide transition-all ${
              loading 
                ? 'bg-slate-700 text-slate-400 cursor-not-allowed' 
                : 'bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white shadow-lg shadow-cyan-500/20'
            }`}
          >
            {loading ? 'Agent Orchestration Running...' : 'Execute AI Pipeline'}
          </button>

          {/* Feedback Messages block */}
          {error && (
            <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4 text-sm text-red-400">
              {error}
            </div>
          )}
        </form>

        {/* Right Hand Output Presentation Viewer Screen (7 Columns wide) */}
        <section className="lg:col-span-7 bg-slate-800/30 border border-slate-800 rounded-2xl p-6 min-h-[450px] flex flex-col justify-center items-center relative overflow-hidden">
          
          {!previewUrl && !result && (
            <div className="text-center text-slate-500 max-w-sm">
              <p className="font-semibold text-lg">No Active Media Asset</p>
              <p className="text-sm mt-1">Select an image profile on the configuration panel to deploy the viewer environment.</p>
            </div>
          )}

          {/* Combined Image Comparison Render Display Workspace */}
          <div className="w-full space-y-6">
            {previewUrl && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
                {/* Original Thumbnail Container Card */}
                <div className="space-y-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-400 bg-slate-900 px-2.5 py-1 rounded-md border border-slate-800 inline-block">
                    Source Asset
                  </span>
                  <div className="bg-slate-950 border border-slate-800/80 rounded-xl overflow-hidden aspect-square flex items-center justify-center p-2">
                    <img src={previewUrl} alt="Source Preview" className="max-w-full max-h-full object-contain rounded-lg" />
                  </div>
                </div>

                {/* Live Processed AI Output Result Container Card */}
                <div className="space-y-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-cyan-400 bg-cyan-950/40 px-2.5 py-1 rounded-md border border-cyan-900/50 inline-block">
                    Enhanced AI Output
                  </span>
                  <div className="bg-slate-950 border border-slate-800/80 rounded-xl overflow-hidden aspect-square flex items-center justify-center p-2 relative">
                    {loading && (
                      <div className="absolute inset-0 bg-slate-950/80 backdrop-blur-sm flex flex-col items-center justify-center space-y-3 z-20">
                        <div className="w-8 h-8 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
                        <p className="text-xs font-medium text-slate-300">Running AI models...</p>
                      </div>
                    )}
                    {result ? (
                      <img src={result.final_url} alt="AI Enhanced Output" className="max-w-full max-h-full object-contain rounded-lg" />
                    ) : (
                      !loading && (
                        <div className="text-slate-600 text-xs text-center p-4">
                          Awaiting execution pipeline return...
                        </div>
                      )
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* Verification Pipeline JSON Response Banner */}
            {result && (
              <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 text-xs font-mono text-slate-400 space-y-1">
                <p className="text-emerald-400 font-bold mb-1">✓ Execution Success</p>
                <p>Pipeline Chain: {JSON.stringify(result.pipeline_steps_executed)}</p>
                <a 
                  href={result.final_url} 
                  target="_blank" 
                  rel="noreferrer" 
                  className="text-cyan-400 underline block mt-2 hover:text-cyan-300"
                >
                  Open processed asset destination link ➜
                </a>
              </div>
            )}
          </div>
        </section>
      </main>

      {/* Presentation Footer Metadata Block */}
      <footer className="mt-12 pt-6 border-t border-slate-800 text-center text-xs text-slate-500">
        AI Enhancer Stack Architecture · Secure Localhost Deployment Network environment active.
      </footer>
    </div>
  );
}

export default App;