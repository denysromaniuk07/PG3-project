import React, { useState, useEffect } from "react"; 
import { Home, BookOpen, Briefcase, Users, User, ArrowLeft } from "lucide-react";
import ScreenNav from "./components/ScreenNav";
import SplashScreen from "./pages/SplashScreen";
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

const CareerPlatformDesign = () => {
  const [activeScreen, setActiveScreen] = useState("splash");
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [profile] = useState({
    name: "Alex Johnson",
    title: "Aspiring Full Stack Developer",
    location: "Warsaw, Poland",
    bio: "I build delightful web experiences. Learning everyday.",
    github: "https://github.com/alexdev",
    linkedin: "https://linkedin.com/in/alexjohnson",
    email: "alex.dev@skillpath.ai",
    telegram: "https://t.me/alex_johnson",
  });
  const [achievements] = useState([
    { id: 1, title: "First Project", date: "2025-03-10", icon: ArrowLeft },
    { id: 2, title: "100% Course Completion", date: "2025-07-21", icon: ArrowLeft },
    { id: 3, title: "Streak: 30 days", date: "2025-10-01", icon: ArrowLeft },
  ]);
  
  // Данні для Dashboard/LearningPath
  const learningCourses = [
    { id: "c1", title: "React Hooks Deep Dive", progress: 75, modules: 8, time: "4h", color: "from-indigo-500 to-purple-500" },
    { id: "c2", title: "TypeScript for JS Devs", progress: 40, modules: 6, time: "6h", color: "from-green-400 to-teal-500" },
    { id: "c3", title: "Node.js & Express", progress: 20, modules: 5, time: "5h", color: "from-yellow-400 to-orange-400" },
  ];

  useEffect(() => {
  
  }, [profile])

  // =========================================================================
  // 🚀 ОНОВЛЕНА ЛОГІКА: Перемикання екранів з підтримкою History API
  // =========================================================================

  // Utility: перемикання екранів (МОДИФІКОВАНО)
  const goTo = (screen, opts = {}) => {
    if (opts.course) setSelectedCourse(opts.course);

    // Використовуємо pushState для додавання нового запису в історію.
    // Використовуємо replaceState, якщо переходимо на той самий екран, щоб уникнути дублікатів.
    const historyMethod = (screen === activeScreen && window.location.search.includes(`?screen=${screen}`))
      ? 'replaceState'
      : 'pushState';

    // Оновлюємо URL-адресу без перезавантаження
    window.history[historyMethod]({ screen }, '', `?screen=${screen}`);

    // Оновлюємо стан React
    setActiveScreen(screen);
    window.scrollTo?.(0, 0);
  };

  // Ефект для прослуховування кнопки "Назад" у браузері
  useEffect(() => {
    // Обробник події 'popstate' (викликається при натисканні 'Назад' або 'Вперед')
    const handlePopState = (event) => {
      // Отримуємо екран зі стану історії або з URL
      const stateScreen = event.state?.screen;
      const urlParams = new URLSearchParams(window.location.search);
      const urlScreen = urlParams.get('screen');

      // Встановлюємо новий активний екран
      const newScreen = stateScreen || urlScreen || "splash";
      setActiveScreen(newScreen);
      window.scrollTo?.(0, 0);
    };

    // Слухаємо подію 'popstate'
    window.addEventListener('popstate', handlePopState);

    // Ініціалізація: читаємо поточний URL при першому завантаженні (наприклад, якщо користувач оновив сторінку)
    const initialUrlParams = new URLSearchParams(window.location.search);
    const urlScreen = initialUrlParams.get('screen');

    if (urlScreen) {
      // Якщо в URL є екран, встановлюємо його як початковий стан історії
      setActiveScreen(urlScreen);
      window.history.replaceState({ screen: urlScreen }, '', `?screen=${urlScreen}`);
    } else {
      // Якщо URL порожній, ініціалізуємо його як 'splash', щоб почати відлік історії
      window.history.replaceState({ screen: "splash" }, '', `?screen=splash`);
    }

    // Прибираємо слухача при демонтажі компонента
    return () => {
      window.removeEventListener('popstate', handlePopState);
    };
  }, []); // Пустий масив залежностей: запускається лише один раз

  // =========================================================================
  // ⚛️ РЕНДЕР (Render)
  // =========================================================================

  return (
    <div className="min-h-screen bg-white text-gray-800">
      {/* ScreenNav імпортується як окремий файл */}
      <ScreenNav activeScreen={activeScreen} goTo={goTo} />

      {/* screens (також імпортуються як окремі файли) */}
      {activeScreen === "splash" && <SplashScreen goTo={goTo} />}
      {activeScreen === "onboarding" && <OnboardingScreen goTo={goTo} />}
      {activeScreen === "resume-analysis" && <ResumeAnalysisScreen goTo={goTo} />}
      {activeScreen === "dashboard" && <DashboardScreen goTo={goTo} profile={profile} learningCourses={learningCourses} />}
      {activeScreen === "learning-path" && <LearningPathScreen goTo={goTo} />}
      {activeScreen === "course-detail" && <CourseDetailScreen goTo={goTo} selectedCourse={selectedCourse} />}
      {activeScreen === "projects" && <ProjectsScreen goTo={goTo} />}
      {activeScreen === "opportunities" && <OpportunitiesScreen goTo={goTo} />}
      {activeScreen === "community" && <CommunityScreen goTo={goTo} />}
      {activeScreen === "profile" && <ProfileScreen goTo={goTo} initialProfile={profile} />}
      {activeScreen === "achievements" && <AchievementsScreen goTo={goTo} achievements={achievements} />}

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