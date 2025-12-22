import React from 'react';
import { TrendingUp, Sparkles, Rocket, Zap } from 'lucide-react';

/**
 * SplashScreen.jsx
 * Enhanced with modern animations and better spacing
 */
const SplashScreen = ({ goTo }) => (
  <div className="min-h-screen animated-gradient flex items-center justify-center p-6 pt-28 pb-12 relative overflow-hidden">
    {/* Animated Background Elements */}
    <div className="absolute inset-0 overflow-hidden">
      <div className="absolute -left-24 -top-24 w-96 h-96 rounded-full bg-white/10 blur-3xl animate-pulse"></div>
      <div className="absolute right-10 bottom-10 w-80 h-80 rounded-full bg-white/15 blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
      <div className="absolute left-1/2 top-1/3 w-64 h-64 rounded-full bg-white/5 blur-2xl animate-pulse" style={{ animationDelay: '2s' }} />
    </div>

    {/* Floating Icons */}
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      <Sparkles className="absolute top-20 left-10 w-6 h-6 text-white/30 animate-pulse" style={{ animationDelay: '0.5s' }} />
      <Rocket className="absolute top-40 right-20 w-8 h-8 text-white/20 animate-pulse" style={{ animationDelay: '1.5s' }} />
      <Zap className="absolute bottom-32 left-1/4 w-7 h-7 text-white/25 animate-pulse" style={{ animationDelay: '2.5s' }} />
    </div>

    {/* Main Content */}
    <div className="relative z-10 text-center max-w-4xl mx-auto px-4 fade-in">
      {/* Logo with Animation */}
      <div className="mb-10 inline-block slide-up">
        <div className="w-32 h-32 bg-white rounded-3xl flex items-center justify-center mb-8 shadow-2xl hover:scale-110 transition-transform duration-500 pulse-glow">
          <TrendingUp className="w-16 h-16 text-indigo-600" />
        </div>
      </div>

      {/* Title with Staggered Animation */}
      <h1 className="text-6xl md:text-8xl font-black text-white mb-6 tracking-tight slide-up" style={{ animationDelay: '0.1s' }}>
        SkillPath AI
      </h1>

      {/* Subtitle */}
      <p className="text-xl md:text-3xl text-white/95 mb-4 font-medium slide-up leading-relaxed max-w-3xl mx-auto" style={{ animationDelay: '0.2s' }}>
        Transform your career with personalized AI-guided learning and projects
      </p>

      {/* Features List */}
      <div className="flex flex-wrap justify-center gap-4 mb-12 slide-up" style={{ animationDelay: '0.3s' }}>
        <div className="glass px-4 py-2 rounded-full text-white/90 text-sm font-medium">
          🎯 Personalized Learning
        </div>
        <div className="glass px-4 py-2 rounded-full text-white/90 text-sm font-medium">
          🚀 Real Projects
        </div>
        <div className="glass px-4 py-2 rounded-full text-white/90 text-sm font-medium">
          💼 Career Opportunities
        </div>
      </div>

      {/* CTA Buttons */}
      <div className="flex flex-col sm:flex-row justify-center gap-5 slide-up" style={{ animationDelay: '0.4s' }}>
        <button
          onClick={() => goTo("onboarding")}
          className="group px-10 py-5 bg-white text-indigo-600 rounded-2xl font-bold text-lg shadow-2xl hover:scale-105 hover:shadow-[0_20px_60px_rgba(255,255,255,0.3)] transition-all duration-300"
        >
          <span className="flex items-center justify-center gap-2">
            Get Started
            <Rocket className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </span>
        </button>
        <button
          onClick={() => goTo("dashboard")}
          className="px-8 py-5 glass text-white rounded-2xl font-bold text-lg border-2 border-white/30 hover:bg-white/30 hover:border-white/50 transition-all duration-300"
        >
          Explore Dashboard
        </button>
      </div>

      {/* Bottom Info */}
      <p className="mt-12 text-white/70 text-sm slide-up" style={{ animationDelay: '0.5s' }}>
        Join 10,000+ learners advancing their careers
      </p>
    </div>
  </div>
);

export default SplashScreen;