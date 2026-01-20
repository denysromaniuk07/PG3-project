import React, { useState, useEffect } from "react";
import {
  ArrowLeft,
  Edit,
  X,
  Save,
  Zap,
  Trophy,
  CheckCircle,
  Star,
  Share2,
  Github,
  Briefcase,
  Mail,
  MessageSquare,
  ExternalLink,
  LogOut,
} from "lucide-react";
import { useUserInfoStore } from "../store";
/**
 * ProfileScreen.jsx
 * Enhanced with better spacing, animations, and dynamic data.
 */
const ProfileScreen = ({ goTo, initialProfile, onUpdateProfile, logout }) => {
  const [edit, setEdit] = useState(false);
  // Ensure profile has default values if something is missing
  const [profile, setProfile] = useState(initialProfile || {});
  const [temp, setTemp] = useState(profile);
  const { username, email } = useUserInfoStore((state) => state);
  // Sync state if prop changes
  useEffect(() => {
    if (initialProfile) {
      setProfile(initialProfile);
      setTemp(initialProfile);
    }
  }, [initialProfile]);

  const save = () => {
    setProfile(temp);
    setEdit(false);
    if (onUpdateProfile) {
      onUpdateProfile(temp);
    }
  };

  const skills = [
    { name: "React", level: 90 },
    { name: "JavaScript", level: 85 },
    { name: "Tailwind CSS", level: 80 },
    { name: "UI/UX Design", level: 70 },
  ];

  const achievements = [
    {
      title: "Top Performer 2025",
      icon: <Trophy className="w-5 h-5 text-yellow-500" />,
    },
    {
      title: "100+ Projects Completed",
      icon: <CheckCircle className="w-5 h-5 text-green-500" />,
    },
    {
      title: "5 Years Experience",
      icon: <Star className="w-5 h-5 text-indigo-500" />,
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-indigo-50/20 to-purple-50/20 pt-32 pb-24">
      <div className="max-w-5xl mx-auto px-6 lg:px-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8 fade-in">
          <h1 className="text-4xl md:text-5xl font-black gradient-text">
            Profile
          </h1>
          <div className="flex items-center gap-3">
            <button
              onClick={() => goTo("dashboard")}
              className="px-4 py-2.5 rounded-xl border-2 border-gray-200 flex items-center gap-2 hover:bg-gray-100 hover:border-gray-300 transition-all font-semibold"
            >
              <ArrowLeft className="w-4 h-4" /> Back
            </button>
            <button
              onClick={logout}
              className="px-4 py-2.5 rounded-xl border-2 border-red-100 bg-red-50 text-red-600 flex items-center gap-2 hover:bg-red-100 hover:border-red-200 transition-all font-semibold"
            >
              <LogOut className="w-4 h-4" /> Logout
            </button>
            <button
              onClick={() => setEdit(!edit)}
              className="px-5 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl flex items-center gap-2 hover:scale-105 hover:shadow-lg transition-all font-semibold"
            >
              {edit ? <X className="w-4 h-4" /> : <Edit className="w-4 h-4" />}
              {edit ? "Cancel" : "Edit"}
            </button>
          </div>
        </div>

        {/* Profile Info */}
        <div className="bg-white rounded-3xl p-8 border-2 border-gray-100 shadow-lg mb-8 slide-up">
          <div className="flex flex-col md:flex-row items-center md:items-start gap-6">
            <div className="w-24 h-24 rounded-2xl bg-gradient-to-br from-indigo-600 to-purple-600 text-white flex items-center justify-center text-4xl font-bold shadow-xl hover:scale-110 transition-transform flex-shrink-0">
              {profile.name ? profile.name.charAt(0).toUpperCase() : "U"}
            </div>
            <div className="flex-1 w-full">
              {!edit ? (
                <>
                  <div className="text-3xl font-bold mb-1">{profile.name}</div>
                  <div className="text-base text-gray-500 mb-3">
                    {profile.title || "No Title"} •{" "}
                    {profile.location || "No Location"}
                  </div>
                  <p className="mt-3 text-gray-600 leading-relaxed">
                    {profile.bio || "No Bio available."}
                  </p>
                </>
              ) : (
                <div className="space-y-3">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Full Name
                      </label>
                      <input
                        value={temp.name || ""}
                        onChange={(e) =>
                          setTemp({ ...temp, name: e.target.value })
                        }
                        className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500 outline-none"
                        placeholder="Full name"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Job Title
                      </label>
                      <input
                        value={temp.title || ""}
                        onChange={(e) =>
                          setTemp({ ...temp, title: e.target.value })
                        }
                        className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500 outline-none"
                        placeholder="Job title"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Location
                      </label>
                      <input
                        value={temp.location || ""}
                        onChange={(e) =>
                          setTemp({ ...temp, location: e.target.value })
                        }
                        className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500 outline-none"
                        placeholder="Location"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Email
                      </label>
                      <input
                        value={temp.email || ""}
                        onChange={(e) =>
                          setTemp({ ...temp, email: e.target.value })
                        }
                        className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500 outline-none"
                        placeholder="Email"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Bio
                    </label>
                    <textarea
                      value={temp.bio || ""}
                      onChange={(e) =>
                        setTemp({ ...temp, bio: e.target.value })
                      }
                      className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500 outline-none"
                      placeholder="Short bio"
                      rows={3}
                    />
                  </div>

                  {/* Editable Social Links */}
                  <h3 className="text-lg font-semibold mt-4">Social Links</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <input
                      value={temp.github || ""}
                      onChange={(e) =>
                        setTemp({ ...temp, github: e.target.value })
                      }
                      className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500 outline-none"
                      placeholder="GitHub URL"
                    />
                    <input
                      value={temp.linkedin || ""}
                      onChange={(e) =>
                        setTemp({ ...temp, linkedin: e.target.value })
                      }
                      className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500 outline-none"
                      placeholder="LinkedIn URL"
                    />
                    <input
                      value={temp.telegram || ""}
                      onChange={(e) =>
                        setTemp({ ...temp, telegram: e.target.value })
                      }
                      className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500 outline-none"
                      placeholder="Telegram link"
                    />
                  </div>

                  <div className="flex gap-2 pt-3">
                    <button
                      onClick={save}
                      className="px-4 py-2 bg-indigo-600 text-white rounded-lg flex items-center gap-2 hover:bg-indigo-700 transition"
                    >
                      <Save className="w-4 h-4" /> Save Changes
                    </button>
                    <button
                      onClick={() => {
                        setEdit(false);
                        setTemp(profile);
                      }}
                      className="px-4 py-2 border rounded-lg hover:bg-gray-100 transition"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Skills Section */}
        <div className="bg-white rounded-2xl p-6 border shadow-sm mb-10">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-yellow-500" /> My Skills
          </h2>
          <div className="space-y-4">
            {skills.map((skill, i) => (
              <div key={i}>
                <div className="flex justify-between text-sm mb-1">
                  <span>{skill.name}</span>
                  <span className="text-gray-500">{skill.level}%</span>
                </div>
                <div className="w-full bg-gray-200 h-2 rounded-full overflow-hidden">
                  <div
                    className="bg-indigo-600 h-2 rounded-full"
                    style={{ width: `${skill.level}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Achievements Section */}
        <div className="bg-white rounded-2xl p-6 border shadow-sm mb-10">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Trophy className="w-5 h-5 text-yellow-500" /> Achievements
          </h2>
          <div className="grid sm:grid-cols-3 gap-4">
            {achievements.map((a, i) => (
              <div
                key={i}
                className="p-4 border rounded-xl flex items-center gap-3 hover:shadow-md transition"
              >
                {a.icon}
                <span className="font-medium">{a.title}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Social & Contact Links */}
        <div className="bg-white rounded-2xl p-6 border shadow-sm">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Share2 className="w-5 h-5 text-indigo-600" /> Social & Contact
            Links
          </h2>
          <div className="grid sm:grid-cols-2 gap-4">
            {profile.github && (
              <a
                href={profile.github}
                target="_blank"
                rel="noopener noreferrer"
                className="p-4 border rounded-xl flex items-center gap-3 hover:shadow-md transition"
              >
                <Github className="w-5 h-5 text-gray-700" /> GitHub
                <ExternalLink className="w-4 h-4 ml-auto text-gray-400" />
              </a>
            )}
            {profile.linkedin && (
              <a
                href={profile.linkedin}
                target="_blank"
                rel="noopener noreferrer"
                className="p-4 border rounded-xl flex items-center gap-3 hover:shadow-md transition"
              >
                <Briefcase className="w-5 h-5 text-blue-600" /> LinkedIn
                <ExternalLink className="w-4 h-4 ml-auto text-gray-400" />
              </a>
            )}
            {profile.email && (
              <a
                href={`mailto:${profile.email}`}
                className="p-4 border rounded-xl flex items-center gap-3 hover:shadow-md transition"
              >
                <Mail className="w-5 h-5 text-red-500" /> {profile.email}
                <ExternalLink className="w-4 h-4 ml-auto text-gray-400" />
              </a>
            )}
            {profile.telegram && (
              <a
                href={profile.telegram}
                target="_blank"
                rel="noopener noreferrer"
                className="p-4 border rounded-xl flex items-center gap-3 hover:shadow-md transition"
              >
                <MessageSquare className="w-5 h-5 text-sky-500" /> Telegram
                <ExternalLink className="w-4 h-4 ml-auto text-gray-400" />
              </a>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfileScreen;
