import React from 'react';

export default function DataTable({ data, columns = [] }) {
  if (!data || data.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>No data to display</p>
      </div>
    );
  }

  const cols = columns.length > 0 ? columns : Object.keys(data[0]);

  return (
    <div className="overflow-x-auto shadow-sm rounded-lg border border-gray-200">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {cols.map((col) => (
              <th key={col} className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {data.slice(0, 10).map((row, idx) => (
            <tr key={idx} className="hover:bg-gray-50">
              {cols.map((col) => (
                <td key={`${idx}-${col}`} className="px-6 py-4 text-sm text-gray-900">
                  {row[col] !== null && row[col] !== undefined ? String(row[col]).substring(0, 50) : 'N/A'}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
