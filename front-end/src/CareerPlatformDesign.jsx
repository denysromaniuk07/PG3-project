import React, { useState } from "react";
import { Routes, Route, useNavigate, useLocation, Navigate } from 'react-router-dom';
import { Home, BookOpen, Briefcase, Users, User, ArrowLeft } from "lucide-react";

// Components
import ScreenNav from "./components/ScreenNav";
import ProtectedRoute from "./components/ProtectedRoute";

// Screens
import SplashScreen from "./pages/SplashScreen";
import LoginPage from "./pages/LoginPage";
import OnboardingScreen from "./pages/OnboardingScreen";
import ResumeAnalysisScreen from "./pages/ResumeAnalysisScreen";
import DashboardScreen from "./pages/DashboardScreen";
import LearningPathScreen from "./pages/LearningPathScreen";
import CourseDetailScreen from "./pages/CourseDetailScreen";
import ProjectsScreen from "./pages/ProjectsScreen";
import OpportunitiesScreen from "./pages/OpportunitiesScreen";
import CommunityScreen from "./pages/CommunityScreen";
import ProfileScreen from "./pages/ProfileScreen";
import AchievementsScreen from "./pages/AchievementsScreen";

/**
 * CareerPlatformDesign.jsx
 * Головний компонент з логікою стану та перемиканням екранів.
 */

const CareerPlatformDesign = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // --- Global State ---
  const [user, setUser] = useState(null); // Auth State
  const [selectedCourse, setSelectedCourse] = useState(null);

  // Default values for new profiles
  const defaultProfile = {
    name: "New User",
    title: "Aspiring Developer",
    location: "Unknown",
    bio: "Ready to learn!",
    github: "",
    linkedin: "",
    email: "",
    telegram: "",
  };

  const [profile, setProfile] = useState(defaultProfile);
  const [achievements] = useState([
    { id: 1, title: "First Project", date: "2025-03-10", icon: ArrowLeft },
    { id: 2, title: "100% Course Completion", date: "2025-07-21", icon: ArrowLeft },
    { id: 3, title: "Streak: 30 days", date: "2025-10-01", icon: ArrowLeft },
  ]);

  // Auth Handlers
  const handleLogin = (userData) => {
    setUser(userData);
    // Update profile with user data if provided (e.g. from registration)
    if (userData) {
      setProfile({
        ...defaultProfile,
        ...userData,
        email: userData.email || defaultProfile.email,
        name: userData.name || defaultProfile.name
      });
    }
    navigate('/dashboard');
  };

  const handleLogout = () => {
    setUser(null);
    setProfile(defaultProfile);
    navigate('/');
  };

  const handleUpdateProfile = (updatedData) => {
    setProfile(updatedData);
    // Optionally connect to backend here
  };

  // Данні для Dashboard/LearningPath
  const learningCourses = [
    { id: "c1", title: "React Hooks Deep Dive", progress: 75, modules: 8, time: "4h", color: "from-indigo-500 to-purple-500" },
    { id: "c2", title: "TypeScript for JS Devs", progress: 40, modules: 6, time: "6h", color: "from-green-400 to-teal-500" },
    { id: "c3", title: "Node.js & Express", progress: 20, modules: 5, time: "5h", color: "from-yellow-400 to-orange-400" },
  ];

  // Determine active screen from URL for navigation highlighting
  const getActiveScreen = () => {
    const path = location.pathname.substring(1); // remove leading /
    if (path === "") return "splash";
    return path;
  };

  const activeScreen = getActiveScreen();

  // Helper for backward compatibility with existing components calling goTo('screenName')
  const goTo = (screen, opts = {}) => {
    if (opts.course) setSelectedCourse(opts.course);

    if (screen === 'splash') {
      navigate('/');
    } else if (screen === 'login') {
      navigate('/login');
    } else {
      navigate(`/${screen}`);
    }

    window.scrollTo(0, 0);
  };

  // =========================================================================
  // ⚛️ РЕНДЕР (Render)
  // =========================================================================

  return (
    <div className="min-h-screen bg-white text-gray-800">
      {/* ScreenNav імпортується як окремий файл */}
      <ScreenNav activeScreen={activeScreen} goTo={goTo} user={user} logout={handleLogout} />

      {/* screens (також імпортуються як окремі файли) */}
      <Routes>
        <Route path="/" element={<SplashScreen goTo={goTo} user={user} />} />
        <Route path="/splash" element={<Navigate to="/" replace />} />
        <Route path="/login" element={<LoginPage onLogin={handleLogin} goTo={goTo} />} />

        {/* Protected Routes */}
        <Route path="/onboarding" element={<ProtectedRoute user={user}><OnboardingScreen goTo={goTo} /></ProtectedRoute>} />
        <Route path="/resume-analysis" element={<ProtectedRoute user={user}><ResumeAnalysisScreen goTo={goTo} /></ProtectedRoute>} />
        <Route path="/dashboard" element={<ProtectedRoute user={user}><DashboardScreen goTo={goTo} profile={profile} learningCourses={learningCourses} /></ProtectedRoute>} />
        <Route path="/learning-path" element={<ProtectedRoute user={user}><LearningPathScreen goTo={goTo} /></ProtectedRoute>} />
        <Route path="/course-detail" element={<ProtectedRoute user={user}><CourseDetailScreen goTo={goTo} selectedCourse={selectedCourse} /></ProtectedRoute>} />
        <Route path="/projects" element={<ProtectedRoute user={user}><ProjectsScreen goTo={goTo} /></ProtectedRoute>} />
        <Route path="/opportunities" element={<ProtectedRoute user={user}><OpportunitiesScreen goTo={goTo} /></ProtectedRoute>} />
        <Route path="/community" element={<ProtectedRoute user={user}><CommunityScreen goTo={goTo} /></ProtectedRoute>} />
        <Route path="/profile" element={<ProtectedRoute user={user}><ProfileScreen goTo={goTo} initialProfile={profile} onUpdateProfile={handleUpdateProfile} logout={handleLogout} /></ProtectedRoute>} />
        <Route path="/achievements" element={<ProtectedRoute user={user}><AchievementsScreen goTo={goTo} achievements={achievements} /></ProtectedRoute>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>

      {/* bottom nav for small screens - ENHANCED */}
      <div className="fixed bottom-0 left-0 right-0 bg-white/95 backdrop-blur-md border-t-2 border-gray-200 p-4 shadow-2xl md:hidden z-40">
        <div className="max-w-4xl mx-auto flex justify-around">
          {[
            { icon: <Home />, screen: "dashboard", label: "Home" },
            { icon: <BookOpen />, screen: "learning-path", label: "Learn" },
            { icon: <Briefcase />, screen: "opportunities", label: "Jobs" },
            { icon: <Users />, screen: "community", label: "Community" },
            { icon: <User />, screen: "profile", label: "Profile" },
          ].map((it, i) => (
            <button
              key={i}
              onClick={() => goTo(it.screen)}
              className={`flex flex-col items-center text-xs font-semibold transition-all ${activeScreen === it.screen
                ? "text-indigo-600 scale-110"
                : "text-gray-600 hover:text-indigo-500 hover:scale-105"
                }`}
            >
              <div className={`w-7 h-7 mb-1 transition-all ${activeScreen === it.screen ? "text-indigo-600" : ""
                }`}>
                {it.icon}
              </div>
              <div>{it.label}</div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CareerPlatformDesign;