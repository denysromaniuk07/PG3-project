import React from 'react';
import { Play, BookOpen, FileText, CheckCircle, Clock, ArrowLeft, Award, TrendingUp } from 'lucide-react';


const CourseDetailScreen = ({ goTo }) => (
  <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 pt-32 pb-24 px-6">
    <div className="max-w-6xl mx-auto">
      <div className="mb-12 flex items-center justify-between fade-in">
        <div className="flex items-center gap-5">
          <div className="p-5 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-3xl shadow-2xl hover:scale-110 transition-transform pulse-glow">
            <Play className="w-10 h-10 text-white" />
          </div>
          <div>
            <h1 className="text-4xl md:text-5xl font-black text-gray-900 mb-2">React Hooks Deep Dive</h1>
            <p className="text-lg text-gray-600">6 modules • Intermediate • 4h 20m</p>
          </div>
        </div>
        <button
          onClick={() => goTo('learning-path')}
          className="px-5 py-3 rounded-xl border-2 border-gray-200 hover:bg-gray-100 hover:border-gray-300 transition-all font-semibold flex items-center gap-2"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Path
        </button>
      </div>

      <div className="bg-white rounded-3xl shadow-2xl overflow-hidden mb-12 border-2 border-gray-100 slide-up">
        <div className="relative bg-gradient-to-br from-gray-900 to-gray-800 aspect-video flex items-center justify-center group">
          <div className="absolute inset-0 bg-gradient-to-b from-black/40 to-black/60"></div>
          <Play className="w-24 h-24 text-white opacity-90 group-hover:opacity-100 group-hover:scale-110 cursor-pointer transition-all" />
          <div className="absolute bottom-6 left-6 glass text-white px-5 py-3 rounded-xl text-sm font-semibold">
            📚 Lesson 1: Understanding useState
          </div>
          <div className="absolute top-6 right-6 bg-green-500 text-white px-4 py-2 rounded-full text-sm font-bold">
            75% Complete
          </div>
        </div>

        <div className="p-10">
          <h2 className="text-3xl font-bold text-gray-900 mb-6 flex items-center gap-3">
            <BookOpen className="w-7 h-7 text-indigo-600" />
            Course Overview
          </h2>
          <p className="text-gray-700 leading-relaxed text-lg mb-8">
            This course dives deep into React Hooks — a revolutionary way to use state and lifecycle features without writing a class.
            You'll learn how to structure components efficiently, manage global state, and optimize performance using advanced techniques.
          </p>

          <div className="border-t-2 border-gray-200 pt-10">
            <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <FileText className="w-6 h-6 text-indigo-600" /> Course Modules
            </h3>
            <div className="space-y-5">
              {[
                { title: 'useState & useEffect Basics', time: '45m', completed: true },
                { title: 'useReducer & State Management', time: '55m', completed: true },
                { title: 'Custom Hooks & Best Practices', time: '1h 10m', completed: false },
                { title: 'Performance Optimization with useMemo', time: '50m', completed: false },
                { title: 'Integrating Context API with Hooks', time: '1h 40m', completed: false },
              ].map((mod, i) => (
                <div
                  key={i}
                  className={`flex items-center justify-between p-6 border-2 rounded-2xl transition-all cursor-pointer group ${mod.completed
                      ? 'border-green-200 bg-green-50 hover:shadow-lg'
                      : 'border-gray-200 hover:border-indigo-300 hover:shadow-xl'
                    }`}
                >
                  <div className="flex items-center gap-4">
                    {mod.completed ? (
                      <CheckCircle className="w-7 h-7 text-green-600" />
                    ) : (
                      <Clock className="w-7 h-7 text-indigo-600" />
                    )}
                    <div>
                      <h4 className="font-bold text-lg text-gray-900">{mod.title}</h4>
                      <p className="text-sm text-gray-500 mt-1">⏱️ {mod.time}</p>
                    </div>
                  </div>
                  <button
                    className={`px-6 py-3 rounded-xl font-bold text-sm transition-all ${mod.completed
                        ? 'bg-green-600 text-white cursor-default'
                        : 'bg-indigo-600 text-white hover:bg-indigo-700 hover:scale-105'
                      }`}
                  >
                    {mod.completed ? '✓ Done' : 'Start →'}
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-500 text-white rounded-3xl p-12 shadow-2xl slide-up relative overflow-hidden">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -right-10 -top-10 w-64 h-64 rounded-full bg-white/10 blur-3xl"></div>
          <div className="absolute -left-10 -bottom-10 w-64 h-64 rounded-full bg-white/10 blur-3xl"></div>
        </div>
        <div className="relative z-10">
          <h3 className="text-4xl font-black mb-5 flex items-center gap-3">
            <Award className="w-10 h-10" />
            🎯 Next Challenge Awaits
          </h3>
          <p className="text-xl opacity-95 mb-8 leading-relaxed max-w-2xl">
            Complete all modules to unlock a hands-on React project and earn your SkillPath Badge.
          </p>
          <button
            onClick={() => goTo('projects')}
            className="bg-white text-indigo-600 font-bold px-10 py-5 rounded-2xl hover:scale-105 hover:shadow-2xl transition-all text-lg flex items-center gap-2"
          >
            Continue to Project
            <TrendingUp className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  </div>
);

export default CourseDetailScreen;