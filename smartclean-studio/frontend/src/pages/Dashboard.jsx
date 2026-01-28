import React, { useState } from 'react';
import Stepper from '../components/Stepper';
import UploadBox from '../components/UploadBox';
import QualityScore from '../components/QualityScore';
import IssueCard from '../components/IssueCard';
import DataTable from '../components/DataTable';
import Button from '../components/Button';
import { configureCleaning, applyCleaning, getReport, downloadData } from '../services/api';

export default function Dashboard() {
  const [step, setStep] = useState(0);
  const [sessionId, setSessionId] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [cleaningResult, setCleaningResult] = useState(null);
  const [report, setReport] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [previewTab, setPreviewTab] = useState('report');

  const steps = ['Analyze', 'Configure', 'Results'];

  const handleUploadSuccess = (result) => {
    setSessionId(result.session_id);
    setAnalysisData(result);
    setStep(1);
  };

  const handleAutoClean = async () => {
    setIsLoading(true);
    try {
      await configureCleaning(sessionId, true);
      const result = await applyCleaning(sessionId);
      setCleaningResult(result);
      const reportData = await getReport(sessionId);
      setReport(reportData);
      setStep(2);
    } catch (error) {
      console.error('Cleaning failed:', error);
      alert('Cleaning failed: ' + (error.response?.data?.detail || error.message));
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = async (format) => {
    try {
      setIsLoading(true);
      await downloadData(sessionId, format);
      alert('Downloaded successfully!');
    } catch (error) {
      console.error('Download failed:', error);
      alert('Download failed: ' + (error.response?.data?.detail || error.message));
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartOver = () => {
    setStep(0);
    setSessionId(null);
    setAnalysisData(null);
    setCleaningResult(null);
    setReport(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <svg className="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10.5 1.5H5.75A2.25 2.25 0 003.5 3.75v12.5A2.25 2.25 0 005.75 18.5h8.5a2.25 2.25 0 002.25-2.25V7" stroke="currentColor" strokeWidth="1.5" fill="none" />
                <path d="M13 1.5v4.5a2 2 0 002 2h4.5" stroke="currentColor" strokeWidth="1.5" fill="none" />
              </svg>
              <h1 className="text-2xl font-bold text-gray-900">SmartClean Studio</h1>
            </div>
            {step > 0 && (
              <button
                onClick={handleStartOver}
                className="text-sm text-gray-600 hover:text-gray-900 underline"
              >
                ← Start Over
              </button>
            )}
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Step 0: Upload */}
        {step === 0 && (
          <div className="max-w-2xl mx-auto">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">Upload Your Dataset</h2>
              <p className="text-gray-600">Upload a CSV or Excel file to get started with data cleaning</p>
            </div>
            <UploadBox onUploadSuccess={handleUploadSuccess} isLoading={isLoading} />
          </div>
        )}

        {/* Steps 1-2: Dashboard */}
        {step > 0 && (
          <>
            <Stepper currentStep={step - 1} steps={steps} />

            {/* Step 1: Analyze */}
            {step === 1 && analysisData && (
              <div className="space-y-6">
                {/* Dataset Info */}
                <div className="grid grid-cols-4 gap-4">
                  <div className="bg-white p-4 rounded-lg shadow-sm">
                    <p className="text-gray-500 text-sm mb-1">Rows</p>
                    <p className="text-2xl font-bold text-gray-900">{analysisData.dataset_info.rows}</p>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-sm">
                    <p className="text-gray-500 text-sm mb-1">Columns</p>
                    <p className="text-2xl font-bold text-gray-900">{analysisData.dataset_info.columns}</p>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-sm">
                    <p className="text-gray-500 text-sm mb-1">File Size</p>
                    <p className="text-2xl font-bold text-gray-900">{analysisData.dataset_info.size_kb.toFixed(2)} KB</p>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-sm">
                    <p className="text-gray-500 text-sm mb-1">Quality Score</p>
                    <p className="text-2xl font-bold text-gray-900">{Math.round(analysisData.dataset_info.quality_score.overall)}/100</p>
                  </div>
                </div>

                {/* Data Preview and Issues */}
                <div className="grid grid-cols-3 gap-6">
                  <div className="col-span-2 bg-white p-6 rounded-lg shadow-sm">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Data Preview</h3>
                    <DataTable data={analysisData.preview_data} columns={analysisData.dataset_info.column_names} />
                  </div>
                  <div className="bg-white p-6 rounded-lg shadow-sm">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">
                      Issues Detected
                      <span className="ml-2 text-blue-600 text-sm font-bold">{analysisData.issues.length}</span>
                    </h3>
                    <div className="space-y-3 max-h-96 overflow-y-auto">
                      {analysisData.issues.slice(0, 5).map((issue, idx) => (
                        <IssueCard key={idx} issue={issue} />
                      ))}
                      {analysisData.issues.length > 5 && (
                        <p className="text-xs text-gray-500 text-center py-2">+{analysisData.issues.length - 5} more issues</p>
                      )}
                    </div>
                  </div>
                </div>

                {/* Quality Breakdown */}
                <div className="bg-white p-6 rounded-lg shadow-sm">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Quality Breakdown</h3>
                  <div className="grid grid-cols-4 gap-4">
                    <div className="text-center">
                      <div className="relative inline-flex items-center justify-center w-20 h-20">
                        <div className="absolute w-20 h-20 rounded-full border-4 border-gray-200"></div>
                        <div
                          className="absolute w-20 h-20 rounded-full border-4 border-green-500"
                          style={{
                            background: `conic-gradient(#10b981 ${analysisData.dataset_info.quality_score.completeness}%, #e5e7eb 0)`
                          }}
                        ></div>
                        <span className="relative text-sm font-bold text-gray-900">
                          {Math.round(analysisData.dataset_info.quality_score.completeness)}%
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mt-2">Completeness</p>
                    </div>
                    <div className="text-center">
                      <div className="relative inline-flex items-center justify-center w-20 h-20">
                        <div className="absolute w-20 h-20 rounded-full border-4 border-gray-200"></div>
                        <span className="relative text-sm font-bold text-gray-900">
                          {Math.round(analysisData.dataset_info.quality_score.uniqueness)}%
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mt-2">Uniqueness</p>
                    </div>
                    <div className="text-center">
                      <div className="relative inline-flex items-center justify-center w-20 h-20">
                        <div className="absolute w-20 h-20 rounded-full border-4 border-gray-200"></div>
                        <span className="relative text-sm font-bold text-gray-900">
                          {Math.round(analysisData.dataset_info.quality_score.consistency)}%
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mt-2">Consistency</p>
                    </div>
                    <div className="text-center">
                      <div className="relative inline-flex items-center justify-center w-20 h-20">
                        <div className="absolute w-20 h-20 rounded-full border-4 border-gray-200"></div>
                        <span className="relative text-sm font-bold text-gray-900">
                          {Math.round(analysisData.dataset_info.quality_score.accuracy)}%
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mt-2">Accuracy</p>
                    </div>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-4 justify-center pt-4">
                  <Button variant="secondary" onClick={() => setStep(0)}>
                    Upload Different File
                  </Button>
                  <Button variant="primary" size="lg" onClick={handleAutoClean} disabled={isLoading}>
                    {isLoading ? 'Cleaning...' : 'Auto Clean Now →'}
                  </Button>
                </div>
              </div>
            )}

            {/* Step 2: Results */}
            {step === 2 && cleaningResult && report && (
              <div className="space-y-6">
                {/* Success Banner */}
                <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
                  <div className="flex items-center justify-center mb-3">
                    <svg className="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">Cleaning Complete!</h3>
                  <p className="text-gray-600">Your dataset has been cleaned successfully. Review the changes below.</p>
                </div>

                {/* Quality Comparison */}
                <div className="bg-white p-6 rounded-lg shadow-sm">
                  <h3 className="text-lg font-semibold text-gray-900 mb-6 text-center">Quality Score Comparison</h3>
                  <div className="flex items-center justify-center gap-12">
                    <div className="text-center">
                      <QualityScore score={cleaningResult.quality_before?.overall || cleaningResult.quality_before || 0} size="medium" />
                      <p className="text-sm text-gray-600 mt-2">Before</p>
                    </div>
                    <div className="text-2xl text-gray-400">→</div>
                    <div className="text-center">
                      <QualityScore score={cleaningResult.quality_after?.overall || cleaningResult.quality_after || 0} size="medium" />
                      <p className="text-sm text-gray-600 mt-2">After</p>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-green-600">
                        +{((cleaningResult.quality_after?.overall || cleaningResult.quality_after || 0) - (cleaningResult.quality_before?.overall || cleaningResult.quality_before || 0)).toFixed(1)}%
                      </div>
                      <p className="text-sm text-gray-600 mt-2">Improvement</p>
                    </div>
                  </div>
                </div>

                {/* Summary Cards */}
                <div className="grid grid-cols-4 gap-4">
                  <div className="bg-white p-4 rounded-lg shadow-sm text-center">
                    <p className="text-gray-500 text-sm mb-1">Rows</p>
                    <p className="text-2xl font-bold text-gray-900">{analysisData?.dataset_info.rows || 0}</p>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-sm text-center">
                    <p className="text-gray-500 text-sm mb-1">Columns</p>
                    <p className="text-2xl font-bold text-gray-900">{analysisData?.dataset_info.columns}</p>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-sm text-center">
                    <p className="text-gray-500 text-sm mb-1">Issues Resolved</p>
                    <p className="text-2xl font-bold text-green-600">{cleaningResult.issues_resolved}</p>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-sm text-center">
                    <p className="text-gray-500 text-sm mb-1">Processing Time</p>
                    <p className="text-2xl font-bold text-gray-900">{cleaningResult.processing_time_ms.toFixed(0)}ms</p>
                  </div>
                </div>

                {/* Tabs */}
                <div className="bg-white rounded-lg shadow-sm overflow-hidden">
                  <div className="border-b border-gray-200 flex">
                    <button
                      onClick={() => setPreviewTab('report')}
                      className={`flex-1 px-6 py-3 text-center font-semibold transition-colors ${
                        previewTab === 'report'
                          ? 'text-blue-600 border-b-2 border-blue-600'
                          : 'text-gray-600 hover:text-gray-900'
                      }`}
                    >
                      Cleaning Report
                    </button>
                    <button
                      onClick={() => setPreviewTab('preview')}
                      className={`flex-1 px-6 py-3 text-center font-semibold transition-colors ${
                        previewTab === 'preview'
                          ? 'text-blue-600 border-b-2 border-blue-600'
                          : 'text-gray-600 hover:text-gray-900'
                      }`}
                    >
                      Data Preview
                    </button>
                  </div>
                  <div className="p-6">
                    {previewTab === 'report' && (
                      <div className="space-y-4">
                        <h4 className="text-sm font-semibold text-gray-900 mb-3">Cleaning Operations Applied</h4>
                        {report.operations.map((op, idx) => (
                          <div key={idx} className="border border-gray-200 rounded p-4 hover:bg-gray-50">
                            <div className="flex items-start justify-between mb-2">
                              <div>
                                <p className="font-semibold text-gray-900">{op.column}</p>
                                <p className="text-sm text-gray-600">{op.description}</p>
                              </div>
                              <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded">
                                {op.applied_by}
                              </span>
                            </div>
                            <p className="text-xs text-gray-500">Affected {op.rows_affected} rows</p>
                          </div>
                        ))}
                      </div>
                    )}
                    {previewTab === 'preview' && (
                      <DataTable data={cleaningResult.cleaned_data} columns={analysisData?.dataset_info.column_names} />
                    )}
                  </div>
                </div>

                {/* Download Section */}
                <div className="bg-white p-6 rounded-lg shadow-sm text-center space-y-4">
                  <p className="text-gray-700 font-semibold">Download your cleaned dataset:</p>
                  <div className="flex gap-4 justify-center">
                    <Button variant="secondary" onClick={() => handleDownload('csv')}>
                      ↓ Download CSV
                    </Button>
                    <Button variant="success" onClick={() => handleDownload('excel')}>
                      ↓ Download Excel
                    </Button>
                  </div>
                </div>

                {/* Start Over */}
                <div className="flex justify-center pt-4">
                  <Button variant="secondary" onClick={handleStartOver}>
                    Clean Another Dataset
                  </Button>
                </div>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}
