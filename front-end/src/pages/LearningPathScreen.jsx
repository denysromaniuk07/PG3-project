import React from 'react';
import { BookOpen, Rocket, Clock, ChevronRight, Play, TrendingUp } from 'lucide-react';

const LearningPathScreen = ({ goTo }) => (
  <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 pt-32 pb-24 px-6">
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="text-center mb-16 fade-in">
        <div className="inline-block p-6 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-3xl mb-8 shadow-2xl hover:scale-110 transition-transform">
          <BookOpen className="w-16 h-16 text-white" />
        </div>
        <h1 className="text-5xl md:text-6xl font-black mb-5 gradient-text">
          Your Learning Path
        </h1>
        <p className="text-xl md:text-2xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
          Personalized roadmap curated by AI based on your skills & goals
        </p>
      </div>

      <div className="bg-white rounded-3xl shadow-xl border border-gray-200 p-10 mb-10">
        <h2 className="text-3xl font-bold text-gray-900 mb-8 flex items-center gap-3">
          <Rocket className="w-7 h-7 text-indigo-600" />
          Recommended Learning Modules
        </h2>

        <div className="space-y-6">
          {[
            {
              title: 'TypeScript Fundamentals',
              description: 'Strongly typed JavaScript for scalable projects',
              progress: 40,
              duration: '2h 15m',
              emoji: '💡',
              next: 'Advanced Type Inference'
            },
            {
              title: 'Node.js & Express API Development',
              description: 'Build backend APIs using Node.js and Express',
              progress: 20,
              duration: '3h 30m',
              emoji: '🧩',
              next: 'RESTful Authentication'
            },
            {
              title: 'MongoDB Masterclass',
              description: 'Learn NoSQL database design and querying',
              progress: 0,
              duration: '4h',
              emoji: '🍃',
              next: 'Aggregation Pipelines'
            }
          ].map((module, i) => (
            <div
              key={i}
              className="border-2 border-gray-200 rounded-2xl p-8 hover:border-indigo-300 hover:shadow-xl transition-all cursor-pointer group"
            >
              <div className="flex justify-between items-start mb-4">
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-2xl">{module.emoji}</span>
                    <h3 className="text-xl font-bold text-gray-900">{module.title}</h3>
                  </div>
                  <p className="text-gray-600 mb-2">{module.description}</p>
                  <div className="flex items-center gap-3 text-sm text-gray-500">
                    <Clock className="w-4 h-4" /> {module.duration}
                    <ChevronRight className="w-4 h-4" /> Next: {module.next}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-black text-indigo-600">{module.progress}%</div>
                  <button
                    onClick={() => goTo('course-detail')}
                    className="mt-2 p-2 bg-indigo-100 rounded-lg group-hover:bg-indigo-600 transition-all"
                  >
                    <Play className="w-4 h-4 text-indigo-600 group-hover:text-white" />
                  </button>
                </div>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full h-3 transition-all"
                  style={{ width: `${module.progress}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-3xl p-10 text-white shadow-2xl">
        <h3 className="text-3xl font-bold mb-4">🔥 Next Step in Your Journey</h3>
        <p className="text-lg opacity-90 mb-6">
          You’re 40% through your current learning path. Keep it up and unlock your next project challenge!
        </p>
        <button
          onClick={() => goTo('projects')}
          className="bg-white text-indigo-600 px-8 py-4 rounded-2xl font-bold hover:scale-105 transition-all"
        >
          Start Project →
        </button>
      </div>
    </div>
  </div>
);

export default LearningPathScreen;