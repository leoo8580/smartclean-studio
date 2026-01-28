import React from 'react';

export default function IssueCard({ issue }) {
  const severityColor = {
    low: 'bg-blue-100 text-blue-800',
    medium: 'bg-yellow-100 text-yellow-800',
    high: 'bg-red-100 text-red-800'
  };

  return (
    <div className="bg-white p-4 rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-2">
        <div>
          <p className="font-semibold text-gray-900 text-sm">"{issue.column}"</p>
          <p className="text-xs text-gray-500 capitalize">{issue.issue_type.replace('_', ' ')}</p>
        </div>
        <span className={`px-2 py-1 rounded text-xs font-semibold ${severityColor[issue.severity]}`}>
          {issue.affected_percentage.toFixed(1)}%
        </span>
      </div>
      <p className="text-sm text-gray-700 mb-3">{issue.suggested_fix}</p>
      <div className="bg-blue-50 border border-blue-200 rounded p-2">
        <p className="text-xs text-blue-800">
          <span className="font-semibold">→ {issue.recommended_operation.operation.replace('_', ' ')}</span>
        </p>
      </div>
    </div>
  );
}
