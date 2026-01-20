import React from 'react';
import { Users, Star, MessageSquare, Heart, Send, TrendingUp, ArrowLeft } from 'lucide-react';


const CommunityScreen = ({ goTo }) => (
  <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-indigo-50 pt-32 pb-24 px-6">
    <div className="max-w-7xl mx-auto">
      <div className="text-center mb-16 fade-in">
        <div className="inline-block p-6 bg-gradient-to-br from-purple-600 to-indigo-600 rounded-3xl mb-8 shadow-2xl hover:scale-110 transition-transform">
          <Users className="w-16 h-16 text-white" />
        </div>
        <h1 className="text-5xl md:text-6xl font-black mb-5 gradient-text">
          AI Developer Community
        </h1>
        <p className="text-xl md:text-2xl text-gray-600 max-w-2xl mx-auto">
          Connect, learn, and grow with other innovators worldwide
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-10 mb-12">
        <div className="lg:col-span-2 space-y-6">
          {[
            {
              user: "Sophia Dev",
              avatar: "🧑‍💻",
              title: "How do I optimize React performance with hooks?",
              content: "I'm struggling with re-rendering issues in my dashboard. Any pro tips on memoization or useCallback?",
              likes: 42,
              comments: 8,
              time: "2h ago",
            },
            {
              user: "Artem AI",
              avatar: "🤖",
              title: "AI-powered resume scoring — my approach",
              content: "I built a small GPT-4 API that gives a 0–100 score to resumes. Would love feedback on my weighting algorithm.",
              likes: 61,
              comments: 14,
              time: "5h ago",
            },
            {
              user: "Lina Codes",
              avatar: "👩‍🎨",
              title: "TailwindCSS design tips",
              content: "Sharing my color palette combos for dashboard aesthetics. Hope it helps others building AI apps 💜",
              likes: 89,
              comments: 23,
              time: "1d ago",
            },
          ].map((post, i) => (
            <div
              key={i}
              className="bg-white p-8 border-2 border-gray-100 rounded-3xl hover:shadow-2xl hover:border-purple-200 transition-all duration-300 slide-up"
              style={{ animationDelay: `${i * 0.1}s` }}
            >
              <div className="flex items-center gap-4 mb-5">
                <div className="w-14 h-14 rounded-full bg-gradient-to-br from-purple-400 to-indigo-500 flex items-center justify-center text-2xl shadow-lg">
                  {post.avatar}
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-lg text-gray-900">{post.user}</h3>
                  <p className="text-sm text-gray-500">{post.time}</p>
                </div>
              </div>
              <h4 className="text-xl font-bold text-indigo-700 mb-3">{post.title}</h4>
              <p className="text-gray-700 mb-5 leading-relaxed">{post.content}</p>
              <div className="flex items-center gap-8 text-gray-500 text-sm pt-4 border-t border-gray-100">
                <button className="flex items-center gap-2 hover:text-rose-500 transition-colors">
                  <Heart className="w-5 h-5" />
                  <span className="font-semibold">{post.likes}</span>
                </button>
                <button className="flex items-center gap-2 hover:text-indigo-600 transition-colors">
                  <MessageSquare className="w-5 h-5" />
                  <span className="font-semibold">{post.comments}</span>
                </button>
                <button className="flex items-center gap-2 hover:text-purple-600 transition-colors ml-auto">
                  <Send className="w-5 h-5" />
                  Share
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="space-y-6">
          <div className="bg-white rounded-3xl p-8 shadow-lg border-2 border-gray-100 slide-up" style={{ animationDelay: '0.3s' }}>
            <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <Star className="w-6 h-6 text-yellow-500" /> Top Mentors
            </h3>
            {[
              { name: "Emma Stone", role: "Frontend Guru", emoji: "🎨" },
              { name: "Liam Patel", role: "Backend Mentor", emoji: "⚙️" },
              { name: "Noah AI", role: "ML Expert", emoji: "🧠" },
            ].map((m, i) => (
              <div
                key={i}
                className="flex items-center justify-between p-4 rounded-xl hover:bg-purple-50 transition-all mb-3"
              >
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-purple-400 to-indigo-500 flex items-center justify-center text-xl shadow-md">
                    {m.emoji}
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">{m.name}</h4>
                    <p className="text-sm text-gray-500">{m.role}</p>
                  </div>
                </div>
                <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-semibold hover:bg-indigo-700 transition-colors">
                  Message
                </button>
              </div>
            ))}
          </div>

          <div className="bg-gradient-to-br from-purple-600 to-indigo-600 text-white p-8 rounded-3xl shadow-2xl slide-up" style={{ animationDelay: '0.4s' }}>
            <h3 className="text-2xl font-bold mb-4 flex items-center gap-2">
              🤖 Ask AI Mentor
            </h3>
            <p className="opacity-95 mb-6 leading-relaxed">
              Need coding advice or design feedback? Get instant insights powered by AI.
            </p>
            <button
              onClick={() => goTo('profile')}
              className="w-full bg-white text-purple-600 font-bold px-6 py-4 rounded-xl hover:scale-105 transition-all shadow-lg"
            >
              Ask AI →
            </button>
          </div>

          <div className="bg-white rounded-3xl p-8 shadow-lg border-2 border-gray-100 slide-up" style={{ animationDelay: '0.5s' }}>
            <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <TrendingUp className="w-6 h-6 text-green-500" /> Trending
            </h3>
            {["#ReactHooks", "#AIResume", "#TailwindCSS", "#WebDev2025"].map((tag, i) => (
              <div key={i} className="mb-3 px-4 py-3 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors cursor-pointer">
                <span className="font-semibold text-purple-700">{tag}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-gradient-to-r from-purple-600 via-indigo-600 to-blue-500 text-white rounded-3xl p-12 shadow-2xl text-center slide-up relative overflow-hidden">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -right-10 -top-10 w-64 h-64 rounded-full bg-white/10 blur-3xl"></div>
        </div>
        <div className="relative z-10">
          <h3 className="text-4xl font-black mb-5">💬 Keep Learning. Keep Sharing.</h3>
          <p className="text-xl opacity-95 mb-8 max-w-2xl mx-auto">
            Collaboration turns knowledge into mastery. Stay active and grow your network!
          </p>
          <button
            onClick={() => goTo('profile')}
            className="bg-white text-purple-600 font-bold px-10 py-5 rounded-2xl hover:scale-105 transition-all shadow-xl text-lg"
          >
            View My Profile →
          </button>
        </div>
      </div>
    </div>
  </div>
);

export default CommunityScreen;