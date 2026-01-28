import React from 'react';

export default function LandingPage({ onStartCleaning }) {
  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 via-pink-50 to-white">
      {/* Header */}
      <header className="bg-white bg-opacity-50 backdrop-blur-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center gap-2">
          <svg className="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10.5 1.5H5.75A2.25 2.25 0 003.5 3.75v12.5A2.25 2.25 0 005.75 18.5h8.5a2.25 2.25 0 002.25-2.25V7" stroke="currentColor" strokeWidth="1.5" fill="none" />
            <path d="M13 1.5v4.5a2 2 0 002 2h4.5" stroke="currentColor" strokeWidth="1.5" fill="none" />
          </svg>
          <h1 className="text-2xl font-bold text-gray-900">SmartClean Studio</h1>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center space-y-8">
          {/* Badge */}
          <div className="inline-block">
            <div className="px-4 py-2 bg-cyan-100 text-cyan-700 rounded-full text-sm font-semibold flex items-center gap-2">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              Hybrid Data Cleaning System
            </div>
          </div>

          {/* Main Headline */}
          <div>
            <h2 className="text-5xl sm:text-6xl font-bold text-gray-900 mb-4">
              Clean Your Data
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-500 to-blue-600">
                Intelligently
              </span>
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Upload your dataset and let our intelligent system detect issues, apply smart fixes, and give you production-ready clean data — with full transparency and control.
            </p>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
            <button
              onClick={onStartCleaning}
              className="px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-semibold rounded-lg hover:shadow-lg hover:scale-105 transition-all flex items-center gap-2 justify-center"
            >
              Start Cleaning
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </button>
            <button
              className="px-8 py-4 bg-white text-gray-900 font-semibold rounded-lg border-2 border-gray-200 hover:border-gray-300 hover:shadow-md transition-all"
            >
              Learn More
            </button>
          </div>

          {/* Features */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 pt-16">
            <div className="space-y-3">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg className="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                </svg>
              </div>
              <h3 className="font-semibold text-gray-900">Automatic Detection</h3>
              <p className="text-gray-600 text-sm">Instantly identifies missing values, outliers, duplicates, and inconsistencies</p>
            </div>
            <div className="space-y-3">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M6.707 6.707a1 1 0 010 1.414L5.414 9l1.293 1.293a1 1 0 01-1.414 1.414l-2-2a1 1 0 010-1.414l2-2a1 1 0 011.414 0zm7.586 0a1 1 0 011.414 0l2 2a1 1 0 010 1.414l-2 2a1 1 0 11-1.414-1.414L14.586 9l-1.293-1.293a1 1 0 010-1.414zM9 11a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
                </svg>
              </div>
              <h3 className="font-semibold text-gray-900">Smart Fixes</h3>
              <p className="text-gray-600 text-sm">Applies intelligent cleaning rules with median imputation, IQR capping, and more</p>
            </div>
            <div className="space-y-3">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg className="w-6 h-6 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                  <path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd" />
                </svg>
              </div>
              <h3 className="font-semibold text-gray-900">Full Transparency</h3>
              <p className="text-gray-600 text-sm">See exactly what changed, why it changed, and who decided it</p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-20 border-t border-gray-200 bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-gray-600 text-sm">
          <p>SmartClean Studio © 2024 · Making data cleaning intelligent and accessible</p>
        </div>
      </footer>
    </div>
  );
}
