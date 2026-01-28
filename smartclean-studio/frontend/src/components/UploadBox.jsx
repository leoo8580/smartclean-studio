import React, { useState, useRef } from 'react';
import { uploadDataset } from '../services/api';

export default function UploadBox({ onUploadSuccess, isLoading }) {
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  };

  const handleDragLeave = () => {
    setDragActive(false);
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const file = e.dataTransfer.files[0];
    if (file && ['text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'].includes(file.type)) {
      await handleFile(file);
    }
  };

  const handleChange = async (e) => {
    const file = e.target.files[0];
    if (file) {
      await handleFile(file);
    }
  };

  const handleFile = async (file) => {
    try {
      const result = await uploadDataset(file);
      onUploadSuccess(result);
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Upload failed: ' + (error.response?.data?.detail || error.message));
    }
  };

  return (
    <div
      onDragEnter={handleDrag}
      onDragLeave={handleDragLeave}
      onDragOver={handleDrag}
      onDrop={handleDrop}
      className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
        dragActive
          ? 'border-blue-500 bg-blue-50'
          : 'border-gray-300 bg-gray-50 hover:border-blue-400'
      }`}
    >
      <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" stroke="currentColor" fill="none" viewBox="0 0 48 48">
        <path d="M28 8H12a4 4 0 00-4 4v20a4 4 0 004 4h24a4 4 0 004-4V20m-8-12l-4-4m0 0l-4 4m4-4v12" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      <p className="text-lg font-semibold text-gray-700 mb-2">Upload your dataset</p>
      <p className="text-gray-500 mb-4">Drag & drop or <button type="button" onClick={() => inputRef.current?.click()} className="text-blue-600 hover:text-blue-700 font-semibold">browse</button> to select</p>
      <p className="text-sm text-gray-400">CSV, XLSX, XLS • Max 50 MB</p>
      <input
        ref={inputRef}
        type="file"
        accept=".csv,.xlsx,.xls"
        onChange={handleChange}
        className="hidden"
        disabled={isLoading}
      />
    </div>
  );
}
