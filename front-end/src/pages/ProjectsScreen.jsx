import React from 'react';
import { Briefcase, Lock, CheckCircle, Rocket, Code, Database, Brain } from 'lucide-react';

/**
 * ProjectsScreen.jsx
 * Enhanced with better spacing and animations
 */
const ProjectsScreen = ({ goTo }) => (
  <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-orange-50 pt-32 pb-24 px-6">
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="text-center mb-16 fade-in">
        <div className="inline-block p-6 bg-gradient-to-br from-purple-600 to-pink-600 rounded-3xl mb-8 shadow-2xl hover:scale-110 transition-transform pulse-glow">
          <Rocket className="w-16 h-16 text-white" />
        </div>
        <h1 className="text-5xl md:text-6xl font-black mb-5 gradient-text">
          AI-Driven Projects
        </h1>
        <p className="text-xl md:text-2xl text-gray-600 max-w-2xl mx-auto">
          Build portfolio-ready projects tailored to your learning path
        </p>
      </div>

      {/* Projects Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        {[
          {
            title: 'Personal Portfolio Website',
            difficulty: 'Beginner',
            progress: 90,
            category: 'Frontend',
            emoji: '🌐',
            icon: Code,
            color: 'from-green-400 to-emerald-600',
            status: 'In Progress',
          },
          {
            title: 'RESTful API with Express',
            difficulty: 'Intermediate',
            progress: 45,
            category: 'Backend',
            emoji: '⚙️',
            icon: Database,
            color: 'from-indigo-400 to-purple-600',
            status: 'In Progress',
          },
          {
            title: 'Full-Stack MERN App',
            difficulty: 'Advanced',
            progress: 0,
            category: 'Full Stack',
            emoji: '🚀',
            icon: Rocket,
            color: 'from-pink-500 to-red-600',
            status: 'Not Started',
          },
          {
            title: 'AI Resume Analyzer',
            difficulty: 'Pro',
            progress: 0,
            category: 'Machine Learning',
            emoji: '🧠',
            icon: Brain,
            color: 'from-yellow-400 to-orange-600',
            status: 'Locked',
          },
        ].map((proj, i) => (
          <div
            key={i}
            className="bg-white rounded-3xl shadow-2xl border-2 border-gray-100 p-8 hover:shadow-[0_20px_60px_rgba(0,0,0,0.15)] transition-all duration-300 slide-up"
            style={{ animationDelay: `${i * 0.1}s` }}
          >
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-4">
                <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${proj.color} flex items-center justify-center text-white shadow-lg`}>
                  <proj.icon className="w-8 h-8" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-gray-900">{proj.title}</h3>
                  <p className="text-sm text-gray-500 mt-1">Difficulty: <span className="font-bold text-gray-900">{proj.difficulty}</span></p>
                </div>
              </div>
              <span
                className={`px-4 py-2 text-xs font-bold text-white rounded-full bg-gradient-to-r ${proj.color} shadow-md`}
              >
                {proj.category}
              </span>
            </div>

            <div className="flex items-center justify-between mb-3">
              <div className="text-sm text-gray-600 font-medium">
                Progress
              </div>
              <div className="text-lg font-black text-indigo-600">{proj.progress}%</div>
            </div>

            <div className="w-full bg-gray-200 rounded-full h-3 mb-6 overflow-hidden">
              <div
                className={`h-full rounded-full bg-gradient-to-r ${proj.color} shimmer transition-all duration-1000`}
                style={{ width: `${proj.progress}%` }}
              ></div>
            </div>

            <button
              className={`w-full py-4 font-bold rounded-2xl transition-all ${proj.status === 'Locked'
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:scale-105 shadow-lg hover:shadow-xl'
                }`}
            >
              {proj.status === 'Locked' ? (
                <div className="flex items-center justify-center gap-2">
                  <Lock className="w-5 h-5" /> Locked
                </div>
              ) : proj.progress === 0 ? (
                'Start Project →'
              ) : proj.progress < 100 ? (
                'Continue Project →'
              ) : (
                <div className="flex items-center justify-center gap-2">
                  <CheckCircle className="w-5 h-5 text-white" /> Completed
                </div>
              )}
            </button>
          </div>
        ))}
      </div>

      {/* CTA Card */}
      <div className="bg-gradient-to-r from-purple-600 via-pink-600 to-orange-500 text-white rounded-3xl p-12 shadow-2xl text-center slide-up relative overflow-hidden">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -right-10 -top-10 w-64 h-64 rounded-full bg-white/10 blur-3xl"></div>
          <div className="absolute -left-10 -bottom-10 w-64 h-64 rounded-full bg-white/10 blur-3xl"></div>
        </div>
        <div className="relative z-10">
          <h3 className="text-4xl font-black mb-5 flex items-center justify-center gap-3">
            <Rocket className="w-10 h-10" />
            🎯 Complete Projects. Build Your Legacy.
          </h3>
          <p className="text-xl opacity-95 mb-8 max-w-2xl mx-auto">
            Each project you complete brings you closer to becoming a certified Full Stack Developer.
          </p>
          <button
            onClick={() => goTo('opportunities')}
            className="bg-white text-purple-600 font-bold px-10 py-5 rounded-2xl hover:scale-105 transition-all shadow-xl text-lg"
          >
            Explore Job Opportunities →
          </button>
        </div>
      </div>
    </div>
  </div>
);

export default ProjectsScreen;