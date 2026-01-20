import React from 'react';
import { Brain, CheckCircle, Sparkles, TrendingUp, Target, Zap, ArrowRight } from 'lucide-react';


const ResumeAnalysisScreen = ({ goTo }) => {
  const skills = [
    { name: "JavaScript", level: 85 },
    { name: "React", level: 70 },
    { name: "HTML/CSS", level: 90 },
    { name: "Git", level: 65 },
  ];

  const gaps = [
    { name: "TypeScript", demand: "High", priority: "Critical" },
    { name: "Node.js", demand: "High", priority: "Important" },
    { name: "AWS", demand: "High", priority: "Important" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 pt-32 pb-24 px-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16 fade-in">
          <div className="inline-block p-6 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-3xl mb-8 shadow-2xl hover:scale-110 transition-transform pulse-glow">
            <Brain className="w-16 h-16 text-white" />
          </div>
          <h1 className="text-5xl md:text-6xl font-black mb-5 gradient-text">
            AI Resume Analysis
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            We analyzed your resume and extracted skills, gaps and best matches
          </p>
        </div>

        {/* Analysis Cards */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
          {/* Top Skills */}
          <div className="bg-white p-8 rounded-3xl shadow-2xl border-2 border-green-100 slide-up">
            <div className="flex items-center gap-4 mb-6">
              <div className="p-3 bg-green-100 rounded-2xl">
                <CheckCircle className="w-7 h-7 text-green-600" />
              </div>
              <div>
                <div className="font-bold text-2xl text-gray-900">Top Skills</div>
                <div className="text-sm text-gray-500">Extracted from your resume</div>
              </div>
            </div>
            <div className="space-y-4">
              {skills.map((s, i) => (
                <div key={i}>
                  <div className="flex justify-between mb-2">
                    <div className="font-semibold text-gray-900">{s.name}</div>
                    <div className="text-sm font-bold text-green-600">{s.level}%</div>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                    <div
                      className="h-3 rounded-full bg-gradient-to-r from-green-400 to-green-600 shimmer transition-all duration-1000"
                      style={{ width: `${s.level}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Skills Gap */}
          <div className="bg-white p-8 rounded-3xl shadow-2xl border-2 border-orange-100 slide-up" style={{ animationDelay: '0.1s' }}>
            <div className="flex items-center gap-4 mb-6">
              <div className="p-3 bg-orange-100 rounded-2xl">
                <Sparkles className="w-7 h-7 text-orange-600" />
              </div>
              <div>
                <div className="font-bold text-2xl text-gray-900">Skills Gap</div>
                <div className="text-sm text-gray-500">What to learn next</div>
              </div>
            </div>
            <div className="space-y-4">
              {gaps.map((g, i) => (
                <div key={i} className="flex items-center justify-between p-4 bg-orange-50 rounded-2xl border-2 border-orange-100 hover:border-orange-300 transition-all">
                  <div>
                    <div className="font-bold text-gray-900">{g.name}</div>
                    <div className="text-sm text-gray-500">{g.demand} demand</div>
                  </div>
                  <div className="px-4 py-2 bg-orange-600 text-white rounded-full text-xs font-bold">
                    {g.priority}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Best Match */}
          <div className="bg-gradient-to-br from-indigo-600 to-purple-600 p-8 rounded-3xl text-white shadow-2xl slide-up relative overflow-hidden" style={{ animationDelay: '0.2s' }}>
            <div className="absolute inset-0 overflow-hidden">
              <div className="absolute -right-10 -top-10 w-48 h-48 rounded-full bg-white/10 blur-3xl"></div>
            </div>
            <div className="relative z-10">
              <div className="flex items-center gap-3 mb-6">
                <Target className="w-8 h-8" />
                <div className="text-sm opacity-90 font-semibold">Best Match</div>
              </div>
              <div className="text-4xl font-black mb-3">Full Stack Developer</div>
              <div className="flex items-center gap-2 mb-8">
                <TrendingUp className="w-5 h-5" />
                <div className="text-lg">Compatibility: <span className="font-bold">92%</span></div>
              </div>
              <button
                onClick={() => goTo("learning-path")}
                className="w-full bg-white/20 backdrop-blur-sm border-2 border-white/30 rounded-xl py-4 font-bold hover:bg-white/30 transition-all text-lg"
              >
                Generate Learning Path →
              </button>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-5 justify-center slide-up" style={{ animationDelay: '0.3s' }}>
          <button
            onClick={() => goTo("dashboard")}
            className="px-8 py-4 bg-white rounded-xl border-2 border-gray-200 hover:bg-gray-100 hover:border-gray-300 transition-all font-semibold text-lg"
          >
            Back to Dashboard
          </button>
          <button
            onClick={() => goTo("learning-path")}
            className="px-10 py-5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-bold hover:scale-105 transition-all shadow-xl text-lg flex items-center justify-center gap-2"
          >
            Start Learning
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ResumeAnalysisScreen;