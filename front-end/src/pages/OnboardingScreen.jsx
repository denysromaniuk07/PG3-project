import React from 'react';
import { Sparkles, Upload, ArrowRight, Target, Zap, TrendingUp } from 'lucide-react';

/**
 * OnboardingScreen.jsx
 * Enhanced with better spacing and animations
 */
const OnboardingScreen = ({ goTo }) => (
  <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 flex items-center justify-center p-6 pt-32 pb-12">
    <div className="max-w-5xl w-full">
      {/* Header */}
      <div className="text-center mb-12 fade-in">
        <div className="inline-block p-6 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-3xl mb-6 shadow-2xl hover:scale-110 transition-transform pulse-glow">
          <Sparkles className="w-14 h-14 text-white" />
        </div>
        <h1 className="text-5xl md:text-6xl font-black mb-4 gradient-text">
          Welcome to SkillPath AI
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
          Upload a resume or answer a few quick questions — and we'll build your personalized roadmap
        </p>
      </div>

      {/* Main Card */}
      <div className="bg-white rounded-3xl p-10 shadow-2xl border-2 border-gray-100 slide-up">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Upload Option */}
          <div className="border-2 border-dashed border-indigo-300 rounded-2xl p-8 text-center cursor-pointer hover:border-indigo-500 hover:bg-indigo-50/50 transition-all group">
            <div className="w-24 h-24 mx-auto mb-6 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform shadow-lg">
              <Upload className="w-10 h-10 text-indigo-600" />
            </div>
            <h3 className="font-bold text-2xl mb-2 text-gray-900">Upload Resume</h3>
            <p className="text-sm text-gray-500 mb-4">PDF, DOCX • Max 5MB</p>
            <div className="inline-block px-4 py-2 bg-indigo-100 text-indigo-600 rounded-lg text-sm font-semibold">
              Click to browse
            </div>
          </div>

          {/* Quick Questions Option */}
          <div className="rounded-2xl p-8 bg-gradient-to-br from-gray-50 to-indigo-50 border-2 border-gray-200">
            <h3 className="font-bold text-2xl mb-3 text-gray-900 flex items-center gap-2">
              <Target className="w-6 h-6 text-indigo-600" />
              Quick Questions
            </h3>
            <p className="text-sm text-gray-600 mb-6">
              We'll customize your learning path based on experience & goals
            </p>
            <div className="grid grid-cols-1 gap-4">
              <div className="border-2 border-gray-200 rounded-xl p-4 bg-white hover:border-indigo-300 transition-all">
                <div className="text-sm font-semibold text-gray-700 mb-1">🎯 Career Goal</div>
                <div className="text-gray-900 font-medium">Full Stack Developer</div>
              </div>
              <div className="border-2 border-gray-200 rounded-xl p-4 bg-white hover:border-indigo-300 transition-all">
                <div className="text-sm font-semibold text-gray-700 mb-1">⚡ Experience Level</div>
                <div className="text-gray-900 font-medium">Intermediate</div>
              </div>
              <div className="border-2 border-gray-200 rounded-xl p-4 bg-white hover:border-indigo-300 transition-all">
                <div className="text-sm font-semibold text-gray-700 mb-1">📚 Preferred Learning</div>
                <div className="text-gray-900 font-medium">Hands-on Projects</div>
              </div>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mt-10 flex flex-col sm:flex-row justify-end gap-4">
          <button
            onClick={() => goTo("splash")}
            className="px-6 py-3 rounded-xl border-2 border-gray-200 hover:bg-gray-100 hover:border-gray-300 transition-all font-semibold"
          >
            Back
          </button>
          <button
            onClick={() => goTo("resume-analysis")}
            className="px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-bold text-lg hover:scale-105 hover:shadow-xl transition-all flex items-center justify-center gap-2"
          >
            Analyze & Build Path
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Features */}
      <div className="mt-10 grid grid-cols-1 md:grid-cols-3 gap-6 slide-up" style={{ animationDelay: '0.2s' }}>
        {[
          { icon: Zap, title: "AI-Powered", desc: "Smart recommendations" },
          { icon: Target, title: "Personalized", desc: "Tailored to your goals" },
          { icon: TrendingUp, title: "Track Progress", desc: "See your growth" }
        ].map((feature, i) => (
          <div key={i} className="text-center p-6 bg-white/60 backdrop-blur-sm rounded-2xl border border-gray-200">
            <feature.icon className="w-8 h-8 text-indigo-600 mx-auto mb-3" />
            <h4 className="font-bold text-gray-900 mb-1">{feature.title}</h4>
            <p className="text-sm text-gray-600">{feature.desc}</p>
          </div>
        ))}
      </div>
    </div>
  </div>
);

export default OnboardingScreen;