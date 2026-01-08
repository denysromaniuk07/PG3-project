import React, { useState } from "react";
import { TrendingUp, Bell, Settings, X, Menu } from "lucide-react";

/**
 * ScreenNav.jsx
 * Enhanced top navigation - FIXED: button text overflow
 */
const ScreenNav = ({ activeScreen, goTo, user }) => {
  const [menuOpen, setMenuOpen] = useState(false);

  // Shortened labels for better fit
  const navItems = [
    { id: "splash", label: "🌟", fullLabel: "Splash" },
    { id: "onboarding", label: "🚀", fullLabel: "Onboarding" },
    { id: "resume-analysis", label: "🔍", fullLabel: "Resume" },
    { id: "dashboard", label: "🏠", fullLabel: "Dashboard" },
    { id: "learning-path", label: "📚", fullLabel: "Learning" },
    { id: "course-detail", label: "📖", fullLabel: "Course" },
    { id: "projects", label: "💼", fullLabel: "Projects" },
    { id: "opportunities", label: "💰", fullLabel: "Jobs" },
    { id: "community", label: "👥", fullLabel: "Community" },
    { id: "profile", label: "👤", fullLabel: "Profile" },
    { id: "achievements", label: "🏆", fullLabel: "Awards" },
  ];

  return (
    <div className="fixed top-0 left-0 right-0 bg-white/95 backdrop-blur-md border-b border-gray-200 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto flex items-center justify-between px-6 py-4">
        {/* Logo */}
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => goTo("splash")}>
          <div className="w-11 h-11 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl flex items-center justify-center text-white shadow-lg hover:scale-110 transition-transform">
            <TrendingUp className="w-6 h-6" />
          </div>
          <div className="font-bold text-xl gradient-text hidden sm:block">SkillPath AI</div>
        </div>

        {/* Desktop nav - FIXED: using only emoji for compact display */}
        <div className="hidden lg:flex flex-1 gap-2 mx-6 justify-center">
          {navItems.map((s) => (
            <button
              key={s.id}
              onClick={() => goTo(s.id)}
              title={s.fullLabel}
              className={`w-12 h-12 rounded-xl text-2xl font-semibold transition-all flex items-center justify-center relative group
                ${activeScreen === s.id
                  ? "bg-gradient-to-r from-indigo-600 to-purple-600 shadow-lg scale-110"
                  : "bg-gray-50 hover:bg-gray-100 hover:scale-105"}`}
            >
              {s.label}
              {/* Tooltip */}
              <span className="absolute -bottom-10 left-1/2 -translate-x-1/2 px-3 py-1 bg-gray-900 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
                {s.fullLabel}
              </span>
            </button>
          ))}
        </div>

        {/* Right icons */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => goTo("dashboard")}
            className="p-2.5 rounded-xl hover:bg-gray-100 transition-all hover:scale-110 relative"
            title="Notifications"
          >
            <Bell className="w-5 h-5 text-gray-600" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>
          <button
            onClick={() => goTo("profile")}
            className="p-2.5 rounded-xl hover:bg-gray-100 transition-all hover:scale-110"
            title="Settings"
          >
            <Settings className="w-5 h-5 text-gray-600" />
          </button>

          {/* Avatar - Opens Profile */}
          {/* Avatar - Opens Profile */}
          <div
            onClick={() => goTo("profile")}
            className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center text-white font-bold shadow-md hover:scale-110 transition-transform cursor-pointer"
            title="My Profile"
          >
            {user && user.name ? user.name.charAt(0).toUpperCase() : 'P'}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="lg:hidden p-2.5 rounded-xl hover:bg-gray-100 transition-all"
          >
            {menuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile dropdown with animation */}
      <div
        className={`lg:hidden bg-white border-t border-gray-200 shadow-md overflow-hidden transition-all duration-300 ease-in-out
          ${menuOpen ? "max-h-screen opacity-100" : "max-h-0 opacity-0"}`}
      >
        <div className="flex flex-col p-3">
          {navItems.map((s) => (
            <button
              key={s.id}
              onClick={() => {
                goTo(s.id);
                setMenuOpen(false);
              }}
              className={`text-left w-full px-4 py-3 rounded-lg text-sm font-medium mb-1 transition-all flex items-center gap-3
                ${activeScreen === s.id
                  ? "bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"}`}
            >
              <span className="text-xl">{s.label}</span>
              <span>{s.fullLabel}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ScreenNav;