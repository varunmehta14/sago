'use client';

import { useState } from 'react';
import { api, type AnalysisResult } from '@/lib/api';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [useAgents, setUseAgents] = useState(false); // Default to simple AI (more reliable)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
      setResult(null);
    }
  };

  const handleUploadAndAnalyze = async () => {
    if (!file) {
      setError('Please select a PDF file');
      return;
    }

    try {
      setUploading(true);
      setError(null);

      // Upload pitch deck
      const uploadResponse = await api.uploadPitchDeck(file);

      setUploading(false);
      setAnalyzing(true);

      // Analyze pitch deck - choose method based on toggle
      const analysisResult = useAgents
        ? await api.analyzePitchDeckWithAgents(uploadResponse.file_id)
        : await api.analyzePitchDeck(uploadResponse.file_id);

      setResult(analysisResult);
      setAnalyzing(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setUploading(false);
      setAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
            Sago Pitch Deck Analyzer
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            AI-powered verification and due diligence for investor pitches
          </p>
        </header>

        {/* Upload Section */}
        <div className="max-w-4xl mx-auto bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
            Upload Pitch Deck
          </h2>

          <div className="space-y-4">
            <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center">
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="cursor-pointer inline-flex items-center px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition-colors"
              >
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                Choose PDF File
              </label>

              {file && (
                <p className="mt-4 text-sm text-gray-600 dark:text-gray-400">
                  Selected: <span className="font-medium">{file.name}</span>
                </p>
              )}
            </div>

            {error && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-lg">
                {error}
              </div>
            )}

            {/* Analysis Method Toggle */}
            <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
              <label className="flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={useAgents}
                  onChange={(e) => setUseAgents(e.target.checked)}
                  className="w-5 h-5 text-indigo-600 rounded focus:ring-indigo-500"
                />
                <div className="ml-3 flex-1">
                  <span className="text-sm font-medium text-gray-900 dark:text-white">
                    🚀 Use Advanced Multi-Agent Analysis
                  </span>
                  <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                    4 specialized agents + web search tools for comprehensive verification.
                  </p>
                </div>
              </label>
            </div>

            <button
              onClick={handleUploadAndAnalyze}
              disabled={!file || uploading || analyzing}
              className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
            >
              {uploading ? 'Uploading...' : analyzing ? (useAgents ? 'Analyzing with Multi-Agent AI...' : 'Analyzing with AI...') : 'Analyze Pitch Deck'}
            </button>
          </div>
        </div>

        {/* Results Section */}
        {result && (
          <div className="max-w-4xl mx-auto space-y-6">
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Claims Extracted</h3>
                <p className="text-3xl font-bold text-indigo-600 dark:text-indigo-400 mt-2">
                  {result.summary.total_claims}
                </p>
              </div>
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Verified Claims</h3>
                <p className="text-3xl font-bold text-green-600 dark:text-green-400 mt-2">
                  {result.summary.verified_claims}
                </p>
              </div>
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Questions Generated</h3>
                <p className="text-3xl font-bold text-purple-600 dark:text-purple-400 mt-2">
                  {result.summary.questions_generated}
                </p>
              </div>
            </div>

            {/* Verification Results */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
                Verification Results
              </h2>
              <div className="space-y-4">
                {result.verification_results.map((item, index) => (
                  <div key={index} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                    <p className="font-medium text-gray-900 dark:text-white mb-2">
                      {item.claim}
                    </p>
                    <div className="text-sm text-gray-600 dark:text-gray-400 whitespace-pre-wrap">
                      {item.verification_result}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Questions for Founder */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
                Questions to Ask the Founder
              </h2>
              <div className="space-y-3">
                {result.questions.map((question, index) => (
                  <div key={index} className="flex items-start">
                    <span className="flex-shrink-0 w-8 h-8 bg-indigo-100 dark:bg-indigo-900 text-indigo-600 dark:text-indigo-400 rounded-full flex items-center justify-center font-semibold text-sm mr-3">
                      {index + 1}
                    </span>
                    <p className="text-gray-700 dark:text-gray-300 pt-1">{question}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
