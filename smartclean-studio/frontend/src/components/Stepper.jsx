import React from 'react';

export default function Stepper({ currentStep, steps }) {
  return (
    <div className="flex items-center justify-center gap-2 mb-8">
      {steps.map((step, index) => (
        <React.Fragment key={index}>
          <div className="flex flex-col items-center">
            <button
              disabled
              className={`w-12 h-12 rounded-full flex items-center justify-center font-semibold transition-all ${
                index < currentStep
                  ? 'bg-blue-600 text-white'
                  : index === currentStep
                  ? 'bg-blue-600 text-white ring-4 ring-blue-200'
                  : 'bg-gray-200 text-gray-600'
              }`}
            >
              {index < currentStep ? '✓' : index + 1}
            </button>
            <span className="text-sm font-medium mt-2 text-gray-700">{step}</span>
          </div>
          {index < steps.length - 1 && (
            <div className={`flex-1 h-1 mx-2 mb-6 ${index < currentStep ? 'bg-blue-600' : 'bg-gray-200'}`} />
          )}
        </React.Fragment>
      ))}
    </div>
  );
}
