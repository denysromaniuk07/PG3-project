import React from 'react';
import { Briefcase, Search, MapPin, TrendingUp, Filter, ArrowLeft } from 'lucide-react';


const OpportunitiesScreen = ({ goTo }) => (
  <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 pt-32 pb-24 px-6">
    <div className="max-w-7xl mx-auto">
      <div className="text-center mb-16 fade-in">
        <div className="inline-block p-6 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-3xl mb-8 shadow-2xl hover:scale-110 transition-transform">
          <Briefcase className="w-16 h-16 text-white" />
        </div>
        <h1 className="text-5xl md:text-6xl font-black mb-5 gradient-text">
          AI Job Opportunities
        </h1>
        <p className="text-xl md:text-2xl text-gray-600 max-w-2xl mx-auto">
          Matched to your learning path and current skillset
        </p>
      </div>

      <div className="bg-white rounded-2xl shadow-lg border-2 border-gray-100 p-6 mb-12 slide-up flex items-center gap-4">
        <Search className="w-6 h-6 text-gray-400" />
        <input
          type="text"
          placeholder="Search for jobs, companies, or skills..."
          className="flex-1 outline-none text-lg"
        />
        <button className="px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-semibold hover:scale-105 transition-all flex items-center gap-2">
          <Filter className="w-5 h-5" />
          Filters
        </button>
      </div>

      <div className="bg-white rounded-3xl shadow-2xl border-2 border-gray-100 p-10 mb-12 slide-up" style={{ animationDelay: '0.2s' }}>
        <h2 className="text-3xl font-bold text-gray-900 mb-8 flex items-center gap-3">
          <TrendingUp className="w-7 h-7 text-green-500" />
          Recommended for You
        </h2>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {[
            {
              company: 'TechNova Labs',
              title: 'Junior Frontend Developer',
              match: 92,
              location: 'Remote • Europe',
              salary: '$1.2k – $2.5k/mo',
              skills: ['React', 'TypeScript', 'TailwindCSS'],
              emoji: '💻',
            },
            {
              company: 'NeuroLink Systems',
              title: 'AI Research Intern',
              match: 88,
              location: 'San Francisco, USA',
              salary: '$2k stipend',
              skills: ['Python', 'TensorFlow', 'Data Science'],
              emoji: '🧠',
            },
            {
              company: 'SkyCloud Global',
              title: 'Backend Engineer',
              match: 76,
              location: 'Hybrid • Berlin',
              salary: '$3k – $4k/mo',
              skills: ['Node.js', 'MongoDB', 'Express'],
              emoji: '☁️',
            },
            {
              company: 'NextWave Startups',
              title: 'Full Stack Developer',
              match: 85,
              location: 'Remote',
              salary: '$2.8k – $3.5k/mo',
              skills: ['MERN', 'API', 'Docker'],
              emoji: '🚀',
            },
          ].map((job, i) => (
            <div
              key={i}
              className="p-8 border-2 border-gray-200 rounded-3xl hover:border-blue-300 hover:shadow-2xl transition-all duration-300 group cursor-pointer"
            >
              <div className="flex justify-between items-start mb-5">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-blue-100 to-indigo-100 flex items-center justify-center text-2xl shadow-md group-hover:scale-110 transition-transform">
                      {job.emoji}
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold text-gray-900">{job.title}</h3>
                      <p className="text-gray-600 font-medium">{job.company}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 text-sm text-gray-500 mt-2">
                    <MapPin className="w-4 h-4" /> {job.location}
                  </div>
                </div>
                <div className="text-right">
                  <div className="px-4 py-2 bg-green-100 text-green-700 rounded-full font-bold text-sm mb-2">
                    {job.match}% Match
                  </div>
                </div>
              </div>

              <div className="flex flex-wrap gap-2 mb-6">
                {job.skills.map((skill, s) => (
                  <span
                    key={s}
                    className="px-3 py-1.5 bg-indigo-100 text-indigo-700 text-sm font-semibold rounded-lg"
                  >
                    {skill}
                  </span>
                ))}
              </div>

              <div className="flex justify-between items-center pt-4 border-t border-gray-200">
                <div className="text-gray-900 font-bold text-lg">{job.salary}</div>
                <button
                  onClick={() => goTo('profile')}
                  className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 rounded-xl font-bold hover:scale-105 transition-all shadow-lg"
                >
                  Apply Now →
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white rounded-3xl p-12 shadow-2xl slide-up relative overflow-hidden">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -right-10 -top-10 w-64 h-64 rounded-full bg-white/10 blur-3xl"></div>
        </div>
        <div className="relative z-10">
          <h3 className="text-4xl font-black mb-5">🚀 Ready to Apply?</h3>
          <p className="text-xl opacity-95 mb-8 max-w-2xl">
            Update your profile and let AI boost your chances with auto-tailored cover letters.
          </p>
          <button
            onClick={() => goTo('community')}
            className="bg-white text-blue-600 font-bold px-10 py-5 rounded-2xl hover:scale-105 transition-all shadow-xl text-lg"
          >
            Go to Community →
          </button>
        </div>
      </div>
    </div>
  </div>
);

export default OpportunitiesScreen;