import React from 'react';


const ProgressBar = ({ value = 0, gradient = "from-indigo-500 to-purple-500", height = "h-3", showPercentage = false }) => (
  <div className="w-full">
    <div className={`w-full bg-gray-200 rounded-full ${height} overflow-hidden relative`}>
      <div
        className={`${height} rounded-full bg-gradient-to-r ${gradient} shimmer transition-all duration-1000 ease-out relative`}
        style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
      >
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"></div>
      </div>
    </div>
    {showPercentage && (
      <div className="text-xs text-gray-600 mt-1 font-semibold text-right">
        {Math.round(value)}%
      </div>
    )}
  </div>
);

export default ProgressBar;