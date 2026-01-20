import React from 'react';
import { Trophy, Award, Star, Medal, Target, Zap, ArrowLeft } from 'lucide-react';


const AchievementsScreen = ({ goTo, achievements }) => (
  <div className="min-h-screen bg-gradient-to-br from-yellow-50 via-orange-50 to-red-50 pt-32 pb-24">
    <div className="max-w-6xl mx-auto px-6 lg:px-8">
      <div className="flex items-center justify-between mb-12 fade-in">
        <div>
          <h1 className="text-5xl md:text-6xl font-black mb-3 gradient-text">
            🏆 Achievements
          </h1>
          <p className="text-xl text-gray-600">Your journey milestones and accomplishments</p>
        </div>
        <button
          onClick={() => goTo("dashboard")}
          className="px-5 py-3 rounded-xl border-2 border-gray-200 hover:bg-gray-100 hover:border-gray-300 transition-all font-semibold flex items-center gap-2"
        >
          <ArrowLeft className="w-4 h-4" />
          Back
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12 slide-up">
        {[
          { label: "Total Achievements", value: achievements?.length || 3, icon: Trophy, color: "from-yellow-400 to-orange-500" },
          { label: "Points Earned", value: "1,250", icon: Star, color: "from-purple-400 to-pink-500" },
          { label: "Rank", value: "#47", icon: Medal, color: "from-blue-400 to-indigo-500" },
          { label: "Streak", value: "18 days", icon: Zap, color: "from-green-400 to-teal-500" }
        ].map((stat, i) => (
          <div
            key={i}
            className="bg-white rounded-2xl p-6 border-2 border-gray-100 shadow-lg hover-lift"
            style={{ animationDelay: `${i * 0.1}s` }}
          >
            <div className={`w-14 h-14 rounded-xl bg-gradient-to-r ${stat.color} flex items-center justify-center text-white mb-4`}>
              <stat.icon className="w-7 h-7" />
            </div>
            <div className="text-3xl font-black mb-1">{stat.value}</div>
            <div className="text-sm text-gray-600 font-medium">{stat.label}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 slide-up" style={{ animationDelay: '0.4s' }}>
        {achievements?.map((a, idx) => (
          <div
            key={a.id}
            className="bg-white p-8 rounded-3xl border-2 border-gray-100 shadow-lg hover:shadow-2xl hover:border-yellow-200 transition-all duration-300 group cursor-pointer"
          >
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-yellow-400 to-orange-500 flex items-center justify-center mb-5 group-hover:scale-110 transition-transform shadow-lg">
              <a.icon className="w-8 h-8 text-white" />
            </div>
            <div className="font-bold text-xl mb-2 text-gray-900">{a.title}</div>
            <div className="text-sm text-gray-500 flex items-center gap-2">
              <Award className="w-4 h-4" />
              Earned on {a.date}
            </div>
          </div>
        ))}

        <div className="bg-gray-50 p-8 rounded-3xl border-2 border-dashed border-gray-300 shadow-lg opacity-60">
          <div className="w-16 h-16 rounded-2xl bg-gray-200 flex items-center justify-center mb-5">
            <Target className="w-8 h-8 text-gray-400" />
          </div>
          <div className="font-bold text-xl mb-2 text-gray-500">??? Locked</div>
          <div className="text-sm text-gray-400">Complete 10 projects to unlock</div>
        </div>
      </div>

      <div className="mt-12 bg-gradient-to-r from-yellow-400 via-orange-500 to-red-500 rounded-3xl p-10 text-white shadow-2xl slide-up relative overflow-hidden" style={{ animationDelay: '0.6s' }}>
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -right-10 -top-10 w-64 h-64 rounded-full bg-white/10 blur-3xl"></div>
        </div>
        <div className="relative z-10">
          <h3 className="text-3xl font-black mb-4 flex items-center gap-3">
            <Trophy className="w-8 h-8" />
            Keep Going!
          </h3>
          <p className="text-lg opacity-95 mb-6">
            You're on fire! Complete 2 more courses to unlock the "Learning Champion" badge.
          </p>
          <button
            onClick={() => goTo('learning-path')}
            className="bg-white text-orange-600 px-8 py-4 rounded-2xl font-bold hover:scale-105 transition-all shadow-xl"
          >
            Continue Learning →
          </button>
        </div>
      </div>
    </div>
  </div>
);

export default AchievementsScreen;