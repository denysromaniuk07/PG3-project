import React from 'react';
import { Home, Star, Trophy, Zap, Users, BookOpen, Briefcase, Rocket, MessageSquare, TrendingUp, Award } from 'lucide-react';
import ProgressBar from '../components/ProgressBar';


const DashboardScreen = ({ goTo, profile, learningCourses }) => (
  <div className="min-h-screen bg-gradient-to-br from-gray-50 via-indigo-50/30 to-purple-50/30 pt-32 pb-24">
    <div className="max-w-7xl mx-auto px-6 lg:px-8">
      <div className="mb-12 fade-in">
        <h1 className="text-5xl md:text-6xl font-black mb-3 gradient-text">
          Welcome back, {profile.name.split(" ")[0]}! 👋
        </h1>
        <p className="text-xl text-gray-600 flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-green-500" />
          You are 67% through your Full Stack Developer path
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {[{ label: "Skills Acquired", value: 12, icon: Star, color: "from-yellow-400 to-orange-500" },
        { label: "Projects Done", value: 5, icon: Trophy, color: "from-purple-400 to-pink-500" },
        { label: "Day Streak", value: 18, icon: Zap, color: "from-blue-400 to-indigo-500" },
        { label: "Network", value: 47, icon: Users, color: "from-green-400 to-teal-500" }].map((s, i) => (
          <div key={i} className="bg-white rounded-2xl p-5 border border-gray-200 shadow-sm">
            <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${s.color} flex items-center justify-center text-white mb-3`}>
              <s.icon className="w-5 h-5" />
            </div>
            <div className="text-2xl font-black">{s.value}</div>
            <div className="text-sm text-gray-600">{s.label}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-white rounded-3xl p-8 shadow-lg border border-gray-100 slide-up" style={{ animationDelay: '0.4s' }}>
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-2xl font-bold flex items-center gap-2">
              <BookOpen className="w-6 h-6 text-indigo-600" />
              Continue Learning
            </h3>
            <button
              onClick={() => goTo("learning-path")}
              className="text-indigo-600 font-bold hover:text-indigo-700 transition-colors flex items-center gap-1 group"
            >
              View All
              <span className="group-hover:translate-x-1 transition-transform inline-block">→</span>
            </button>
          </div>

          <div className="space-y-5">
            {learningCourses.map((c, idx) => (
              <div
                key={c.id}
                className="border-2 border-gray-100 rounded-2xl p-5 hover:border-indigo-200 hover:shadow-xl transition-all duration-300 flex items-center justify-between group cursor-pointer"
                onClick={() => goTo("course-detail", { course: c })}
              >
                <div className="flex items-center gap-5 flex-1">
                  <div className={`w-16 h-16 rounded-xl bg-gradient-to-r ${c.color} flex items-center justify-center text-white shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                    <BookOpen className="w-7 h-7" />
                  </div>
                  <div className="flex-1">
                    <div className="font-bold text-lg mb-1 text-gray-900">{c.title}</div>
                    <div className="text-sm text-gray-500 flex items-center gap-3">
                      <span>📚 {c.modules ?? "—"} modules</span>
                      <span>•</span>
                      <span>⏱️ {c.time ?? "—"}</span>
                    </div>
                  </div>
                </div>
                <div className="w-52">
                  <div className="flex items-center justify-between mb-3">
                    <div className="text-sm font-bold text-indigo-600">{c.progress}%</div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        goTo("course-detail", { course: c });
                      }}
                      className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors"
                    >
                      Continue
                    </button>
                  </div>
                  <ProgressBar value={c.progress} gradient={c.color} />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-3xl p-8 shadow-lg border border-gray-100 slide-up" style={{ animationDelay: '0.5s' }}>
          <h3 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <Zap className="w-6 h-6 text-yellow-500" />
            Quick Actions
          </h3>
          <div className="space-y-4">
            <button
              onClick={() => goTo("opportunities")}
              className="w-full p-4 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-xl flex items-center justify-center gap-2 font-semibold hover:scale-105 hover:shadow-xl transition-all duration-300"
            >
              <Briefcase className="w-5 h-5" />
              Find Jobs
            </button>
            <button
              onClick={() => goTo("projects")}
              className="w-full p-4 bg-gradient-to-r from-green-400 to-teal-500 text-white rounded-xl flex items-center justify-center gap-2 font-semibold hover:scale-105 hover:shadow-xl transition-all duration-300"
            >
              <Rocket className="w-5 h-5" />
              Start Project
            </button>
            <button
              onClick={() => goTo("community")}
              className="w-full p-4 border-2 border-gray-200 rounded-xl flex items-center justify-center gap-2 text-gray-700 font-semibold hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-700 transition-all duration-300"
            >
              <MessageSquare className="w-5 h-5" />
              Community
            </button>
          </div>

          <div className="mt-8 p-5 bg-gradient-to-br from-yellow-50 to-orange-50 rounded-2xl border border-yellow-200">
            <div className="flex items-center gap-3 mb-3">
              <Award className="w-6 h-6 text-yellow-600" />
              <h4 className="font-bold text-gray-900">Next Achievement</h4>
            </div>
            <p className="text-sm text-gray-600 mb-3">Complete 2 more projects to unlock "Project Master" badge!</p>
            <div className="w-full bg-yellow-200 h-2 rounded-full overflow-hidden">
              <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '60%' }}></div>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-10 bg-white rounded-3xl p-8 shadow-lg border border-gray-100 slide-up" style={{ animationDelay: '0.6s' }}>
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-2xl font-bold flex items-center gap-2">
            <Briefcase className="w-6 h-6 text-indigo-600" />
            New Opportunities
          </h3>
          <button
            onClick={() => goTo("opportunities")}
            className="text-indigo-600 font-bold hover:text-indigo-700 transition-colors flex items-center gap-1 group"
          >
            View All
            <span className="group-hover:translate-x-1 transition-transform inline-block">→</span>
          </button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            { company: "TechCorp", role: "Frontend Intern", match: 92, type: "Internship", salary: "$800", emoji: "💼" },
            { company: "StartupXYZ", role: "UI/UX Project", match: 88, type: "Freelance", salary: "$600", emoji: "🎨" },
            { company: "DevAgency", role: "React Dev", match: 85, type: "Contract", salary: "$1.2k", emoji: "⚛️" }
          ].map((o, i) => (
            <div
              key={i}
              className="border-2 border-gray-100 rounded-2xl p-6 hover:border-indigo-200 hover:shadow-xl transition-all duration-300 cursor-pointer group"
              onClick={() => goTo("opportunities")}
            >
              <div className="flex items-center justify-between mb-4">
                <div className="text-sm px-3 py-1 bg-green-100 text-green-700 rounded-full font-bold">
                  {o.match}% Match
                </div>
                <div className="text-3xl group-hover:scale-110 transition-transform">{o.emoji}</div>
              </div>
              <div className="font-bold text-lg mb-1 text-gray-900">{o.role}</div>
              <div className="text-sm text-gray-500 mb-4">{o.company}</div>
              <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                <div className="text-xs px-3 py-1 bg-indigo-50 text-indigo-600 rounded-lg font-semibold">
                  {o.type}
                </div>
                <div className="font-bold text-lg text-gray-900">{o.salary}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
);

export default DashboardScreen;